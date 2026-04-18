#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
\u5272\u5b89\u6210\u9577\u682a LINE\u901a\u77e5\uff08broadcast\uff09
\u901a\u5e38\u9298\u67c4: NC\u6bd4\u7387\u306e\u524d\u56de\u6bd4\u4e0a\u6607\u3067\u901a\u77e5
\u91d1\u878d\u30fb\u4e0d\u52d5\u7523: PBR\u306e\u524d\u56de\u6bd4\u4e0b\u843d\u3067\u901a\u77e5
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Any, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

# --- \u95be\u5024 ---
SCORE_MIN_GENERAL = 55
SCORE_MIN_FINANCE = 60

# \u901a\u5e38\u9298\u67c4: NC\u6bd4\u7387\u4e0a\u6607\u5e45
NC_NORMAL = 0.2
NC_BIG = 0.5
NC_BARGAIN = 1.0

# \u91d1\u878d\u30fb\u4e0d\u52d5\u7523: PBR\u4e0b\u843d\u5e45\uff08\u7d76\u5bfe\u5024\uff09
PBR_NORMAL = 0.1
PBR_BIG = 0.2
PBR_BARGAIN = 0.3

SCORE_DROP_THRESHOLD_G = 50
SCORE_DROP_THRESHOLD_F = 55
SCORE_DROP_MIN = 5

LINE_BROADCAST_URL = "https://api.line.me/v2/bot/message/broadcast"
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"

APP_URL = "https://stock-screening-nine.vercel.app"

MSG_BARGAIN_NC = (
    "\U0001F514\U0001F514\U0001F514 \u30d0\u30fc\u30b2\u30f3\u30c1\u30e3\u30f3\u30b9\uff01"
    "{count}\u4ef6\u306e\u5272\u5b89\u682a\u306eNC\u6bd4\u7387\u304c\u5927\u5e45\u4e0a\u6607\uff01\n\n"
    "{details}\n\n"
    "\u30e9\u30f3\u30ad\u30f3\u30b0\u3092\u78ba\u8a8d\u3059\u308b \u2192\n" + APP_URL
)
MSG_BIG_NC = (
    "\U0001F514\U0001F514 {count}\u4ef6\u306e\u5272\u5b89\u682a\u306eNC\u6bd4\u7387\u304c\u4e0a\u6607\u4e2d\uff01\n\n"
    "{details}\n\n"
    "\u30e9\u30f3\u30ad\u30f3\u30b0\u3092\u78ba\u8a8d\u3059\u308b \u2192\n" + APP_URL
)
MSG_NORMAL_NC = (
    "\U0001F514 {count}\u4ef6\u306e\u5272\u5b89\u682a\u306eNC\u6bd4\u7387\u304c\u4e0a\u6607\u3057\u3066\u3044\u307e\u3059\u3002\n\n"
    "{details}\n\n"
    "\u30e9\u30f3\u30ad\u30f3\u30b0\u3092\u78ba\u8a8d\u3059\u308b \u2192\n" + APP_URL
)
MSG_BARGAIN_PBR = (
    "\U0001F514\U0001F514\U0001F514 \u30d0\u30fc\u30b2\u30f3\u30c1\u30e3\u30f3\u30b9\uff01"
    "{count}\u4ef6\u306e\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u682a\u306ePBR\u304c\u5927\u5e45\u4e0b\u843d\uff01\n\n"
    "{details}\n\n"
    "\u30e9\u30f3\u30ad\u30f3\u30b0\u3092\u78ba\u8a8d\u3059\u308b \u2192\n" + APP_URL
)
MSG_BIG_PBR = (
    "\U0001F514\U0001F514 {count}\u4ef6\u306e\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u682a\u306ePBR\u304c\u4e0b\u843d\u4e2d\uff01\n\n"
    "{details}\n\n"
    "\u30e9\u30f3\u30ad\u30f3\u30b0\u3092\u78ba\u8a8d\u3059\u308b \u2192\n" + APP_URL
)
MSG_NORMAL_PBR = (
    "\U0001F514 {count}\u4ef6\u306e\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u682a\u306ePBR\u304c\u4e0b\u843d\u3057\u3066\u3044\u307e\u3059\u3002\n\n"
    "{details}\n\n"
    "\u30e9\u30f3\u30ad\u30f3\u30b0\u3092\u78ba\u8a8d\u3059\u308b \u2192\n" + APP_URL
)


