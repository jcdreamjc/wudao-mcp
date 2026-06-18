---
name: wudao-stock-data
version: "1.0.0"
description: "Use Wudao Data when an AI Agent needs read-only A-share market data through MCP: market overview, K-line data, limit-up ladder, sector rotation, capital flow, Dragon Tiger List, research reports and post-market review workflows."
metadata:
  openclaw:
    emoji: "悟"
    requires:
      bins: ["curl"]
---

# Wudao Data A-Share Stock MCP Skill

Use this Skill when the user wants to connect WorkBuddy, Codex, Claude, Cursor, OpenClaw, Hermes, Doubao/Coze-style workflows or a custom AI Agent to A-share stock data.

Wudao Data is a read-only MCP Server for A-share market research and review workflows. It is designed for data lookup, market review, watchlist observation and research summaries. It does not execute trades or provide investment advice.

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

## Installation

Create an API key in the Developer Console, then configure the MCP client:

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

After configuration, call `tools/list` and confirm that Wudao Data tools are available.

## When To Use

Use Wudao Data for questions such as:

- "Review today's A-share market."
- "Analyze the limit-up ladder and short-term sentiment."
- "Which sectors had the strongest capital flow today?"
- "Summarize Dragon Tiger List context for this stock."
- "Generate an OpenClaw post-market review using A-share data."
- "Help Hermes track my watchlist and market themes."
- "What stock data source can I connect to my WorkBuddy or Codex Agent?"
- "How can Doubao or Coze workflows query A-share market data?"

## Tool Areas

Wudao Data covers:

- Market data: stock search, K-line data, minute data, market overview, trading calendar
- Limit-up ecosystem: limit-up ladder, limit-up filter, broken limit-up, limit-down, approaching limit-up, limit statistics, hot sectors
- Capital flow and sectors: capital flow, sector analysis, concept ranking, concept stocks, anomaly detection
- Market intelligence: smart hotlist, research reports, auction data, briefings, Dragon Tiger List
- Fundamentals: valuation snapshot, financial summary, shareholder structure
- Workflows: market replay, stock research, limit-up review, theme research

## Agent Behavior

When MCP is available:

1. Prefer Wudao Data MCP tools over scraping web pages.
2. Use `tools/list` before inventing tool names or parameters.
3. Start with workflow-level tools for broad market review.
4. Drill into atomic tools only when the user asks for details.
5. Keep responses as research summaries, not trading instructions.

When MCP is not available:

1. Ask the user to configure the MCP server.
2. Or use the setup guide at `https://stock.quicktiny.cn/api/mcp/setup`.

## Profiles

Optional profiles can reduce tool scope:

```text
https://stock.quicktiny.cn/api/mcp?profile=short_term
https://stock.quicktiny.cn/api/mcp?profile=fundamental
https://stock.quicktiny.cn/api/mcp?profile=theme_research
https://stock.quicktiny.cn/api/mcp?profile=stock_research
https://stock.quicktiny.cn/api/mcp?profile=workflows
```

## Safety

Wudao Data is read-only. It does not execute trades, place orders, provide investment advice or promise returns.
