"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";

type TooltipContent = { title: string; desc: string; formula: string; intent: string };

const TOOLTIP_PER: TooltipContent = {
  title: "PER",
  desc: "\u682A\u4FA1\u304C1\u5E74\u5206\u306E\u5229\u76CA\u306E\u4F55\u500D\u304B\u3092\u793A\u3059\u6307\u6a19\u300210\u500D\u4EE5\u4E0B\uFF1D\u5E02\u5834\u306B\u307E\u3060\u6C17\u3065\u304B\u308C\u3066\u3044\u306A\u3044\u5272\u5B89\u306E\u8A3C\u62E0",
  formula: "\u682A\u4FA1 \u00F7 EPS",
  intent: "10\u500D\u4EE5\u4E0B\uFF1D\u5272\u5B89",
};

const TOOLTIP_NC: TooltipContent = {
  title: "\u30cd\u30c3\u30c8\u30ad\u30e3\u30c3\u30b7\u30e5\u6bd4\u7387",
  desc: "\u4f1a\u793e\u304c\u6301\u3064\u73fe\u91d1\u304b\u3089\u8ca0\u50b5\u3092\u5f15\u3044\u305f\u7d14\u73fe\u91d1\u304c\u6642\u4fa1\u7dcf\u984d\u306e\u4f55\u500d\u304b\u3092\u793a\u3059\u6307\u6a19\u30021.0\u4ee5\u4e0a\uff1d\u682a\u4fa1\u3088\u308a\u73fe\u91d1\u304c\u591a\u3044\u8d85\u5272\u5b89\u72b6\u614b",
  formula: "\u7d14\u73fe\u91d1 \u00f7 \u6642\u4fa1\u7dcf\u984d",
  intent: "1.0\u4ee5\u4e0a\uff1d\u8d85\u5272\u5b89",
};

const TOOLTIP_MARKETCAP: TooltipContent = {
  title: "\u6642\u4FA1\u7DCF\u984D",
  desc: "\u4F1A\u793E\u5168\u4F53\u306E\u4FA1\u5024\uff08\u682A\u4FA1\u00D7\u767A\u884C\u6E08\u682A\u5F0F\u6570\uff09\u300230\u301C500\u5104\u5186\uFF1D\u6A5F\u95A2\u6295\u8CC7\u5BB6\u304C\u624B\u3092\u51FA\u3057\u306B\u304F\u3044\u5C0F\u578B\u682A\u30BE\u30FC\u30F3",
  formula: "\u682A\u4FA1 \u00D7 \u767A\u884C\u6E08\u682A\u5F0F\u6570",
  intent: "30\u301C500\u5104\u5186\uFF1D\u5C0F\u578B\u682A\u30BE\u30FC\u30F3",
};

const TOOLTIP_DIVIDEND: TooltipContent = {
  title: "\u914D\u5F53\u5229\u56DE\u308A",
  desc: "\u682A\u4FA1\u306B\u5BFE\u3057\u3066\u5E74\u9593\u914D\u5F53\u91D1\u306E\u5272\u5408\u3002\u9AD8\u3044\u307B\u3069\u4FDD\u6709\u3059\u308B\u3060\u3051\u3067\u591A\u304F\u306E\u914D\u5F53\u3092\u3082\u3089\u3048\u308B",
  formula: "\u5E74\u9593\u914D\u5F53\u91D1 \u00F7 \u682A\u4FA1 \u00D7 100",
  intent: "\u9AD8\u3044\u307B\u3069\u9084\u5143\u4F59\u5730\u306E\u89B3\u70B9",
};

const TOOLTIP_ROE: TooltipContent = {
  title: "ROE",
  desc: "\u81EA\u5DF1\u8CC7\u672C\uff08\u682A\u4E3B\u306E\u304A\u91D1\uff09\u3092\u3069\u308C\u3060\u3051\u52B9\u7387\u826F\u304F\u4F7F\u3063\u3066\u5229\u76CA\u3092\u51FA\u3057\u3066\u3044\u308B\u304B\u300215%\u4EE5\u4E0A\uFF1D\u30D0\u30D5\u30A7\u30C3\u30C8\u304C\u91CD\u8996\u3059\u308B\u512A\u826F\u4F01\u696D\u306E\u57FA\u6E96",
  formula: "\u7D14\u5229\u76CA \u00F7 \u81EA\u5DF1\u8CC7\u672C \u00D7 100",
  intent: "15%\u4EE5\u4E0A\uFF1D\u512A\u826F\u4F01\u696D",
};

const TOOLTIP_ROIC: TooltipContent = {
  title: "ROIC",
  desc: "\u4f1a\u793e\u304c\u6295\u8cc7\u3057\u305f\u304a\u91d1\u5168\u4f53\u306b\u5bfe\u3057\u3066\u3069\u308c\u3060\u3051\u7a3c\u3044\u3067\u3044\u308b\u304b\u3092\u793a\u3059\u6307\u6a19\u3002ROE\u3088\u308a\u8ca1\u52d9\u306e\u6b6a\u307f\u304c\u5c11\u306a\u3044",
  formula: "\u55b6\u696d\u5229\u76ca \u00f7 \u6295\u8cc7\u8cc7\u672c",
  intent: "8\uff05\u4ee5\u4e0a\u304c\u76ee\u5b89\u3002\u9ad8\u3044\u307b\u3069\u8cc7\u672c\u52b9\u7387\u304c\u826f\u3044",
};

const TOOLTIP_EQUITY_RATIO: TooltipContent = {
  title: "\u81ea\u5df1\u8cc7\u672c\u6bd4\u7387",
  desc: "\u7dcf\u8cc7\u7523\u306b\u5bfe\u3059\u308b\u81ea\u5df1\u8cc7\u672c\u306e\u5272\u5408\u3002\u9280\u884c\u3067\u306fBIS\u898f\u5236\u3068\u306e\u95a2\u9023\u304c\u5927\u304d\u3044",
  formula: "\u81ea\u5df1\u8cc7\u672c \u00f7 \u7dcf\u8cc7\u7523 \u00d7 100",
  intent: "8\uff05\u4ee5\u4e0a\u3092\u76ee\u5b89\u306b\u3057\u305f\u30c1\u30a7\u30c3\u30af\uff08\u672c\u30bf\u30d6\uff09",
};

const TOOLTIP_PBR: TooltipContent = {
  title: "PBR",
  desc: "\u682A\u4FA1\u304C\u7D14\u8CC7\u7523\uff08\u4F1A\u793E\u306E\u6B63\u5473\u8CC7\u7523\uff09\u306E\u4F55\u500D\u304B\u3092\u793A\u3059\u6307\u6a19\u30021\u500D\u672A\u6E80\uFF1D\u89E3\u6563\u3057\u3066\u3082\u682A\u4FA1\u3088\u308A\u591A\u304F\u304A\u91D1\u304C\u623B\u3063\u3066\u304F\u308B\u8D85\u5272\u5B89\u72B6\u614B",
  formula: "\u682A\u4FA1 \u00F7 \u7D14\u8CC7\u7523\u4FA1\u5024",
  intent: "1\u500D\u672A\u6E80\uFF1D\u8D85\u5272\u5B89",
};

const TOOLTIP_PAYOUT: TooltipContent = {
  title: "\u914D\u5F53\u6027\u5411",
  desc: "\u5229\u76CA\u306E\u3046\u3061\u4F55%\u3092\u914D\u5F53\u3068\u3057\u3066\u682A\u4E3B\u306B\u9084\u5143\u3057\u3066\u3044\u308B\u304B\u300230%\u672A\u6E80\uFF1D\u307E\u3060\u9084\u5143\u4F59\u5730\u304C\u5927\u304D\u3044",
  formula: "\u914D\u5F53\u91D1 \u00F7 \u7D14\u5229\u76CA \u00D7 100",
  intent: "30%\u672A\u6E80\uFF1D\u9084\u5143\u4F59\u5730",
};

const TOOLTIP_THEORETICAL: TooltipContent = {
  title: "\u7406\u8ad6\u682a\u4fa1",
  desc: "\u8cc7\u7523\u4fa1\u5024\uff08BPS\u00d7\u81ea\u5df1\u8cc7\u672c\u6bd4\u7387\u306b\u3088\u308b\u5272\u5f15\u8a55\u4fa1\uff09\u3068\u4e8b\u696d\u4fa1\u5024\uff08EPS\u00d7\u57fa\u6e96PER\u00d7ROE\u88dc\u6b63\uff09\u306e\u5408\u8a08",
  formula: "\u8cc7\u7523\u4fa1\u5024(BPS\u00d7\u5272\u5f15\u7387) + \u4e8b\u696d\u4fa1\u5024(EPS\u00d712\u00d7ROE\u88dc\u6b63)",
  intent: "\u73fe\u5728\u306e\u682a\u4fa1\u304c\u7406\u8ad6\u7684\u306a\u4fa1\u5024\u3068\u6bd4\u3079\u3066\u5272\u5b89\u304b\u5272\u9ad8\u304b\u306e\u76ee\u5b89\u3002\u7c21\u6613\u8a08\u7b97\u306e\u305f\u3081\u53c2\u8003\u5024",
};

const TOOLTIP_UPSIDE: TooltipContent = {
  title: "\u4e0a\u6607\u4f59\u5730",
  desc: "\u7406\u8ad6\u682a\u4fa1\u3068\u73fe\u5728\u306e\u682a\u4fa1\u306e\u304b\u3044\u308a\u7387",
  formula: "(\u7406\u8ad6\u682a\u4fa1 - \u73fe\u5728\u682a\u4fa1) \u00f7 \u73fe\u5728\u682a\u4fa1 \u00d7 100",
  intent: "\u30d7\u30e9\u30b9\u306a\u3089\u5272\u5b89\u306e\u53ef\u80fd\u6027\u3001\u30de\u30a4\u30ca\u30b9\u306a\u3089\u5272\u9ad8\u306e\u53ef\u80fd\u6027\u3002\u7c21\u6613\u8a08\u7b97\u306e\u305f\u3081\u53c2\u8003\u5024",
};

const TOOLTIP_CHEAP_SCORE: TooltipContent = {
  title: "\u5272\u5b89\u5ea6\u30b9\u30b3\u30a2\uff08\u6700\u592730\u70b9\uff09",
  desc: "\u30cd\u30c3\u30c8\u30ad\u30e3\u30c3\u30b7\u30e5\u6bd4\u7387\uff08NC\u6bd4\u7387\uff09\u3068PER\u3067\u5272\u5b89\u5ea6\u3092\u70b9\u6570\u5316\u3057\u307e\u3059",
  formula: "NC\u6bd4\u7387\u30b9\u30b3\u30a2\uff08\u6700\u592720\u70b9\uff09\uff0bPER\u30b9\u30b3\u30a2\uff08\u6700\u592710\u70b9\uff09",
  intent: "\u6e05\u539f\u9054\u90ce\u5f0f\u306e\u6838\u5fc3\u3002NC\u6bd4\u7387\u3068PER\u304c\u4f4e\u3044\u307b\u3069\u5272\u5b89\u5ea6\u304c\u9ad8\u304f\u8a55\u4fa1\u3055\u308c\u307e\u3059",
};

