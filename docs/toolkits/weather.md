# Weather Tools for AI Agents

The Weather Tools provide current weather conditions and forecasts with multi-language support for AI agents that need weather information.

## 🤖 AI Agent Setup

```python
from enhancedtoolkits import WeatherTools

# Initialize for your AI agent
weather = WeatherTools(
    timeout=30,                    # Request timeout in seconds
    base_url="https://wttr.in"     # Weather API base URL
)

# Register with your agent
agent.register_tools([weather])
```

## ⚙️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | int | `30` | Request timeout in seconds |
| `base_url` | str | `"https://wttr.in"` | Weather API base URL |

## 🌤️ Available Functions

Your AI agent will have access to these weather functions:

### `get_current_weather()`
Get current weather conditions for any location.

**Parameters:**
- `location`: Location name (city, address, coordinates)
- `language`: Language code for response (default: "en")

**Returns:** JSON with current weather including:
- Temperature (Celsius and Fahrenheit)
- Weather description
- Humidity, wind speed, pressure
- Visibility, UV index
- Feels like temperature

### `get_weather_forecast()`
Get multi-day weather forecast.

**Parameters:**
- `location`: Location name (city, address, coordinates)
- `days`: Number of forecast days (1-3)
- `language`: Language code for response (default: "en")

**Returns:** JSON with forecast data including:
- Daily temperature ranges
- Weather conditions per day
- Precipitation probability
- Wind conditions

### `get_temperature()`
Get detailed temperature information.

**Parameters:**
- `location`: Location name
- `language`: Language code (default: "en")

**Returns:** JSON with temperature data:
- Current temperature
- Feels like temperature
- Daily min/max temperatures
- Both Celsius and Fahrenheit

### `get_weather_description()`
Get textual weather description.

**Parameters:**
- `location`: Location name
- `language`: Language code (default: "en")

**Returns:** Human-readable weather description

## 🌍 Location Support

The Weather Tools support flexible location formats:

### City Names
- `"New York"` - City name
- `"London, UK"` - City with country
- `"Tokyo, Japan"` - International cities

### Addresses
- `"1600 Pennsylvania Avenue, Washington DC"`
- `"Times Square, New York"`
- `"Eiffel Tower, Paris"`

### Coordinates
- `"40.7128,-74.0060"` - Latitude, longitude
- `"51.5074,-0.1278"` - London coordinates

### Airports
- `"JFK"` - Airport codes
- `"LAX"` - Los Angeles International
- `"LHR"` - London Heathrow

## 🗣️ Language Support

Supports 30+ languages including:

| Language | Code | Example |
|----------|------|---------|
| English | `en` | "Sunny, 25°C" |
| Spanish | `es` | "Soleado, 25°C" |
| French | `fr` | "Ensoleillé, 25°C" |
| German | `de` | "Sonnig, 25°C" |
| Chinese | `zh` | "晴天, 25°C" |
| Japanese | `ja` | "晴れ, 25°C" |
| Korean | `ko` | "맑음, 25°C" |
| Portuguese | `pt` | "Ensolarado, 25°C" |
| Russian | `ru` | "Солнечно, 25°C" |
| Arabic | `ar` | "مشمس, 25°C" |
| Italian | `it` | "Soleggiato, 25°C" |
| Dutch | `nl` | "Zonnig, 25°C" |

## 🎯 AI Agent Integration Examples

### OpenAI Function Calling
```python
import openai
from enhancedtoolkits import WeatherTools

weather = WeatherTools()

# Get function schema for OpenAI
tools = [weather.get_openai_schema()]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user", 
        "content": "What's the weather like in Paris today?"
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Agno Framework
```python
from agno.agent import Agent
from enhancedtoolkits import WeatherTools

agent = Agent(
    name="Weather Assistant",
    model="gpt-4",
    tools=[WeatherTools(timeout=60)]
)

# Agent can now provide weather information
response = agent.run("Should I bring an umbrella in London tomorrow?")
```

## 🔧 Production Configuration

### Basic Setup
```python
weather = WeatherTools()
```

### Custom API Setup
```python
weather = WeatherTools(
    timeout=60,                    # Longer timeout for reliability
    base_url="https://wttr.in"     # Default weather service
)
```

### Environment Variables
```bash
# Optional: Custom weather API URL
WEATHER_API_URL=https://wttr.in

# Optional: Set timeout
WEATHER_TIMEOUT=30
```

## 📊 Example Agent Interactions

**Agent Query:** "What's the weather in Tokyo?"

**Weather Tool Response:**
```json
{
  "location": "Tokyo, Japan",
  "current_temperature": "22°C (72°F)",
  "condition": "Partly cloudy",
  "humidity": "65%",
  "wind": "10 km/h NE",
  "feels_like": "24°C (75°F)",
  "description": "Partly cloudy with comfortable temperatures"
}
```

**Agent Query:** "Will it rain in London this week?"

**Weather Tool Operations:**
1. `get_weather_forecast("London", 7)` - Get 7-day forecast
2. Analyze precipitation data
3. Provide rain probability and recommendations

**Agent Query:** "Compare weather in New York and Los Angeles"

**Weather Tool Operations:**
1. `get_current_weather("New York")` - NYC weather
2. `get_current_weather("Los Angeles")` - LA weather
3. Agent compares and contrasts conditions

## 🌡️ Temperature Formats

All temperature data includes both Celsius and Fahrenheit:
- **Celsius**: Primary metric format
- **Fahrenheit**: Imperial format in parentheses
- **Feels like**: Apparent temperature with wind chill/heat index

## 🚨 Error Handling

The Weather Tools handle various scenarios:
- **Invalid locations**: Unknown cities or addresses
- **Network errors**: API timeouts and connection issues
- **Service unavailable**: Weather service downtime
- **Rate limiting**: API usage limits

## 🔍 Use Cases for AI Agents

### Travel Planning
- Check weather for destination cities
- Compare conditions across multiple locations
- Provide clothing and activity recommendations

### Event Planning
- Assess weather for outdoor events
- Monitor forecast changes
- Suggest backup plans for weather

### Daily Assistance
- Morning weather briefings
- Commute weather conditions
- Weekend activity planning

### Business Intelligence
- Weather impact on business operations
- Seasonal trend analysis
- Location-based decision making

## 📈 Performance

### Response Times
- **Current weather**: ~1-2 seconds
- **Forecasts**: ~2-3 seconds
- **Multiple locations**: Sequential requests

### Caching
- Weather data cached for 10 minutes
- Reduces API calls for repeated requests
- Improves response times

## 📊 Monitoring

Enable detailed logging for weather operations:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

weather = WeatherTools(debug=True)
```

## 🚀 Next Steps

1. **Initialize** WeatherTools with appropriate timeout
2. **Register** with your AI agent framework
3. **Test** with various location formats
4. **Configure** language preferences for your users
5. **Monitor** API usage and response times

The Weather Tools enable your AI agent to provide accurate, localized weather information in multiple languages while handling various location formats and error conditions gracefully.