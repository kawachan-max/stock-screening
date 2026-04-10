#!/usr/bin/env python3
"""
IR\u4e8c\u6b21\u5be9\u67fb\uff08\u5272\u5b89\u5c0f\u578b\u6210\u9577\u682a\u7528\uff09
\u30ab\u30bf\u30ea\u30b9\u30c8\u691c\u51fa\uff08\u81ea\u793e\u682a\u8cb7\u3044\u30fb\u5897\u914d\u30fb\u4e0a\u65b9\u4fee\u6b63\uff09
\u30ea\u30b9\u30af\u691c\u51fa\uff08\u4e0b\u65b9\u4fee\u6b63\u30fb\u6e1b\u914d\u30fb\u4e0d\u7965\u4e8b\uff09
"""

import argparse
import json
import math
import os
import time
from datetime import datetime
from typing import Any


CACHE_DAYS = 14
SCRIPT_DEADLINE_SEC = 2400


def load_json_file(path: str, default: Any) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json_file(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_results_full(path: str) -> tuple[dict, list[dict]]:
    raw = load_json_file(path, {})
    if not isinstance(raw, dict):
        return {}, []
    stocks = raw.get("stocks", [])
    if not isinstance(stocks, list):
        return raw, []
    return raw, stocks


def _norm_code(code: str) -> str:
    code = str(code).strip()
    if code.endswith(".0"):
        code = code[:-2]
    return code


def _extract_json_object(text: str) -> dict:
    clean = text.replace("```json", "").replace("```", "").strip()
    start = clean.find("{")
    if start < 0:
        raise ValueError("no json object")
    depth = 0
    for i in range(start, len(clean)):
        ch = clean[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(clean[start : i + 1])
    raise ValueError("unbalanced braces")


def _build_ir_prompt(code: str, name: str, current_data: dict) -> str:
    current_score = current_data.get("score", 0)
    net_cash_ratio = current_data.get("net_cash_ratio", 0)
    per = current_data.get("per", 0)
    pbr = current_data.get("pbr", 0)
    roe = current_data.get("roe", 0)
    dividend_yield = current_data.get("dividend_yield", 0)
    tab = current_data.get("tab", "general")

    return f"""
\u4ee5\u4e0b\u306e\u65e5\u672c\u306e\u4e0a\u5834\u4f01\u696d\u306b\u3064\u3044\u3066\u3001\u6700\u65b0\u306eIR\u60c5\u5831\u3092\u691c\u7d22\u3057\u3066\u3001\u682a\u4fa1\u306b\u5f71\u97ff\u3059\u308b\u30ab\u30bf\u30ea\u30b9\u30c8\u3068\u30ea\u30b9\u30af\u3092\u691c\u8a3c\u3057\u3066\u304f\u3060\u3055\u3044\u3002

\u3010\u5bfe\u8c61\u9298\u67c4\u3011
\u9298\u67c4\u30b3\u30fc\u30c9: {code}
\u9298\u67c4\u540d: {name}
\u30b9\u30b3\u30a2: {current_score}\u70b9
\u30cd\u30c3\u30c8\u30ad\u30e3\u30c3\u30b7\u30e5\u6bd4\u7387: {net_cash_ratio}
PER: {per}\u500d / PBR: {pbr}\u500d / ROE: {roe}%
\u914d\u5f53\u5229\u56de\u308a: {dividend_yield}%
\u30bf\u30d6: {tab}

\u3010\u691c\u7d22\u3057\u3066\u78ba\u8a8d\u3059\u308b\u3053\u3068\u3011
1. \u81ea\u793e\u682a\u8cb7\u3044\u306e\u767a\u8868\uff08\u76f4\u8fd1\u534a\u5e74\u4ee5\u5185\uff09
2. \u5897\u914d\u30fb\u914d\u5f53\u5897\u984d\u306e\u767a\u8868
3. \u696d\u7e3e\u4e0a\u65b9\u4fee\u6b63\u306e\u767a\u8868
4. \u682a\u4e3b\u9084\u5143\u5f37\u5316\u30fbPBR\u6539\u5584\u5bfe\u5fdc\u30fb\u4e2d\u8a08\u3067\u306e\u6210\u9577\u6226\u7565
5. \u696d\u7e3e\u4e0b\u65b9\u4fee\u6b63\u306e\u767a\u8868
6. \u6e1b\u914d\u306e\u767a\u8868
7. \u4e0d\u7965\u4e8b\u30fb\u8a34\u8a1f\u30fb\u898f\u5236\u30ea\u30b9\u30af
8. MBO\u30fbTOB\u30fb\u5927\u682a\u4e3b\u5909\u52d5

\u3010\u56de\u7b54\u30d5\u30a9\u30fc\u30de\u30c3\u30c8\u3011
\u4ee5\u4e0b\u306eJSON\u306e\u307f\u3092\u8fd4\u3057\u3066\u304f\u3060\u3055\u3044\u3002\u524d\u5f8c\u306b\u8aac\u660e\u6587\u3084Markdown\u306e\u30d0\u30c3\u30af\u30c6\u30a3\u30af\u306f\u4e0d\u8981\u3067\u3059\u3002

{{
  "review_status": "positive" / "neutral" / "negative" / "critical",
  "catalysts_found": [],
  "risks_found": [],
  "score_adjustment": 0,
  "add_badges": [],
  "ir_comment": "",
  "review_note": "",
  "source_urls": []
}}

\u3010\u5224\u5b9a\u30eb\u30fc\u30eb\u3011

A. \u30ab\u30bf\u30ea\u30b9\u30c8\uff08\u30d7\u30e9\u30b9\u8a55\u4fa1\uff09:
   - \u81ea\u793e\u682a\u8cb7\u3044\u767a\u8868: score_adjustment +3\u301c+5, badge "\u2b06\ufe0f\u81ea\u793e\u682a\u8cb7\u3044" positive
   - \u5897\u914d\u767a\u8868: score_adjustment +2\u301c+4, badge "\u2b06\ufe0f\u5897\u914d\u767a\u8868" positive
   - \u4e0a\u65b9\u4fee\u6b63: score_adjustment +3\u301c+6, badge "\u2b06\ufe0f\u4e0a\u65b9\u4fee\u6b63" positive
   - PBR\u6539\u5584\u5bfe\u5fdc\u30fb\u4e2d\u8a08\u6210\u9577\u6226\u7565: score_adjustment +2\u301c+3, badge "\u2b06\ufe0f\u9084\u5143\u5f37\u5316" positive
   - MBO\u30fbTOB: score_adjustment +5, badge "\u2757MBO/TOB" positive

B. \u30ea\u30b9\u30af\uff08\u30de\u30a4\u30ca\u30b9\u8a55\u4fa1\uff09:
   - \u4e0b\u65b9\u4fee\u6b63: score_adjustment -5\u301c-10, badge "\u26a0\ufe0f\u4e0b\u65b9\u4fee\u6b63" negative
   - \u6e1b\u914d: score_adjustment -8\u301c-15, badge "\u26a0\ufe0f\u6e1b\u914d" negative
   - \u4e0d\u7965\u4e8b: score_adjustment -10\u4ee5\u4e0a, badge "\u26a0\ufe0f\u4e0d\u7965\u4e8b" negative
   - \u9700\u8981\u5931\u901f\u30fb\u4e00\u904e\u6027\u5229\u76ca: score_adjustment -3\u301c-5, badge "\u26a0\ufe0f\u4e00\u904e\u6027" negative
   - \u5e0c\u8584\u5316\u30ea\u30b9\u30af: score_adjustment -5\u301c-8, badge "\u26a0\ufe0f\u5e0c\u8584\u5316" negative

C. \u7279\u306b\u5909\u5316\u306a\u3057:
   - review_status = "neutral", score_adjustment = 0

\u3010\u91cd\u8981\u3011
- \u8907\u6570\u306e\u30ab\u30bf\u30ea\u30b9\u30c8/\u30ea\u30b9\u30af\u304c\u3042\u308b\u5834\u5408\u306f\u5408\u7b97\u3057\u3066\u304f\u3060\u3055\u3044
- source_urls\u306bIR\u30da\u30fc\u30b8URL\u3092\u5165\u308c\u3066\u304f\u3060\u3055\u3044
- review_note\u306f100\u6587\u5b57\u4ee5\u5185
- ir_comment\u306f200\u6587\u5b57\u4ee5\u5185\u3067\u3001\u6700\u65b0IR\u60c5\u5831\u306e\u8981\u7d04
- \u6295\u8cc7\u63a8\u5968\u306b\u306a\u3089\u306a\u3044\u3088\u3046\u306b
"""


def review_stock_ir(code: str, name: str, current_data: dict) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY missing")
    import anthropic
    client = anthropic.Anthropic(api_key=api_key, timeout=120.0)
    prompt = _build_ir_prompt(code, name, current_data)
    tools = [{"name": "web_search", "type": "web_search_20250305", "max_uses": 5}]
    messages: list = [{"role": "user", "content": prompt}]
    full_text_parts: list[str] = []
    for _ in range(16):
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            tools=tools,
            messages=messages,
        )
        for block in msg.content:
            if block.type == "text":
                full_text_parts.append(block.text)
        if msg.stop_reason == "end_turn":
            break
        messages.append({"role": "assistant", "content": msg.content})
        tool_results = []
        for block in msg.content:
            if block.type == "tool_use":
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": (
                            '{"status":"completed",'
                            '"note":"web_search handled by Anthropic"}'
                        ),
                    }
                )
        if not tool_results:
            break
        messages.append({"role": "user", "content": tool_results})
    full_text = "\n".join(full_text_parts)
    return _extract_json_object(full_text)