const TOOLTIP_GROWTH_SCORE: TooltipContent = {
  title: "\u6210\u9577\u6027\u30b9\u30b3\u30a2\uff08\u6700\u592720\u70b9\uff09",
  desc: "\u58f2\u4e0a\u30fb\u5229\u76ca\u306e\u5897\u53ce\u5897\u76ca\u3068\u6210\u9577\u7387\u3067\u6210\u9577\u6027\u3092\u8a55\u4fa1\u3057\u307e\u3059",
  formula: "3\u671f\u9023\u7d9a\u5897\u53ce(5)\uff0b\u58f2\u4e0a\u6210\u9577\u7387(5)\uff0b3\u671f\u9023\u7d9a\u5897\u76ca(5)\uff0b\u5229\u76ca\u6210\u9577\u7387(5)",
  intent: "\u4e2d\u9577\u671f\u306b\u6210\u9577\u304c\u7d9a\u3044\u3066\u3044\u308b\u304b\u3092\u898b\u308b\u9805\u76ee\u3067\u3059",
};

const TOOLTIP_QUALITY_DETAIL: TooltipContent = {
  title: "\u53ce\u76ca\u6027\uff08\u6700\u592715\u70b9\uff09",
  desc: "ROE\u3068ROIC\u306e\u6c34\u6e96\u3068\u55b6\u696d\u5229\u76ca\u7387\u306e\u5b89\u5b9a\u6027\u3067\u4e8b\u696d\u306e\u8cea\u3092\u8a55\u4fa1\u3057\u307e\u3059",
  formula: "ROE\u30b9\u30b3\u30a2(5)\uff0bROIC\u30b9\u30b3\u30a2(5)\uff0b\u53ce\u76ca\u5b89\u5b9a\u6027\u30b9\u30b3\u30a2(5)",
  intent: "\u55b6\u696d\u5229\u76ca\u306e\u7d9a\u304f\u5b9f\u7e3e\u3092\u898b\u306a\u304c\u3089\u3001\u5229\u76ca\u306e\u8cea\u3092\u8a55\u4fa1\u3057\u307e\u3059",
};

const TOOLTIP_SHAREHOLDER_SCORE: TooltipContent = {
  title: "\u682a\u4e3b\u9084\u5143\u4f59\u5730\u30b9\u30b3\u30a2\uff08\u6700\u592710\u70b9\uff09",
  desc: "\u914d\u5f53\u6027\u5411\u3068\u30ad\u30e3\u30c3\u30b7\u30e5\u306e\u5897\u52a0\u3001\u5897\u914d\u30fb\u81ea\u793e\u682a\u8cb7\u3044\u306e\u5b9f\u7e3e\u3001PBR\u5bfe\u5fdc\u3092\u8a55\u4fa1\u3057\u307e\u3059",
  formula: "\u914d\u5f53\u6027\u5411(3)\uff0b\u30ad\u30e3\u30c3\u30b7\u30e5\u7a4d\u307f\u4e0a\u304c\u308a(3)\uff0b\u9084\u5143\u65b9\u91dd\u5909\u5316(2)\uff0b\u6771\u8a3cPBR\u5bfe\u5fdc(2)",
  intent: "\u9084\u5143\u4f59\u5730\u304c\u5927\u304d\u3044\u9298\u67c4\u306f\u3001\u4eca\u5f8c\u306e\u914d\u5f53\u5897\u3084\u682a\u4fa1\u4e0a\u6607\u306e\u304d\u3063\u304b\u3051\u306b\u306a\u308a\u307e\u3059",
};

const TOOLTIP_BONUS: TooltipContent = {
  title: "\u30dc\u30fc\u30ca\u30b9\uff08\u6700\u59275\u70b9\uff09",
  desc: "\u55b6\u696dCF3\u671f\u9023\u7d9a\u30d7\u30e9\u30b9\u30013\u671f\u9023\u7d9a\u5897\u914d\u3001\u4e0a\u65b9\u4fee\u6b63\u3001\u9ad8\u914d\u5f53\uff0b\u4f4ePBR\u3001\u8d85\u5272\u5b89\u30b3\u30f3\u30dc\u306e5\u6761\u4ef6\u3067\u52a0\u70b9",
  formula: "\u55b6\u696dCF\u5b89\u5b9a\uff0b\u5897\u914d\uff0b\u4e0a\u65b9\u4fee\u6b63\uff0b\u5272\u5b89\u30b3\u30f3\u30dc\u52a0\u70b9",
  intent: "\u5b9f\u7e3e\u3068\u5b89\u5b9a\u6027\u304c\u78ba\u8a8d\u3067\u304d\u308b\u9298\u67c4\u306b\u8ffd\u52a0\u70b9\u3092\u4e0e\u3048\u307e\u3059",
};

const TOOLTIP_RISK_SCORE: TooltipContent = {
  title: "\u30ea\u30b9\u30af\u6e1b\u70b9\uff08\u6700\u5927\u7d0430\u70b9\uff09",
  desc: "\u8ca1\u52d9\u5065\u5168\u6027\u30fbFCF\u30fb\u6d41\u52d5\u6027\u30fb\u5229\u76ca\u306e\u8cea\u306a\u3069\u3092\u7dcf\u5408\u7684\u306b\u8a55\u4fa1\u3057\u6e1b\u70b9\u3057\u307e\u3059",
  formula: "\u51fa\u6765\u9ad8\u30ea\u30b9\u30af(-3)\uff0b\u4e00\u904e\u6027\u5229\u76ca(-4)\uff0bROE\u4f4e\u4f4d(-2)\uff0b\u81ea\u5df1\u8cc7\u672c(-3)\uff0b\u9577\u671f\u8ca0\u50b5(-4)\uff0bFCF(-4)\uff0b\u8907\u6570\u00d7\u8ffd\u52a0\u30da\u30ca\u30eb\u30c6\u30a3",
  intent: "\u3069\u308c\u3060\u3051\u826f\u3044\u30b9\u30b3\u30a2\u3067\u3082\u30ea\u30b9\u30af\u304c\u9ad8\u3051\u308c\u3070\u6e1b\u70b9\u3002\u5371\u967a\u306a\u9298\u67c4\u3092\u6392\u9664\u3059\u308b\u305f\u3081\u306e\u4ed5\u7d44\u307f",
};
const TOOLTIP_AI_TREND: TooltipContent = {
  title: "AI\u696d\u7e3e\u5206\u6790\uff08\u6700\u592710\u70b9\uff09",
  desc: "AI\u304c\u6c7a\u7b97\u66f8\u3092\u8aad\u307f\u3001\u58f2\u4e0a\u30fb\u5229\u76ca\u306e\u30c8\u30ec\u30f3\u30c9\u3092\u5206\u6790\u3057\u3066\u70b9\u6570\u5316\u3057\u307e\u3059",
  formula: "3\u671f\u9023\u7d9a\u5897\u53ce\u5897\u76ca\u219210\u70b9\u3001\u5897\u53ce or \u5897\u76ca\u21927\u70b9\u3001\u6a2a\u3070\u3044\u21924\u70b9\u3001\u6e1b\u53ce\u6e1b\u76ca\u21920\u70b9",
  intent: "AI\u304c\u5ba2\u89b3\u7684\u306b\u696d\u7e3e\u306e\u6d41\u308c\u3092\u5224\u5b9a\u3057\u307e\u3059",
};
const TOOLTIP_AI_QUALITY: TooltipContent = {
  title: "AI\u7af6\u4e89\u512a\u4f4d\u6027\uff08\u6700\u592710\u70b9\uff09",
  desc: "AI\u304c\u4e8b\u696d\u306e\u7af6\u4e89\u512a\u4f4d\u6027\u30fb\u53c2\u5165\u969c\u58c1\u30fb\u53ce\u76ca\u57fa\u76e4\u306e\u5f37\u3055\u3092\u8a55\u4fa1\u3057\u307e\u3059",
  formula: "\u5f37\u56fa\u306a\u512a\u4f4d\u6027\u219210\u70b9\u3001\u4e00\u5b9a\u306e\u512a\u4f4d\u6027\u21927\u70b9\u3001\u5e73\u5747\u7684\u21924\u70b9\u3001\u61f8\u5ff5\u21920\u70b9",
  intent: "\u4e8b\u696d\u304c\u9577\u671f\u7684\u306b\u7a3c\u304e\u7d9a\u3051\u3089\u308c\u308b\u304b\u3092AI\u304c\u5224\u5b9a\u3057\u307e\u3059",
};

const TOOLTIP_CHEAP_SCORE_FINANCE: TooltipContent = {
  title: "\u5272\u5b89\u5ea6\u30b9\u30b3\u30a2\uff08\u6700\u592735\u70b9\uff09",
  desc: "PBR\u3068PER\u3067\u5272\u5b89\u5ea6\u3092\u8a55\u4fa1\uff08\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u5411\u3051\uff09",
  formula:
    "PBR<0.5=30\u30010.5\u301c0.8=24\u30010.8\u301c1.0=18\u30011.0\u301c1.2=8\u30011.2\u301c1.5=3\u30011.5+=0\u3001PER<8=5\u30018\u301c12=3\u300112\u301c20=1\u300120+=0",
  intent: "\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u306f\u8ca1\u52d9\u69cb\u9020\u304c\u7570\u306a\u308b\u305f\u3081PBR\u3092\u91cd\u8996",
};

const TOOLTIP_GROWTH_SCORE_FINANCE: TooltipContent = {
  title: "\u6210\u9577\u6027\u30b9\u30b3\u30a2\uff08\u6700\u592715\u70b9\uff09",
  desc: "\u6700\u592715\u70b9\uff08\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u306f\u6210\u9577\u6027\u306e\u6bd4\u91cd\u3092\u8efd\u6e1b\uff09",
  formula: "3\u671f\u9023\u7d9a\u5897\u6536(4)\uff0b\u58f2\u4e0a\u6210\u9577\u7387(4)\uff0b3\u671f\u9023\u7d9a\u5897\u76ca(4)\uff0b\u5229\u76ca\u6210\u9577\u7387(3)",
  intent: "\u4e00\u822c\u4e8b\u696d\u30bf\u30d6\u3088\u308a\u6210\u9577\u9805\u76ee\u306e\u6bd4\u91cd\u3092\u4e0b\u3052\u305f\u914d\u70b9",
};

const TOOLTIP_AI_TREND_FINANCE: TooltipContent = {
  title: "AI\u696d\u7e3e\u5206\u6790\uff08\u6700\u592710\u70b9\uff09",
  desc: "\u6700\u592710\u70b9\uff08\u5229\u76ca\u306e\u5b89\u5b9a\u6027\u30fb\u91d1\u5229\u5f71\u97ff\u30fb\u53ce\u76ca\u306e\u8cea\u3092\u91cd\u8996\uff09",
  formula: "AI\u304c\u696d\u7e3e\u30c8\u30ec\u30f3\u30c9\u30920\u301c10\u3067\u8a55\u4fa1",
  intent: "\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u5411\u3051\u306b\u30d7\u30ed\u30f3\u30d7\u30c8\u3092\u5f37\u5316",
};