def load_json_file(path: str, default: Any) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json_file(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_stocks(path: str) -> list[dict]:
    raw = load_json_file(path, {})
    if isinstance(raw, dict):
        return raw.get("stocks", [])
    return []


def _norm_code(code: str) -> str:
    code = str(code).strip()
    if code.endswith(".0"):
        code = code[:-2]
    return code[:4]


def _safe_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(val) if val is not None else default
    except (TypeError, ValueError):
        return default


def _build_lines(items: list[dict], key: str) -> str:
    lines = []
    for item in items:
        val = item.get("val", 0)
        prev_val = item.get("prev_val", 0)
        diff = item.get("diff", 0)
        if key == "nc":
            lines.append(
                f'{item["code"]} {item["name"]}  NC {prev_val:.2f} \u2192 {val:.2f} (+{diff:.2f})'
            )
        else:
            lines.append(
                f'{item["code"]} {item["name"]}  PBR {prev_val:.2f} \u2192 {val:.2f} ({diff:.2f})'
            )
    return "\n".join(lines)


def send_line_broadcast(text: str, token: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    body = {"messages": [{"type": "text", "text": text}]}
    try:
        resp = requests.post(LINE_BROADCAST_URL, headers=headers, json=body, timeout=30)
        print(f"LINE broadcast: {resp.status_code}")
    except Exception as e:
        print(f"LINE broadcast error: {e}", file=sys.stderr)


def send_line_group_push(text: str, token: str, group_id: str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    body = {
        "to": group_id,
        "messages": [{"type": "text", "text": text}],
    }
    try:
        resp = requests.post(LINE_PUSH_URL, headers=headers, json=body, timeout=30)
        print(f"LINE group push: {resp.status_code}")
    except Exception as e:
        print(f"LINE group push error: {e}", file=sys.stderr)


def _send_notification(msg: str, token: str, group_id: str, dry_run: bool) -> None:
    print(msg)
    if not dry_run:
        send_line_broadcast(msg, token)
        if group_id:
            send_line_group_push(msg, token, group_id)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="\u5272\u5b89\u6210\u9577\u682a LINE\u901a\u77e5"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--results-dir", default=".", help="\u7d50\u679cJSON\u306e\u30c7\u30a3\u30ec\u30af\u30c8\u30ea")
    args = parser.parse_args()

    base_dir = os.path.abspath(args.results_dir)
    general_path = os.path.join(base_dir, "screening_result.json")
    finance_path = os.path.join(base_dir, "screening_result_finance.json")
    prev_general_path = os.path.join(base_dir, "screening_result_prev.json")
    prev_finance_path = os.path.join(base_dir, "screening_result_finance_prev.json")

    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN_GROWTH", "").strip()
    group_id = os.environ.get("LINE_GROUP_ID_GROWTH", "").strip()
    if not args.dry_run and not token:
        print("LINE_CHANNEL_ACCESS_TOKEN_GROWTH missing", file=sys.stderr)
        sys.exit(1)

    # --- \u73fe\u5728\u306e\u30c7\u30fc\u30bf\u8aad\u307f\u8fbc\u307f ---
    general_stocks = load_stocks(general_path)
    finance_stocks = load_stocks(finance_path)

    # --- \u524d\u56de\u306e\u30c7\u30fc\u30bf\u8aad\u307f\u8fbc\u307f ---
    prev_general = load_stocks(prev_general_path)
    prev_finance = load_stocks(prev_finance_path)

    # --- \u524d\u56de\u30c7\u30fc\u30bf\u3092code\u3067\u7d22\u5f15 ---
    prev_g_map: dict[str, dict] = {}
    for s in prev_general:
        c = _norm_code(str(s.get("code", "")))
        if c:
            prev_g_map[c] = s

    prev_f_map: dict[str, dict] = {}
    for s in prev_finance:
        c = _norm_code(str(s.get("code", "")))
        if c:
            prev_f_map[c] = s

    # === \u901a\u5e38\u9298\u67c4: NC\u6bd4\u7387\u306e\u524d\u56de\u6bd4\u4e0a\u6607 ===
    nc_bargain: list[dict] = []
    nc_big: list[dict] = []
    nc_normal: list[dict] = []

    for s in general_stocks:
        score = _safe_float(s.get("score"))
        if score < SCORE_MIN_GENERAL:
            continue
        code = _norm_code(str(s.get("code", "")))
        if not code:
            continue
        nc_now = _safe_float(s.get("net_cash_ratio"))
        if nc_now <= 0:
            continue
        prev = prev_g_map.get(code)
        if prev is None:
            continue
        nc_prev = _safe_float(prev.get("net_cash_ratio"))
        if nc_prev <= 0:
            continue
        diff = nc_now - nc_prev
        if diff < NC_NORMAL:
            continue
        item = {
            "code": code,
            "name": s.get("name_jp", "") or s.get("name", ""),
            "val": nc_now,
            "prev_val": nc_prev,
            "diff": diff,
        }
        if diff >= NC_BARGAIN:
            nc_bargain.append(item)
        elif diff >= NC_BIG:
            nc_big.append(item)
        else:
            nc_normal.append(item)

    # === \u91d1\u878d\u30fb\u4e0d\u52d5\u7523: PBR\u306e\u524d\u56de\u6bd4\u4e0b\u843d ===
    pbr_bargain: list[dict] = []
    pbr_big: list[dict] = []
    pbr_normal: list[dict] = []

    for s in finance_stocks:
        score = _safe_float(s.get("score"))
        if score < SCORE_MIN_FINANCE:
            continue
        code = _norm_code(str(s.get("code", "")))
        if not code:
            continue
        pbr_now = _safe_float(s.get("pbr"))
        if pbr_now <= 0:
            continue
        prev = prev_f_map.get(code)
        if prev is None:
            continue
        pbr_prev = _safe_float(prev.get("pbr"))
        if pbr_prev <= 0:
            continue
        diff = pbr_now - pbr_prev
        if diff >= 0:
            continue
        abs_diff = abs(diff)
        if abs_diff < PBR_NORMAL:
            continue
        item = {
            "code": code,
            "name": s.get("name_jp", "") or s.get("name", ""),
            "val": pbr_now,
            "prev_val": pbr_prev,
            "diff": diff,
        }
        if abs_diff >= PBR_BARGAIN:
            pbr_bargain.append(item)
        elif abs_diff >= PBR_BIG:
            pbr_big.append(item)
        else:
            pbr_normal.append(item)

    # === \u901a\u77e5\u9001\u4fe1 ===
    if nc_bargain:
        msg = MSG_BARGAIN_NC.format(count=len(nc_bargain), details=_build_lines(nc_bargain, "nc"))
        _send_notification(msg, token, group_id, args.dry_run)
    if nc_big:
        msg = MSG_BIG_NC.format(count=len(nc_big), details=_build_lines(nc_big, "nc"))
        _send_notification(msg, token, group_id, args.dry_run)
    if nc_normal:
        msg = MSG_NORMAL_NC.format(count=len(nc_normal), details=_build_lines(nc_normal, "nc"))
        _send_notification(msg, token, group_id, args.dry_run)

    if pbr_bargain:
        msg = MSG_BARGAIN_PBR.format(count=len(pbr_bargain), details=_build_lines(pbr_bargain, "pbr"))
        _send_notification(msg, token, group_id, args.dry_run)
    if pbr_big:
        msg = MSG_BIG_PBR.format(count=len(pbr_big), details=_build_lines(pbr_big, "pbr"))
        _send_notification(msg, token, group_id, args.dry_run)
    if pbr_normal:
        msg = MSG_NORMAL_PBR.format(count=len(pbr_normal), details=_build_lines(pbr_normal, "pbr"))
        _send_notification(msg, token, group_id, args.dry_run)

    # === \u30b9\u30b3\u30a2\u4f4e\u4e0b\u30a2\u30e9\u30fc\u30c8 ===
    drop_items: list[dict] = []

    for s in general_stocks:
        code = _norm_code(str(s.get("code", "")))
        if not code:
            continue
        cur = _safe_float(s.get("score"))
        prev = prev_g_map.get(code)
        if prev is None:
            continue
        prev_score = _safe_float(prev.get("score"))
        if prev_score >= SCORE_MIN_GENERAL and cur <= SCORE_DROP_THRESHOLD_G and (prev_score - cur) >= SCORE_DROP_MIN:
            drop_items.append({"code": code, "name": s.get("name_jp", ""), "prev": int(prev_score), "cur": int(cur)})

    for s in finance_stocks:
        code = _norm_code(str(s.get("code", "")))
        if not code:
            continue
        cur = _safe_float(s.get("score"))
        prev = prev_f_map.get(code)
        if prev is None:
            continue
        prev_score = _safe_float(prev.get("score"))
        if prev_score >= SCORE_MIN_FINANCE and cur <= SCORE_DROP_THRESHOLD_F and (prev_score - cur) >= SCORE_DROP_MIN:
            drop_items.append({"code": code, "name": s.get("name_jp", ""), "prev": int(prev_score), "cur": int(cur)})

    if drop_items:
        lines = []
        for item in drop_items:
            lines.append(f'{item["code"]} {item["name"]}  {item["prev"]}\u70b9 \u2192 {item["cur"]}\u70b9')
        msg = (
            "\u26a0\ufe0f \u30b9\u30b3\u30a2\u4f4e\u4e0b\u9298\u67c4\u304c\u3042\u308a\u307e\u3059\u3002\n\n"
            + "\n".join(lines)
            + "\n\n\u8a73\u7d30\u306f\u3053\u3061\u3089 \u2192\n" + APP_URL
        )
        _send_notification(msg, token, group_id, args.dry_run)

    # === prev\u30d5\u30a1\u30a4\u30eb\u3092\u66f4\u65b0 ===
    if os.path.exists(general_path):
        save_json_file(prev_general_path, load_json_file(general_path, {}))
        print(f"prev\u4fdd\u5b58: {prev_general_path}")
    if os.path.exists(finance_path):
        save_json_file(prev_finance_path, load_json_file(finance_path, {}))
        print(f"prev\u4fdd\u5b58: {prev_finance_path}")

    total = len(nc_bargain) + len(nc_big) + len(nc_normal) + len(pbr_bargain) + len(pbr_big) + len(pbr_normal)
    print(f"\u901a\u77e5\u5b8c\u4e86: NC\u901a\u77e5{len(nc_bargain)+len(nc_big)+len(nc_normal)}\u4ef6, PBR\u901a\u77e5{len(pbr_bargain)+len(pbr_big)+len(pbr_normal)}\u4ef6, \u30b9\u30b3\u30a2\u4f4e\u4e0b{len(drop_items)}\u4ef6")


if __name__ == "__main__":
    main()
