# Weather Tools

The [`WeatherTools`](../api/weather.md) toolkit provides weather lookups via **wttr.in** using the `pywttr` client.

All public functions return **JSON strings**.

## 📦 Installation

This toolkit requires the optional dependencies:

```bash
pip install -U pywttr pywttr-models
```

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import WeatherTools

agent = Agent(
    name="Weather Assistant",
    model="gpt-4",
    tools=[WeatherTools(timeout=30)],
)
```

## ⚙️ Configuration

Constructor parameters for `WeatherTools`:

| Parameter | Type | Default | Notes |
|---|---:|---:|---|
| `timeout` | `int` | `30` | Clamped internally (5..120) |
| `base_url` | `str \| None` | `None` | Optional custom wttr base URL |

## 🌤️ Available Functions

- `fetch_current_weather_conditions(location, language='en')`
- `fetch_weather_forecast(location, days=3, language='en')` (days clamped 1..7)
- `fetch_temperature_data(location, language='en')`
- `fetch_weather_text_description(location, language='en')`

## ✅ Examples

```python
from enhancedtoolkits import WeatherTools

weather = WeatherTools(timeout=30)

current_json = weather.fetch_current_weather_conditions("Berlin", language="de")
forecast_json = weather.fetch_weather_forecast("Berlin", days=3, language="en")

temp_json = weather.fetch_temperature_data("52.5200,13.4050")
text_json = weather.fetch_weather_text_description("Paris")
```

## 🗣️ Languages

Language codes are normalized (e.g. `pt` → `pt_br`, `de-DE` → `de`) and fall back to English if unsupported.

See `WeatherTools.SUPPORTED_LANGUAGES`.

## API Reference

- [`docs/api/weather.md`](../api/weather.md)