const TOOLTIP_AI_QUALITY_FINANCE: TooltipContent = {
  title: "AI\u4e8b\u696d\u8a55\u4fa1\uff08\u6700\u592710\u70b9\uff09",
  desc: "\u6700\u592710\u70b9\uff08\u4e8b\u696d\u306e\u7d99\u7d9a\u6027\u30fb\u8cc7\u672c\u653f\u7b56\u30fb\u9084\u5143\u59ff\u52e2\u3092\u91cd\u8996\uff09",
  formula: "AI\u304c\u4e8b\u696d\u8cea\u30920\u301c10\u3067\u8a55\u4fa1",
  intent: "\u7d99\u7d9a\u6027\u30fb\u8fd4\u5143\u30fb\u8cc7\u672c\u653f\u7b56\u306e\u89b3\u70b9\u3092\u91cd\u8996",
};

const TOOLTIP_QUALITY_EARNINGS_FINANCE: TooltipContent = {
  title: "\u8cea\u30fb\u6536\u76ca\u6027\uff08\u6700\u592720\u70b9\uff09",
  desc: "ROE\u30fb\u55b6\u696d\u5229\u76ca\u5b89\u5b9a\u6027\u30fb\u914d\u5f53\u5b89\u5b9a\u6027\u30fb\u81ea\u5df1\u8cc7\u672c\u6bd4\u3067\u8a55\u4fa1",
  formula:
    "ROE5\u70b9+\u5229\u76ca\u5b895+\u914d\u5f535+\u81ea\u5df1\u8cc7\u672c5\u3001\u5897\u914d3\u9023\u7d9a=5\u6e1b\u914d\u306a\u3057=3\u6e1b\u914d=0\u7b49",
  intent: "\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u306e\u8cea\u3068\u53ce\u76ca\u306e\u5b89\u5b9a\u6027",
};

const TOOLTIP_SHAREHOLDER_RETURN_FINANCE: TooltipContent = {
  title: "\u682a\u4e3b\u9084\u5143\uff08\u6700\u592710\u70b9\uff09",
  desc: "\u914d\u5f53\u5229\u56de\u308a\u30fb\u914d\u5f53\u6027\u5411\u30fb\u9084\u5143\u59ff\u52e2\uff08\u5897\u914d\u30fb\u81ea\u793e\u682a\u8cb7\u3044\u7b49\uff09",
  formula: "\u5229\u56de\u308a4+\u6027\u54113+\u59ff\u52e23\u3001\u7121\u914d\u6642\u6027\u5411\u306f0",
  intent: "\u682a\u4e3b\u3078\u306e\u8fd4\u3057\u306e\u5145\u5b9f\u5ea6",
};

const TAB_GENERAL = "\u901a\u5e38\u9298\u67c4";
const TAB_FINANCE = "\u91d1\u878d\u30fb\u4e0d\u52d5\u7523";

const UNLOCK_PASSWORD = "tenbagger2024";
const STORAGE_KEY = "tenbagger_unlocked";
const MAX_SCORE = 100;

// All copy as Unicode escapes (ASCII-safe, no encoding issues)
const TITLE = "\u30c6\u30f3\u30d0\u30fc\u30ac\u30fc\u3092\u72d9\u3046\u5272\u5b89\u5c0f\u578b\u6210\u9577\u682a";
const SUBTITLE = "\u6e05\u539f\u9054\u90ce\u5f0f \u00d7 \u30d0\u30d5\u30a7\u30c3\u30c8\u6d41 \u00d7 AI\u6c7a\u7b97\u5206\u6790 \uff5c \u6bce\u55b6\u696d\u65e5\u66f4\u65b0";
const TAB_SERVICE_ABOUT = "\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306b\u3064\u3044\u3066";
const MODAL_BENEFITS_TITLE = "\u89e3\u653e\u3067\u304d\u308b\u3053\u3068";
const BENEFIT_1 = "\u4e0a\u4f4d1\uff5e10\u4f4d\u306e\u9298\u67c4\u540d\u30fb\u8a3c\u5238\u30b3\u30fc\u30c9";
const BENEFIT_2 = "\u30b9\u30b3\u30a2\u5185\u8a33\u5168\u9805\u76ee\uff08\u5272\u5b89\u5ea6\u30fb\u6210\u9577\u6027\u30fb\u696d\u7e3e\u30fb\u7af6\u4e89\u512a\u4f4d\u6027\u30fb\u682a\u4e3b\u9084\u5143\u30fb\u30ea\u30b9\u30af\uff09";
const BENEFIT_3 = "AI\u306b\u3088\u308b\u6c7a\u7b97\u5206\u6790\u30b3\u30e1\u30f3\u30c8";
const BENEFIT_4 = "\u30d0\u30d5\u30a7\u30c3\u30c8\u6d41\u30ea\u30b9\u30af\u30c1\u30a7\u30c3\u30af\uff886\u9805\u76ee\uff09";
const BENEFIT_5 = "\u8a73\u7d30\u6307\u6a19\u30b0\u30ea\u30c3\u30c9\uff08PER\u30fbROE\u30fbROIC\u30fbPBR\u7b49\uff09";
const CONDITION_TITLE = "\ud83d\udccb \u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0\u6761\u4ef6";
const DIFF_TITLE = "\u306a\u305c\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306f\u4ed6\u3068\u9055\u3046\u306e\u304b\uff1f";
const CATCH_1 = "\u3082\u30571998\u5e74\u3001\u3042\u306a\u305f\u304c\u30e6\u30cb\u30af\u30ed\u682a\u3092\u6301\u3063\u3066\u3044\u305f\u3089\u3002";
const CATCH_2 = "\u4eca\u9803\u3001\u6295\u8cc7\u984d\u306f900\u500d\u306b\u306a\u3063\u3066\u3044\u305f\u3002";
const CATCH_3 = "100\u4e07\u5186\u304c\u2014\u20149\u5104\u5186\u306b\u3002";
const CATCH_4 = "\u30cb\u30c8\u30ea\u3082\u540c\u3058\u3067\u3059\u3002\u4e0a\u5834\u5f53\u6642\u306e\u682a\u4fa1\u306f\u4eca\u306e300\u5206\u306e\u0031\u3002";
const CATCH_5 = "\u306a\u305c\u304b\uff1f\u3000\u5c0f\u3055\u3059\u304e\u3066\u3001\u8ab0\u3082\u898b\u3066\u3044\u306a\u304b\u3063\u305f\u304b\u3089\u3002";
const CATCH_6 = "\u6b21\u306e\u30e6\u30cb\u30af\u30ed\u306f\u3001\u4eca\u3053\u306e\u77ac\u9593\u3082\u6771\u8a3c\u306e\u3069\u3053\u304b\u306b\u3044\u308b\u3002";
const CATCH_7 = "\u6642\u4fa1\u7dcf\u984d30\uff5e500\u5104\u5186\u3002\u6a5f\u95a2\u6295\u8cc7\u5bb6\u304c\u624b\u3092\u51fa\u305b\u306a\u3044\u30b5\u30a4\u30ba\u3002\u3060\u304b\u3089\u5272\u5b89\u306a\u307e\u307e\u653e\u7f6e\u3055\u308c\u3066\u3044\u308b\u3002";
const CATCH_8 = "\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306f\u3001\u305d\u306e\u300c\u307e\u3060\u8ab0\u3082\u6c17\u3065\u3044\u3066\u3044\u306a\u3044\u9298\u67c4\u300d\u3092\u2014\u2014\u4f1d\u8aac\u306e\u6295\u8cc7\u5bb62\u4eba\u306e\u624b\u6cd5\u3068AI\u3092\u4f7f\u3063\u3066\u3001\u6bce\u55b6\u696d\u65e5\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0\u3057\u307e\u3059\u3002";
const FEATURE_TITLE = "\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u3067\u3067\u304d\u308b\u3053\u3068";
const FEATURE_1 = "\u6bce\u55b6\u696d\u65e5\u3001\u6771\u8a3c3\uff0c300\u9298\u67c4\u3092\u81ea\u52d5\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0";
const FEATURE_2 = "\u5272\u5b89\u5ea6\u00d7\u6210\u9577\u6027\u00d7\u682a\u4e3b\u9084\u5143\u3092\u30b9\u30b3\u30a2\u5316\u3057\u3066\u9806\u4f4d\u4ed8\u3051";
const FEATURE_3 = "AI\u304c\u6c7a\u7b97\u66f8\u3092\u8aad\u3093\u3067\u3001\u696d\u7e3e\u30c8\u30ec\u30f3\u30c9\u3092\u89e3\u8aac";
const HOWTO_TITLE = "\u30e9\u30f3\u30ad\u30f3\u30b0\u306e\u898b\u65b9";
const HOWTO_SCORE = "\u30b9\u30b3\u30a2\uff08100\u70b9\u6e80\u70b9\uff09";
const HOWTO_SCORE_DESC = "\u5272\u5b89\u5ea6\u30fb\u6210\u9577\u6027\u30fb\u682a\u4e3b\u9084\u5143\u4f59\u5730\u30fb\u30ea\u30b9\u30af\u6e1b\u70b9\u306e\u5408\u8a08\u3002\u9ad8\u3044\u307b\u3069\u5272\u5b89\u304b\u3064\u512a\u826f\u306a\u9298\u67c4";
const HOWTO_BADGE = "\u8a55\u4fa1\u30d0\u30c3\u30b8\uff08\u25ce\u25cb\u25b3\u00d7\uff09";
const HOWTO_BADGE_DESC = "\u5404\u9805\u76ee\u306e\u5272\u5b89\u5ea6\u30fb\u6210\u9577\u6027\u3092\u76f4\u611f\u7684\u306b\u8868\u793a\u3002\u25ce\uff1d\u512a\u79c0\u3001\u00d7\uff1d\u8981\u6ce8\u610f";
const HOWTO_LOCK = "\u30ed\u30c3\u30af\u89e3\u9664";
const HOWTO_LOCK_DESC =
  "\u4e0a\u4f4d10\u9298\u67c4\u306f\u6709\u6599\u30d7\u30e9\u30f3\u3067\u89e3\u653e\u3055\u308c\u307e\u3059\u3002note\u8a18\u4e8b\u3092\u8cfc\u5165\u3057\u3001\u8a18\u4e8b\u5185\u306e\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u5165\u529b\u3057\u3066\u304f\u3060\u3055\u3044\u3002";
