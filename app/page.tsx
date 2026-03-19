"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";

type TooltipContent = { title: string; desc: string; formula: string; intent: string };

const TOOLTIP_PER: TooltipContent = {
  title: "\u682A\u4FA1\u6536\u76CA\u7387",
  desc: "\u4ECA\u306E\u682A\u4FA1\u304C1\u5E74\u5206\u306E\u5229\u76CA\u306E\u4F55\u500D\u304B\u3092\u793A\u3057\u307E\u3059",
  formula: "\u682A\u4FA1 \u00F7 EPS\uff081\u682A\u3042\u305F\u308A\u5229\u76CA\uff09",
  intent: "10\u500D\u4EE5\u4E0B \uFF1D \u5E02\u5834\u306B\u307E\u3060\u671F\u5F85\u3055\u308C\u3066\u3044\u306A\u3044\u5272\u5B89\u306E\u8A3C\u62E0",
};

const TOOLTIP_NC: TooltipContent = {
  title: "\u30CD\u30C3\u30C8\u30AD\u30E3\u30C3\u30B7\u30E5\u6BD4\u7387\uff08\u6E05\u539F\u9054\u90C3\u5F0F\uff09",
  desc: "\u4F1A\u793E\u304C\u4ECA\u3059\u3050\u73FE\u91D1\u5316\u3067\u304D\u308B\u8CC7\u7523\u304C\u6642\u4FA1\u7D4C\u984D\u3092\u4E0A\u56DE\u3063\u3066\u3044\u308B\u304B\u3069\u3046\u304B",
  formula: "\uff08\u6D41\u52D5\u8CC7\u7523 \uFF0B \u6295\u8CC7\u6709\u50F1\u8A3C\u5238\u00D770% \u2014 \u8CA0\u50B5\u5408\u8A08\uff09\u00F7 \u6642\u4FA1\u7D4C\u984D",
  intent: "1.0\u4EE5\u4E0A \uFF1D \u5272\u5B89\u3002\u6E05\u539F\u9054\u90C3\u5F0F\u304C\u5B9A\u7FA9\u3057\u305F\u72EC\u81EA\u306E\u5272\u5B89\u6307\u6807",
};

const TOOLTIP_MARKETCAP: TooltipContent = {
  title: "\u6642\u4FA1\u7D4C\u984D",
  desc: "\u4F1A\u793E\u5168\u4F53\u306E\u5024\u6B67\u3002\u682A\u4FA1\u00D7\u767A\u884C\u6E08\u682A\u4F01\u696D\u6570",
  formula: "\u682A\u4FA1 \u00D7 \u767A\u884C\u6E08\u682A\u4F01\u696D\u6570",
  intent: "30\u301C500\u5104\u5186 \uFF1D \u6A5F\u95A2\u6295\u8CC7\u5BB6\u304C\u624B\u3092\u51FA\u3057\u306B\u304F\u3044\u5E02\u5834\u672A\u767B\u898B\u30BE\u30FC\u30F3",
};

const TOOLTIP_DIVIDEND: TooltipContent = {
  title: "\u914D\u5F53\u5229\u56DE\u308A",
  desc: "\u682A\u4FA1\u306B\u5BFE\u3057\u3066\u5E74\u9593\u3069\u308C\u3060\u3051\u914D\u5F53\u3092\u3082\u3089\u3048\u308B\u304B\u306E\u5272\u5408",
  formula: "\u5E74\u9593\u914D\u5F53\u91D1 \u00F7 \u682A\u4FA1 \u00D7 100",
  intent: "\u5272\u5B89\u4E14\u3064\u914D\u5F53\u5229\u56DE\u308A\u304C\u9AD8\u3044\u9298\u67C4\u306F\u682A\u4E3B\u9084\u5143\u4F59\u5730\u306E\u89B3\u70B9\u3067\u3082\u9B45\u529B\u7684",
};

const TOOLTIP_CHEAP_SCORE: TooltipContent = {
  title: "\u5272\u5B89\u5EA6\u30B9\u30B3\u30A2\uff08\u6700\u592727\u70B9\uff09",
  desc: "\u30CD\u30C3\u30C8\u30AD\u30E3\u30C3\u30B7\u30E5\u6BD4\u7387\u3068PER\u306E2\u8EF8\u3067\u5272\u5B89\u3055\u3092\u6570\u5024\u5316",
  formula: "NC\u6BD4\u7387\u30B9\u30B3\u30A2\uff08\u6700\u592718\u70B9\uff09\uFF0B PER\u30B9\u30B3\u30A2\uff08\u6700\u59279\u70B9\uff09",
  intent: "\u6E05\u539F\u9054\u90C3\u5F0F\u306E\u6838\u5FC3\u3002\u3053\u306E\u6570\u5024\u304C\u9AD8\u3044\u307B\u3069\u5E02\u5834\u306B\u6C17\u3065\u304B\u308C\u3066\u3044\u306A\u3044\u5272\u5B89\u9298\u67C4",
};

const TOOLTIP_GROWTH_SCORE: TooltipContent = {
  title: "\u6210\u9577\u6027\u30FB\u4E8B\u696D\u306E\u8CEA\u30B9\u30B3\u30A2\uff08\u6700\u592746\u70B9\uff09",
  desc: "\u58F2\u4E0A\u30FB\u5229\u76CA\u306E\u6210\u9577\u30C8\u30EC\u30F3\u30C9\u3068ROE\u30FBROIC\u3092\u8A55\u4FA1\u3002AI\u6C7A\u7B97\u5206\u6790\u3082\u52A0\u5473",
  formula: "3\u671F\u9023\u7D9A\u5897\u53CE(9)\uFF0B\u58F2\u4E0A\u6210\u9577\u7387(9)\uFF0B3\u671F\u9023\u7D9A\u5897\u76CA(9)\uFF0BROE(5)\uFF0BROIC(5)\uFF0BAI\u5B9A\u6027(4)\uFF0B\u305D\u306E\u4ED6",
  intent: "\u30D0\u30D5\u30A7\u30C3\u30C8\u6D41\u306E\u6210\u9577\u6027\u8A55\u4FA1\u3002\u3053\u306E\u6570\u5024\u304C\u9AD8\u3044\u307B\u3069\u4E2D\u9577\u671F\u3067\u4F38\u3073\u308B\u53EF\u80FD\u6027\u304C\u9AD8\u3044",
};

