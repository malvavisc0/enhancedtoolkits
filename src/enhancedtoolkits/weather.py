"""
Enhanced Weather Tools v1.0

A comprehensive weather toolkit that provides:
- Current weather conditions
- Weather forecasts
- Temperature data
- Weather descriptions
- Support for multiple languages
- Robust error handling and logging

Author: malvavisc0
License: MIT
Version: 1.0.0
"""

import json
from datetime import datetime
from typing import Optional

from agno.utils.log import log_debug, log_error, log_info, log_warning

from .base import StrictToolkit

# Note: This module requires the pywttr package to be installed
# Install with: pip install -U pywttr pywttr-models
try:
    import pywttr
    from pywttr import Language

    PYWTTR_AVAILABLE = True
except ImportError:
    PYWTTR_AVAILABLE = False
    log_warning(
        "pywttr package not available. Install with: pip install -U pywttr pywttr-models"
    )


class WeatherError(Exception):
    """Base exception for weather-related errors."""

    pass


class WeatherRequestError(WeatherError):
    """Exception for weather request errors."""

    pass


class WeatherValidationError(WeatherError):
    """Exception for input validation errors."""

    pass


class EnhancedWeatherTools(StrictToolkit):
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
        self.timeout = max(5, min(120, timeout))  # Limit between 5-120 seconds
        self.base_url = base_url
        self.add_instructions = add_instructions
        self.instructions = EnhancedWeatherTools.get_llm_usage_instructions()

        super().__init__(name="enhanced_weather_tools", **kwargs)

        # Register weather methods
        self.register(self.fetch_current_weather_conditions)
        self.register(self.fetch_weather_forecast)
        self.register(self.fetch_temperature_data)
        self.register(self.fetch_weather_text_description)

        log_info(
            f"Enhanced Weather Tools initialized - Timeout: {self.timeout}, Base URL: {self.base_url or 'default'}"
        )

    def fetch_current_weather_conditions(self, location: str, language: str = "en") -> str:
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

            # Create Wttr instance with optional custom base URL
            wttr_kwargs = {}
            if self.base_url:
                import pydantic

                wttr_kwargs["base_url"] = pydantic.AnyHttpUrl(self.base_url)

            # Get weather data
            with pywttr.Wttr(**wttr_kwargs) as wttr:
                weather_data = wttr.weather(location, language=lang)

            # Extract current weather
            if (
                not weather_data
                or not hasattr(weather_data, "weather")
                or not weather_data.weather
            ):
                raise WeatherError("No weather data available for this location")

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
                    "precipitation_mm": getattr(current, "totalprecip_mm", None),
                    "precipitation_in": getattr(current, "totalprecip_in", None),
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
            raise WeatherError(f"Failed to get current weather: {e}")

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

            log_debug(f"Getting {days}-day forecast for {location} in {language}")

            # Create Wttr instance with optional custom base URL
            wttr_kwargs = {}
            if self.base_url:
                import pydantic

                wttr_kwargs["base_url"] = pydantic.AnyHttpUrl(self.base_url)

            # Get weather data
            with pywttr.Wttr(**wttr_kwargs) as wttr:
                weather_data = wttr.weather(location, language=lang)

            # Extract forecast
            if (
                not weather_data
                or not hasattr(weather_data, "weather")
                or not weather_data.weather
            ):
                raise WeatherError("No weather data available for this location")

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
                        "total_precip_mm": getattr(day, "totalprecip_mm", None),
                        "total_precip_in": getattr(day, "totalprecip_in", None),
                        "chance_of_rain": getattr(day, "daily_chance_of_rain", None),
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
            raise WeatherError(f"Failed to get weather forecast: {e}")

    def fetch_temperature_data(self, location: str, language: str = "en") -> str:
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

            # Create Wttr instance with optional custom base URL
            wttr_kwargs = {}
            if self.base_url:
                import pydantic

                wttr_kwargs["base_url"] = pydantic.AnyHttpUrl(self.base_url)

            # Get weather data
            with pywttr.Wttr(**wttr_kwargs) as wttr:
                weather_data = wttr.weather(location, language=lang)

            # Extract temperature data
            if (
                not weather_data
                or not hasattr(weather_data, "weather")
                or not weather_data.weather
            ):
                raise WeatherError("No weather data available for this location")

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
            raise WeatherError(f"Failed to get temperature data: {e}")

    def fetch_weather_text_description(self, location: str, language: str = "en") -> str:
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

            log_debug(f"Getting weather description for {location} in {language}")

            # Create Wttr instance with optional custom base URL
            wttr_kwargs = {}
            if self.base_url:
                import pydantic

                wttr_kwargs["base_url"] = pydantic.AnyHttpUrl(self.base_url)

            # Get weather data
            with pywttr.Wttr(**wttr_kwargs) as wttr:
                weather_data = wttr.weather(location, language=lang)

            # Extract weather description
            if (
                not weather_data
                or not hasattr(weather_data, "weather")
                or not weather_data.weather
            ):
                raise WeatherError("No weather data available for this location")

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
            raise WeatherError(f"Failed to get weather description: {e}")

    def _validate_location(self, location: str) -> None:
        """
        Validate location input.
        """
        if not location or not location.strip():
            raise WeatherValidationError("Location cannot be empty")

        if len(location) > 100:
            raise WeatherValidationError("Location name is too long")

    def _validate_language(self, language: str) -> str:
        """
        Validate and convert language code to pywttr Language.
        """
        language = language.lower()

        # Handle special cases
        if language == "pt-br" or language == "pt_br":
            language = "pt_br"
        elif language == "zh-cn" or language == "zh_cn":
            language = "zh_cn"
        elif language == "zh-tw" or language == "zh_tw":
            language = "zh_tw"

        if language not in self.SUPPORTED_LANGUAGES:
            log_warning(f"Unsupported language: {language}, falling back to English")
            language = "en"

        # Convert language code to pywttr Language
        try:
            if language == "en":
                return pywttr.Language.EN
            elif language == "af":
                return pywttr.Language.AF
            elif language == "am":
                return pywttr.Language.AM
            elif language == "ar":
                return pywttr.Language.AR
            elif language == "be":
                return pywttr.Language.BE
            elif language == "bn":
                return pywttr.Language.BN
            elif language == "ca":
                return pywttr.Language.CA
            elif language == "da":
                return pywttr.Language.DA
            elif language == "de":
                return pywttr.Language.DE
            elif language == "el":
                return pywttr.Language.EL
            elif language == "es":
                return pywttr.Language.ES
            elif language == "et":
                return pywttr.Language.ET
            elif language == "fa":
                return pywttr.Language.FA
            elif language == "fr":
                return pywttr.Language.FR
            elif language == "gl":
                return pywttr.Language.GL
            elif language == "hi":
                return pywttr.Language.HI
            elif language == "hu":
                return pywttr.Language.HU
            elif language == "ia":
                return pywttr.Language.IA
            elif language == "id":
                return pywttr.Language.ID
            elif language == "it":
                return pywttr.Language.IT
            elif language == "lt":
                return pywttr.Language.LT
            elif language == "mg":
                return pywttr.Language.MG
            elif language == "nb":
                return pywttr.Language.NB
            elif language == "nl":
                return pywttr.Language.NL
            elif language == "oc":
                return pywttr.Language.OC
            elif language == "pl":
                return pywttr.Language.PL
            elif language == "pt_br":
                return pywttr.Language.PT_BR
            elif language == "ro":
                return pywttr.Language.RO
            elif language == "ru":
                return pywttr.Language.RU
            elif language == "ta":
                return pywttr.Language.TA
            elif language == "th":
                return pywttr.Language.TH
            elif language == "tr":
                return pywttr.Language.TR
            elif language == "uk":
                return pywttr.Language.UK
            elif language == "vi":
                return pywttr.Language.VI
            elif language == "zh_cn":
                return pywttr.Language.ZH_CN
            elif language == "zh_tw":
                return pywttr.Language.ZH_TW
            else:
                return pywttr.Language.EN
        except Exception as e:
            log_warning(f"Error converting language code: {e}, falling back to English")
            return pywttr.Language.EN

    def _get_weather_desc(self, weather_obj) -> str:
        """
        Extract weather description from weather object.
        """
        try:
            if hasattr(weather_obj, "condition") and weather_obj.condition:
                return weather_obj.condition.text
            elif hasattr(weather_obj, "weather_desc") and weather_obj.weather_desc:
                return weather_obj.weather_desc[0].value
            else:
                return "No description available"
        except Exception:
            return "No description available"

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use each tool in EnhancedWeatherTools.
        Each instruction includes the method name, description, parameters, types, and example values.
        """
        instructions = """
