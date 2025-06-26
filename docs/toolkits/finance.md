# Finance Tools (YFinance)

The Finance Tools provide comprehensive financial data retrieval with robust error handling and caching for real-time market information.

## Overview

The `YFinanceTools` class offers access to comprehensive financial data including stock prices, company information, financial statements, news, and analyst recommendations through the Yahoo Finance API.

## Key Features

- **Real-time Stock Prices**: Current prices with change data
- **Company Information**: Comprehensive company details and metrics
- **Financial Statements**: Income statements, balance sheets, cash flows
- **News & Analysis**: Latest news articles and analyst recommendations
- **Caching System**: Configurable response caching with TTL
- **Rate Limiting**: Built-in request throttling and retry logic

## Installation

```bash
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

## Basic Usage

```python
from enhancedtoolkits import YFinanceTools

# Initialize finance tools
finance = YFinanceTools(
    enable_caching=True,
    cache_ttl=300,
    rate_limit_delay=0.1
)
```

## Available Methods

### `get_current_price()`

Get current stock price with change data.

```python
price_info = finance.get_current_price("AAPL")
print(price_info)
```

**Returns JSON with:**
- Current price
- Price change
- Percentage change
- Volume
- Market cap

### `get_company_information()`

Get comprehensive company details.

```python
company_info = finance.get_company_information("TSLA")
print(company_info)
```

**Returns information about:**
- Business summary
- Industry and sector
- Employee count
- Market metrics
- Financial ratios

### `get_news_for_ticker()`

Get latest news articles for a stock.

```python
news = finance.get_news_for_ticker("GOOGL", max_articles=5)
print(news)
```

### `get_earnings_history()`

Get historical earnings data.

```python
earnings = finance.get_earnings_history("MSFT")
print(earnings)
```

### Financial Statements

#### Income Statement
```python
income = finance.get_income_statement("AAPL")
quarterly_income = finance.get_quarterly_financials("AAPL")
```

#### Balance Sheet
```python
balance_sheet = finance.get_balance_sheet("AAPL")
quarterly_balance = finance.get_quarterly_balance_sheet("AAPL")
```

#### Cash Flow
```python
cashflow = finance.get_cashflow("AAPL")
quarterly_cashflow = finance.get_quarterly_cashflow("AAPL")
```

### Ownership Information

```python
# Major shareholders
major_holders = finance.get_major_holders("AAPL")

# Institutional ownership
institutional = finance.get_institutional_holders("AAPL")
```

### Analyst Data

```python
# Analyst recommendations
recommendations = finance.get_recommendations("AAPL")

# ESG sustainability scores
sustainability = finance.get_sustainability_scores("AAPL")
```

### Historical Data

```python
# Price history
history = finance.get_price_history(
    ticker="AAPL",
    period="1y",  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    interval="1d"  # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
)
```

## Configuration Options

```python
finance = YFinanceTools(
    enable_caching=True,        # Enable response caching
    cache_ttl=300,             # Cache time-to-live (seconds)
    rate_limit_delay=0.1,      # Delay between requests (seconds)
    timeout=30,                # Request timeout (seconds)
    max_retries=3              # Maximum retry attempts
)
```

## Advanced Examples

### Portfolio Analysis

```python
def analyze_portfolio(tickers):
    finance = YFinanceTools(enable_caching=True)
    portfolio_data = {}
    
    for ticker in tickers:
        try:
            # Get current price
            price_info = finance.get_current_price(ticker)
            
            # Get company information
            company_info = finance.get_company_information(ticker)
            
            # Get recommendations
            recommendations = finance.get_recommendations(ticker)
            
            portfolio_data[ticker] = {
                'price': price_info,
                'company': company_info,
                'recommendations': recommendations
            }
            
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    
    return portfolio_data

# Analyze a portfolio
portfolio = analyze_portfolio(["AAPL", "GOOGL", "MSFT", "TSLA"])
```

### Market Screening

```python
def screen_stocks(tickers, criteria):
    finance = YFinanceTools()
    screened_stocks = []
    
    for ticker in tickers:
        try:
            company_info = finance.get_company_information(ticker)
            price_info = finance.get_current_price(ticker)
            
            # Parse JSON responses
            import json
            company_data = json.loads(company_info)
            price_data = json.loads(price_info)
            
            # Apply screening criteria
            if meets_criteria(company_data, price_data, criteria):
                screened_stocks.append({
                    'ticker': ticker,
                    'company': company_data,
                    'price': price_data
                })
                
        except Exception as e:
            print(f"Error screening {ticker}: {e}")
    
    return screened_stocks