const TOOLTIP_SHAREHOLDER_SCORE: TooltipContent = {
  title: "\u682A\u4E3B\u9084\u5143\u4F59\u5730\u30B9\u30B3\u30A2\uff08\u6700\u592718\u70B9\uff09",
  desc: "\u307E\u3060\u9084\u5143\u3057\u3066\u3044\u306A\u3044\u30AD\u30E3\u30C3\u30B7\u30E5\u304C\u3069\u308C\u3060\u3051\u3042\u308B\u304B\u3092\u8A55\u4FA1",
  formula: "\u914D\u5F53\u6027\u5411(5)\uFF0B\u30AD\u30E3\u30C3\u30B7\u30E5\u7A4D\u307F\u4E0A\u304C\u308A(5)\uFF0B\u9084\u5143\u65B9\u91DD\u5909\u5316(4)\uFF0B\u6771\u8A3CPBR\u5BFE\u5FDC(4)",
  intent: "\u3053\u308C\u304B\u3089\u6C17\u3065\u304B\u308C\u308B\u9298\u67C4\u306E\u767A\u6398\u306B\u91CD\u8981\u3002\u9084\u5143\u4F59\u5730\u304C\u5927\u304D\u3044\u307B\u3069\u682A\u4FA1\u4E0A\u6607\u306E\u89E6\u5287\u306B\u306A\u308A\u3046\u308B",
};

const TOOLTIP_RISK_SCORE: TooltipContent = {
  title: "\u30EA\u30B9\u30AF\u51CF\u70B9\uff08\u6700\u5927-18\u70B9\uff09",
  desc: "\u6D41\u52D5\u6027\u30FB\u5229\u76CA\u306E\u8CEA\u30FB\u8CA1\u52D9\u5065\u5168\u6027\u306E3\u8EF8\u3067\u30EA\u30B9\u30AF\u3092\u8A55\u4FA1\u3057\u51CF\u70B9",
  formula: "\u51FA\u6765\u91CF\u30EA\u30B9\u30AF(-5)\uFF0B\u4E00\u904E\u6027\u5229\u76CA\u30EA\u30B9\u30AF(-5)\uFF0B\u8CA1\u52D9\u5065\u5168\u6027\u30EA\u30B9\u30AF(-3)\uFF0B\u305D\u306E\u4ED6",
  intent: "\u3069\u308C\u3060\u3051\u826F\u3044\u30B9\u30B3\u30A2\u3067\u3082\u30EA\u30B9\u30AF\u304C\u9AD8\u3051\u308C\u3070\u51CF\u70B9\u3002\u7B49\u7B4B\u9298\u67C4\u3092\u639B\u9664\u3059\u308B\u305F\u3081\u306E\u4ED5\u7D44\u307F",
};

const UNLOCK_PASSWORD = "tenbagger2024";
const STORAGE_KEY = "tenbagger_unlocked";
const MAX_SCORE = 100;

// All copy as Unicode escapes (ASCII-safe, no encoding issues)
const TITLE = "\uD83C\uDFAF \u30C6\u30F3\u30D0\u30FC\u30AC\u30FC\u3092\u72E9\u3046\u5272\u5B89\u5C0F\u578B\u6210\u9577\u682A";
const SUBTITLE = "\u6E05\u539F\u9054\u90C3\u5F0F \u00D7 \u30D0\u30D5\u30A7\u30C3\u30C8\u6D41 \u00D7 AI\u6C7A\u7B97\u5206\u6790\uFF5C\u6BCE\u55A7\u696D\u65E5\u66F4\u65B0";
const BADGE_PAID = "\u2705 \u6709\u6599\u30D7\u30E9\u30F3";
const BTN_UNLOCK = "\uD83D\uDD13 1\u301C5\u4F4D\u3092\u89E3\u653E \u00A51,980";
const BADGE_MARKET_CAP = "\u6642\u4FA1\u7D4C\u984D 30\u301C500\u5104\u5186";
const BADGE_PER = "PER 10\u500D\u4EE5\u4E0B";
const BADGE_NC = "NC\u6BD4\u7387 1.0\u4EE5\u4E0A";
const BADGE_PROFIT = "\u9ED2\u5B57\u4F01\u696D\u306E\u307F";
const BADGE_EXCLUDE = "\u91D1\u878D\u30FB\u4E0D\u52D5\u7523\u9664\u5916";
const BANNER_LOCK = "\uD83D\uDD12 1\u301C5\u4F4D\u306E\u9298\u67C4\u540D\u306F\u6709\u6599\u30D7\u30E9\u30F3\u3067\u89E3\u653E\u3067\u304D\u307E\u3059";
const UPDATE_PASSED = "\u901A\u904B\u9298\u67C4";
const UPDATE_COUNT = "\u4EF6";
const UPDATE_SCAN = "\u30B9\u30AD\u30E3\u30F3\u6570";
const UPDATE_MARKETS = "\u9298\u67C4";
const UPDATE_DATE = "\u66F4\u65B0\u65E5";
const UPDATE_EM_DASH = "\u2014";
const MSG_NO_JSON = "screening_result.json \u3092 public \u306B\u914D\u7F6E\u3057\u3066\u304F\u3060\u3055\u3044\u3002";
const RANK_SUFFIX = "\u4F4D";
const MASK_NAME = "\u2588\u2588\u2588\u2588\u2588\u2588";
const LABEL_MARKET = "\u30FB\u2014";
const LABEL_OKU = "\u5104\u5186";
const LABEL_NC_RATIO = "NC\u6BD4";
const LABEL_NC = "\u30CD\u30C3\u30C8\u30AD\u30E3\u30C3\u30B7\u30E5\u6BD4\u7387";
const LABEL_MARKETCAP = "\u6642\u4FA1\u7D4C\u984D";
const LABEL_DIVIDEND = "\u914D\u5F53\u5229\u56DE\u308A";
const LABEL_PAYOUT = "\u914D\u5F53\u6027\u5411";
const LABEL_SCORE = "\u30B9\u30B3\u30A2";
const FOOTER_DISCLAIMER = "\u672C\u30B5\u30FC\u30D3\u30B9\u306F\u60C5\u5831\u63D0\u4F9B\u3092\u76EE\u7684\u3068\u3057\u3066\u304A\u308A\u3001\u6295\u8CC7\u52A9\u8A00\u3067\u306F\u3042\u308A\u307E\u305B\u3093\u3002\u6295\u8CC7\u5224\u65AD\u306F\u3054\u81EA\u8EAB\u306E\u8CAC\u4EFB\u3067\u884C\u3063\u3066\u304F\u3060\u3055\u3044\u3002";
const BTN_NOTE = "note\u3067\u8CFC\u5165\u3059\u308B";
const BTN_NOTE_PURCHASE = "\uD83D\uDCDD note\u3067\u8CFC\u5165\u3059\u308B\uff08\u00A51,980\uff09\u2192";
const NOTE_URL = "https://note.com/kawachan_max";
const PLACEHOLDER_PASSWORD = "\u30D1\u30B9\u30EF\u30FC\u30C9";
const ERROR_PASSWORD = "\u30D1\u30B9\u30EF\u30FC\u30C9\u304C\u9055\u3044\u307E\u3059";
const BTN_UNLOCK_SUBMIT = "\u89E3\u653E\u3059\u308B";
const BTN_CANCEL = "\u30AD\u30E3\u30F3\u30BB\u30EB";
const SEP_LINE = "\uFF5C";

