# Finance Tools (Yahoo Finance)

The [`YFinanceTools`](../api/finance.md) toolkit provides market + company data via the [`yfinance`](https://pypi.org/project/yfinance/) library.

All public functions return **JSON strings**.

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import YFinanceTools

agent = Agent(
    name="Market Analyst",
    model="gpt-4",
    tools=[YFinanceTools(enable_caching=True, cache_ttl=300, rate_limit_delay=0.1)],
)
```

## ⚙️ Configuration

Constructor parameters for `YFinanceTools`:

| Parameter | Type | Default | Notes |
|---|---:|---:|---|
| `enable_caching` | `bool` | `True` | Enables internal caches for ticker objects/responses |
| `cache_ttl` | `int` | `300` | Cache TTL in seconds |
| `rate_limit_delay` | `float` | `0.1` | Minimum delay between outbound requests |

## 📈 Available Functions

### Market price

- `fetch_current_stock_price(ticker)`
- `fetch_price_history(ticker, period='1y', interval='1d')`

### Company profile / fundamentals

- `fetch_company_information(ticker)`

### News

- `fetch_ticker_news(ticker, max_articles=10)`

### Financial statements

- `fetch_income_statement(ticker)`
- `fetch_quarterly_financials(ticker)`
- `fetch_balance_sheet(ticker)`
- `fetch_quarterly_balance_sheet(ticker)`
- `fetch_cashflow_statement(ticker)`
- `fetch_quarterly_cashflow_statement(ticker)`

### Ownership / analyst / ESG

- `fetch_major_shareholders(ticker)`
- `fetch_institutional_shareholders(ticker)`
- `fetch_analyst_recommendations(ticker)`
- `fetch_sustainability_scores(ticker)`

## ✅ Examples

```python
from enhancedtoolkits import YFinanceTools

finance = YFinanceTools()

price_json = finance.fetch_current_stock_price("AAPL")
company_json = finance.fetch_company_information("TSLA")
news_json = finance.fetch_ticker_news("MSFT", max_articles=5)

history_json = finance.fetch_price_history(
    ticker="AAPL",
    period="1mo",
    interval="1d",
)
```

## 🚨 Error Handling

The module defines:

- `YFinanceValidationError` (invalid tickers / invalid period or interval)
- `YFinanceDataError` (network/data retrieval failures)

When used via agent tool calling, errors may be raised by the toolkit method (depending on the caller), so you should wrap direct calls in `try/except`.

## API Reference

- [`docs/api/finance.md`](../api/finance.md)
