# Weather Tools API Reference

API documentation for the Weather Tools toolkit - weather data and forecasts with support for 30+ languages.

## Class: WeatherTools

Weather data toolkit providing current conditions, forecasts, and historical weather information.

### WeatherTools()

Initialize the Weather Tools toolkit.

**Parameters:**
- `api_key` (str, optional): OpenWeatherMap API key. Can be set via OPENWEATHERMAP_API_KEY environment variable
- `units` (str, optional): Temperature units (metric, imperial, kelvin). Default: 'metric'
- `language` (str, optional): Language for weather descriptions. Default: 'en'
- `enable_caching` (bool, optional): Enable response caching. Default: True
- `cache_ttl` (int, optional): Cache time-to-live in seconds. Default: 300

### Methods

#### get_current_weather()

Get current weather conditions for a location.

**Parameters:**
- `location` (str): City name, coordinates, or location identifier
- `units` (str, optional): Temperature units override
- `language` (str, optional): Language override for descriptions

**Returns:**
- `dict`: Current weather data including temperature, humidity, pressure, and conditions

#### get_weather_forecast()

Get weather forecast for a location.

**Parameters:**
- `location` (str): City name, coordinates, or location identifier
- `days` (int): Number of forecast days (1-16). Default: 5
- `units` (str, optional): Temperature units override
- `language` (str, optional): Language override for descriptions

**Returns:**
- `dict`: Weather forecast with daily predictions and detailed conditions

#### get_hourly_forecast()

Get hourly weather forecast for a location.

**Parameters:**
- `location` (str): City name, coordinates, or location identifier
- `hours` (int): Number of forecast hours (1-48). Default: 24
- `units` (str, optional): Temperature units override

**Returns:**
- `dict`: Hourly weather forecast with detailed hourly predictions

#### get_weather_alerts()

Get active weather alerts and warnings for a location.

**Parameters:**
- `location` (str): City name, coordinates, or location identifier
- `language` (str, optional): Language for alert descriptions

**Returns:**
- `dict`: Active weather alerts, warnings, and advisories

#### get_air_quality()

Get air quality information for a location.

**Parameters:**
- `location` (str): City name, coordinates, or location identifier
- `components` (bool): Include detailed pollutant components. Default: True

**Returns:**
- `dict`: Air quality index and pollutant levels

## Usage Examples

```python
from agno.agent import Agent
from enhancedtoolkits import WeatherTools

# Initialize with API key
weather = WeatherTools(
    api_key="your_openweathermap_api_key",
    units="metric",
    language="en"
)

# Add to agent
agent = Agent(
    name="Weather Assistant",
    model="gpt-4",
    tools=[weather]
)

# Agent can now provide weather information
response = agent.run("What's the weather like in London today?")
```

## Features

- **Current Conditions**: Real-time weather data
- **Forecasts**: Daily and hourly weather predictions
- **Weather Alerts**: Severe weather warnings and advisories
- **Air Quality**: Pollution levels and air quality index
- **Multi-language**: Support for 30+ languages
- **Flexible Units**: Metric, imperial, and Kelvin temperature units
- **Global Coverage**: Worldwide weather data

## Related Documentation

- [Weather Tools Guide](../toolkits/weather.md)
- [StrictToolkit Base](base.md)
- [API Configuration](../getting-started/configuration.md)