// ?????????????????????????????????
const MODAL_UNLOCK_TITLE = (lockCount: number) =>
  `\uD83D\uDD13 1\u301C${lockCount}\u4F4D\u3092\u89E3\u653E\u3059\u308B`;
const MODAL_UNLOCK_DESC = (lockCount: number) =>
  `note\u306E\u6709\u6599\u8A18\u4E8B\uFF08\uFFE51,980\uFF09\u306B\u8A18\u8F09\u306E\u30D1\u30B9\u30EF\u30FC\u30C9\u3092\u5165\u529B\u3059\u308B\u3068 1\u301C${lockCount}\u4F4D\u306E\u9298\u67C4\u540D\u304C\u8868\u793A\u3055\u308C\u307E\u3059`;

const PITCH_UNIQLO = "\u30E6\u30CB\u30AF\u30ED\uff08\u30D5\u30A1\u30FC\u30B9\u30C8\u30EA\u30C6\u30A4\u30EA\u30F3\u30B0\uff09";
const PITCH_UNIQLO_GROWTH = "\u4E0A\u5834\u6642\u304B\u3089\u7D04900\u500D\u306B\u6210\u9577";
const PITCH_NITORI = "\u30CB\u30C8\u30EA\u30DB\u30FC\u30EB\u30C7\u30A3\u30F3\u30B0\u30B9";
const PITCH_NITORI_GROWTH = "\u4E0A\u5834\u6642\u304B\u3089\u7D04300\u500D\u306B\u6210\u9577";
const PITCH_IF = "\u3082\u3057\u3042\u306E\u6642\u3001\u5272\u5B89\u306A\u5C0F\u578B\u682A\u3060\u3063\u305F\u9803\u306B\u4ED5\u8FBC\u3081\u3066\u3044\u305F\u3089\u2014\u2014\u3002";
const PITCH_WHY = "\u306A\u305C\u3053\u306E\u30B5\u30FC\u30D3\u30B9\u306F\u4ED6\u3068\u9055\u3046\u306E\u304B\uff1F";
const PITCH_BUFFETT_QUOTE = "\u300C\u4E2D\u8EAB\u306E\u308F\u304B\u3089\u306A\u3044\u3082\u306E\u306B\u306F\u6295\u8CC7\u3057\u306A\u3044\u300D\u2014 \u30A6\u30A9\u30FC\u30EC\u30F3\u30FB\u30D0\u30D5\u30A7\u30C3\u30C8";
const PITCH_BODY1 = "\u30A4\u30F3\u30D5\u30EB\u30A8\u30F3\u30B5\u30FC\u306E\u6839\u64E0\u306E\u306A\u3044\u9298\u67C4\u63A8\u5968\u3084\u3001\u4E2D\u8EAB\u306E\u308F\u304B\u3089\u306A\u3044\u8A3C\u5238\u4F1A\u793E\u304C\u63D0\u6848\u3059\u308B\u30D5\u30A1\u30F3\u30C9\u30FB\u4ED5\u7D44\u307F\u5024\u306B\u8E0A\u3089\u3055\u308C\u3066\u3044\u307E\u3059\u304B\uff1F";
const PITCH_BODY2 = "\u3053\u306E\u30B5\u30FC\u30D3\u30B9\u306F\u30012\u4EBA\u306E\u5049\u5927\u306A\u6295\u8CC7\u5BB6\u306E\u6295\u8CC7\u6CD5\u3092\u3082\u3068\u306B\u3001\u3059\u3079\u3066\u306E\u6839\u64E0\u3092\u30B9\u30B3\u30A2\u3067\u898B\u3048\u5316\u3057\u3066\u3044\u307E\u3059\u3002";
const PITCH_BODY3 = "\u3042\u306A\u305F\u81EA\u8EAB\u304C\u9298\u67C4\u3092\u898B\u6975\u3081\u308B\u76EE\u3092\u990A\u3044\u306A\u304C\u3089\u7B2C\u4E8C\u306E\u30E6\u30CB\u30AF\u30ED\u3001\u7B2C\u4E8C\u306E\u30CB\u30C8\u30EA\u3092\u8AB0\u3088\u308A\u3082\u65E9\u304F\u898B\u3064\u3051\u308B\u3053\u3068\u304C\u3067\u304D\u308B\u3002\u305D\u308C\u304C\u3053\u306E\u30B5\u30FC\u30D3\u30B9\u306E\u672C\u8CEA\u3067\u3059\u3002";
const PITCH_DESCRIPTION = "\u500B\u4EBA\u8CC7\u7523900\u5104\u5186\u8D85\u306E\u4F1D\u8AAC\u306E\u6295\u8CC7\u5BB6\u30FB\u6E05\u539F\u9054\u90C3\u306E\u6295\u8CC7\u6CD5\u3068\u3001\u500B\u4EBA\u8CC7\u7523\u7D0424\u5146\u5186\u30FB\u6295\u8CC7\u306E\u795E\u69D8\u30A6\u30A9\u30FC\u30EC\u30F3\u30FB\u30D0\u30D5\u30A7\u30C3\u30C8\u306E\u30CF\u30A4\u30D6\u30EA\u30C3\u30C9\u300C\u30CD\u30C3\u30C8\u30AD\u30E3\u30C3\u30B7\u30E5\u6BD4\u7387\u00D7\u30D0\u30EA\u30E5\u30FC\u6295\u8CC7\u300D\u306B\u6C7A\u7B97\u66F8\u3092\u8AAD\u307F\u8FBC\u307E\u305B\u30B9\u30B3\u30A2\u30EA\u30F3\u30B0\u3057\u305F\u552F\u4E00\u7121\u4E8C\u306E\u30B9\u30AF\u30EA\u30FC\u30CB\u30F3\u30B0\u30B5\u30FC\u30D3\u30B9";