def meets_criteria(company, price, criteria):
    # Example criteria: P/E ratio < 20, Market cap > 1B
    try:
        pe_ratio = company.get('trailingPE', float('inf'))
        market_cap = company.get('marketCap', 0)
        
        return (pe_ratio < criteria.get('max_pe', float('inf')) and
                market_cap > criteria.get('min_market_cap', 0))
    except:
        return False

# Screen stocks
criteria = {'max_pe': 20, 'min_market_cap': 1000000000}
results = screen_stocks(["AAPL", "GOOGL", "MSFT"], criteria)
```

### Financial Analysis Dashboard

```python
def create_financial_dashboard(ticker):
    finance = YFinanceTools(enable_caching=True)
    
    dashboard = {
        'ticker': ticker,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # Core data
        dashboard['price'] = finance.get_current_price(ticker)
        dashboard['company'] = finance.get_company_information(ticker)
        dashboard['news'] = finance.get_news_for_ticker(ticker, max_articles=3)
        
        # Financial statements
        dashboard['income_statement'] = finance.get_income_statement(ticker)
        dashboard['balance_sheet'] = finance.get_balance_sheet(ticker)
        dashboard['cashflow'] = finance.get_cashflow(ticker)
        
        # Analysis
        dashboard['recommendations'] = finance.get_recommendations(ticker)
        dashboard['sustainability'] = finance.get_sustainability_scores(ticker)
        
        # Historical performance
        dashboard['price_history'] = finance.get_price_history(
            ticker=ticker,
            period="1y",
            interval="1d"
        )
        
    except Exception as e:
        dashboard['error'] = str(e)
    
    return dashboard

# Create dashboard for Apple
apple_dashboard = create_financial_dashboard("AAPL")
```

## Error Handling

```python
from enhancedtoolkits.finance import YFinanceError, YFinanceValidationError

try:
    price_info = finance.get_current_price("INVALID_TICKER")
except YFinanceValidationError as e:
    print(f"Validation error: {e}")
except YFinanceError as e:
    print(f"Finance API error: {e}")
except Exception as e:
    print(f"General error: {e}")
```

## Supported Ticker Formats

- **US Stocks**: `AAPL`, `GOOGL`, `MSFT`
- **International**: `ASML.AS` (Amsterdam), `7203.T` (Tokyo)
- **ETFs**: `SPY`, `QQQ`, `VTI`
- **Indices**: `^GSPC` (S&P 500), `^IXIC` (NASDAQ)
- **Currencies**: `EURUSD=X`, `GBPUSD=X`
- **Crypto**: `BTC-USD`, `ETH-USD`

## Rate Limiting

The tool includes built-in rate limiting to respect Yahoo Finance's usage policies:

```python
# Configure rate limiting
finance = YFinanceTools(
    rate_limit_delay=0.5,  # 500ms delay between requests
    max_retries=3          # Retry failed requests up to 3 times
)
```

## Caching

Enable caching to improve performance and reduce API calls:

```python
finance = YFinanceTools(
    enable_caching=True,
    cache_ttl=300  # Cache responses for 5 minutes
)

# First call hits the API
price1 = finance.get_current_price("AAPL")

# Second call uses cached data (if within TTL)
price2 = finance.get_current_price("AAPL")
```

## Best Practices

1. **Enable Caching**: Use caching for frequently accessed data
2. **Handle Errors**: Always wrap calls in try-catch blocks
3. **Respect Rate Limits**: Don't make too many requests too quickly
4. **Validate Tickers**: Check ticker symbols before making requests
5. **Use Appropriate Timeouts**: Set reasonable timeout values

## Performance Tips

- Use caching for repeated requests
- Batch multiple ticker requests with delays
- Choose appropriate cache TTL based on data freshness needs
- Monitor rate limits to avoid API restrictions

## Related Tools

- [Calculator Tools](../calculators/index.md) - Financial calculations and analysis
- [Reasoning Tools](reasoning.md) - Investment decision reasoning
- [Downloader Tools](downloader.md) - Additional financial data sources

## API Reference

For complete API documentation, see the [API Reference](../api/finance.md).
