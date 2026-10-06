---
name: wudao-a-share-review
description: 用悟道 A股数据连接器查询行情、涨停梯队、题材资金、集合竞价、龙虎榜和事件日历，生成写明数据日期的盘后复盘；用户明确要求时管理本人自选股。
---

# 悟道 A股数据：复盘与研究

## 什么时候用

用户要做 A股盘后复盘、看涨停梯队和题材、查资金流或龙虎榜、看开盘前集合竞价、查解禁和财报披露等事件，或者管理自己的自选股时使用。

不要用来下单或给买卖建议。悟道不执行交易，输出定位为研究材料。

## 先确认交易日

1. 任何按日期的任务，先调用 `trading_calendar` 确认目标日期是否为交易日。
2. 非交易日时，告诉用户最近的交易日，并按那一天查询；回答里写清两个日期。
3. 每个返回都看 `tradeDate`、`actualTradeDate`、`dateStatus` 和 `qualityWarnings`。`dateStatus=mismatch` 时，不要把实际日期的数据说成用户要的日期。

## 常见任务用哪些工具

| 任务 | 工具 |
| --- | --- |
| 收盘复盘 | `market_replay_workflow`（一次返回交易日、市场概况、涨跌停、梯队、题材排行和简报）；要细节再用 `market_overview`、`limit_stats`、`limit_up_ladder` |
| 涨停与情绪 | `limitup_review_workflow`、`board_break_analysis`、`short_term_emotion`、`limit_up_premium` |
| 题材与资金 | `theme_intraday_capital`、`theme_stocks`、`sector_analysis`、`capital_flow` |
| 开盘前竞价 | `auction_opening_snapshot`、`auction_market_scan`、`auction_theme_strength`；不要把几百个代码塞进 `auction_data` |
| 个股研究 | `stock_search` 解析代码，再用 `stock_research_workflow`，按需补 `financial_summary`、`official_disclosure_evidence` |
| 事件排雷 | `stock_event_calendar`、`unlock_events`、`market_catalyst_calendar`、`macro_calendar` |
| 自选股 | `watchlist_list`、`watchlist_group_list` 只读；`watchlist_add`、`watchlist_remove`、`watchlist_update_stock`、`watchlist_group_create`、`watchlist_group_rename`、`watchlist_group_delete` 会修改用户本人的自选 |

`kline` 一次最多查约 20 只股票，更多时分批。

## 修改自选股前先确认

写入类工具只修改当前用户本人的自选股和分组。只有用户明确要求“加入 / 移除 / 改分组 / 删分组”时才调用；删除分组或移除股票前，先把要改的内容列给用户确认。

## 出错时怎么办

| 返回 | 处理 |
| --- | --- |
| `FREE_TIER_MARKET_OPEN_RESTRICTED` | 免费 Key 在北京时间 09:15–10:30 暂停。不要反复重试，告诉用户 10:30 后再试，或查看 https://stock.quicktiny.cn/membership?tab=apiQuota |
| `DAILY_LIMIT_EXCEEDED` 且 `quotaTier=free` | 今日免费次数用完，告诉用户次日再试或查看同一套餐链接 |
| `RATE_LIMIT_EXCEEDED` | 每分钟次数超限，按 Retry-After 等待后重试；这不代表需要购买套餐 |
| `INVALID_ARGUMENTS` | 按返回的 errors 修正参数后重试一次 |
| `AUCTION_DATA_NOT_READY` | 竞价数据未就绪，按 `retryAfterMs` 稍后重试，不要改查前一交易日来冒充今天 |
| 认证失败 / 401 | 提示用户在连接器设置里检查悟道 API Key |

只有看到上面这些确切错误码时才按对应原因说明；超时或数据缺失要如实说明，继续排查。

## 输出要求

- 写明数据日期，以及哪些结论来自哪个工具。
- 缺失或未就绪的数据单独列出，不要猜。
- 列举股票时用 `[名称(代码)](https://stock.quicktiny.cn/quote/代码)` 的链接格式。
- 不说底层数据供应商或内部字段名，用“站内数据”“实时快讯”这类中性说法。
- 不给买卖建议，不承诺收益。
