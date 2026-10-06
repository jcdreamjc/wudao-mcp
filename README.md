# Wudao A-Share Stock Data MCP

Wudao A-Share Stock Data MCP (悟道 A股股票数据 MCP) is a remote HTTP MCP server for China A-share market data. It serves 63 tools to AI agents: 57 read-only query tools and 6 tools that manage the caller's own watchlist. It does not place trades.

It is maintained by 杭州瞬微网络科技有限公司 (QuickTiny) and shares accounts with 连板天梯. The facts below were checked against the live manifest on 2026-10-06; the manifest and `tools/list` are authoritative.

- Endpoint: `https://stock.quicktiny.cn/api/mcp` (Streamable HTTP, stateless JSON-RPC over POST; no stdio)
- Auth: `Authorization: Bearer YOUR_API_KEY`, with a key from the [developer console](https://stock.quicktiny.cn/developer); gateways that reserve `Authorization` (for example Smithery) can send the same key as `X-API-Key: YOUR_API_KEY`
- Manifest: https://stock.quicktiny.cn/api/mcp/manifest
- Docs: [client setup](https://data.quicktiny.cn/docs.html#clients) · [tool catalog](https://data.quicktiny.cn/stock-data-mcp.html#tools) · [pricing and limits](https://data.quicktiny.cn/pricing.html) · [product facts](https://data.quicktiny.cn/agent-discovery.html)
- Not affiliated with Tushare

## Quick start

Claude Code:

```bash
claude mcp add --transport http wudao https://stock.quicktiny.cn/api/mcp --header "Authorization: Bearer YOUR_API_KEY"
```

Codex CLI:

```bash
export WUDAO_API_KEY=YOUR_API_KEY
codex mcp add wudao --url https://stock.quicktiny.cn/api/mcp --bearer-token-env-var WUDAO_API_KEY
```

Cursor, WorkBuddy and other clients configured with JSON:

```json
{
  "mcpServers": {
    "wudao-stock-data": {
      "url": "https://stock.quicktiny.cn/api/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Then ask the agent to call `trading_calendar` with `date="2026-09-04"`; it should return `isTradingDay: true`.

Tested on 2026-10-06 with Claude Code 2.1.284: tool discovery, `trading_calendar` and `limit_up_ladder` returned structured results. The Codex command follows `codex mcp add --help` in Codex CLI 0.130.0. Other clients use the standard remote HTTP configuration and were not each tested end to end. WorkBuddy steps: [WorkBuddy guide](https://data.quicktiny.cn/workbuddy-stock-data-mcp.html).

## Pricing and limits

| Tier | Calls per day | Per minute | Price | 09:15–10:30 Beijing time |
| --- | ---: | ---: | --- | --- |
| Free | 50 | 30 | 0 | MCP calls paused |
| Basic | 2,000 | 30 | ¥1,000 / 365 days | not paused |
| Pro | 5,000 | 50 | ¥2,000 / 365 days | not paused |
| Enterprise | 20,000 | 150 | ¥5,000 / 365 days | not paused |

Each `tools/call` counts once, workflow tools included; `initialize`, `tools/list` and the manifest are free. Quota is per account across all keys and resets at 00:00 Beijing time. Prices are as of 2026-10-06; the [purchase page](https://stock.quicktiny.cn/membership?tab=apiQuota) is authoritative.

## Tools

57 tools only read data. The 6 marked "writes" change only the caller's own watchlist and groups.

### Market data

- `stock_search`: find a stock by name, code, pinyin or industry keyword
- `kline`: daily K-line, optional forward adjustment, merged with intraday quotes
- `minute_data`: intraday or historical minute prices, average price and volume
- `stock_rank`: live rankings by gain, loss, turnover and amount
- `market_overview`: market breadth: advancers, decliners and market temperature
- `trading_calendar`: whether a date is an A-share trading day
- `index_market`: index search, snapshots, rankings, daily and minute bars
- `etf_market`: ETF search, snapshots, rankings, daily and minute bars
- `convertible_bond_market`: convertible bonds with underlying mapping and conversion premium

### Limit-up ecosystem

- `limit_up_ladder`: limit-up stocks layered by consecutive boards, theme ranking and promotion rates
- `limit_up_filter`: filter limit-up records by date range, boards, theme, industry, market cap and orders
- `limit_up_premium`: next-day premium statistics for limit-up stocks
- `broken_limit_up`: stocks that touched limit-up but failed to hold it
- `limit_down`: limit-down pool with sealed orders
- `approaching_limit_up`: stocks close to limit-up that have not sealed
- `limit_stats`: sealed and broken counts, seal rate, day-over-day comparison
- `limit_events`: second-level seal and break event stream
- `limit_event_summary`: earliest seals, most breaks, re-seals and late-session events
- `board_break_analysis`: how yesterday's limit-up stocks trade today
- `short_term_emotion`: short-term sentiment snapshot: limits, break rate, promotion rate, breadth

### Capital flow and sectors

- `capital_flow`: daily money flow for stocks, the market and northbound funds
- `intraday_main_flow`: intraday main-force flow for selected stocks
- `theme_intraday_capital`: theme and sector strength with intraday capital curves
- `theme_stocks`: constituents of a theme or sector
- `sector_analysis`: sector rotation quadrants (momentum x strength)
- `anomaly_detection`: exchange-rule price deviation alerts
- `stock_screener`: screen by theme, industry, price, market cap, change, turnover and valuation

### Call auction

- `auction_market_scan`: market-wide auction scan by amount, limit-up bids, change and volume ratio
- `auction_opening_snapshot`: six fixed opening-auction views in one call
- `auction_theme_strength`: auction strength aggregated by theme
- `auction_data`: auction details for given stocks with historical percentiles

### Market intelligence and news

- `dragon_tiger`: Dragon Tiger List entries and broker seats
- `research_reports`: broker ratings, target prices and earnings forecasts
- `smart_hotlist`: combined stock popularity rankings
- `news_hotlist`: financial news hot lists
- `cls_news`: real-time newsflash filtered by keyword, stock, level and time
- `briefings`: morning, midday, close and evening market briefings

### Events and calendars

- `stock_event_calendar`: unlocks, holder changes, buybacks, dividends and report dates
- `unlock_events`: restricted share unlock schedule
- `market_catalyst_calendar`: policy meetings, industry events, launches and index changes
- `macro_calendar`: global economic data and central bank events

### Fundamentals

- `valuation_snapshot`: valuation, market cap, turnover and dividend yield
- `financial_summary`: statements, ratios, audit opinion and revenue mix
- `shareholder_structure`: top holders, holder count, pledges, dividends and buybacks
- `margin_trading`: margin financing and securities lending
- `northbound_holdings`: Stock Connect holdings

### Official disclosures

- `official_announcements`: listed company announcements
- `official_interactions`: exchange investor Q&A platforms
- `official_disclosure_evidence`: announcements and Q&A bundled for one stock

### Overseas disclosures

- `sec_company_search`: SEC CIK lookup by ticker or name
- `sec_filings`: 10-K, 10-Q, 8-K and other SEC filings
- `sec_company_facts`: SEC XBRL company facts

### Review workflows

- `market_replay_workflow`: trading day, breadth, limits, ladder, theme ranking and briefing in one call
- `limitup_review_workflow`: limit stats, ladder, themes, broken and limit-down pools in one call
- `stock_research_workflow`: search, K-line, flow, reports and Dragon Tiger data for one stock

### Watchlist (caller's own)

- `watchlist_list`: read your watchlist with groups, tags and notes
- `watchlist_group_list`: read your watchlist groups
- `watchlist_add`: add stocks the user named to the watchlist (writes)
- `watchlist_remove`: remove stocks from the watchlist (writes)
- `watchlist_update_stock`: change group, tags or notes of a watchlist entry (writes)
- `watchlist_group_create`: create an empty group (writes)
- `watchlist_group_rename`: rename a group (writes)
- `watchlist_group_delete`: delete a group (writes)

## Profiles

One server with the default `all` profile is enough for most agents. To narrow the tool list, append `?profile=` or send `X-MCP-Profile`: `short_term`, `fundamental`, `market_replay`, `stock_research`, `theme_research`, `auction_review`, `personal`, `user`, `workflows`, `all`.

```text
https://stock.quicktiny.cn/api/mcp?profile=market_replay
```

## Fit

Good fit: agents that run A-share post-market reviews (limit-up ladder, theme rotation, capital flow, Dragon Tiger List), opening-auction checks and event or risk calendars without building their own data tools.

Not a fit: long-horizon historical warehouses and factor research (Tushare or a local database), low-latency trading systems (broker or commercial market data APIs), research centred on global markets (for example Alpha Vantage), and anything that needs trade execution.

## Evidence

- [2026-09-04 market review case](https://data.quicktiny.cn/ai-agent-a-share-workflow.html) with its [public JSON](https://data.quicktiny.cn/examples/market-replay-2026-09-04.json)
- [Reproducible source check](examples/source-check/README.md): maintainer-run, failed requests included; not an independent ranking
- [Empty results, date mismatches and error states](https://data.quicktiny.cn/stock-agent-data-status.html)
- [OpenClaw / Hermes review workflow](docs/openclaw-hermes-a-share-review.md)

## Directories

- Official MCP Registry: `io.github.jcdreamjc/wudao-mcp`
- [ModelScope](https://www.modelscope.cn/mcp/servers/quicktiny/wudao-a-share-stock-data-mcp) · [Glama](https://glama.ai/mcp/servers/jcdreamjc/wudao-mcp) · [LobeHub](https://lobehub.com/zh/mcp/jcdreamjc-wudao-mcp) · [MCP.so](https://chat.mcp.so/server/wudao-a-share-stock-data-mcp/quicktiny)

Directory pages may lag; the manifest and this README are current.

## Skill

[`skills/wudao-stock-data/SKILL.md`](skills/wudao-stock-data/SKILL.md) explains when to use the server, how to configure it and how to pick tools for review tasks.

## Wrapped config for marketplaces

Some marketplaces ask for a wrapped config object:

```json
{
  "config": {
    "mcpServers": {
      "wudao-stock-data": {
        "url": "https://stock.quicktiny.cn/api/mcp",
        "headers": {
          "Authorization": "Bearer YOUR_API_KEY"
        },
        "params": {}
      }
    }
  }
}
```

## Safety boundary

Read-only except the 6 watchlist tools, which change only the caller's own watchlist. No trade execution, investment advice or return promises.
