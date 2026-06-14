# Wudao A-Share Stock Data MCP

Wudao A-Share Stock Data MCP is a structured China A-share market data MCP Server for WorkBuddy, OpenClaw, Hermes, Claude, Cursor, Codex and custom AI Agents.

It provides structured, read-only tools for A-share market overview, K-line data, minute data, stock ranking, limit-up ladder, sector rotation, capital flow, Dragon Tiger List, research reports, valuation snapshots, financial summaries and post-market review workflows.

- Website: https://data.quicktiny.cn/
- GitHub Pages: https://jcdreamjc.github.io/wudao-mcp/
- Developer Console: https://stock.quicktiny.cn/developer
- MCP endpoint: https://stock.quicktiny.cn/api/mcp
- Streamable HTTP endpoint: https://stock.quicktiny.cn/api/mcp-stream
- Manifest: https://stock.quicktiny.cn/api/mcp/manifest
- Setup guide: https://stock.quicktiny.cn/api/mcp/setup
- OpenClaw / Hermes guide: https://data.quicktiny.cn/openclaw-hermes-stock-data-mcp.html
- WorkBuddy guide: https://data.quicktiny.cn/workbuddy-stock-data-mcp.html

## MCP Directories

Wudao A-Share Stock Data MCP is listed in several MCP directories and AI agent marketplaces:

- Glama: https://glama.ai/mcp/servers/jcdreamjc/wudao-mcp
- MCP.so: https://chat.mcp.so/server/wudao-a-share-stock-data-mcp/quicktiny
- LobeHub: https://lobehub.com/zh/mcp/jcdreamjc-wudao-mcp
- ModelScope MCP: https://www.modelscope.cn/mcp/servers/quicktiny/wudao-a-share-stock-data-mcp

## Docs

- OpenClaw / Hermes A-share review workflow: [docs/openclaw-hermes-a-share-review.md](docs/openclaw-hermes-a-share-review.md)

## Installation

Create an API key in the Developer Console:

```text
https://stock.quicktiny.cn/developer
```

Then add Wudao A-Share Stock Data MCP as a Streamable HTTP MCP server.

```json
{
  "mcpServers": {
    "wudao-stock-data": {
      "type": "streamableHttp",
      "url": "https://stock.quicktiny.cn/api/mcp-stream",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

If your MCP client does not support Streamable HTTP yet, use the JSON-RPC compatible endpoint:

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

For Chinese setup instructions across WorkBuddy, Cursor, Codex CLI, Claude Code, OpenClaw, Hermes and generic MCP clients, see:

```text
https://stock.quicktiny.cn/api/mcp/setup
```

## OpenClaw / Hermes Submission Config

Some MCP marketplaces request a wrapped config object. Use this version:

```json
{
  "type": "streamableHttp",
  "config": {
    "mcpServers": {
      "wudao-stock-data": {
        "type": "streamableHttp",
        "url": "https://stock.quicktiny.cn/api/mcp-stream",
        "headers": {
          "Authorization": "Bearer YOUR_API_KEY"
        },
        "params": {}
      }
    }
  }
}
```

## Skill

This repository includes a market-friendly Skill guide:

```text
skills/wudao-stock-data/SKILL.md
```

The Skill explains when to use Wudao A-Share Stock Data MCP, how to configure the MCP server, how to verify `tools/list`, and how agents should choose tools for A-share market review tasks.

## Available Tool Areas

Wudao A-Share Stock Data MCP currently exposes 61 tools across these areas:

- Market data: stock search, K-line data, minute data, stock ranking, market overview, trading calendar
- Limit-up ecosystem: limit-up ladder, limit-up filter, broken limit-up, limit-down, approaching limit-up, limit statistics, hot sectors, limit events
- Capital flow and sectors: capital flow, sector analysis, concept ranking, concept stocks, anomaly detection
- Market intelligence: smart hotlist, news hotlist, CLS news, research reports, auction data, market briefings, Dragon Tiger List
- Fundamentals: valuation snapshot, financial summary, shareholder structure
- Workflows: market replay, stock research, limit-up review, theme research
- Events and official disclosures: company events, macro calendar, short-term catalysts, official announcements, investor interactions, SEC disclosures
- Watchlist: personal watchlist lookup, grouping, tags and remarks

## Common Agent Tasks

Wudao A-Share Stock Data MCP is useful when the user asks an AI Agent to:

- Review today's A-share market after close
- Analyze limit-up ladder and short-term sentiment
- Find the strongest sectors and capital-flow themes
- Summarize Dragon Tiger List and research-report context
- Track watchlists and generate market observation notes
- Compare A-share data workflows for WorkBuddy, OpenClaw, Hermes, Claude or Cursor

## Profiles

Profiles can be used to reduce the tool surface:

- `short_term`: short-term trading and market intelligence tools
- `auction_review`: opening auction review tools
- `theme_research`: sector and concept research
- `stock_research`: individual stock research
- `market_replay`: market review tools
- `personal` / `user`: personal watchlist tools
- `workflows`: workflow-level tools only
- `all`: all available tools

Example:

```text
https://stock.quicktiny.cn/api/mcp-stream?profile=short_term
```

## Safety Boundary

Wudao A-Share Stock Data MCP is a read-only data layer for AI Agent research, market review and observation workflows.

It does not execute trades, place orders, provide investment advice or promise returns.

## Tags

```text
mcp,stock,a-share,china-stock,market-data,ai-agent,openclaw,hermes,finance,research-data
```