const DIFF_QUOTE = "\u300c\u4e2d\u8eab\u306e\u308f\u304b\u3089\u306a\u3044\u3082\u306e\u306b\u306f\u6295\u8cc7\u3057\u306a\u3044\u300d\u2014 \u30a6\u30a9\u30fc\u30ec\u30f3\u30fb\u30d0\u30d5\u30a7\u30c3\u30c8";
const DIFF_BODY1 = "\u30a4\u30f3\u30d5\u30eb\u30a8\u30f3\u30b5\u30fc\u306e\u6839\u62e0\u306e\u306a\u3044\u9298\u67c4\u63a8\u5968\u3084\u3001\u4e2d\u8eab\u306e\u308f\u304b\u3089\u306a\u3044\u8a3c\u5238\u4f1a\u793e\u304c\u63d0\u6848\u3059\u308b\u30d5\u30a1\u30f3\u30c9\u30fb\u4ed7\u7d44\u307f\u50b5\u306b\u8e0a\u3089\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u304b\uff1f";
const DIFF_BODY2 = "\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306f\u30012\u4eba\u306e\u5049\u5927\u306a\u6295\u8cc7\u5bb6\u306e\u6295\u8cc7\u6cd5\u3092\u3082\u3068\u306b\u3001\u3059\u3079\u3066\u306e\u6839\u62e0\u3092\u30b9\u30b3\u30a2\u3067\u898b\u3048\u308b\u5316\u3057\u3066\u3044\u307e\u3059\u3002";
const DIFF_BODY3 = "\u3042\u306a\u305f\u81ea\u8eab\u304c\u9298\u67c4\u3092\u898b\u6975\u3081\u308b\u76ee\u3092\u990a\u3044\u306a\u304c\u3089\u7b2c\u4e8c\u306e\u30e6\u30cb\u30af\u30ed\u3001\u7b2c\u4e8c\u306e\u30cb\u30c8\u30ea\u3092\u8ab0\u3088\u308a\u3082\u65e9\u304f\u898b\u3064\u3051\u308b\u3053\u3068\u304c\u3067\u304d\u308b\u3002\u305d\u308c\u304c\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306e\u672c\u8cea\u3067\u3059\u3002";
const BADGE_PAID = "\u2705 \u6709\u6599\u30D7\u30E9\u30F3";
const BADGE_MARKET_CAP = "\u6642\u4FA1\u7DCF\u984D 30\u301C500\u5104\u5186";
const BADGE_PER = "PER 10\u500D\u4EE5\u4E0B";
const BADGE_NC = "NC\u6BD4\u7387 1.0\u4EE5\u4E0A";
const BADGE_PROFIT = "\u9ED2\u5B57\u4F01\u696D\u306E\u307F";
const BADGE_EXCLUDE = "\u91D1\u878D\u30FB\u4E0D\u52D5\u7523\u9664\u5916";
const UPDATE_PASSED = "\u901A\u904E\u9298\u67C4";
const UPDATE_COUNT = "\u4EF6";
const UPDATE_SCAN = "\u30B9\u30AD\u30E3\u30F3\u6570";
const UPDATE_MARKETS = "\u9298\u67C4";
const UPDATE_DATE = "\u66F4\u65B0\u65E5";
const MSG_NO_JSON = "screening_result.json \u3092 public \u306B\u914D\u7F6E\u3057\u3066\u304F\u3060\u3055\u3044\u3002";
const MSG_NO_JSON_FINANCE =
  "screening_result_finance.json \u3092 public \u306B\u914D\u7F6E\u3057\u3066\u304F\u3060\u3055\u3044\u3002";
const MSG_LOADING = "\u30C7\u30FC\u30BF\u3092\u8AAD\u307F\u8FBC\u307F\u4E2D...";
const RANK_SUFFIX = "\u4F4D";
const MASK_NAME = "\u2588\u2588\u2588\u2588\u2588\u2588";
const LABEL_OKU = "\u5104\u5186";
const LABEL_NC_RATIO = "NC\u6BD4";
const LABEL_NC = "\u30CD\u30C3\u30C8\u30AD\u30E3\u30C3\u30B7\u30E5\u6BD4\u7387";
const LABEL_MARKETCAP = "\u6642\u4fa1\u7dcf\u984d";
const LABEL_DIVIDEND = "\u914D\u5F53\u5229\u56DE\u308A";
const LABEL_PAYOUT = "\u914D\u5F53\u6027\u5411";
const LABEL_THEORETICAL = "\u7406\u8ad6\u682a\u4fa1";
const LABEL_UPSIDE = "\u4e0a\u6607\u4f59\u5730";
const LABEL_SCORE = "\u30B9\u30B3\u30A2";
const FOOTER_DISCLAIMER = "\u672C\u30B5\u30FC\u30D3\u30B9\u306F\u60C5\u5831\u63D0\u4F9B\u3092\u76EE\u7684\u3068\u3057\u3066\u304A\u308A\u3001\u6295\u8CC7\u52A9\u8A00\u3067\u306F\u3042\u308A\u307E\u305B\u3093\u3002\u6295\u8CC7\u5224\u65AD\u306F\u3054\u81EA\u8EAB\u306E\u8CAC\u4EFB\u3067\u884C\u3063\u3066\u304F\u3060\u3055\u3044\u3002";
const DISCLAIMER_TITLE = "\u514d\u8cac\u4e8b\u9805";
const DISCLAIMER_1 = "\u672c\u30b5\u30fc\u30d3\u30b9\u306f\u60c5\u5831\u63d0\u4f9b\u3092\u76ee\u7684\u3068\u3057\u305f\u3082\u306e\u3067\u3042\u308a\u3001\u6295\u8cc7\u52a9\u8a00\u30fb\u9298\u67c4\u63a8\u5968\u3092\u884c\u3046\u3082\u306e\u3067\u306f\u3042\u308a\u307e\u305b\u3093\u3002";
const DISCLAIMER_2 = "\u8868\u793a\u3055\u308c\u308b\u30b9\u30b3\u30a2\u30fb\u30e9\u30f3\u30ad\u30f3\u30b0\u306f\u30a2\u30eb\u30b4\u30ea\u30ba\u30e0\u304a\u3088\u3073AI\u306b\u3088\u308b\u5206\u6790\u306b\u57fa\u3065\u304f\u3082\u306e\u3067\u3059\u3002\u5c06\u6765\u306e\u682a\u4fa1\u5909\u52d5\u3084\u6295\u8cc7\u6210\u679c\u3092\u4fdd\u8a3c\u3059\u308b\u3082\u306e\u3067\u306f\u3042\u308a\u307e\u305b\u3093\u3002";
const DISCLAIMER_3 = "\u6295\u8cc7\u306b\u306f\u5e38\u306b\u30ea\u30b9\u30af\u304c\u4f34\u3044\u307e\u3059\u3002\u5143\u672c\u640d\u5931\u306e\u53ef\u80fd\u6027\u304c\u3042\u308a\u3001\u6295\u8cc7\u5224\u65ad\u306f\u5fc5\u305a\u3054\u81ea\u8eab\u306e\u8cac\u4efb\u3067\u884c\u3063\u3066\u304f\u3060\u3055\u3044\u3002";
const DISCLAIMER_4 = "\u30b9\u30b3\u30a2\u30ea\u30f3\u30b0\u306b\u306f\u30d0\u30d5\u30a7\u30c3\u30c8\u6c0f\u30fb\u6e05\u539f\u9054\u90ce\u6c0f\u306e\u516c\u958b\u60c5\u5831\u306b\u57fa\u3065\u304f\u6295\u8cc7\u54f2\u5b66\u3092\u53c2\u8003\u306b\u3057\u3066\u3044\u307e\u3059\u304c\u3001\u4e21\u6c0f\u3068\u306f\u7121\u95a2\u4fc2\u3067\u3059\u3002";
const DISCLAIMER_5 =
  "\u672c\u30b5\u30fc\u30d3\u30b9\u306f\u3001\u30c7\u30fc\u30bf\u53d6\u5f97\u5143\u306e\u4ed5\u69d8\u5909\u66f4\u30fb\u30b5\u30fc\u30d3\u30b9\u7d42\u4e86\u306b\u3088\u308a\u3001\u4e88\u544a\u306a\u304f\u505c\u6b62\u30fb\u7d42\u4e86\u3059\u308b\u5834\u5408\u304c\u3042\u308a\u307e\u3059\u3002";
const DISCLAIMER_6 =
  "AI\u306b\u3088\u308b\u5206\u6790\u30b3\u30e1\u30f3\u30c8\u306f\u53c2\u8003\u60c5\u5831\u3067\u3042\u308a\u3001\u8aa4\u308a\u3092\u542b\u3080\u5834\u5408\u304c\u3042\u308a\u307e\u3059\u3002\u6295\u8cc7\u5224\u65ad\u306f\u5fc5\u305a\u3054\u81ea\u8eab\u306e\u8cac\u4efb\u3067\u884c\u3063\u3066\u304f\u3060\u3055\u3044\u3002";
const BTN_NOTE = "note\u3067\u8CFC\u5165\u3059\u308B";
const BTN_NOTE_PURCHASE = "\uD83D\uDCDD note\u3067\u8cfc\u5165\u3059\u308b \u2192";
const NOTE_URL = "https://note.com/dreamy_okapi3047/n/n0fafb7449d15";
const PLACEHOLDER_PASSWORD = "\u30D1\u30B9\u30EF\u30FC\u30C9";
const ERROR_PASSWORD = "\u30D1\u30B9\u30EF\u30FC\u30C9\u304C\u9055\u3044\u307E\u3059";
const BTN_UNLOCK_SUBMIT = "\u89E3\u653E\u3059\u308B";
const BTN_CANCEL = "\u30AD\u30E3\u30F3\u30BB\u30EB";
const SEP_LINE = "\uFF5C";

// ?????????????????????????????????
const MODAL_UNLOCK_TITLE = (lockCount: number) =>
  `\uD83D\uDD13 1\u301C${lockCount}\u4F4D\u3092\u89E3\u653E\u3059\u308B`;
const MODAL_UNLOCK_DESC = (lockCount: number) =>
  `note\u306e\u6709\u6599\u8a18\u4e8b\u306b\u8a18\u8f09\u306e\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u5165\u529b\u3059\u308b\u3068 1\u301c${lockCount}\u4f4d\u306e\u9298\u67c4\u540d\u304c\u8868\u793a\u3055\u308c\u307e\u3059`;

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
const PITCH_DESCRIPTION = "\u500B\u4EBA\u8CC7\u7523900\u5104\u5186\u8D85\u306E\u4F1D\u8AAC\u306E\u6295\u8CC7\u5BB6\u30FB\u6E05\u539F\u9054\u90CE\u306E\u6295\u8CC7\u6CD5\u3068\u3001\u500B\u4EBA\u8CC7\u7523\u7D0424\u5146\u5186\u30FB\u6295\u8CC7\u306E\u795E\u69D8\u30A6\u30A9\u30FC\u30EC\u30F3\u30FB\u30D0\u30D5\u30A7\u30C3\u30C8\u306E\u30CF\u30A4\u30D6\u30EA\u30C3\u30C9\u300C\u30CD\u30C3\u30C8\u30AD\u30E3\u30C3\u30B7\u30E5\u6BD4\u7387\u00D7\u30D0\u30EA\u30E5\u30FC\u6295\u8CC7\u300D\u306B\u6C7A\u7B97\u66F8\u3092\u8AAD\u307F\u8FBC\u307E\u305B\u30B9\u30B3\u30A2\u30EA\u30F3\u30B0\u3057\u305F\u552F\u4E00\u7121\u4E8C\u306E\u30B9\u30AF\u30EA\u30FC\u30CB\u30F3\u30B0\u30B5\u30FC\u30D3\u30B9";

