"""
A comprehensive weather toolkit that provides:
- Current weather conditions
- Weather forecasts
- Temperature data
- Weather descriptions
- Support for multiple languages
- Robust error handling and logging
"""

import json
from datetime import datetime
from typing import Any, Optional

from agno.utils.log import log_debug, log_error, log_info, log_warning

from .base import StrictToolkit

PywttrLanguage = Any

try:
    import pydantic
except ImportError:  # pragma: no cover
    pydantic = None  # type: ignore[assignment]

# Note: This module requires the pywttr package to be installed
# Install with: pip install -U pywttr pywttr-models
try:
    from pywttr import Language, Wttr

    PYWTTR_AVAILABLE = True
except ImportError:  # pragma: no cover
    PYWTTR_AVAILABLE = False
    Language = None  # type: ignore[assignment]
    Wttr = None  # type: ignore[assignment]
    log_warning(
        "pywttr package not available. Install with: "
        "pip install -U pywttr pywttr-models"
    )


class WeatherError(Exception):
    """Base exception for weather-related errors."""


class WeatherRequestError(WeatherError):
    """Exception for weather request errors."""


class WeatherValidationError(WeatherError):
    """Exception for input validation errors."""


class WeatherTools(StrictToolkit):
    """
    Enhanced Weather Tools v1.0

    A comprehensive toolkit for weather data including:
    - Current weather conditions
    - Weather forecasts
    - Temperature data
    - Weather descriptions
    - Support for multiple languages
    """

    # Supported languages mapping
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "af": "Afrikaans",
        "am": "Amharic",
        "ar": "Arabic",
        "be": "Belarusian",
        "bn": "Bengali",
        "ca": "Catalan",
        "da": "Danish",
        "de": "German",
        "el": "Greek",
        "es": "Spanish",
        "et": "Estonian",
        "fa": "Persian",
        "fr": "French",
        "gl": "Galician",
        "hi": "Hindi",
        "hu": "Hungarian",
        "ia": "Interlingua",
        "id": "Indonesian",
        "it": "Italian",
        "lt": "Lithuanian",
        "mg": "Malagasy",
        "nb": "Norwegian Bokmål",
        "nl": "Dutch",
        "oc": "Occitan",
        "pl": "Polish",
        "pt_br": "Portuguese (Brazil)",
        "ro": "Romanian",
        "ru": "Russian",
        "ta": "Tamil",
        "th": "Thai",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "vi": "Vietnamese",
        "zh_cn": "Chinese (Simplified)",
        "zh_tw": "Chinese (Traditional)",
    }

    def __init__(
        self,
        timeout: int = 30,
        base_url: Optional[str] = None,
        add_instructions: bool = True,
        **kwargs,
    ):
        """
        Initialize Enhanced Weather Tools.

        Args:
            timeout: Request timeout in seconds
            base_url: Custom base URL for the weather API (default: wttr.in)
            add_instructions: Whether to add usage instructions
        """
        if not PYWTTR_AVAILABLE:
            raise ImportError(
                "pywttr package is required. Install with: pip install -U pywttr pywttr-models"
            )

        # Configuration
        self.timeout = max(5, min(120, timeout))
        self.base_url = base_url
        self.instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )

        super().__init__(
            name="enhanced_weather_tools",
            instructions=self.instructions,
            add_instructions=add_instructions,
            **kwargs,
        )

        # Register weather methods
        self.register(self.fetch_current_weather_conditions)
        self.register(self.fetch_weather_forecast)
        self.register(self.fetch_temperature_data)
        self.register(self.fetch_weather_text_description)

        log_info(
            f"Enhanced Weather Tools initialized - Timeout: {self.timeout}, "
            f"Base URL: {self.base_url or 'default'}"
        )

    def fetch_current_weather_conditions(
        self, location: str, language: str = "en"
    ) -> str:
        """
        Get current weather conditions for a location.

        Args:
            location: Location name or coordinates
            language: Language code (default: en)

        Returns:
            JSON string containing current weather data

        Raises:
            WeatherError: If weather data retrieval fails
        """
        try:
            # Validate inputs
            self._validate_location(location)
            lang = self._validate_language(language)

            log_debug(f"Getting current weather for {location} in {language}")

            wttr_kwargs = self._build_wttr_kwargs()

            # Get weather data
            assert Wttr is not None
            with Wttr(**wttr_kwargs) as wttr:
                weather_data = wttr.weather(location, language=lang)

            # Extract current weather
            if (
                not weather_data
                or not hasattr(weather_data, "weather")
                or not weather_data.weather
            ):
                raise WeatherError(
                    "No weather data available for this location"
                )

            current = weather_data.weather[0]

            # Format response
            result = {
                "operation": "current_weather",
                "location": location,
                "timestamp": datetime.now().isoformat(),
                "current_condition": {
                    "temp_c": getattr(current, "avgtemp_c", None),
                    "temp_f": getattr(current, "avgtemp_f", None),
                    "feels_like_c": getattr(current, "feelslike_c", None),
                    "feels_like_f": getattr(current, "feelslike_f", None),
                    "humidity": getattr(current, "humidity", None),
                    "weather_desc": self._get_weather_desc(current),
                    "wind_speed_kmph": getattr(current, "maxwind_kph", None),
                    "wind_speed_mph": getattr(current, "maxwind_mph", None),
                    "precipitation_mm": getattr(
                        current, "totalprecip_mm", None
                    ),
                    "precipitation_in": getattr(
                        current, "totalprecip_in", None
                    ),
                    "uv_index": getattr(current, "uv", None),
                },
                "metadata": {
                    "language": language,
                    "source": "wttr.in",
                },
            }

            log_info(f"Retrieved current weather for {location}")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except WeatherError:
            raise
        except Exception as e:
            log_error(f"Error getting current weather: {e}")
            raise WeatherError(f"Failed to get current weather: {e}") from e

    def fetch_weather_forecast(
        self, location: str, days: int = 3, language: str = "en"
    ) -> str:
        """
        Get weather forecast for a location.

        Args:
            location: Location name or coordinates
            days: Number of days for forecast (1-7)
            language: Language code (default: en)

        Returns:
            JSON string containing weather forecast

        Raises:
            WeatherError: If weather data retrieval fails
        """
        try:
            # Validate inputs
            self._validate_location(location)
            lang = self._validate_language(language)
            days = max(1, min(7, days))  # Limit between 1-7 days

            log_debug(
                f"Getting {days}-day forecast for {location} in {language}"
            )

            wttr_kwargs = self._build_wttr_kwargs()

            # Get weather data
            assert Wttr is not None
            with Wttr(**wttr_kwargs) as wttr:
                weather_data = wttr.weather(location, language=lang)

            # Extract forecast
            if (
                not weather_data
                or not hasattr(weather_data, "weather")
                or not weather_data.weather
            ):
                raise WeatherError(
                    "No weather data available for this location"
                )

            forecast_days = weather_data.weather[:days]

            # Format response
            forecast = []
            for day in forecast_days:
                forecast.append(
                    {
                        "date": getattr(day, "date", None),
                        "max_temp_c": getattr(day, "maxtemp_c", None),
                        "max_temp_f": getattr(day, "maxtemp_f", None),
                        "min_temp_c": getattr(day, "mintemp_c", None),
                        "min_temp_f": getattr(day, "mintemp_f", None),
                        "avg_temp_c": getattr(day, "avgtemp_c", None),
                        "avg_temp_f": getattr(day, "avgtemp_f", None),
                        "weather_desc": self._get_weather_desc(day),
                        "max_wind_kph": getattr(day, "maxwind_kph", None),
                        "max_wind_mph": getattr(day, "maxwind_mph", None),
                        "total_precip_mm": getattr(
                            day, "totalprecip_mm", None
                        ),
                        "total_precip_in": getattr(
                            day, "totalprecip_in", None
                        ),
                        "chance_of_rain": getattr(
                            day, "daily_chance_of_rain", None
                        ),
                        "uv_index": getattr(day, "uv", None),
                    }
                )

            result = {
                "operation": "weather_forecast",
                "location": location,
                "timestamp": datetime.now().isoformat(),
                "forecast_days": days,
                "forecast": forecast,
                "metadata": {
                    "language": language,
                    "source": "wttr.in",
                },
            }

            log_info(f"Retrieved {days}-day forecast for {location}")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except WeatherError:
            raise
        except Exception as e:
            log_error(f"Error getting weather forecast: {e}")
            raise WeatherError(f"Failed to get weather forecast: {e}") from e

    def fetch_temperature_data(
        self, location: str, language: str = "en"
    ) -> str:
        """
        Get temperature data for a location.

        Args:
            location: Location name or coordinates
            language: Language code (default: en)

        Returns:
            JSON string containing temperature data

        Raises:
            WeatherError: If weather data retrieval fails
        """
        try:
            # Validate inputs
            self._validate_location(location)
            lang = self._validate_language(language)

            log_debug(f"Getting temperature for {location} in {language}")

            wttr_kwargs = self._build_wttr_kwargs()

            # Get weather data
            assert Wttr is not None
            with Wttr(**wttr_kwargs) as wttr:
                weather_data = wttr.weather(location, language=lang)

            # Extract temperature data
            if (
                not weather_data
                or not hasattr(weather_data, "weather")
                or not weather_data.weather
            ):
                raise WeatherError(
                    "No weather data available for this location"
                )

            current = weather_data.weather[0]

            # Format response
            result = {
                "operation": "temperature",
                "location": location,
                "timestamp": datetime.now().isoformat(),
                "temperature": {
                    "current_c": getattr(current, "avgtemp_c", None),
                    "current_f": getattr(current, "avgtemp_f", None),
                    "feels_like_c": getattr(current, "feelslike_c", None),
                    "feels_like_f": getattr(current, "feelslike_f", None),
                    "max_c": getattr(current, "maxtemp_c", None),
                    "max_f": getattr(current, "maxtemp_f", None),
                    "min_c": getattr(current, "mintemp_c", None),
                    "min_f": getattr(current, "mintemp_f", None),
                },
                "metadata": {
                    "language": language,
                    "source": "wttr.in",
                },
            }

            log_info(f"Retrieved temperature data for {location}")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except WeatherError:
            raise
        except Exception as e:
            log_error(f"Error getting temperature data: {e}")
            raise WeatherError(f"Failed to get temperature data: {e}") from e

    def fetch_weather_text_description(
        self, location: str, language: str = "en"
    ) -> str:
        """
        Get weather description for a location.

        Args:
            location: Location name or coordinates
            language: Language code (default: en)

        Returns:
            JSON string containing weather description

        Raises:
            WeatherError: If weather data retrieval fails
        """
        try:
            # Validate inputs
            self._validate_location(location)
            lang = self._validate_language(language)

            log_debug(
                f"Getting weather description for {location} in {language}"
            )

            wttr_kwargs = self._build_wttr_kwargs()

            # Get weather data
            assert Wttr is not None
            with Wttr(**wttr_kwargs) as wttr:
                weather_data = wttr.weather(location, language=lang)

            # Extract weather description
            if (
                not weather_data
                or not hasattr(weather_data, "weather")
                or not weather_data.weather
            ):
                raise WeatherError(
                    "No weather data available for this location"
                )

            current = weather_data.weather[0]
            weather_desc = self._get_weather_desc(current)

            # Format response
            result = {
                "operation": "weather_description",
                "location": location,
                "timestamp": datetime.now().isoformat(),
                "description": weather_desc,
                "metadata": {
                    "language": language,
                    "source": "wttr.in",
                },
            }

            log_info(f"Retrieved weather description for {location}")
            return json.dumps(result, indent=2, ensure_ascii=False)

        except WeatherError:
            raise
        except Exception as e:
            log_error(f"Error getting weather description: {e}")
            raise WeatherError(
                f"Failed to get weather description: {e}"
            ) from e

    def _build_wttr_kwargs(self) -> dict:
        """Build kwargs for `pywttr.Wttr`.

        - Always uses `self.timeout`.
        - Uses `self.base_url` if provided.
        """
        wttr_kwargs: dict = {"timeout": self.timeout}

        if self.base_url:
            if pydantic is not None:
                wttr_kwargs["base_url"] = pydantic.AnyHttpUrl(self.base_url)
            else:
                # pywttr typically accepts this as-is; keep it best-effort.
                wttr_kwargs["base_url"] = self.base_url

        return wttr_kwargs

    def _validate_location(self, location: str) -> None:
        """Validate location input."""
        if not location or not location.strip():
            raise WeatherValidationError("Location cannot be empty")

        if len(location) > 100:
            raise WeatherValidationError("Location name is too long")

    def _validate_language(self, language: str) -> "PywttrLanguage":
        """Validate and convert language code to a pywttr Language enum."""
        normalized = (language or "en").strip().lower().replace("-", "_")
        if normalized in ("pt", "pt_br"):
            normalized = "pt_br"

        if normalized not in self.SUPPORTED_LANGUAGES:
            log_warning(
                f"Unsupported language: {normalized}, falling back to English"
            )
            normalized = "en"

        assert Language is not None
        try:
            return getattr(Language, normalized.upper())
        except AttributeError:
            log_warning(
                f"Language enum not found for: {normalized}, falling back to English"
            )
            return Language.EN

    def _get_weather_desc(self, weather_obj) -> str:
        """Extract weather description from a pywttr weather object."""
        try:
            if hasattr(weather_obj, "condition") and weather_obj.condition:
                return weather_obj.condition.text

            if (
                hasattr(weather_obj, "weather_desc")
                and weather_obj.weather_desc
            ):
                return weather_obj.weather_desc[0].value

            return "No description available"
        except (AttributeError, IndexError, TypeError):
            return "No description available"

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for the weather tools."""
        return """
<weather_tools>
Weather lookup via wttr.in (pywttr)

GOAL
- Weather lookup via wttr.in (pywttr). All tools return JSON strings.

TOOLS
- fetch_current_weather_conditions(location, language='en')
- fetch_weather_forecast(location, days=3, language='en')  # days clamped 1..7
- fetch_temperature_data(location, language='en')
- fetch_weather_text_description(location, language='en')

CONTEXT-SIZE RULES (IMPORTANT)
- Prefer days<=3 unless the user explicitly asks for a longer forecast.
- Do not paste the full JSON into the final answer; summarize key fields.

NOTES
- location: city name or "lat,lon".
- language: falls back to English if unsupported.
</weather_tools>
"""