def _default_error_review(err_snip: str) -> dict:
    return {
        "review_status": "neutral",
        "catalysts_found": [],
        "risks_found": [],
        "score_adjustment": 0,
        "add_badges": [],
        "ir_comment": "",
        "review_note": "IR\u5be9\u67fb\u30a8\u30e9\u30fc: " + err_snip[:50],
        "source_urls": [],
    }


def apply_ir_review(stocks: list[dict], reviews: dict) -> list[dict]:
    """
    IR\u5be9\u67fb\u7d50\u679c\u3092 stocks \u306b\u9069\u7528\u3002
    """
    if not isinstance(reviews, dict):
        return stocks
    for stock in stocks:
        code = _norm_code(str(stock.get("code", "")))
        if not code or code not in reviews:
            continue
        review = reviews[code]
        if not isinstance(review, dict):
            continue
        reviewed_at = review.get("reviewed_at", "")
        if reviewed_at:
            try:
                review_date = datetime.strptime(str(reviewed_at)[:10], "%Y-%m-%d")
                if (datetime.now() - review_date).days > CACHE_DAYS:
                    continue
            except ValueError:
                pass
        adj = int(review.get("score_adjustment", 0) or 0)
        if adj != 0:
            bl = stock.get("score_before_ir")
            if bl is None:
                baseline = int(stock.get("score", 0) or 0)
            else:
                baseline = int(bl)
            stock["score_before_ir"] = baseline
            stock["score"] = max(0, baseline + adj)

        add_badges = review.get("add_badges", [])
        if isinstance(add_badges, list) and add_badges:
            existing = stock.get("badges") or []
            if not isinstance(existing, list):
                existing = []
            stock["badges"] = existing + [b for b in add_badges if isinstance(b, dict)]

        ir_comment = review.get("ir_comment", "")
        if isinstance(ir_comment, str) and ir_comment.strip():
            existing_comment = stock.get("ai_comment", "") or ""
            stock["ai_comment"] = existing_comment.rstrip() + "\n\n\u3010IR\u5be9\u67fb\u3011" + ir_comment.strip()

        stock["ir_review_status"] = review.get("review_status", "neutral")
        stock["ir_review_note"] = review.get("review_note", "")
        stock["ir_reviewed_at"] = review.get("reviewed_at", "")

    stocks.sort(key=lambda x: int(x.get("score", 0) or 0), reverse=True)
    return stocks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="IR\u4e8c\u6b21\u5be9\u67fb\uff08\u5272\u5b89\u6210\u9577\u682a\u7528\uff09"
    )
    parser.add_argument(
        "--results-dir",
        default=".",
        help="\u7d50\u679cJSON\u306e\u30c7\u30a3\u30ec\u30af\u30c8\u30ea",
    )
    parser.add_argument(
        "--refresh-ir",
        action="store_true",
        help="\u30ad\u30e3\u30c3\u30b7\u30e5\u7121\u8996\u3057\u5168\u4ef6\u518d\u5be9\u67fb",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="\u7d50\u679cJSON\u306b\u306f\u66f8\u304d\u8fbc\u307e\u306a\u3044",
    )
    parser.add_argument("--test", nargs="*", default=None)
    args = parser.parse_args()

    deadline = time.monotonic() + SCRIPT_DEADLINE_SEC

    base_dir = os.path.abspath(args.results_dir)
    general_path = os.path.join(base_dir, "screening_result.json")
    finance_path = os.path.join(base_dir, "screening_result_finance.json")
    cache_path = os.path.join(base_dir, "ir_review_growth_cache.json")

    env_general, general_stocks = load_results_full(general_path)
    env_finance, finance_stocks = load_results_full(finance_path)

    all_stocks: list[dict] = []
    for s in general_stocks:
        s["_source"] = "general"
        all_stocks.append(s)
    for s in finance_stocks:
        s["_source"] = "finance"
        all_stocks.append(s)

    if not all_stocks:
        print("\u7d50\u679c\u304c\u7a7a\u307e\u305f\u306f\u8aad\u307f\u8fbc\u3081\u307e\u305b\u3093")
        raise SystemExit(1)

    if args.test is not None and len(args.test) > 0:
        test_set = {_norm_code(c) for c in args.test}
        targets = [
            s for s in all_stocks if _norm_code(str(s.get("code", ""))) in test_set
        ]
    else:
        # general: 45\u70b9\u4ee5\u4e0a, finance: 50\u70b9\u4ee5\u4e0a, \u5408\u7b97\u30b9\u30b3\u30a2\u9806\u4e0a\u4f4d30\u4ef6
        candidates = []
        for s in all_stocks:
            score = int(s.get("score", 0) or 0)
            source = s.get("_source", "general")
            if source == "finance" and score >= 50:
                candidates.append(s)
            elif source == "general" and score >= 45:
                candidates.append(s)
        candidates.sort(key=lambda x: int(x.get("score", 0) or 0), reverse=True)
        targets = candidates[:30]

    print("\u5be9\u67fb\u5bfe\u8c61: " + str(len(targets)) + "\u9298\u67c4")

    cache = load_json_file(cache_path, {})
    if not isinstance(cache, dict):
        cache = {}

    today = datetime.now().strftime("%Y-%m-%d")
    reviewed = 0
    skipped = 0

    for stock in targets:
        if time.monotonic() > deadline:
            print("\u30bf\u30a4\u30e0\u30a2\u30a6\u30c8\u3001\u6b8b\u308a\u306f\u6b21\u56de\u3002")
            break

        code = _norm_code(str(stock.get("code", "")))
        name = stock.get("name_jp", "") or stock.get("name", "")

        if not args.refresh_ir and code in cache:
            cached = cache[code]
            cached_date = str(cached.get("reviewed_at", ""))[:10]
            try:
                if (datetime.now() - datetime.strptime(cached_date, "%Y-%m-%d")).days <= CACHE_DAYS:
                    skipped += 1
                    continue
            except ValueError:
                pass

        print(f"  [{code}] {name} ... ", end="", flush=True)
        try:
            result = review_stock_ir(code, name, stock)
            result["reviewed_at"] = today
            cache[code] = result
            adj = result.get("score_adjustment", 0)
            status = result.get("review_status", "neutral")
            print(f"{status} (adj={adj})")
            reviewed += 1
        except Exception as e:
            err = str(e)[:80]
            print(f"ERROR: {err}")
            cache[code] = _default_error_review(err)
            cache[code]["reviewed_at"] = today
            reviewed += 1

        time.sleep(2)

    print(f"\u5be9\u67fb\u5b8c\u4e86: {reviewed}\u4ef6\u5be9\u67fb, {skipped}\u4ef6\u30b9\u30ad\u30c3\u30d7")

    save_json_file(cache_path, cache)
    print("\u30ad\u30e3\u30c3\u30b7\u30e5\u4fdd\u5b58: " + cache_path)

    if args.dry_run:
        print("--dry-run: \u7d50\u679cJSON\u306b\u306f\u66f8\u304d\u8fbc\u307f\u307e\u305b\u3093")
        return

    # general\u306b\u9069\u7528
    if general_stocks:
        general_stocks = apply_ir_review(general_stocks, cache)
        env_general["stocks"] = general_stocks
        save_json_file(general_path, env_general)
        print("\u66f8\u304d\u8fbc\u307f: " + general_path)

    # finance\u306b\u9069\u7528
    if finance_stocks:
        finance_stocks = apply_ir_review(finance_stocks, cache)
        env_finance["stocks"] = finance_stocks
        save_json_file(finance_path, env_finance)
        print("\u66f8\u304d\u8fbc\u307f: " + finance_path)


if __name__ == "__main__":
    main()