const PITCH_ABOUT_TOGGLE = "\u3053\u306E\u30B5\u30FC\u30D3\u30B9\u306B\u3064\u3044\u3066";
const BTN_DETAIL_OPEN = "\u25BC \u8A73\u7D30\u3092\u898B\u308B";
const BTN_DETAIL_CLOSE = "\u25B2 \u9589\u3058\u308B";
const LABEL_SCORE_BREAKDOWN = "\u30B9\u30B3\u30A2\u5185\u8A33";
const LABEL_CHEAP = "\u5272\u5B89\u5EA6";
const LABEL_CHEAP_SHORT = "\u5272\u5B89";
const LABEL_GROWTH = "\u6210\u9577\u6027\u30FB\u4E8B\u696D\u306E\u8CEA";
const LABEL_GROWTH_SHORT = "\u6210\u9577";
const LABEL_SHAREHOLDER = "\u682A\u4E3B\u9084\u5143\u4F59\u5730";
const LABEL_RISK = "\u30EA\u30B9\u30AF\u51CF\u70B9";
const LABEL_METRICS = "\u6307\u6A5F\u30B0\u30EA\u30C3\u30C9";
const LABEL_AI_ANALYSIS = "AI\u5206\u6790\u30B3\u30E1\u30F3\u30C8";
const MSG_AI_PLACEHOLDER = "AI\u5206\u6790\u306F\u6B21\u56DE\u56DB\u534A\u671F\u66F4\u65B0\u6642\u306B\u8FFD\u52A0\u4E88\u5B9A\u3067\u3059";
const LABEL_RISK_CHECK = "\u30EA\u30B9\u30AF\u30C1\u30A7\u30C3\u30AF\uff08\u30D0\u30D5\u30A7\u30C3\u30C8\u6D41\uff09";
const RISK_CHECK_ITEMS: { key: keyof NonNullable<Row["risk_checks"]>; label: string; inverted: boolean }[] = [
  { key: "roe_15_percent", label: "ROE 15%\u4EE5\u4E0A\u306E\u7D9A\u7D9A", inverted: false },
  { key: "equity_ratio_50_percent", label: "\u81EA\u5DF1\u8CC7\u672C\u6BD4\u7387 50%\u4EE5\u4E0A", inverted: false },
  { key: "debt_to_profit_5x", label: "\u9577\u671F\u8CA0\u50B5/\u7D14\u5229\u76CA 5\u500D\u4EE5\u5185", inverted: false },
  { key: "fcf_stability", label: "FCF\u306E\u5B89\u5B9A\u6027", inverted: false },
  { key: "liquidity_risk", label: "\u51FA\u6765\u91CF\uff08\u6D41\u52D5\u6027\uff09", inverted: true },
  { key: "one_time_profit_risk", label: "\u4E00\u904E\u6027\u5229\u76CA\u30EA\u30B9\u30AF", inverted: true },
];
const DASH = "\u2014";

const PITCH_TIMES = "\u500D"; // \u500D

const GRADE_LABELS = {
  excellent: "\u25CE", // \u25CE
  good: "\u25CB",      // \u25CB
  fair: "\u25B3",      // \u25B3
  poor: "\u00D7",      // \u00D7
} as const;

type GradeKey = keyof typeof GRADE_LABELS;

const BADGES = [BADGE_MARKET_CAP, BADGE_PER, BADGE_NC, BADGE_PROFIT, BADGE_EXCLUDE] as const;

type Row = {
  code: string;
  name: string;
  name_jp?: string;
  score: number;
  net_cash_ratio: number;
  per: number;
  market_cap_oku: number;
  dividend_yield?: number | null;
  valuation_score?: number;
  growth_score?: number;
  shareholder_score?: number;
  risk_penalty?: number;
  payout_ratio?: number | null;
  roe?: number | null;
  roic?: number | null;
  pbr?: number | null;
  ai_comment?: string;
  risk_checks?: {
    roe_15_percent: boolean | null;
    equity_ratio_50_percent: boolean | null;
    debt_to_profit_5x: boolean | null;
    fcf_stability: boolean | null;
    liquidity_risk: boolean | null;
    one_time_profit_risk: boolean | null;
  } | null;
};