<weather_tools_instructions>
*** Weather Tools Instructions ***

By leveraging the following set of tools, you can retrieve current weather conditions, forecasts, temperature data, and weather descriptions for locations worldwide. These tools provide accurate, real-time weather information in multiple languages. Here are the detailed instructions for using each tool:

- Use fetch_current_weather_conditions to retrieve current weather conditions for a location.
   Parameters:
      - location (str): Location name or coordinates, e.g., "New York", "London", "48.8566,2.3522"
      - language (str, optional): Language code (default: "en"), e.g., "fr", "es", "de"

- Use fetch_weather_forecast to retrieve a multi-day weather forecast for a location.
   Parameters:
      - location (str): Location name or coordinates, e.g., "Tokyo", "Sydney", "35.6762,139.6503"
      - days (int, optional): Number of days for forecast (default: 3, range: 1-7)
      - language (str, optional): Language code (default: "en"), e.g., "it", "ru", "zh_cn"

- Use fetch_temperature_data to retrieve temperature data for a location.
   Parameters:
      - location (str): Location name or coordinates, e.g., "Berlin", "Cairo", "52.5200,13.4050"
      - language (str, optional): Language code (default: "en"), e.g., "de", "ar", "fr"

- Use fetch_weather_text_description to retrieve a textual description of the weather for a location.
   Parameters:
      - location (str): Location name or coordinates, e.g., "Rio de Janeiro", "Mumbai", "-22.9068,-43.1729"
      - language (str, optional): Language code (default: "en"), e.g., "pt_br", "hi", "es"

Notes:
- The language parameter is always optional and defaults to English ("en").
- Supported language codes include: en, af, am, ar, be, bn, ca, da, de, el, es, et, fa, fr, gl, hi, hu, ia, id, it, lt, mg, nb, nl, oc, pl, pt_br, ro, ru, ta, th, tr, uk, vi, zh_cn, zh_tw.
- Location can be specified as a city name, address, or latitude,longitude coordinates.
- Temperature values are provided in both Celsius and Fahrenheit where available.
- Weather data is sourced from wttr.in, which aggregates data from various weather services.
</weather_tools_instructions>
"""
        return instructions
