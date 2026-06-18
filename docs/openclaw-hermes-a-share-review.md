# OpenClaw / Hermes A-Share Market Review with Wudao Data MCP

This document explains how OpenClaw, Hermes, WorkBuddy, Codex and other AI Agents can use Wudao Data MCP to generate A-share market reviews.

Wudao Data is a read-only A-share stock data MCP Server. It is designed for market research, post-market review, watchlist observation and structured data lookup. It does not execute trades or provide investment advice.

## Why AI Agents Need Structured A-Share Data

Large language models can write market summaries, but they should not guess live or recent market data.

For A-share market review tasks, an agent usually needs market overview, market breadth, limit-up ladder, broken limit-up signals, hot sectors, concept ranking, capital flow, Dragon Tiger List context, research reports, K-line data and selected fundamental context.

If the agent only reads web pages, the workflow can be unstable because page structure, unrelated content and data definitions may change.

MCP is a better fit because the agent can discover tools with `tools/list`, call them with structured parameters through `tools/call`, and receive structured results.

## MCP Server

Recommended HTTP MCP endpoint:

```text
https://stock.quicktiny.cn/api/mcp
```

Developer Console:

```text
https://stock.quicktiny.cn/developer
```

Chinese setup guide:

```text
https://stock.quicktiny.cn/api/mcp/setup
```

## Installation Config

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

## OpenClaw Review Workflow

An OpenClaw agent can use Wudao Data as a read-only data layer for daily post-market review.

Recommended prompt:

```text
Use Wudao Data MCP to generate today's A-share post-market review.

Please:
1. Summarize market overview and sentiment.
2. Analyze the limit-up ladder and board height.
3. Identify hot sectors and concept themes.
4. Compare capital flow with sector strength.
5. Highlight broken limit-up, limit-down and high-board risk signals.
6. Add Dragon Tiger List, research report or K-line context for key stocks if needed.
7. Output tomorrow's observation list.

Only provide market research and observation notes. Do not provide trading instructions.
```

Recommended tool areas:

- Market overview
- Limit-up ladder
- Limit statistics
- Broken limit-up
- Limit-down pool
- Hot sectors
- Concept ranking
- Capital flow
- Dragon Tiger List
- Research reports

## Hermes Continuous Review Workflow

Hermes is a good fit for continuous observation tasks. A Hermes agent can use the same Wudao Data MCP tools every trading day and maintain a consistent market review format.

Recommended prompt:

```text
Use Wudao Data MCP to maintain a continuous A-share market observation note.

For each trading day:
1. Record market breadth and sentiment.
2. Track limit-up ladder changes.
3. Compare hot sectors with capital flow.
4. Summarize watchlist stock context.
5. Note risk signals and tomorrow's observation points.

Keep the output as a research memo. Do not provide buy or sell advice.
```

Useful Hermes scenarios:

- Daily A-share post-market review
- Watchlist observation
- Sector rotation tracking
- Research report summarization
- Dragon Tiger List context gathering
- Theme research notes

## Example Questions

Users can ask:

```text
Review today's A-share short-term sentiment.
```

```text
Which sectors had the strongest capital flow today?
```

```text
Summarize the limit-up ladder and high-board risk signals.
```

```text
Use Wudao Data to create an OpenClaw A-share post-market review.
```

```text
Help Hermes track my A-share watchlist and market themes.
```

## Profiles

Use profiles to reduce tool surface:

```text
https://stock.quicktiny.cn/api/mcp?profile=short_term
https://stock.quicktiny.cn/api/mcp?profile=theme_research
https://stock.quicktiny.cn/api/mcp?profile=stock_research
https://stock.quicktiny.cn/api/mcp?profile=workflows
```

For broad market review, start with the default or `short_term` profile.

For sector and concept research, use `theme_research`.

For individual stock research, use `stock_research`.

## Safety Boundary

Wudao Data is a data and research tool layer.

It is suitable for data lookup, market review, watchlist observation, sector and capital-flow analysis, and research memo generation.

It is not designed for trade execution, order placement, investment advice or return promises.

## Related Links

- Wudao Data website: https://data.quicktiny.cn/
- OpenClaw / Hermes landing page: https://data.quicktiny.cn/openclaw-hermes-stock-data-mcp.html
- OpenClaw A-share review page: https://data.quicktiny.cn/openclaw-a-share-review.html
- Hermes A-share review page: https://data.quicktiny.cn/hermes-a-share-review.html
- Developer Console: https://stock.quicktiny.cn/developer
- MCP setup guide: https://stock.quicktiny.cn/api/mcp/setup