const POPUP_WIDTH = 280;
const POPUP_EST_HEIGHT = 160;
const POPUP_MARGIN = 8;

function IndicatorTooltip({ content }: { content: TooltipContent }) {
  const [hover, setHover] = useState(false);
  const [clicked, setClicked] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const containerRef = useRef<HTMLSpanElement>(null);
  const visible = hover || clicked;

  useEffect(() => {
    if (!clicked) return;
    const onDocClick = (e: MouseEvent) => {
      if (containerRef.current?.contains(e.target as Node)) return;
      setClicked(false);
    };
    document.addEventListener("click", onDocClick);
    return () => document.removeEventListener("click", onDocClick);
  }, [clicked]);

  useEffect(() => {
    if (!visible || !containerRef.current) return;
    const el = containerRef.current;
    const rect = el.getBoundingClientRect();
    const vw = typeof window !== "undefined" ? window.innerWidth : 1024;
    const vh = typeof window !== "undefined" ? window.innerHeight : 768;
    const w = Math.min(POPUP_WIDTH, vw * 0.9);
    let top = rect.top - POPUP_EST_HEIGHT - POPUP_MARGIN;
    let left = rect.left;
    if (top < POPUP_MARGIN) top = rect.bottom + POPUP_MARGIN;
    if (left + w > vw - POPUP_MARGIN) left = vw - w - POPUP_MARGIN;
    if (left < POPUP_MARGIN) left = POPUP_MARGIN;
    if (top + POPUP_EST_HEIGHT > vh - POPUP_MARGIN) top = vh - POPUP_EST_HEIGHT - POPUP_MARGIN;
    setPosition({ top, left });
  }, [visible]);

  return (
    <span
      ref={containerRef}
      className="relative inline-flex items-center"
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          setClicked((c) => !c);
        }}
        className="w-4 h-4 flex items-center justify-center rounded-full bg-gray-200 text-gray-600 text-xs font-medium hover:bg-gray-300 transition-colors shrink-0"
        aria-label="\u8AAC\u660E\u3092\u8868\u793A"
      >
        ?
      </button>
      {visible && (
        <span
          className="fixed z-50 p-3 bg-white rounded-lg shadow-lg border border-gray-200 text-left max-w-[90vw]"
          style={{
            top: position.top,
            left: position.left,
            width: Math.min(POPUP_WIDTH, typeof window !== "undefined" ? window.innerWidth * 0.9 : POPUP_WIDTH),
          }}
          role="tooltip"
        >
          <div className="text-xs font-bold text-[#1a1a1a] mb-1">{content.title}</div>
          <div className="text-xs text-[#4a4a4a] mb-2">{content.desc}</div>
          <div className="text-xs text-[#6b6b6b] bg-gray-100 rounded px-2 py-1 mb-2">{content.formula}</div>
          <div className="text-xs text-amber-700">{content.intent}</div>
        </span>
      )}
    </span>
  );
}

function getCheapScore(net_cash_ratio: number, per: number): number {
  let nc = 0;
  if (net_cash_ratio >= 2.0) nc = 18;
  else if (net_cash_ratio >= 1.5) nc = 14;
  else if (net_cash_ratio >= 1.2) nc = 9;
  else if (net_cash_ratio >= 1.0) nc = 5;
  let pr = 0;
  if (per < 5) pr = 9;
  else if (per >= 5 && per < 8) pr = 5;
  return nc + pr;
}

function getCheapBadge(cheapScore: number): GradeKey {
  if (cheapScore >= 22) return "excellent";
  if (cheapScore >= 14) return "good";
  if (cheapScore >= 5) return "fair";
  return "poor";
}

function getGrowthBadge(score: number, cheapScore: number): GradeKey {
  const rest = score - cheapScore;
  if (rest >= 35) return "excellent";
  if (rest >= 25) return "good";
  if (rest >= 15) return "fair";
  return "poor";
}

function getGradeFromGrowthScore(s: number): GradeKey {
  if (s >= 35) return "excellent";
  if (s >= 25) return "good";
  if (s >= 15) return "fair";
  return "poor";
}

function getGradeFromShareholderScore(s: number): GradeKey {
  if (s >= 14) return "excellent";
  if (s >= 9) return "good";
  if (s >= 4) return "fair";
  return "poor";
}

function getBadgeClass(grade: GradeKey): string {
  const classes: Record<GradeKey, string> = {
    excellent: "bg-emerald-100 text-emerald-700",
    good: "bg-blue-100 text-blue-700",
    fair: "bg-amber-100 text-amber-700",
    poor: "bg-red-100 text-red-700",
  };
  return classes[grade];
}

