"""Small reproducible sample, not a latency or availability benchmark.

Python 3.11+. Wudao uses only the standard library; AkShare is optional.
Credentials are read from WUDAO_API_KEY, never written to the result.
"""

import argparse
import datetime as dt
import importlib.metadata
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

ENDPOINT = "https://stock.quicktiny.cn/api/mcp"
FIELDS = ("open", "high", "low", "close")


def date_text(value):
    text = str(value)
    return dt.datetime.strptime(text, "%Y%m%d").date().isoformat() if len(text) == 8 else dt.date.fromisoformat(text).isoformat()


def validate(rows, expected_dates):
    dates = [row.get("date") for row in rows]
    issues = []
    if dates != expected_dates:
        issues.append("date_set_or_order_mismatch")
    if len(dates) != len(set(dates)):
        issues.append("duplicate_date")
    for row in rows:
        values = [row.get(field) for field in FIELDS]
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0 for v in values):
            issues.append("invalid_price")
            continue
        if not row["low"] <= min(row["open"], row["close"]) <= max(row["open"], row["close"]) <= row["high"]:
            issues.append("ohlc_order_invalid")
    return sorted(set(issues))


class MCP:
    def __init__(self, token):
        self.headers = {"Authorization": token if token.startswith("Bearer ") else "Bearer " + token,
                        "Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        self.next_id = 0

    def request(self, method, params=None, notification=False):
        message = {"jsonrpc": "2.0", "method": method}
        if not notification:
            self.next_id += 1
            message["id"] = self.next_id
        if params is not None:
            message["params"] = params
        request = urllib.request.Request(ENDPOINT, data=json.dumps(message).encode(), headers=self.headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.headers.get("Mcp-Session-Id"):
                self.headers["Mcp-Session-Id"] = response.headers["Mcp-Session-Id"]
            payload = response.read().decode()
            if notification:
                return None
            if "text/event-stream" in response.headers.get("Content-Type", ""):
                candidates = []
                for event in payload.replace("\r\n", "\n").split("\n\n"):
                    data = "\n".join(line[5:].lstrip() for line in event.splitlines() if line.startswith("data:"))
                    if data:
                        candidates.append(json.loads(data))
                result = next(item for item in candidates if item.get("id") == message["id"])
            else:
                result = json.loads(payload)
        if "error" in result:
            raise ValueError("JSON_RPC_ERROR")
        return result["result"]


def wudao(codes, dates):
    token = os.environ.get("WUDAO_API_KEY")
    if not token:
        return {"status": "not_tested", "reason": "WUDAO_API_KEY_not_set"}
    client = MCP(token)
    initialization = client.request("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                                   "clientInfo": {"name": "public-source-check", "version": "1.0"}})
    client.headers["MCP-Protocol-Version"] = initialization["protocolVersion"]
    client.request("notifications/initialized", notification=True)
    tools = client.request("tools/list")["tools"]
    if not any(tool["name"] == "kline" and tool.get("annotations", {}).get("readOnlyHint") for tool in tools):
        raise ValueError("read_only_kline_unavailable")
    arguments = {"codes": codes, "endDate": dates[-1], "days": len(dates), "maxRows": len(dates), "adjust": "none"}
    result = client.request("tools/call", {"name": "kline", "arguments": arguments})
    structured = result.get("structuredContent", {})
    if result.get("isError") or structured.get("success") is not True:
        return {"status": "failed", "reason": "tool_error", "request": arguments}
    data = structured["data"]
    items = []
    for item in data.get("items", []):
        rows = [{"date": date_text(row["date"]), **{key: row.get(key) for key in FIELDS}} for row in item.get("rows", [])]
        issues = validate(rows, dates)
        if item.get("adjust") != "none":
            issues.append("adjust_mismatch")
        if any(item.get(key) for key in ("qualityWarnings", "partialErrors")):
            issues.append("provider_quality_warning")
        items.append({"code": item.get("stock", {}).get("code"), "rows": rows, "issues": issues})
    codes_match = len(items) == len(codes) and sorted(item["code"] for item in items if item["code"]) == sorted(codes)
    top_warning = any(structured.get(key) or data.get(key) for key in ("qualityWarnings", "partialErrors"))
    return {"status": "passed" if codes_match and not top_warning and all(not item["issues"] for item in items) else "check_failed",
            "request": arguments, "codesMatch": codes_match, "providerWarning": top_warning, "items": items}


def akshare_worker(code, dates):
    import akshare as ak
    frame = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=dates[0].replace("-", ""),
                             end_date=dates[-1].replace("-", ""), adjust="", timeout=20)
    mapping = {"open": "开盘", "high": "最高", "low": "最低", "close": "收盘"}
    rows = [{"date": date_text(str(row["日期"])), **{key: float(row[label]) for key, label in mapping.items()}}
            for _, row in frame.iterrows()]
    return {"code": code, "rows": rows, "issues": validate(rows, dates)}


def akshare(codes, dates):
    try:
        version = importlib.metadata.version("akshare")
    except importlib.metadata.PackageNotFoundError:
        return {"status": "not_tested", "reason": "akshare_not_installed"}
    items = []
    # Isolate each request so a third-party client's own retry cannot hang the run.
    for code in codes:
        try:
            child = subprocess.run([sys.executable, __file__, "--worker", code, "--dates", ",".join(dates)],
                                   capture_output=True, text=True, timeout=45)
            item = json.loads(child.stdout) if child.returncode == 0 else {"code": code, "rows": [], "issues": ["worker_error"]}
        except subprocess.TimeoutExpired:
            item = {"code": code, "rows": [], "issues": ["request_timeout"]}
        except (ValueError, OSError):
            item = {"code": code, "rows": [], "issues": ["worker_output_error"]}
        items.append(item)
    return {"status": "passed" if all(not item["issues"] for item in items) else "check_failed",
            "version": version, "entry": "stock_zh_a_hist", "adjust": "", "items": items}


def compare(left, right):
    if left.get("status") != "passed" or right.get("status") != "passed":
        return {"status": "not_comparable", "reason": "both_providers_must_pass_first"}
    index = {(item["code"], row["date"]): row for item in right["items"] for row in item["rows"]}
    differences = []
    checked = 0
    for item in left["items"]:
        for row in item["rows"]:
            peer = index.get((item["code"], row["date"]))
            if peer is None:
                return {"status": "not_comparable", "reason": "date_or_symbol_set_differs"}
            for field in FIELDS:
                checked += 1
                if abs(row[field] - peer[field]) > 0.010001:
                    differences.append({"code": item["code"], "date": row["date"], "field": field,
                                        "wudao": row[field], "akshare": peer[field]})
    return {"status": "matched" if not differences else "differences_found", "fieldsChecked": checked,
            "absoluteTolerance": 0.01, "differences": differences}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dates", required=True, help="Explicit comma-separated trading dates, ascending; verify the calendar yourself")
    parser.add_argument("--codes", default="600519,000001,300750")
    parser.add_argument("--output", default="source-check.json")
    parser.add_argument("--network", choices=("environment", "direct"), default="environment")
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.network == "direct":
        for key in list(os.environ):
            if key.lower() in ("http_proxy", "https_proxy", "all_proxy", "no_proxy"):
                del os.environ[key]
        # macOS can supply system proxies even when proxy environment variables are absent.
        os.environ["NO_PROXY"] = "*"
    dates = [date_text(value) for value in args.dates.split(",")]
    if dates != sorted(set(dates)) or not 1 <= len(dates) <= 150:
        parser.error("dates must be unique, ascending, and contain 1 to 150 entries")
    if args.worker:
        try:
            result = akshare_worker(args.worker, dates)
        except Exception as error:
            result = {"code": args.worker, "rows": [], "issues": [type(error).__name__]}
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return
    codes = args.codes.split(",")
    if len(set(codes)) != len(codes) or not 1 <= len(codes) <= 20 or not all(len(c) == 6 and c.isascii() and c.isdigit() for c in codes):
        parser.error("use 1 to 20 unique six-digit stock codes")
    output = {"testedAt": dt.datetime.now(dt.timezone.utc).isoformat(), "method": "one sequential run, no retries added by harness",
              "network": args.network,
              "task": {"codes": codes, "dates": dates, "adjust": "unadjusted", "fields": list(FIELDS)},
              "limits": ["Provider-maintained sample, not independent evaluation", "No latency ranking or SLA conclusion",
                         "OHLC agreement is not independent proof of accuracy", "No turnover, volume, or corporate-action comparison"],
              "providers": {}}
    for name, run in (("wudao", wudao), ("akshare", akshare)):
        try:
            output["providers"][name] = run(codes, dates)
        except Exception as error:
            output["providers"][name] = {"status": "failed", "reason": type(error).__name__}
    output["comparison"] = compare(output["providers"]["wudao"], output["providers"]["akshare"])
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output, "providers": {name: value["status"] for name, value in output["providers"].items()},
                      "comparison": output["comparison"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
