# Manual API Reference

This page is a **manual**, import-free overview of the public tool/function surface.

For authoritative details, see the API pages in this section (or browse the repository source).

## Core Toolkits (function names agents can call)

### OrchestrationTools
Class: `OrchestrationTools` (see [API page](orchestration.md))

Returns: **JSON string**

Direct toolkit function names:

- `create_plan(agent_or_team, goal, tasks=None, constraints=None, max_tasks=50)`
- `add_task(agent_or_team, title, description=None, priority=0, depends_on=None)`
- `update_task_status(agent_or_team, task_id, status, result_summary=None)`
- `next_actions(agent_or_team, max_actions=1, mark_in_progress=True)`
- `summarize_progress(agent_or_team)`
- `reset_plan(agent_or_team)`

Auto-injected function names (available from any toolkit instance):

- `orchestrator_create_plan(...)`
- `orchestrator_add_task(...)`
- `orchestrator_update_task_status(...)`
- `orchestrator_next_actions(...)`
- `orchestrator_summarize_progress(...)`
- `orchestrator_reset_plan(...)`

### ReasoningTools
Class: `ReasoningTools` (see [API page](reasoning.md))

Returns: **text**

- `add_structured_reasoning_step(agent_or_team, problem, cognitive_mode='analysis', reasoning_type='deductive', evidence=None, confidence=0.5)`
- `add_meta_cognitive_reflection(agent_or_team, reflection, step_id=None)`
- `manage_working_memory_scratchpad(agent_or_team, key, value=None, operation='set')`
- `assess_reasoning_quality_and_suggest_improvements(agent_or_team)`
- `synthesize_reasoning_chain_into_conclusion_or_insight(agent_or_team, synthesis_type='conclusion')`
- `retrieve_current_reasoning_session_state(agent_or_team)`
- `reset_reasoning_session_state(agent_or_team)`

### SearxngTools
Class: `SearxngTools` (see [API page](searxng.md))

Returns: **JSON string**

- `perform_web_search(query, max_results=None)`
- `perform_news_search(query, max_results=None)`
- `perform_image_search(query, max_results=None)`
- `perform_video_search(query, max_results=None)`
- `perform_category_search(query, category, max_results=None)`

### ThinkingTools
Class: `ThinkingTools` (see [API page](thinking.md))

Returns: **text**

- `build_step_by_step_reasoning_chain(agent, problem, thinking_type='analysis', context=None, evidence=None, confidence=0.5)`
- `add_meta_cognitive_reflection(agent, reflection, step_id=None)`
- `manage_working_memory_scratchpad(agent, key, value=None, operation='set')`
- `assess_reasoning_chain_quality_and_suggest_improvements(agent)`
- `synthesize_reasoning_chain_into_output(agent, synthesis_type='conclusion')`
- `retrieve_current_thinking_chain_state(agent)`
- `reset_current_thinking_chain(agent)`

### FilesTools
Class: `FilesTools` (see [API page](files.md))

Returns: **JSON string**

- `read_file_lines_chunk(file_name, chunk_size=100, offset=0)`
- `replace_file_lines_chunk(file_name, new_lines, offset, length)`
- `insert_lines_into_file_chunk(file_name, new_lines, offset)`
- `delete_lines_from_file_chunk(file_name, offset, length)`
- `save_file_with_validation(contents, file_name, overwrite=True)`
- `retrieve_file_metadata(file_name)`
- `list_files_with_pattern(pattern='**/*')`
- `search_files_by_name_regex(regex_pattern, recursive=True, max_results=1000)`
- `search_file_contents_by_regex(regex_pattern, file_pattern='**/*', recursive=False, max_files=100, max_matches=1000, context_lines=2)`

### YFinanceTools
Class: `YFinanceTools` (see [API page](finance.md))

Returns: **JSON string**

- `fetch_current_stock_price(ticker)`
- `fetch_company_information(ticker)`
- `fetch_ticker_news(ticker, max_articles=10)`
- `fetch_earnings_history(ticker)`
- `fetch_income_statement(ticker)`
- `fetch_quarterly_financials(ticker)`
- `fetch_balance_sheet(ticker)`
- `fetch_quarterly_balance_sheet(ticker)`
- `fetch_cashflow_statement(ticker)`
- `fetch_quarterly_cashflow_statement(ticker)`
- `fetch_major_shareholders(ticker)`
- `fetch_institutional_shareholders(ticker)`
- `fetch_analyst_recommendations(ticker)`
- `fetch_sustainability_scores(ticker)`
- `fetch_price_history(ticker, period='1y', interval='1d')`

### YouTubeTools
Class: `YouTubeTools` (see [API page](youtube.md))

Returns: **JSON string**

- `fetch_youtube_video_metadata(video_url)`
- `extract_youtube_video_id(video_url)`
- `fetch_comprehensive_youtube_video_info(video_url, include_transcript=False)`
- `fetch_youtube_video_transcript(video_url, language='en', auto_generated=True)`
- `fetch_available_youtube_transcripts(video_url)`
- `fetch_youtube_transcript_languages(video_url)`

### WeatherTools
Class: `WeatherTools` (see [API page](weather.md))

Returns: **JSON string**

- `fetch_current_weather_conditions(location, language='en')`
- `fetch_weather_forecast(location, days=3, language='en')`
- `fetch_temperature_data(location, language='en')`
- `fetch_weather_text_description(location, language='en')`

### DownloadingTools
Class: `DownloadingTools` (see [API page](downloader.md))

Returns: **text** (sometimes JSON strings for metadata)

- `get_file_from_url(url, output='auto')`
- `access_website_content(url, output='auto')`
- `download_multiple_urls(urls, output='auto')`
- `get_url_metadata(url)`
- `check_url_accessibility(url)`

## Calculator Modules

Calculator tools are exposed as independent classes under `enhancedtoolkits.calculators`. All functions return **JSON strings**.

- [`ArithmeticCalculatorTools`](calculators/arithmetic.md)
- [`TimeValueCalculatorTools`](calculators/time-value.md)
- [`InvestmentAnalysisCalculatorTools`](calculators/investment.md)
- [`LoanCalculatorTools`](calculators/loan.md)
- [`BondCalculatorTools`](calculators/bond.md)
- [`RiskMetricsCalculatorTools`](calculators/risk.md)
- [`DepreciationCalculatorTools`](calculators/depreciation.md)
- [`BusinessAnalysisCalculatorTools`](calculators/business.md)
- [`UtilityCalculatorTools`](calculators/utility.md)

## Base

All toolkits inherit from [`StrictToolkit`](base.md).