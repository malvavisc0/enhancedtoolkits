"""
A production-ready financial data toolkit that provides:
- Comprehensive stock market data retrieval
- Robust error handling and validation
- Input sanitization and caching
- Rate limiting and retry logic
- Consistent data formatting
- Performance optimizations
"""

import json
import re
import time
from datetime import datetime
from typing import Any, Dict, Optional

import yfinance as yf
from agno.utils.log import log_debug, log_error, log_info, log_warning

from .base import StrictToolkit


class YFinanceError(Exception):
    """Custom exception for YFinance-related errors."""


class YFinanceValidationError(YFinanceError):
    """Exception for input validation errors."""


class YFinanceDataError(YFinanceError):
    """Exception for data retrieval errors."""


class YFinanceTools(
    StrictToolkit
):  # pylint: disable=too-many-instance-attributes
    """
    Enhanced YFinance Tools v2.0

    A production-ready financial data toolkit with comprehensive error handling,
    input validation, caching, and consistent data formatting.
    """

    # Valid ticker symbol pattern (letters, numbers, dots, hyphens)
    TICKER_PATTERN = re.compile(r"^[A-Z0-9.-]{1,10}$")

    # Valid periods for price history
    VALID_PERIODS = [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    ]

    # Valid intervals for price history
    VALID_INTERVALS = [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ]

    def __init__(
        self,
        enable_caching: bool = True,
        cache_ttl: int = 300,  # 5 minutes
        rate_limit_delay: float = 0.1,  # 100ms between requests
        **kwargs,
    ):
        """
        Initialize Enhanced YFinance Tools.

        Args:
            enable_caching: Whether to enable response caching
            cache_ttl: Cache time-to-live in seconds
            rate_limit_delay: Delay between API requests in seconds
        """
        self.add_instructions = True
        self.instructions = YFinanceTools.get_llm_usage_instructions()

        super().__init__(
            name="enhanced_yfinance_tools",
            instructions=self.instructions,
            add_instructions=True,
            **kwargs,
        )

        # Configuration
        self.enable_caching = enable_caching
        self.cache_ttl = cache_ttl
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0.0

        # Cache for ticker objects and responses
        self._ticker_cache: Dict[str, Any] = {}
        self._response_cache: Dict[str, Dict[str, Any]] = {}

        # Register all methods
        self.register(self.fetch_current_stock_price)
        self.register(self.fetch_company_information)
        self.register(self.fetch_ticker_news)
        self.register(self.fetch_earnings_history)
        self.register(self.fetch_income_statement)
        self.register(self.fetch_quarterly_financials)
        self.register(self.fetch_balance_sheet)
        self.register(self.fetch_quarterly_balance_sheet)
        self.register(self.fetch_cashflow_statement)
        self.register(self.fetch_quarterly_cashflow_statement)
        self.register(self.fetch_major_shareholders)
        self.register(self.fetch_institutional_shareholders)
        self.register(self.fetch_analyst_recommendations)
        self.register(self.fetch_sustainability_scores)
        self.register(self.fetch_price_history)

        log_info(
            f"Enhanced YFinance Tools initialized - Caching: {enable_caching}, "
            f"Rate Limit: {rate_limit_delay}s"
        )

    def fetch_current_stock_price(self, ticker: str) -> str:
        """
        Retrieves the current price of a stock given its ticker symbol.

        Args:
            ticker: The ticker symbol of the stock

        Returns:
            JSON string containing current price information

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If price data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting current price for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)
            info = self._get_ticker_info(ticker_obj, ticker)

            # Try multiple price fields
            current_price = (
                info.get("regularMarketPrice")
                or info.get("currentPrice")
                or info.get("previousClose")
            )

            if current_price is None:
                raise YFinanceDataError(
                    f"No price data available for {ticker}"
                )

            # Get additional price context
            currency = info.get("currency", "USD")
            market_state = info.get("marketState", "UNKNOWN")

            result = {
                "ticker": ticker,
                "current_price": round(float(current_price), 2),
                "currency": currency,
                "market_state": market_state,
                "timestamp": datetime.now().isoformat(),
                "previous_close": info.get("previousClose"),
                "day_change": None,
                "day_change_percent": None,
            }

            # Calculate day change if possible
            prev_close = info.get("previousClose")
            if prev_close and current_price and prev_close != 0:
                day_change = current_price - prev_close
                day_change_percent = (day_change / prev_close) * 100
                result.update(
                    {
                        "day_change": round(day_change, 2),
                        "day_change_percent": round(day_change_percent, 2),
                    }
                )

            return self._format_json_response(result)

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting current price for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get current price for {ticker}: {exc}"
            ) from exc

    def fetch_company_information(self, ticker: str) -> str:
        """
        Retrieve comprehensive information about a company.

        Args:
            ticker: The ticker symbol of the company

        Returns:
            JSON string containing company information

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If company data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting company information for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)
            info = self._get_ticker_info(ticker_obj, ticker)

            # Organize company information with safe extraction
            company_info = {
                "basic_info": {
                    "name": info.get("shortName") or info.get("longName"),
                    "symbol": info.get("symbol"),
                    "sector": info.get("sector"),
                    "industry": info.get("industry"),
                    "website": info.get("website"),
                    "summary": info.get("longBusinessSummary"),
                    "employees": info.get("fullTimeEmployees"),
                },
                "financial_metrics": {
                    "market_cap": info.get("marketCap"),
                    "enterprise_value": info.get("enterpriseValue"),
                    "trailing_pe": info.get("trailingPE"),
                    "forward_pe": info.get("forwardPE"),
                    "peg_ratio": info.get("pegRatio"),
                    "price_to_book": info.get("priceToBook"),
                    "eps_trailing": info.get("trailingEps"),
                    "eps_forward": info.get("forwardEps"),
                },
                "price_data": {
                    "current_price": info.get("regularMarketPrice")
                    or info.get("currentPrice"),
                    "currency": info.get("currency", "USD"),
                    "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                    "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                    "fifty_day_average": info.get("fiftyDayAverage"),
                    "two_hundred_day_average": info.get(
                        "twoHundredDayAverage"
                    ),
                },
                "financial_health": {
                    "total_cash": info.get("totalCash"),
                    "total_debt": info.get("totalDebt"),
                    "free_cashflow": info.get("freeCashflow"),
                    "operating_cashflow": info.get("operatingCashflow"),
                    "ebitda": info.get("ebitda"),
                    "revenue_growth": info.get("revenueGrowth"),
                    "gross_margins": info.get("grossMargins"),
                    "ebitda_margins": info.get("ebitdaMargins"),
                },
                "analyst_data": {
                    "recommendation_key": info.get("recommendationKey"),
                    "recommendation_mean": info.get("recommendationMean"),
                    "number_of_analyst_opinions": info.get(
                        "numberOfAnalystOpinions"
                    ),
                    "target_high_price": info.get("targetHighPrice"),
                    "target_low_price": info.get("targetLowPrice"),
                    "target_mean_price": info.get("targetMeanPrice"),
                },
                "location": {
                    "address": info.get("address1"),
                    "city": info.get("city"),
                    "state": info.get("state"),
                    "zip": info.get("zip"),
                    "country": info.get("country"),
                },
                "metadata": {
                    "ticker": ticker,
                    "timestamp": datetime.now().isoformat(),
                    "data_source": "Yahoo Finance",
                },
            }

            return self._format_json_response(company_info)

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting company info for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get company information for {ticker}: {exc}"
            ) from exc

    def fetch_ticker_news(self, ticker: str, max_articles: int = 10) -> str:
        """
        Retrieve the latest news articles for a given stock ticker.

        Args:
            ticker: The stock ticker symbol
            max_articles: Maximum number of articles to return

        Returns:
            JSON string containing news articles

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If news data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            max_articles = max(1, min(50, max_articles))  # Limit between 1-50

            log_debug(f"Getting news for {ticker} (max: {max_articles})")

            ticker_obj = self._get_ticker_with_cache(ticker)

            # Rate limiting
            self._apply_rate_limit()

            try:
                news_data = ticker_obj.news
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch news data: {exc}"
                ) from exc

            if not news_data:
                return self._format_json_response(
                    {
                        "ticker": ticker,
                        "articles": [],
                        "count": 0,
                        "message": "No news articles found",
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            articles = []
            for i, article in enumerate(news_data[:max_articles]):
                try:
                    # Handle different news data structures
                    if isinstance(article, dict):
                        if "content" in article:
                            # New format
                            content = article["content"]
                            processed_article = {
                                "title": content.get("title", "No title"),
                                "summary": content.get("summary", ""),
                                "published_date": content.get("pubDate", ""),
                                "url": content.get("canonicalUrl", {}).get(
                                    "url", ""
                                ),
                                "source": article.get("source", "Unknown"),
                            }
                        else:
                            # Direct format
                            processed_article = {
                                "title": article.get("title", "No title"),
                                "summary": article.get("summary", ""),
                                "published_date": article.get(
                                    "providerPublishTime", ""
                                ),
                                "url": article.get("link", ""),
                                "source": article.get("publisher", "Unknown"),
                            }

                        articles.append(processed_article)

                except (KeyError, TypeError, ValueError) as exc:
                    log_warning(f"Error processing news article {i}: {exc}")
                    continue

            result = {
                "ticker": ticker,
                "articles": articles,
                "count": len(articles),
                "timestamp": datetime.now().isoformat(),
            }

            return self._format_json_response(result)

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"Unexpected error getting news for {ticker}: {exc}")
            raise YFinanceDataError(
                f"Failed to get news for {ticker}: {exc}"
            ) from exc

    def fetch_earnings_history(self, ticker: str) -> str:
        """
        Retrieves the earnings history for a specified stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing earnings history

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If earnings data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting earnings history for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                earnings_data = ticker_obj.earnings_history
                return self._process_dataframe_response(
                    earnings_data, ticker, "earnings_history"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch earnings history: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting earnings history for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get earnings history for {ticker}: {exc}"
            ) from exc

    def fetch_income_statement(self, ticker: str) -> str:
        """
        Retrieves the income statement for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing income statement data

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If financial data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting income statement for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                financials_data = ticker_obj.financials
                return self._process_dataframe_response(
                    financials_data, ticker, "income_statement"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch income statement: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting income statement for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get income statement for {ticker}: {exc}"
            ) from exc

    def fetch_quarterly_financials(self, ticker: str) -> str:
        """
        Retrieve the quarterly financials for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing quarterly financial data

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If financial data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting quarterly financials for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                quarterly_data = ticker_obj.quarterly_financials
                return self._process_dataframe_response(
                    quarterly_data, ticker, "quarterly_financials"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch quarterly financials: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting quarterly financials for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get quarterly financials for {ticker}: {exc}"
            ) from exc

    def fetch_balance_sheet(self, ticker: str) -> str:
        """
        Retrieve the balance sheet for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing balance sheet data

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If financial data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting balance sheet for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                balance_sheet_data = ticker_obj.balance_sheet
                return self._process_dataframe_response(
                    balance_sheet_data, ticker, "balance_sheet"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch balance sheet: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting balance sheet for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get balance sheet for {ticker}: {exc}"
            ) from exc

    def fetch_quarterly_balance_sheet(self, ticker: str) -> str:
        """
        Retrieve the quarterly balance sheet for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing quarterly balance sheet data

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If financial data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting quarterly balance sheet for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                quarterly_balance_data = ticker_obj.quarterly_balance_sheet
                return self._process_dataframe_response(
                    quarterly_balance_data, ticker, "quarterly_balance_sheet"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch quarterly balance sheet: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting quarterly balance sheet for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get quarterly balance sheet for {ticker}: {exc}"
            ) from exc

    def fetch_cashflow_statement(self, ticker: str) -> str:
        """
        Retrieve the annual cash flow statement for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing cash flow data

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If financial data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting cash flow for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                cashflow_data = ticker_obj.cashflow
                return self._process_dataframe_response(
                    cashflow_data, ticker, "cashflow"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch cash flow: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting cash flow for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get cash flow for {ticker}: {exc}"
            ) from exc

    def fetch_quarterly_cashflow_statement(self, ticker: str) -> str:
        """
        Retrieve the quarterly cash flow statement for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing quarterly cash flow data

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If financial data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting quarterly cash flow for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                quarterly_cashflow_data = ticker_obj.quarterly_cashflow
                return self._process_dataframe_response(
                    quarterly_cashflow_data, ticker, "quarterly_cashflow"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch quarterly cash flow: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting quarterly cash flow for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get quarterly cash flow for {ticker}: {exc}"
            ) from exc

    def fetch_major_shareholders(self, ticker: str) -> str:
        """
        Retrieve the list of major shareholders for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing major shareholders data

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If holder data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting major holders for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                major_holders_data = ticker_obj.major_holders
                return self._process_dataframe_response(
                    major_holders_data, ticker, "major_holders"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch major holders: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting major holders for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get major holders for {ticker}: {exc}"
            ) from exc

    def fetch_institutional_shareholders(self, ticker: str) -> str:
        """
        Retrieve the list of institutional shareholders for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing institutional shareholders data

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If holder data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting institutional holders for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                institutional_holders_data = ticker_obj.institutional_holders
                return self._process_dataframe_response(
                    institutional_holders_data, ticker, "institutional_holders"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch institutional holders: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting institutional holders for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get institutional holders for {ticker}: {exc}"
            ) from exc

    def fetch_analyst_recommendations(self, ticker: str) -> str:
        """
        Retrieve stock recommendations for a given ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing stock recommendations

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If recommendation data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting recommendations for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                recommendations_data = ticker_obj.recommendations
                return self._process_dataframe_response(
                    recommendations_data, ticker, "recommendations"
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch recommendations: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting recommendations for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get recommendations for {ticker}: {exc}"
            ) from exc

    def fetch_sustainability_scores(self, ticker: str) -> str:
        """
        Retrieve sustainability scores for a given stock ticker.

        Args:
            ticker: The stock ticker symbol

        Returns:
            JSON string containing sustainability scores

        Raises:
            YFinanceValidationError: If ticker is invalid
            YFinanceDataError: If sustainability data cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)
            log_debug(f"Getting sustainability scores for {ticker}")

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                sustainability_data = ticker_obj.sustainability

                if sustainability_data is None or sustainability_data.empty:
                    return self._format_json_response(
                        {
                            "ticker": ticker,
                            "sustainability_scores": None,
                            "message": "No sustainability data available",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                # Convert to JSON and parse
                sustainability_json = sustainability_data.to_json()
                sustainability_dict = json.loads(sustainability_json)

                # Extract ESG scores safely
                esg_scores = {}
                if "esgScores" in sustainability_dict:
                    esg_data = sustainability_dict["esgScores"]
                    # Get the first (and usually only) entry
                    if esg_data:
                        first_key = list(esg_data.keys())[0]
                        scores = esg_data[first_key]

                        esg_scores = {
                            "total_esg": scores.get("totalEsg"),
                            "environment_score": scores.get(
                                "environmentScore"
                            ),
                            "social_score": scores.get("socialScore"),
                            "governance_score": scores.get("governanceScore"),
                            "esg_performance": scores.get("esgPerformance"),
                            "peer_count": scores.get("peerCount"),
                            "peer_group": scores.get("peerGroup"),
                        }

                result = {
                    "ticker": ticker,
                    "sustainability_scores": esg_scores,
                    "timestamp": datetime.now().isoformat(),
                }

                return self._format_json_response(result)

            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch sustainability scores: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting sustainability scores for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get sustainability scores for {ticker}: {exc}"
            ) from exc

    def fetch_price_history(
        self, ticker: str, period: str = "1y", interval: str = "1d"
    ) -> str:
        """
        Retrieves the price history of a specified stock ticker.

        Args:
            ticker: The stock ticker symbol
            period: The time period. One of:
                '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd',
                'max'
            interval: The time interval. One of:
                '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d',
                '1wk', '1mo', '3mo'

        Returns:
            JSON string containing price history data

        Raises:
            YFinanceValidationError: If ticker, period, or interval is invalid
            YFinanceDataError: If price history cannot be retrieved
        """
        try:
            ticker = self._validate_ticker(ticker)

            # Validate period and interval
            if period not in self.VALID_PERIODS:
                valid_periods = ", ".join(self.VALID_PERIODS)
                raise YFinanceValidationError(
                    f"Invalid period '{period}'. Valid periods: {valid_periods}"
                )

            if interval not in self.VALID_INTERVALS:
                valid_intervals = ", ".join(self.VALID_INTERVALS)
                raise YFinanceValidationError(
                    f"Invalid interval '{interval}'. Valid intervals: {valid_intervals}"
                )

            log_debug(
                f"Getting price history for {ticker} (period: {period}, interval: {interval})"
            )

            ticker_obj = self._get_ticker_with_cache(ticker)

            try:
                history_data = ticker_obj.history(
                    period=period, interval=interval
                )

                if history_data.empty:
                    return self._format_json_response(
                        {
                            "ticker": ticker,
                            "period": period,
                            "interval": interval,
                            "data": [],
                            "message": "No price history data available",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                return self._process_dataframe_response(
                    history_data,
                    ticker,
                    "price_history",
                    {"period": period, "interval": interval},
                )

            except Exception as exc:  # pylint: disable=broad-exception-caught
                raise YFinanceDataError(
                    f"Failed to fetch price history: {exc}"
                ) from exc

        except (YFinanceValidationError, YFinanceDataError):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting price history for {ticker}: {exc}"
            )
            raise YFinanceDataError(
                f"Failed to get price history for {ticker}: {exc}"
            ) from exc

    # Private helper methods

    def _validate_ticker(self, ticker: str) -> str:
        """
        Validate and normalize ticker symbol.

        Args:
            ticker: Raw ticker symbol

        Returns:
            Normalized ticker symbol

        Raises:
            YFinanceValidationError: If ticker is invalid
        """
        if not ticker or not isinstance(ticker, str):
            raise YFinanceValidationError("Ticker symbol cannot be empty")

        # Normalize ticker (uppercase, strip whitespace)
        ticker = ticker.strip().upper()

        if not ticker:
            raise YFinanceValidationError(
                "Ticker symbol cannot be empty after normalization"
            )

        if not self.TICKER_PATTERN.match(ticker):
            raise YFinanceValidationError(
                f"Invalid ticker symbol format: {ticker}"
            )

        return ticker

    def _get_ticker_with_cache(self, ticker: str) -> Any:
        """
        Get ticker object with caching.

        Args:
            ticker: Validated ticker symbol

        Returns:
            YFinance Ticker object
        """
        if self.enable_caching and ticker in self._ticker_cache:
            cache_entry = self._ticker_cache[ticker]
            if time.time() - cache_entry["timestamp"] < self.cache_ttl:
                log_debug(f"Using cached ticker object for {ticker}")
                return cache_entry["ticker"]

        # Rate limiting
        self._apply_rate_limit()

        # Create new ticker object
        ticker_obj = yf.Ticker(ticker)

        if self.enable_caching:
            self._ticker_cache[ticker] = {
                "ticker": ticker_obj,
                "timestamp": time.time(),
            }

        return ticker_obj

    def _get_ticker_info(self, ticker_obj: Any, ticker: str) -> Dict[str, Any]:
        """
        Get ticker info with error handling.

        Args:
            ticker_obj: YFinance Ticker object
            ticker: Ticker symbol for error messages

        Returns:
            Ticker info dictionary

        Raises:
            YFinanceDataError: If info cannot be retrieved
        """
        try:
            info = ticker_obj.info
            if not info or not isinstance(info, dict):
                raise YFinanceDataError(
                    f"No information available for {ticker}"
                )
            return info
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise YFinanceDataError(
                f"Failed to get ticker info for {ticker}: {exc}"
            ) from exc

    def _apply_rate_limit(self) -> None:
        """Apply rate limiting between API requests."""
        if self.rate_limit_delay > 0:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - time_since_last
                time.sleep(sleep_time)
            self.last_request_time = time.time()

    def _format_json_response(self, data: Any) -> str:
        """
        Format response data as clean JSON string.

        Args:
            data: Data to format

        Returns:
            Clean JSON string
        """
        try:
            json_str = json.dumps(
                data, indent=2, ensure_ascii=False, default=str
            )
            return json_str
        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"Error formatting JSON response: {exc}")
            return json.dumps({"error": f"Failed to format response: {exc}"})

    def _process_dataframe_response(
        self,
        dataframe: Any,
        ticker: str,
        data_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Process pandas DataFrame response into JSON.

        Args:
            dataframe: Pandas DataFrame
            ticker: Ticker symbol
            data_type: Type of data for metadata
            metadata: Additional metadata to include

        Returns:
            JSON string containing processed data
        """
        try:
            if dataframe is None or (
                hasattr(dataframe, "empty") and dataframe.empty
            ):
                return self._format_json_response(
                    {
                        "ticker": ticker,
                        "data_type": data_type,
                        "data": [],
                        "message": f"No {data_type} data available",
                        "timestamp": datetime.now().isoformat(),
                        **(metadata or {}),
                    }
                )

            # Convert DataFrame to JSON
            if hasattr(dataframe, "to_json"):
                json_data = dataframe.to_json(
                    orient="index", date_format="iso"
                )
                parsed_data = json.loads(json_data)
            else:
                # Handle non-DataFrame data
                parsed_data = str(dataframe)

            result = {
                "ticker": ticker,
                "data_type": data_type,
                "data": parsed_data,
                "timestamp": datetime.now().isoformat(),
                **(metadata or {}),
            }

            return self._format_json_response(result)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            log_error(f"Error processing {data_type} data for {ticker}: {exc}")
            return self._format_json_response(
                {
                    "ticker": ticker,
                    "data_type": data_type,
                    "error": f"Failed to process {data_type} data: {exc}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return precise, structured instructions for LLM tool calling."""
        instructions = """
<yahoo_finance_tools_instructions>
Yahoo Finance market + company data for a single ticker

GOAL
- Fetch market + company fundamentals from Yahoo Finance (via yfinance) for ONE ticker.

OUTPUT (ALWAYS)
- Returns a JSON string.
- Many responses include `timestamp`.

INPUT
- ticker: e.g. "AAPL", "MSFT", or with exchange suffix like "ASML.AS".

ROUTING (PICK ONE)
- Price now: fetch_current_stock_price(ticker)
- Profile/summary/metrics: fetch_company_information(ticker)
- News: fetch_ticker_news(ticker, max_articles=10)  # 1..50
- Chart/history: fetch_price_history(ticker, period="1mo", interval="1d")
- Earnings: fetch_earnings_history(ticker)
- Annual statements: fetch_income_statement / fetch_balance_sheet / fetch_cashflow_statement
- Quarterly statements: fetch_quarterly_financials / fetch_quarterly_balance_sheet / fetch_quarterly_cashflow_statement
- Ownership: fetch_major_shareholders / fetch_institutional_shareholders
- Analyst sentiment: fetch_analyst_recommendations
- ESG: fetch_sustainability_scores

VALID PERIODS / INTERVALS
- period: 1d/5d/1mo/3mo/6mo/1y/2y/5y/10y/ytd/max
- interval: 1m/2m/5m/15m/30m/60m/90m/1h/1d/5d/1wk/1mo/3mo

CONTEXT-SIZE RULES (IMPORTANT)
- Prefer SHORTER `period` and COARSER `interval` to keep outputs small.
  - Good defaults: period="1mo", interval="1d" (or period="1y", interval="1wk").
- Avoid dumping full JSON history/statements into the final answer; summarize key values.

ERRORS
- Bad input: YFinanceValidationError
- Retrieval/processing: YFinanceDataError

</yahoo_finance_tools_instructions>
"""
        return instructions