const PITCH_ABOUT_TOGGLE = "\u3053\u306E\u30B5\u30FC\u30D3\u30B9\u306B\u3064\u3044\u3066";
const BTN_DETAIL_OPEN = "\u25BC \u8A73\u7D30\u3092\u898B\u308B";
const BTN_DETAIL_CLOSE = "\u25B2 \u9589\u3058\u308B";
const LABEL_SCORE_BREAKDOWN = "\u30B9\u30B3\u30A2\u5185\u8A33";
const LABEL_CHEAP = "\u5272\u5B89\u5EA6";
const LABEL_CHEAP_SHORT = "\u5272\u5B89";
const LABEL_GROWTH = "\u6210\u9577\u6027";
const LABEL_GROWTH_SHORT = "\u6210\u9577";
const LABEL_QUALITY_DETAIL = "\u53CE\u76CA\u6027";
const LABEL_BONUS = "\u30DC\u30FC\u30CA\u30B9";
const LABEL_SHAREHOLDER = "\u682A\u4E3B\u9084\u5143\u4F59\u5730";
const LABEL_QUALITY_EARNINGS_FINANCE = "\u8cea\u30fb\u6536\u76ca\u6027";
const LABEL_SHAREHOLDER_RETURN_FINANCE = "\u682a\u4e3b\u9084\u5143\u4f59\u5730";
const LABEL_AI_TREND = "AI\u696d\u7e3e\u5206\u6790";
const LABEL_AI_QUALITY = "AI\u7af6\u4e89\u512a\u4f4d\u6027";
const LABEL_RISK = "\u30EA\u30B9\u30AF\u51CF\u70B9";
const LABEL_METRICS = "\u6307\u6A19\u30B0\u30EA\u30C3\u30C9";
const LABEL_AI_ANALYSIS = "AI\u5206\u6790\u30B3\u30E1\u30F3\u30C8";
const MSG_AI_PLACEHOLDER = "AI\u5206\u6790\u306F\u6B21\u56DE\u56DB\u534A\u671F\u66F4\u65B0\u6642\u306B\u8FFD\u52A0\u4E88\u5B9A\u3067\u3059";
const LABEL_RISK_CHECK = "\u30EA\u30B9\u30AF\u30C1\u30A7\u30C3\u30AF\uff08\u30D0\u30D5\u30A7\u30C3\u30C8\u6D41\uff09";
const LABEL_RISK_CHECK_FINANCE =
  "\u30ea\u30b9\u30af\u30c1\u30a7\u30c3\u30af\uff08\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u5411\u3051\uff09";
const LABEL_EQUITY_RATIO = "\u81ea\u5df1\u8cc7\u672c\u6bd4\u7387";
const RISK_CHECK_ITEMS: { key: keyof NonNullable<Row["risk_checks"]>; label: string; inverted: boolean }[] = [
  { key: "roe_15_percent", label: "ROE 15%\u4EE5\u4E0A\u306E\u7D9A\u7D9A", inverted: false },
  { key: "equity_ratio_50_percent", label: "\u81EA\u5DF1\u8CC7\u672C\u6BD4\u7387 50%\u4EE5\u4E0A", inverted: false },
  { key: "debt_to_profit_5x", label: "\u9577\u671F\u8CA0\u50B5/\u7D14\u5229\u76CA 5\u500D\u4EE5\u5185", inverted: false },
  { key: "fcf_stability", label: "FCF\u306E\u5B89\u5B9A\u6027", inverted: false },
  { key: "liquidity_risk", label: "\u51fa\u6765\u9ad8\uff08\u6d41\u52d5\u6027\uff09", inverted: true },
  { key: "one_time_profit_risk", label: "\u4E00\u904E\u6027\u5229\u76CA\u30EA\u30B9\u30AF", inverted: true },
];

const RISK_CHECK_TOOLTIPS: Record<string, TooltipContent> = {
  roe_15_percent: {
    title: "ROE 15\uff05\u4ee5\u4e0a\u306e\u7d99\u7d9a",
    desc: "\u682a\u4e3b\u306e\u304a\u91d1\u3092\u4f7f\u3063\u3066\u3069\u308c\u3060\u3051\u52b9\u7387\u3088\u304f\u5229\u76ca\u3092\u51fa\u305b\u308b\u304b\u3002\u30d0\u30d5\u30a7\u30c3\u30c8\u304c\u91cd\u8996\u3059\u308b\u512a\u826f\u4f01\u696d\u306e\u57fa\u6e96",
    formula: "",
    intent: "15\uff05\u4ee5\u4e0a\u304c\u7d99\u7d9a\u3057\u3066\u3044\u308b\u4f01\u696d\u306f\u7af6\u4e89\u512a\u4f4d\u6027\u304c\u9ad8\u3044\u8a3c\u62e0",
  },
  equity_ratio_50_percent: {
    title: "\u81ea\u5df1\u8cc7\u672c\u6bd4\u7387",
    desc: "\u4f1a\u793e\u306e\u8cc7\u91d1\u306e\u3046\u3061\u3001\u501f\u91d1\u306b\u983c\u3089\u306a\u3044\u81ea\u5df1\u8cc7\u91d1\u306e\u5272\u5408\u3002\u9ad8\u3044\u307b\u3069\u8ca1\u52d9\u304c\u5065\u5168",
    formula: "",
    intent: "50\uff05\u4ee5\u4e0a\u3067\u8ca1\u52d9\u5065\u5168\u3002\u30d0\u30d5\u30a7\u30c3\u30c8\u306f\u7121\u501f\u91d1\u307e\u305f\u306f\u4f4e\u500d\u50b5\u306e\u4f01\u696d\u3092\u597d\u3080",
  },
  debt_to_profit_5x: {
    title: "\u9577\u671f\u8ca0\u50b5\u30fb\u7d14\u5229\u76ca\u6bd4\u7387",
    desc: "\u9577\u671f\u501f\u91d1\u304c\u5e74\u9593\u7d14\u5229\u76ca\u306e\u4f55\u5e74\u5206\u304b\u3092\u793a\u3059\u3002\u5c0f\u3055\u3044\u307b\u3069\u50b5\u52d9\u8fd4\u6e08\u80fd\u529b\u304c\u9ad8\u3044",
    formula: "",
    intent: "5\u500d\u4ee5\u5185\u306a\u3089\u8ca1\u52d9\u30ea\u30b9\u30af\u304c\u4f4e\u3044\u3002\u30d0\u30d5\u30a7\u30c3\u30c8\u306f5\u5e74\u4ee5\u5185\u306b\u8fd4\u6e08\u3067\u304d\u308b\u8ca0\u50b5\u3092\u597d\u3080",
  },
  fcf_stability: {
    title: "FCF\uff08\u30d5\u30ea\u30fc\u30ad\u30e3\u30c3\u30b7\u30e5\u30d5\u30ed\u30fc\uff09",
    desc: "\u4e8b\u696d\u3067\u7a3c\u3044\u3060\u73fe\u91d1\u304b\u3089\u8a2d\u5099\u6295\u8cc7\u3092\u5f15\u3044\u305f\u300c\u672c\u5f53\u306e\u5229\u76ca\u300d\u3002\u30d7\u30e9\u30b9\u3067\u7d9a\u3051\u3070\u81ea\u7136\u306b\u73fe\u91d1\u304c\u6e9c\u307e\u308b",
    formula: "",
    intent: "\u30d7\u30e9\u30b9\u304c\u7d9a\u3044\u3066\u3044\u308b\u4f01\u696d\u306f\u914d\u5f53\u30fb\u81ea\u793e\u682a\u8cb7\u3044\u306e\u4f59\u5730\u304c\u3042\u308a\u3001\u8ca1\u52d9\u5065\u5168\u306e\u8a3c\u62e0",
  },
  liquidity_risk: {
    title: "\u51fa\u6765\u9ad8\uff08\u6d41\u52d5\u6027\u30ea\u30b9\u30af\uff09",
    desc: "1\u65e5\u306b\u4f55\u5186\u5206\u306e\u682a\u304c\u58f2\u8cb7\u3055\u308c\u3066\u3044\u308b\u304b\u3002\u5c11\u306a\u3044\u3068\u3001\u58f2\u308a\u305f\u3044\u6642\u306b\u58f2\u308c\u306a\u3044\u30ea\u30b9\u30af\u304c\u3042\u308b",
    formula: "",
    intent: "20\u65e5\u5e73\u5747\u58f2\u8cb7\u4ee3\u91d15000\u4e07\u5186\u672a\u6e80\u306e\u9298\u67c4\u306f\u6d41\u52d5\u6027\u30ea\u30b9\u30af\u3042\u308a\u3068\u5224\u5b9a",
  },
  one_time_profit_risk: {
    title: "\u4e00\u904e\u6027\u5229\u76ca\u30ea\u30b9\u30af",
    desc: "\u571f\u5730\u58f2\u5374\u30fb\u4fdd\u967a\u91d1\u53d7\u53d6\u306a\u3069\u3001\u672c\u696d\u3068\u7121\u95a2\u4fc2\u306a\u4e00\u6642\u7684\u306a\u5229\u76ca\u304c\u5897\u76ca\u306b\u898b\u305b\u304b\u3051\u3066\u3044\u308b\u30b1\u30fc\u30b9",
    formula: "",
    intent: "\u55b6\u696d\u5229\u76ca\u3068\u7d14\u5229\u76ca\u306e\u5dee\u304c\u5927\u304d\u3044\u5834\u5408\u3001\u4e00\u904e\u6027\u5229\u76ca\u306b\u4f9d\u5b58\u3057\u3066\u3044\u308b\u53ef\u80fd\u6027\u304c\u9ad8\u3044",
  },
};

const RISK_CHECK_ITEMS_FINANCE: { key: string; label: string; inverted: boolean }[] = [
  { key: "roe_15_percent", label: "ROE 10%\u4ee5\u4e0a\u306e\u7d99\u7d9a", inverted: false },
  { key: "profit_stability", label: "\u5229\u76ca\u306e\u5b89\u5b9a\u6027", inverted: false },
  { key: "dividend_stability", label: "\u914d\u5f53\u306e\u5b89\u5b9a\u6027", inverted: false },
  { key: "one_time_profit_risk", label: "\u4e00\u904e\u6027\u5229\u76ca\u4f9d\u5b58", inverted: true },
  { key: "liquidity_risk", label: "\u51fa\u6765\u9ad8\uff08\u6d41\u52d5\u6027\uff09", inverted: true },
  { key: "financial_health", label: "\u8ca1\u52d9\u5065\u5168\u6027", inverted: false },
];

