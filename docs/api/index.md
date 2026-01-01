# API Reference

This section is the **API-level reference** for Enhanced Toolkits.

In this project, most API pages are rendered from the Python source via MkDocs plugins (e.g. MkDocstrings). If your docs build does not include those plugins, you can still use the toolkit guides under [`docs/toolkits/`](../toolkits/index.md).

> Note: tool schemas are **strict**. Agents should pass **all parameters** shown in tool signatures.

## Core Toolkits

- **[Reasoning Tools](reasoning.md)** — `ReasoningTools`
- **[Search Tools (SearxNG)](searxng.md)** — `SearxngTools`
- **[Thinking Tools](thinking.md)** — `ThinkingTools`
- **[Files Tools](files.md)** — `FilesTools`
- **[Finance Tools](finance.md)** — `YFinanceTools`
- **[YouTube Tools](youtube.md)** — `YouTubeTools`
- **[Weather Tools](weather.md)** — `WeatherTools`
- **[Downloading Tools](downloader.md)** — `DownloadingTools`

## Calculator Modules

Calculator tools are separate classes under `enhancedtoolkits.calculators`.

- **[Arithmetic](calculators/arithmetic.md)**
- **[Time Value](calculators/time-value.md)**
- **[Investment](calculators/investment.md)**
- **[Loan](calculators/loan.md)**
- **[Bond](calculators/bond.md)**
- **[Risk](calculators/risk.md)**
- **[Depreciation](calculators/depreciation.md)**
- **[Business](calculators/business.md)**
- **[Utility](calculators/utility.md)**

## Base Classes

- **[StrictToolkit](base.md)** — `StrictToolkit`

## Common Import Patterns

```python
# Core toolkits
from enhancedtoolkits import (
    ReasoningTools,
    SearxngTools,
    ThinkingTools,
    FilesTools,
    YFinanceTools,
    YouTubeTools,
    WeatherTools,
    DownloadingTools,
)

# Calculator modules
from enhancedtoolkits.calculators import (
    ArithmeticCalculatorTools,
    TimeValueCalculatorTools,
    InvestmentAnalysisCalculatorTools,
    LoanCalculatorTools,
    BondCalculatorTools,
    RiskMetricsCalculatorTools,
    DepreciationCalculatorTools,
    BusinessAnalysisCalculatorTools,
    UtilityCalculatorTools,
)
```

## Related Docs

- [`docs/toolkits/index.md`](../toolkits/index.md)
- [`docs/calculators/index.md`](../calculators/index.md)
- [`docs/getting-started/index.md`](../getting-started/index.md)