export default function Home() {
  const [rows, setRows] = useState<Row[]>([]);
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [pitchOpen, setPitchOpen] = useState(false);
  const [expandedCode, setExpandedCode] = useState<string | null>(null);

  useEffect(() => {
    fetch("/screening_result.json")
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => setRows(Array.isArray(data) ? data : []))
      .catch(() => setRows([]));
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    setIsUnlocked(stored === "true");
  }, []);

  const handleUnlock = () => {
    if (password === UNLOCK_PASSWORD) {
      localStorage.setItem(STORAGE_KEY, "true");
      setIsUnlocked(true);
      setModalOpen(false);
      setPassword("");
      setPasswordError("");
    } else {
      setPasswordError(ERROR_PASSWORD);
    }
  };

  const openModal = () => {
    setModalOpen(true);
    setPassword("");
    setPasswordError("");
  };

  const rankStyle = (i: number) => {
    if (i === 0) return "text-yellow-400 font-bold";
    if (i === 1) return "text-[#1a1a1a] font-bold";
    if (i === 2) return "text-amber-600 font-bold";
    return "text-[#6b6b6b]";
  };

  const lockCount = rows.length >= 20 ? 10 : 5;
  const displayName = (r: Row) => (r.name_jp || r.name || r.code) || r.code;

  return (
    <div className="min-h-screen bg-[#f9f7f4] text-[#1a1a1a]">
      <header className="sticky top-0 z-20 border-b border-[#e5e0d8] bg-white backdrop-blur">
        <div className="max-w-4xl mx-auto px-4 py-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-[#1a1a1a]">
              {TITLE}
            </h1>
            <p className="text-xs text-[#6b6b6b] mt-0.5">{SUBTITLE}</p>
          </div>
          <div>
            {isUnlocked ? (
              <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#f0ece6] text-[#16a34a] text-sm">
                {BADGE_PAID}
              </span>
            ) : (
              <button
                type="button"
                onClick={openModal}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#1a1a1a] text-white font-medium text-sm hover:opacity-90 transition-colors"
              >
                {`\uD83D\uDD13 1\u301C${lockCount}\u4F4D\u3092\u89E3\u653E \u00A51,980`}
              </button>
            )}
          </div>
        </div>

        {/* ????????????????????? */}
        <div className="max-w-4xl mx-auto px-4 mt-4 mb-3">
          <div className="rounded-xl border border-[#f59e0b] bg-[#fffbeb] p-4">
            <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-6 mb-3">
              <div className="flex items-baseline gap-1.5">
                <span className="text-2xl font-bold text-[#b45309]">900{PITCH_TIMES}</span>
                <span className="text-xs text-[#6b6b6b] ml-0.5">{PITCH_UNIQLO}</span>
              </div>
              <div className="flex items-baseline gap-1.5">
                <span className="text-2xl font-bold text-[#b45309]">300{PITCH_TIMES}</span>
                <span className="text-xs text-[#6b6b6b] ml-0.5">{PITCH_NITORI}</span>
              </div>
            </div>
            <p className="text-center italic text-[#4a4a4a] text-xs mb-3">
              {PITCH_IF}
            </p>
            <button
              type="button"
              onClick={() => setPitchOpen(!pitchOpen)}
              className="w-full flex items-center justify-center gap-1 py-2 text-sm text-[#92400e] font-medium hover:bg-[#fef3c7]/50 rounded-lg transition-colors"
            >
              {PITCH_ABOUT_TOGGLE} {pitchOpen ? "?" : "?"}
            </button>
            {pitchOpen && (
              <>
                <hr className="border-[#f59e0b]/50 my-3" />
                <h2 className="text-sm font-semibold text-[#1a1a1a] mb-2">
                  {PITCH_WHY}
                </h2>
                <blockquote className="pl-3 py-1.5 my-2 rounded-lg bg-[#e5e0d8]/80 text-[#4a4a4a] text-xs border-l-4 border-[#f59e0b]">
                  {PITCH_BUFFETT_QUOTE}
                </blockquote>
                <p className="text-xs text-[#4a4a4a] leading-relaxed mb-3">
                  {PITCH_BODY1}
                  {PITCH_BODY2}
                  {PITCH_BODY3}
                </p>
                <hr className="border-[#f59e0b]/50 my-3" />
                <p className="text-center font-bold text-xs text-[#1a1a1a] leading-relaxed">
                  {PITCH_DESCRIPTION}
                </p>
              </>
            )}
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4 pb-3 flex flex-wrap gap-2">
          {BADGES.map((label) => (
            <span
              key={label}
              className="px-2.5 py-1 rounded-md bg-[#f0ece6] text-[#4a4a4a] text-xs"
            >
              {label}
            </span>
          ))}
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6">
        {!isUnlocked && rows.length > 0 && (
          <button
            type="button"
            onClick={openModal}
            className="w-full mb-4 py-3 px-4 rounded-xl bg-[#fef9ec] border border-[#f59e0b] text-[#92400e] text-sm font-medium hover:bg-[#fef3c7] transition-colors text-left"
          >
            {`\uD83D\uDD12 1\u301C${lockCount}\u4F4D\u306E\u9298\u67C4\u540D\u306F\u6709\u6599\u30D7\u30E9\u30F3\u3067\u89E3\u653E\u3067\u304D\u307E\u3059`}
          </button>
        )}

        {rows.length > 0 && (
          <p className="text-xs text-[#6b6b6b] mb-4">
            {UPDATE_PASSED} {rows.length} {UPDATE_COUNT} {SEP_LINE} {UPDATE_SCAN} 3,327 {UPDATE_MARKETS} {SEP_LINE} {UPDATE_DATE}: {UPDATE_EM_DASH}
          </p>
        )}

        <div className="space-y-3">
          {rows.length === 0 ? (
            <p className="text-[#6b6b6b] py-8 text-sm">{MSG_NO_JSON}</p>
          ) : (
            rows.map((r, i) => {
              const valuationScore = r.valuation_score ?? getCheapScore(r.net_cash_ratio, r.per);
              const cheapBadge = getCheapBadge(valuationScore);
              const growthScore = r.growth_score ?? (r.score - valuationScore);
              const growthBadge = r.growth_score != null ? getGradeFromGrowthScore(r.growth_score) : getGrowthBadge(r.score, valuationScore);
              const isExpanded = expandedCode === r.code;
              return (
                <div
                  key={r.code}
                  className="rounded-xl border border-[#e5e0d8] bg-white p-4 shadow-sm hover:shadow-md transition-shadow"
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div className="flex items-center gap-3 min-w-0">
                      <span className={`text-lg shrink-0 ${rankStyle(i)}`}>
                        {i + 1}{RANK_SUFFIX}
                      </span>
                      <div className="min-w-0">
                        <div className="font-medium truncate text-[#1a1a1a]">
                          {i < lockCount && !isUnlocked ? MASK_NAME : displayName(r)}
                        </div>
                        {!(i < lockCount && !isUnlocked) && (
                          <div className="flex items-center gap-2 mt-0.5 text-sm text-[#6b6b6b]">
                            <Link
                              href={`https://finance.yahoo.co.jp/quote/${r.code}.T`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="font-mono text-[#2563eb] hover:underline"
                            >
                              {r.code}
                            </Link>
                            <span>{LABEL_MARKET}</span>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex flex-wrap items-center gap-3 text-sm shrink-0">
                      <span className="inline-flex items-center gap-0.5 text-[#1a1a1a]">
                        {r.market_cap_oku} {LABEL_OKU}
                        <IndicatorTooltip content={TOOLTIP_MARKETCAP} />
                      </span>
                      <span className="inline-flex items-center gap-0.5 text-[#2563eb]">
                        PER {r.per}
                        <IndicatorTooltip content={TOOLTIP_PER} />
                      </span>
                      <span className="inline-flex items-center gap-0.5 text-[#16a34a]">
                        {LABEL_NC_RATIO} {r.net_cash_ratio.toFixed(2)}
                        <IndicatorTooltip content={TOOLTIP_NC} />
                      </span>
                      {r.dividend_yield != null && r.dividend_yield !== undefined && (
                        <span className="inline-flex items-center gap-0.5 text-yellow-600">
                          {LABEL_DIVIDEND} {r.dividend_yield}%
                          <IndicatorTooltip content={TOOLTIP_DIVIDEND} />
                        </span>
                      )}
                      <span className="inline-flex items-center gap-2">
                        <span className="inline-flex items-center gap-1">
                          <span className="text-xs text-gray-400">{LABEL_CHEAP_SHORT}</span>
                          <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${getBadgeClass(cheapBadge)}`} title={LABEL_CHEAP}>
                            {GRADE_LABELS[cheapBadge]}
                          </span>
                        </span>
                        <span className="inline-flex items-center gap-1">
                          <span className="text-xs text-gray-400">{LABEL_GROWTH_SHORT}</span>
                          <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${getBadgeClass(growthBadge)}`} title={LABEL_GROWTH}>
                            {GRADE_LABELS[growthBadge]}
                          </span>
                        </span>
                      </span>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center gap-3">
                    <span className="text-sm text-[#6b6b6b]">{LABEL_SCORE}</span>
                    <div className="flex-1 h-2 rounded-full bg-[#e5e0d8] overflow-hidden max-w-[200px]">
                      <div
                        className="h-full rounded-full bg-[#d97706] transition-all"
                        style={{
                          width: `${Math.min(100, (r.score / MAX_SCORE) * 100)}%`,
                        }}
                      />
                    </div>
                    <span className="text-[#d97706] font-medium tabular-nums">
                      {r.score} / {MAX_SCORE}
                    </span>
                  </div>
                  <div className="mt-3 pt-3 border-t border-[#e5e0d8]">
                    <button
                      type="button"
                      onClick={() => {
                        if (!isUnlocked) {
                          setModalOpen(true);
                          return;
                        }
                        setExpandedCode(isExpanded ? null : r.code);
                      }}
                      className="text-xs text-[#92400e] font-medium hover:underline"
                    >
                      {isExpanded ? BTN_DETAIL_CLOSE : BTN_DETAIL_OPEN}
                    </button>
                  </div>
                  {isUnlocked && isExpanded && (
                    <div className="mt-4 pt-4 border-t border-[#e5e0d8] space-y-4 text-sm">
                      <section>
                        <h3 className="text-xs font-semibold text-[#6b6b6b] mb-2">{LABEL_SCORE_BREAKDOWN}</h3>
                        <div className="space-y-2">
                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {LABEL_CHEAP}
                              <IndicatorTooltip content={TOOLTIP_CHEAP_SCORE} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div className="h-full rounded-full bg-emerald-500" style={{ width: `${Math.min(100, ((r.valuation_score ?? valuationScore) / 27) * 100)}%` }} />
                            </div>
                            <span className="text-xs tabular-nums w-10">{(r.valuation_score ?? valuationScore)}/27</span>
                            <span className={`px-1 py-0.5 rounded text-xs ${getBadgeClass(cheapBadge)}`}>{GRADE_LABELS[cheapBadge]}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {LABEL_GROWTH}
                              <IndicatorTooltip content={TOOLTIP_GROWTH_SCORE} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div className="h-full rounded-full bg-blue-500" style={{ width: `${Math.min(100, ((r.growth_score ?? growthScore) / 46) * 100)}%` }} />
                            </div>
                            <span className="text-xs tabular-nums w-10">{(r.growth_score ?? growthScore)}/46</span>
                            <span className={`px-1 py-0.5 rounded text-xs ${getBadgeClass(growthBadge)}`}>{GRADE_LABELS[growthBadge]}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {LABEL_SHAREHOLDER}
                              <IndicatorTooltip content={TOOLTIP_SHAREHOLDER_SCORE} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div className="h-full rounded-full bg-amber-400" style={{ width: `${Math.min(100, ((r.shareholder_score ?? 0) / 18) * 100)}%` }} />
                            </div>
                            <span className="text-xs tabular-nums w-10">{(r.shareholder_score ?? 0)}/18</span>
                            <span className={`px-1 py-0.5 rounded text-xs ${getBadgeClass(getGradeFromShareholderScore(r.shareholder_score ?? 0))}`}>{GRADE_LABELS[getGradeFromShareholderScore(r.shareholder_score ?? 0)]}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {LABEL_RISK}
                              <IndicatorTooltip content={TOOLTIP_RISK_SCORE} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div className="h-full rounded-full bg-red-300" style={{ width: `${Math.min(100, (Math.abs(r.risk_penalty ?? 0) / 18) * 100)}%` }} />
                            </div>
                            <span className="text-xs tabular-nums w-12">{(r.risk_penalty ?? 0)}/-18</span>
                            <span className={`px-1 py-0.5 rounded text-xs ${getBadgeClass("poor")}`}>{GRADE_LABELS.poor}</span>
                          </div>
                        </div>
                      </section>
                      <section>
                        <h3 className="text-xs font-semibold text-[#6b6b6b] mb-2">{LABEL_METRICS}</h3>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div className="text-[#6b6b6b]">{LABEL_NC}</div>
                          <div className="font-medium">{r.net_cash_ratio}</div>
                          <div className="text-[#6b6b6b]">PER</div>
                          <div className="font-medium">{r.per}{PITCH_TIMES}</div>
                          <div className="text-[#6b6b6b]">{LABEL_MARKETCAP}</div>
                          <div className="font-medium">{r.market_cap_oku}{LABEL_OKU}</div>
                          <div className="text-[#6b6b6b]">{LABEL_DIVIDEND}</div>
                          <div className="font-medium">{r.dividend_yield != null ? `${r.dividend_yield}%` : DASH}</div>
                          <div className="text-[#6b6b6b]">ROE</div>
                          <div className="font-medium">{r.roe != null ? `${r.roe}%` : DASH}</div>
                          <div className="text-[#6b6b6b]">ROIC</div>
                          <div className="font-medium">{r.roic != null ? `${r.roic}%` : DASH}</div>
                          <div className="text-[#6b6b6b]">PBR</div>
                          <div className="font-medium">{r.pbr != null ? `${r.pbr}${PITCH_TIMES}` : DASH}</div>
                          <div className="text-[#6b6b6b]">{LABEL_PAYOUT}</div>
                          <div className="font-medium">{r.payout_ratio != null ? `${r.payout_ratio}%` : DASH}</div>
                        </div>
                      </section>
                      <section>
                        <h3 className="text-xs font-semibold text-[#6b6b6b] mb-2">{LABEL_AI_ANALYSIS}</h3>
                        <div className="rounded-lg bg-[#e5e0d8]/60 p-3 text-xs text-[#4a4a4a]">
                          {r.ai_comment?.trim() || MSG_AI_PLACEHOLDER}
                        </div>
                      </section>
                      <section>
                        <h3 className="text-xs font-semibold text-[#6b6b6b] mb-2">{LABEL_RISK_CHECK}</h3>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          {RISK_CHECK_ITEMS.map(({ key, label, inverted }) => {
                            const val = r.risk_checks?.[key];
                            let badge: "\u25CE" | "\u25CB" | "\u25B3" | "\u00D7" = "\u25B3";
                            let badgeClass = "bg-amber-100 text-amber-700";
                            let suffix = "";
                            if (val === null || val === undefined) {
                              badge = "\u25B3";
                              badgeClass = "bg-amber-100 text-amber-700";
                            } else if (inverted) {
                              if (val === false) {
                                badge = "\u25CE";
                                badgeClass = "bg-emerald-100 text-emerald-700";
                                suffix = " \u554F\u984C\u306A\u3057";
                              } else {
                                badge = "\u00D7";
                                badgeClass = "bg-red-100 text-red-700";
                                suffix = " \u30EA\u30B9\u30AF\u3042\u308A";
                              }
                            } else {
                              if (val === true) {
                                badge = "\u25CE";
                                badgeClass = "bg-emerald-100 text-emerald-700";
                              } else {
                                badge = "\u00D7";
                                badgeClass = "bg-red-100 text-red-700";
                              }
                            }
                            return (
                              <div key={key} className="flex items-center gap-1.5 flex-wrap">
                                <span className="text-[#6b6b6b]">{label}</span>
                                <span className={`inline-flex items-center px-1.5 py-0.5 rounded font-medium shrink-0 ${badgeClass}`}>{badge}{suffix}</span>
                              </div>
                            );
                          })}
                        </div>
                      </section>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        <footer className="mt-12 py-6 border-t border-[#e5e0d8]">
          <p className="text-xs text-[#9ca3af] leading-relaxed">
            {FOOTER_DISCLAIMER}
          </p>
        </footer>
      </main>

      {modalOpen && (
        <div
          className="fixed inset-0 z-30 flex items-center justify-center p-4 bg-black/40"
          onClick={() => setModalOpen(false)}
        >
          <div
            className="w-full max-w-md rounded-2xl border border-[#e5e0d8] bg-white p-6 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-lg font-semibold mb-2 text-[#1a1a1a]">
              {MODAL_UNLOCK_TITLE(lockCount)}
            </h2>
            <p className="text-sm text-[#6b6b6b] mb-4">
              {MODAL_UNLOCK_DESC(lockCount)}
            </p>
            <input
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setPasswordError("");
              }}
              placeholder={PLACEHOLDER_PASSWORD}
              className="w-full px-3 py-2 rounded-lg bg-white border border-[#e5e0d8] text-[#1a1a1a] placeholder-[#9ca3af] focus:outline-none focus:ring-2 focus:ring-[#d97706]/60 mb-2"
            />
            {passwordError && (
              <p className="text-sm text-red-500 mb-2">{passwordError}</p>
            )}
            <a
              href={NOTE_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="block w-full mb-3 py-2 rounded-lg bg-amber-400 text-white font-bold text-center hover:opacity-90 transition-colors"
            >
              {BTN_NOTE_PURCHASE}
            </a>
            <div className="flex gap-2 mt-2">
              <button
                type="button"
                onClick={handleUnlock}
                className="flex-1 py-2 rounded-lg bg-[#1a1a1a] text-white font-medium hover:opacity-90 transition-colors"
              >
                {BTN_UNLOCK_SUBMIT}
              </button>
              <button
                type="button"
                onClick={() => {
                  setModalOpen(false);
                  setPassword("");
                  setPasswordError("");
                }}
                className="flex-1 py-2 rounded-lg bg-[#f0ece6] text-[#4a4a4a] hover:bg-[#e5dfd4] transition-colors"
              >
                {BTN_CANCEL}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