const RISK_CHECK_TOOLTIPS_FINANCE: Record<string, TooltipContent> = {
  roe_15_percent: {
    title: "ROE 10\uff05\u4ee5\u4e0a\u306e\u7d99\u7d9a",
    desc: "\u91d1\u878d\u30bf\u30d6\u7528\u3002ROE10\uff05\u4ee5\u4e0a\u304c\u7d99\u7d9a\u3059\u308b\u304b",
    formula: "",
    intent: "",
  },
  profit_stability: {
    title: "\u5229\u76ca\u306e\u5b89\u5b9a\u6027",
    desc: "\u6700\u65b03\u671f\u306e\u55b6\u696d\u5229\u76ca\u304c\u3059\u3079\u3066\u30d7\u30e9\u30b9\u304b",
    formula: "",
    intent: "",
  },
  dividend_stability: {
    title: "\u914d\u5f53\u306e\u5b89\u5b9a\u6027",
    desc: "\u5e74\u9593\u914d\u5f53\u306e\u6700\u65b0\u5e74\u304c\u524d\u5e74\u672a\u6e80\u306b\u6e1b\u914d\u3057\u3066\u3044\u306a\u3044\u304b\uff08\u53d6\u5f97\u4e0d\u53ef\u6642\u306f\u8981\u6ce8\u610f\u5916\uff09",
    formula: "",
    intent: "",
  },
  one_time_profit_risk: {
    title: "\u4e00\u904e\u6027\u5229\u76ca\u4f9d\u5b58",
    desc: "\u55b6\u696d\u5229\u76ca\u3068\u7d20\u5229\u76ca\u306e\u5dee\uff08\u5f62\u614b\u7387\uff09\u304c50\uff05\u672a\u6e80\u3067\u3001\u4e00\u904e\u6027\u5229\u76ca\u4f9d\u5b58\u3067\u306a\u3044\u304b",
    formula: "",
    intent: "",
  },
  liquidity_risk: RISK_CHECK_TOOLTIPS.liquidity_risk,
  financial_health: {
    title: "\u8ca1\u52d9\u5065\u5168\u6027",
    desc: "\u81ea\u5df1\u8cc7\u672c\u6bd4\u73875\uff05\u4ee5\u4e0a\uff08\u9280\u884c8\uff05\u7406\u60f3\u3092\u53c2\u8003\u3057\u4e0d\u52d5\u7523\u542b\u30815\uff05\u7de9\u548c\uff09",
    formula: "\u81ea\u5df1\u8cc7\u672c \u00f7 \u7dcf\u8cc7\u7523 \u00d7 100",
    intent: "",
  },
};
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
  website?: string;
  market?: string | null;
  score: number;
  net_cash_ratio: number;
  per: number;
  market_cap_oku: number;
  dividend_yield?: number | null;
  valuation_score?: number;
  growth_score?: number;
  quality_score_detail?: number;
  shareholder_score?: number;
  trend_score?: number;
  quality_score?: number;
  bonus_score?: number;
  risk_penalty?: number;
  chart_signals?: {
    volume_surge?: boolean;
    above_ma?: boolean;
    near_high?: boolean;
  };
  payout_ratio?: number | null;
  roe?: number | null;
  roic?: number | null;
  pbr?: number | null;
  equity_ratio?: number | null;
  ai_comment?: string;
  risk_checks?: {
    roe_15_percent?: boolean;
    equity_ratio_50_percent?: boolean;
    debt_to_profit_5x?: boolean;
    fcf_stability?: boolean;
    liquidity_risk?: boolean;
    one_time_profit_risk?: boolean;
    profit_stability?: boolean;
    dividend_stability?: boolean;
    financial_health?: boolean;
    capital_adequacy?: boolean;
    revenue_diversity?: boolean;
  } | null;
  tab?: "general" | "finance";
  tenbagger_stars?: number;
  theoretical_price?: number;
  upside_percent?: number;
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

function getGradeFromAIScore(s: number): GradeKey {
  if (s >= 8) return "excellent";
  if (s >= 5) return "good";
  if (s >= 2) return "fair";
  return "poor";
}

function getFinanceValuationBadge(v: number): GradeKey {
  if (v >= 28) return "excellent";
  if (v >= 20) return "good";
  if (v >= 12) return "fair";
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

function formatDate(iso: string): string {
  if (!iso) return "\u2014";
  const d = new Date(iso);
  return `${d.getFullYear()}\u5e74${d.getMonth() + 1}\u6708${d.getDate()}\u65e5`;
}

function formatTenbaggerExpectLabel(n: number): string | null {
  if (n < 2 || n > 5) return null;
  const fire = "\uD83D\uDD25";
  const label = "\u5927\u5316\u3051\u671f\u5f85";
  const star = "\u2605";
  return fire + label + star.repeat(n);
}

function getStockTag(r: Row, isFinanceTab: boolean): string {
  const tags: string[] = [];
  if (isFinanceTab) {
    const pb = r.pbr;
    if (pb != null && pb <= 0.5) tags.push("\u8d85\u4f4ePBR");
    else if (pb != null && pb <= 1.0) tags.push("\u4f4ePBR");
    if (r.per <= 8) tags.push("\u4f4ePER");
    else if (r.per <= 12) tags.push("PER\u901a\u5e38");
  } else {
    if (r.net_cash_ratio >= 1.5) tags.push("\u9ad8NC");
    else if (r.net_cash_ratio >= 1.0) tags.push("NC\u5272\u5b89");
    if (r.per <= 5) tags.push("\u8d85\u4f4e\u500d");
    else if (r.per <= 8) tags.push("\u4f4e\u500d");
  }
  if ((r.roe ?? 0) >= 15) tags.push("ROE\u512a\u79c0");
  const trendTh = isFinanceTab ? 10 : 8;
  if ((r.trend_score ?? 0) >= trendTh) tags.push("\u696d\u7e3e\u5897\u52a0");
  if ((r.shareholder_score ?? 0) >= 12) tags.push("\u9084\u5143\u4f59\u5730\u5927");
  if ((r.dividend_yield ?? 0) >= 3.5) tags.push("\uD83D\uDCB0\u9AD8\u914D\u5F53");
  if (r.chart_signals?.volume_surge) tags.push("\uD83D\uDCCA\u51fa\u6765\u9ad8\u6025\u5897");
  if (r.chart_signals?.above_ma) tags.push("\u2b06\ufe0fMA\u4e0a\u629c\u3051");
  if (r.chart_signals?.near_high) tags.push("\uD83C\uDFAF\u65b0\u9ad8\u5024\u63a5\u8fd1");
  return tags.slice(0, 6).join(" \u30fb ");
}

export default function Home() {
  const [loading, setLoading] = useState(true);
  const [rows, setRows] = useState<Row[]>([]);
  const [updatedAt, setUpdatedAt] = useState("");
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [expandedCode, setExpandedCode] = useState<string | null>(null);
  const [screeningTab, setScreeningTab] = useState<"general" | "finance">("general");

  useEffect(() => {
    setExpandedCode(null);
  }, [screeningTab]);

  useEffect(() => {
    setLoading(true);
    const url =
      screeningTab === "finance" ? "/screening_result_finance.json" : "/screening_result.json";
    fetch(url)
      .then((res) => {
        if (!res.ok) {
          setRows([]);
          setUpdatedAt("");
          return Promise.resolve(null);
        }
        return res.json();
      })
      .then((d: unknown) => {
        if (d === null) return;
        if (Array.isArray(d)) {
          setRows(d);
          setUpdatedAt("");
        } else if (d !== null && typeof d === "object") {
          const o = d as { stocks?: unknown; updated_at?: unknown };
          setRows(Array.isArray(o.stocks) ? o.stocks : []);
          setUpdatedAt(typeof o.updated_at === "string" ? o.updated_at : "");
        } else {
          setRows([]);
          setUpdatedAt("");
        }
      })
      .catch(() => {
        setRows([]);
        setUpdatedAt("");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [screeningTab]);

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
    <>
      <main className="min-h-screen bg-[#f9f7f4] text-[#1a1a1a]">
        <header className="sticky top-0 z-40 border-b border-[#e5e0d8] bg-white backdrop-blur">
        <div className="max-w-4xl mx-auto flex flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:gap-3">
          <div className="min-w-0">
            <h1 className="text-lg font-bold tracking-tight text-[#1a1a1a] sm:text-xl">
              {TITLE}
            </h1>
            <p className="mt-0.5 text-[11px] leading-snug text-[#6b6b6b] sm:text-xs">{SUBTITLE}</p>
          </div>
          <div className="flex w-full shrink-0 flex-row items-center justify-center gap-2 sm:w-auto sm:justify-end">
            <button
              type="button"
              onClick={() => window.location.reload()}
              className="text-gray-500 hover:text-gray-700 text-lg p-1 cursor-pointer"
              title={"\u30c7\u30fc\u30bf\u3092\u66f4\u65b0"}
            >
              {"\ud83d\udd04"}
            </button>
            {isUnlocked ? (
              <span className="inline-flex min-w-0 flex-1 items-center justify-center gap-1.5 rounded-lg bg-[#f0ece6] px-3 py-2 text-sm text-[#16a34a] sm:flex-initial sm:justify-start sm:py-1.5">
                {BADGE_PAID}
              </span>
            ) : (
              <button
                type="button"
                onClick={openModal}
                className="inline-flex min-w-0 flex-1 items-center justify-center gap-1.5 rounded-lg bg-[#1a1a1a] px-3 py-2 text-xs font-medium text-white transition-colors hover:opacity-90 sm:flex-initial sm:py-1.5 sm:text-sm"
              >
                {`\uD83D\uDD13 \u4e0a\u4f4d${lockCount}\u4f4d\u3092\u89e3\u653e`}
              </button>
            )}
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-center gap-2 mb-4 flex-wrap">
            <button
              type="button"
              onClick={() => setScreeningTab("general")}
              className={
                screeningTab === "general"
                  ? "bg-[#d97706] text-white font-bold rounded-full px-4 py-2 text-sm"
                  : "bg-[#f5f0e8] text-[#6b6b6b] rounded-full px-4 py-2 text-sm"
              }
            >
              {TAB_GENERAL}
            </button>
            <button
              type="button"
              onClick={() => setScreeningTab("finance")}
              className={
                screeningTab === "finance"
                  ? "bg-[#d97706] text-white font-bold rounded-full px-4 py-2 text-sm"
                  : "bg-[#f5f0e8] text-[#6b6b6b] rounded-full px-4 py-2 text-sm"
              }
            >
              {TAB_FINANCE}
            </button>
            <a
              href="/about"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center bg-[#f5f0e8] text-[#6b6b6b] rounded-full px-4 py-2 text-sm hover:bg-[#ebe5db]"
            >
              {TAB_SERVICE_ABOUT}
            </a>
          </div>
        </div>
        </header>

        <div className="max-w-4xl mx-auto px-3 py-6 sm:px-4 sm:py-8">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div
              className="h-8 w-8 animate-spin rounded-full border-b-2 border-[#d97706]"
              aria-hidden
            />
            <span className="ml-3 text-sm text-[#d97706] sm:text-base">{MSG_LOADING}</span>
          </div>
        ) : rows.length === 0 ? (
          <p className="py-8 text-sm text-[#6b6b6b]">
            {screeningTab === "finance" ? MSG_NO_JSON_FINANCE : MSG_NO_JSON}
          </p>
        ) : (
          <>
        <p className="mb-4 text-[11px] text-[#6b6b6b] sm:text-xs">
          {UPDATE_PASSED} {rows.length} {UPDATE_COUNT} {SEP_LINE} {UPDATE_SCAN} 3,327 {UPDATE_MARKETS} {SEP_LINE} {UPDATE_DATE}: {formatDate(updatedAt)}
        </p>

        <div className="space-y-3">
          {rows.map((r, i) => {
              const isFinance = screeningTab === "finance";
              const maxCheap = isFinance ? 35 : 30;
              const maxGrowth = 20;
              const maxAi = 10;
              const maxQualityDetail = isFinance ? 20 : 15;
              const valuationScore = isFinance
                ? (r.valuation_score ?? 0)
                : (r.valuation_score ?? getCheapScore(r.net_cash_ratio, r.per));
              const cheapBadge = isFinance
                ? getFinanceValuationBadge(r.valuation_score ?? 0)
                : getCheapBadge(valuationScore);
              const growthScore = r.growth_score ?? (r.score - valuationScore);
              const growthBadge = isFinance
                ? "fair"
                : r.growth_score != null
                  ? getGradeFromGrowthScore(r.growth_score)
                  : getGrowthBadge(r.score, valuationScore);
              const tipCheap = isFinance ? TOOLTIP_CHEAP_SCORE_FINANCE : TOOLTIP_CHEAP_SCORE;
              const tipGrowth = isFinance ? TOOLTIP_GROWTH_SCORE_FINANCE : TOOLTIP_GROWTH_SCORE;
              const tipAiTrend = isFinance ? TOOLTIP_AI_TREND_FINANCE : TOOLTIP_AI_TREND;
              const tipAiQuality = isFinance ? TOOLTIP_AI_QUALITY_FINANCE : TOOLTIP_AI_QUALITY;
              const tipQualityBreakdown = isFinance
                ? TOOLTIP_QUALITY_EARNINGS_FINANCE
                : TOOLTIP_QUALITY_DETAIL;
              const labelQualityBreakdown = isFinance ? LABEL_QUALITY_EARNINGS_FINANCE : LABEL_QUALITY_DETAIL;
              const tipShareholderBreakdown = isFinance
                ? TOOLTIP_SHAREHOLDER_RETURN_FINANCE
                : TOOLTIP_SHAREHOLDER_SCORE;
              const labelShareholderBreakdown = isFinance
                ? LABEL_SHAREHOLDER_RETURN_FINANCE
                : LABEL_SHAREHOLDER;
              const isExpanded = expandedCode === r.code;
              return (
                <div
                  key={r.code}
                  id={`stock-${i}`}
                  style={{ scrollMarginTop: "120px" }}
                  className="rounded-xl border border-[#e5e0d8] bg-white p-3 shadow-sm transition-shadow hover:shadow-md sm:p-4"
                >
                  <div className="flex flex-col items-stretch justify-between gap-3 sm:flex-row sm:flex-wrap sm:items-start">
                    <div className="flex min-w-0 items-center gap-2 sm:gap-3">
                      <span className={`shrink-0 text-base sm:text-lg ${rankStyle(i)}`}>
                        {i + 1}{RANK_SUFFIX}
                      </span>
                      <div className="min-w-0">
                        <div className="truncate text-sm font-medium text-[#1a1a1a] sm:text-base">
                          {i < lockCount && !isUnlocked ? MASK_NAME : displayName(r)}
                        </div>
                        {!(i < lockCount && !isUnlocked) && (() => {
                          const tagLine = getStockTag(r, isFinance);
                          const tenbaggerLabel =
                            !isFinance && (r.tenbagger_stars ?? 0) >= 2
                              ? formatTenbaggerExpectLabel(r.tenbagger_stars ?? 0)
                              : null;
                          return (
                            <>
                              <div className="mt-1 flex flex-wrap items-center gap-x-2 gap-y-1">
                                {tagLine ? (
                                  <span className="text-xs text-[#92400e] bg-[#fef3c7] px-2 py-0.5 rounded-full inline-block">
                                    {tagLine}
                                  </span>
                                ) : null}
                                {tenbaggerLabel ? (
                                  <span className="text-sm font-bold text-orange-600 ml-2">
                                    {tenbaggerLabel}
                                  </span>
                                ) : null}
                              </div>
                              <div className="mt-0.5 flex flex-wrap items-center gap-2 text-xs text-[#6b6b6b] sm:text-sm">
                                <Link
                                  href={`https://finance.yahoo.co.jp/quote/${r.code}.T`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="font-mono text-[#2563eb] hover:underline"
                                >
                                  {r.code}
                                </Link>
                                {(r.market ?? "").trim()
                                  ? ` \u30fb ${(r.market ?? "").trim()}`
                                  : ""}
                                {(isUnlocked || i >= lockCount) && r.website ? (
                                  <a
                                    href={r.website}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-sm transition-opacity hover:opacity-70"
                                    title={r.website}
                                  >
                                    {"\uD83C\uDF10"}
                                  </a>
                                ) : null}
                              </div>
                            </>
                          );
                        })()}
                      </div>
                    </div>
                    <div className="w-full shrink-0 sm:flex sm:w-auto sm:flex-wrap sm:items-center sm:gap-3">
                      <div className="grid grid-cols-2 gap-x-2 gap-y-2 text-[11px] leading-tight sm:contents sm:text-sm sm:leading-normal">
                        <span className="inline-flex min-w-0 items-center gap-0.5 text-[#1a1a1a]">
                          {r.market_cap_oku} {LABEL_OKU}
                          <IndicatorTooltip content={TOOLTIP_MARKETCAP} />
                        </span>
                        <span className="inline-flex min-w-0 items-center gap-0.5 text-[#2563eb]">
                          PER {r.per}
                          <IndicatorTooltip content={TOOLTIP_PER} />
                        </span>
                        <span className="inline-flex min-w-0 items-center gap-0.5 text-[#16a34a]">
                          {isFinance ? (
                            <>
                              PBR{" "}
                              {r.pbr != null && r.pbr !== undefined
                                ? `${r.pbr}${PITCH_TIMES}`
                                : DASH}
                              <IndicatorTooltip content={TOOLTIP_PBR} />
                            </>
                          ) : (
                            <>
                              {LABEL_NC_RATIO} {r.net_cash_ratio.toFixed(2)}
                              <IndicatorTooltip content={TOOLTIP_NC} />
                            </>
                          )}
                        </span>
                        {r.dividend_yield != null && r.dividend_yield !== undefined && (
                          <span className="inline-flex min-w-0 items-center gap-0.5 text-yellow-600">
                            {LABEL_DIVIDEND} {r.dividend_yield}%
                            <IndicatorTooltip content={TOOLTIP_DIVIDEND} />
                          </span>
                        )}
                      </div>
                      <div className="mt-2 flex flex-wrap items-center gap-2 sm:mt-0 sm:justify-end">
                        <span className="inline-flex items-center gap-1">
                          <span className="text-[10px] text-gray-400 sm:text-xs">{LABEL_CHEAP_SHORT}</span>
                          <span className={`rounded px-1.5 py-0.5 text-[10px] font-medium sm:text-xs ${getBadgeClass(cheapBadge)}`} title={LABEL_CHEAP}>
                            {GRADE_LABELS[cheapBadge]}
                          </span>
                        </span>
                        {!isFinance ? (
                          <span className="inline-flex items-center gap-1">
                            <span className="text-[10px] text-gray-400 sm:text-xs">{LABEL_GROWTH_SHORT}</span>
                            <span
                              className={`rounded px-1.5 py-0.5 text-[10px] font-medium sm:text-xs ${getBadgeClass(growthBadge)}`}
                              title={LABEL_GROWTH}
                            >
                              {GRADE_LABELS[growthBadge]}
                            </span>
                          </span>
                        ) : null}
                      </div>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center gap-2 sm:gap-3">
                    <span className="text-xs text-[#6b6b6b] sm:text-sm">{LABEL_SCORE}</span>
                    <div className="flex-1 h-2 rounded-full bg-[#e5e0d8] overflow-hidden max-w-[200px]">
                      <div
                        className="h-full rounded-full bg-[#d97706] transition-all"
                        style={{
                          width: `${Math.min(100, (r.score / MAX_SCORE) * 100)}%`,
                        }}
                      />
                    </div>
                    <span className="tabular-nums text-sm font-medium text-[#d97706] sm:text-base">
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
                        const willExpand = !isExpanded;
                        setExpandedCode(isExpanded ? null : r.code);
                        if (willExpand) {
                          const el = document.getElementById(`stock-${i}`);
                          if (el) {
                            setTimeout(() => {
                              el.scrollIntoView({
                                behavior: "smooth",
                                block: "start",
                              });
                            }, 100);
                          }
                        }
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
                              <IndicatorTooltip content={tipCheap} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div
                                className="h-full rounded-full bg-emerald-500"
                                style={{
                                  width: `${Math.min(100, ((r.valuation_score ?? valuationScore) / maxCheap) * 100)}%`,
                                }}
                              />
                            </div>
                            <span className="text-xs tabular-nums w-12 shrink-0">
                              {(r.valuation_score ?? valuationScore)}/{maxCheap}
                            </span>
                          </div>

                          {!isFinance ? (
                            <div className="flex items-center gap-2">
                              <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                                {LABEL_GROWTH}
                                <IndicatorTooltip content={tipGrowth} />
                              </span>
                              <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                                <div
                                  className="h-full rounded-full bg-blue-500"
                                  style={{
                                    width: `${Math.min(100, ((r.growth_score ?? growthScore) / maxGrowth) * 100)}%`,
                                  }}
                                />
                              </div>
                              <span className="text-xs tabular-nums w-12 shrink-0">
                                {(r.growth_score ?? growthScore)}/{maxGrowth}
                              </span>
                            </div>
                          ) : null}

                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {labelQualityBreakdown}
                              <IndicatorTooltip content={tipQualityBreakdown} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div
                                className="h-full rounded-full bg-cyan-500"
                                style={{
                                  width: `${Math.min(
                                    100,
                                    ((r.quality_score_detail ?? 0) / maxQualityDetail) * 100,
                                  )}%`,
                                }}
                              />
                            </div>
                            <span className="text-xs tabular-nums w-10">
                              {r.quality_score_detail ?? 0}/{maxQualityDetail}
                            </span>
                          </div>

                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {LABEL_AI_TREND}
                              <IndicatorTooltip content={tipAiTrend} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div
                                className="h-full rounded-full bg-purple-400"
                                style={{
                                  width: `${Math.min(100, ((r.trend_score ?? 0) / maxAi) * 100)}%`,
                                }}
                              />
                            </div>
                            <span className="text-xs tabular-nums w-12 shrink-0">
                              {(r.trend_score ?? 0)}/{maxAi}
                            </span>
                          </div>

                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {LABEL_AI_QUALITY}
                              <IndicatorTooltip content={tipAiQuality} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div
                                className="h-full rounded-full bg-indigo-400"
                                style={{
                                  width: `${Math.min(100, ((r.quality_score ?? 0) / maxAi) * 100)}%`,
                                }}
                              />
                            </div>
                            <span className="text-xs tabular-nums w-12 shrink-0">
                              {(r.quality_score ?? 0)}/{maxAi}
                            </span>
                          </div>

                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {labelShareholderBreakdown}
                              <IndicatorTooltip content={tipShareholderBreakdown} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div
                                className="h-full rounded-full bg-amber-400"
                                style={{ width: `${Math.min(100, ((r.shareholder_score ?? 0) / 10) * 100)}%` }}
                              />
                            </div>
                            <span className="text-xs tabular-nums w-10">{(r.shareholder_score ?? 0)}/10</span>
                          </div>

                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {LABEL_BONUS}
                              <IndicatorTooltip content={TOOLTIP_BONUS} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div
                                className="h-full rounded-full bg-yellow-400"
                                style={{ width: `${Math.min(100, ((r.bonus_score ?? 0) / 5) * 100)}%` }}
                              />
                            </div>
                            <span className="text-xs tabular-nums w-10">{r.bonus_score ?? 0}/5</span>
                          </div>

                          <div className="flex items-center gap-2">
                            <span className="flex items-center gap-0.5 w-28 text-xs shrink-0">
                              {LABEL_RISK}
                              <IndicatorTooltip content={TOOLTIP_RISK_SCORE} />
                            </span>
                            <div className="flex-1 h-1.5 rounded-full bg-[#e5e0d8] overflow-hidden">
                              <div
                                className="h-full rounded-full bg-red-300"
                                style={{ width: `${Math.min(100, (Math.abs(r.risk_penalty ?? 0) / 30) * 100)}%` }}
                              />
                            </div>
                            <span className="text-xs tabular-nums w-12">{(r.risk_penalty ?? 0)}/-30</span>
                          </div>
                        </div>
                      </section>
                      <section>
                        <h3 className="text-xs font-semibold text-[#6b6b6b] mb-2">{LABEL_METRICS}</h3>
                        <div className="grid grid-cols-2 gap-2">
                          {isFinance ? (
                            <>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  PBR
                                  <IndicatorTooltip content={TOOLTIP_PBR} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.pbr != null ? `${r.pbr}${PITCH_TIMES}` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  PER
                                  <IndicatorTooltip content={TOOLTIP_PER} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">{r.per}{PITCH_TIMES}</div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_MARKETCAP}
                                  <IndicatorTooltip content={TOOLTIP_MARKETCAP} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">{r.market_cap_oku}{LABEL_OKU}</div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_DIVIDEND}
                                  <IndicatorTooltip content={TOOLTIP_DIVIDEND} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.dividend_yield != null ? `${r.dividend_yield}%` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  ROE
                                  <IndicatorTooltip content={TOOLTIP_ROE} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.roe != null ? `${r.roe}%` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_EQUITY_RATIO}
                                  <IndicatorTooltip content={TOOLTIP_EQUITY_RATIO} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.equity_ratio != null && r.equity_ratio !== undefined
                                    ? `${r.equity_ratio}%`
                                    : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_PAYOUT}
                                  <IndicatorTooltip content={TOOLTIP_PAYOUT} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.payout_ratio != null ? `${r.payout_ratio}%` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_THEORETICAL}
                                  <IndicatorTooltip content={TOOLTIP_THEORETICAL} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.theoretical_price != null &&
                                  r.theoretical_price !== undefined &&
                                  r.theoretical_price > 0
                                    ? `${r.theoretical_price.toLocaleString()}\u5186`
                                    : DASH}
                                </div>
                                <span className="text-[10px] text-gray-400 block mt-1">
                                  {
                                    "\u203b\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u306f\u7cbe\u5ea6\u304c\u4f4e\u3044\u5834\u5408\u304c\u3042\u308a\u307e\u3059"
                                  }
                                </span>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_UPSIDE}
                                  <IndicatorTooltip content={TOOLTIP_UPSIDE} />
                                </div>
                                <div
                                  className={`text-sm font-medium mt-0.5 ${
                                    r.upside_percent != null &&
                                    r.upside_percent !== undefined &&
                                    r.upside_percent > 0
                                      ? "text-green-600"
                                      : r.upside_percent != null &&
                                          r.upside_percent !== undefined &&
                                          r.upside_percent < 0
                                        ? "text-red-500"
                                        : "text-gray-800"
                                  }`}
                                >
                                  {r.upside_percent != null &&
                                  r.upside_percent !== undefined &&
                                  r.upside_percent > 0
                                    ? `+${r.upside_percent}%`
                                    : r.upside_percent != null &&
                                        r.upside_percent !== undefined &&
                                        r.upside_percent < 0
                                      ? `${r.upside_percent}%`
                                      : DASH}
                                </div>
                                <span className="text-[10px] text-gray-400 block mt-1">
                                  {"\u203b\u53c2\u8003\u5024"}
                                </span>
                              </div>
                            </>
                          ) : (
                            <>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_NC}
                                  <IndicatorTooltip content={TOOLTIP_NC} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">{r.net_cash_ratio}</div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  PER
                                  <IndicatorTooltip content={TOOLTIP_PER} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">{r.per}{PITCH_TIMES}</div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_MARKETCAP}
                                  <IndicatorTooltip content={TOOLTIP_MARKETCAP} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">{r.market_cap_oku}{LABEL_OKU}</div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_DIVIDEND}
                                  <IndicatorTooltip content={TOOLTIP_DIVIDEND} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.dividend_yield != null ? `${r.dividend_yield}%` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  ROE
                                  <IndicatorTooltip content={TOOLTIP_ROE} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.roe != null ? `${r.roe}%` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  ROIC
                                  <IndicatorTooltip content={TOOLTIP_ROIC} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.roic != null ? `${r.roic}%` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  PBR
                                  <IndicatorTooltip content={TOOLTIP_PBR} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.pbr != null ? `${r.pbr}${PITCH_TIMES}` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_PAYOUT}
                                  <IndicatorTooltip content={TOOLTIP_PAYOUT} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.payout_ratio != null ? `${r.payout_ratio}%` : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_THEORETICAL}
                                  <IndicatorTooltip content={TOOLTIP_THEORETICAL} />
                                </div>
                                <div className="text-sm font-medium text-gray-800 mt-0.5">
                                  {r.theoretical_price != null &&
                                  r.theoretical_price !== undefined &&
                                  r.theoretical_price > 0
                                    ? `${r.theoretical_price.toLocaleString()}\u5186`
                                    : DASH}
                                </div>
                              </div>
                              <div className="bg-[#f5f0e8] rounded-lg p-3">
                                <div className="text-xs text-gray-500 flex items-center gap-0.5">
                                  {LABEL_UPSIDE}
                                  <IndicatorTooltip content={TOOLTIP_UPSIDE} />
                                </div>
                                <div
                                  className={`text-sm font-medium mt-0.5 ${
                                    r.upside_percent != null &&
                                    r.upside_percent !== undefined &&
                                    r.upside_percent > 0
                                      ? "text-green-600"
                                      : r.upside_percent != null &&
                                          r.upside_percent !== undefined &&
                                          r.upside_percent < 0
                                        ? "text-red-500"
                                        : "text-gray-800"
                                  }`}
                                >
                                  {r.upside_percent != null &&
                                  r.upside_percent !== undefined &&
                                  r.upside_percent > 0
                                    ? `+${r.upside_percent}%`
                                    : r.upside_percent != null &&
                                        r.upside_percent !== undefined &&
                                        r.upside_percent < 0
                                      ? `${r.upside_percent}%`
                                      : DASH}
                                </div>
                              </div>
                            </>
                          )}
                        </div>
                      </section>
                      <section>
                        <h3 className="text-xs font-semibold text-[#6b6b6b] mb-2">{LABEL_AI_ANALYSIS}</h3>
                        <div className="rounded-lg bg-[#e5e0d8]/60 p-3 text-xs text-[#4a4a4a]">
                          {r.ai_comment?.trim() || MSG_AI_PLACEHOLDER}
                        </div>
                      </section>
                      <section>
                        <h3 className="text-xs font-semibold text-[#6b6b6b] mb-2">
                          {isFinance ? LABEL_RISK_CHECK_FINANCE : LABEL_RISK_CHECK}
                        </h3>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          {(isFinance ? RISK_CHECK_ITEMS_FINANCE : RISK_CHECK_ITEMS).map(
                            ({ key, label, inverted }) => {
                              const val = (r.risk_checks as Record<string, boolean | null | undefined> | null)?.[
                                key
                              ];
                              const tip = isFinance
                                ? RISK_CHECK_TOOLTIPS_FINANCE[key]
                                : RISK_CHECK_TOOLTIPS[key as string];
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
                                  <span className="text-[#6b6b6b] flex items-center gap-0.5">
                                    {label}
                                    {tip ? <IndicatorTooltip content={tip} /> : null}
                                  </span>
                                  <span
                                    className={`inline-flex items-center px-1.5 py-0.5 rounded font-medium shrink-0 ${badgeClass}`}
                                  >
                                    {badge}
                                    {suffix}
                                  </span>
                                </div>
                              );
                            },
                          )}
                        </div>
                      </section>
                    </div>
                  )}
                </div>
              );
            })}
        </div>

          <div className="mt-12 rounded-xl bg-[#f5f0e8] p-6">
            <h2 className="text-sm font-bold text-[#4a4a4a] mb-3">{DISCLAIMER_TITLE}</h2>
            <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_1}</p>
            <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_2}</p>
            <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_3}</p>
            <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_4}</p>
            <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2 font-semibold">{DISCLAIMER_5}</p>
            <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2 font-semibold">{DISCLAIMER_6}</p>
          </div>

          <footer className="mt-12 border-t border-[#e5e0d8] py-6">
            <p className="text-xs leading-relaxed text-[#9ca3af]">
              {FOOTER_DISCLAIMER}
            </p>
          </footer>
          </>
        )}
        </div>
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
            <div className="text-xs text-[#78350f] bg-[#fef3c7] rounded-lg p-3 mb-3">
              <p className="font-bold text-[#92400e] mb-2">{MODAL_BENEFITS_TITLE}</p>
              <p>{"\u2705 "}{BENEFIT_1}</p>
              <p>{"\u2705 "}{BENEFIT_2}</p>
              <p>{"\u2705 "}{BENEFIT_3}</p>
              <p>{"\u2705 "}{BENEFIT_4}</p>
              <p>{"\u2705 "}{BENEFIT_5}</p>
            </div>
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
    </>
  );
}



