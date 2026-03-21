content = open('app/page.tsx', 'r', encoding='utf-8').read()
count = 0

# 「増」の正しいコードは \u5897
# 文字化けパターンを探す
import re

# 増加、増収、増益、増配 に関連する文字化けを探す
# 正しい「増」= 5897、間違いの候補を探す
for pattern in ['\\u589E', '\\u589F', '\\u58A0', '\\u58A1', '\\u5896', '\\u5898']:
    if pattern in content:
        n = content.count(pattern)
        content = content.replace(pattern, '\\u5897')
        count += n
        print(f'Fixed {pattern} -> \\u5897 ({n} occurrences)')

# 大文字の増も確認
for pattern in ['\\u589e']:
    if pattern in content:
        # これは正しい小文字版なのでスキップ（\u589eと\u5897は同じ文字）
        pass

print(f'Total 増 fixes: {count}')

# AI業績分析のツールチップを追加
# まず既存のTOOLTIP定数の後に追加する
# TOOLTIP_RISK_SCOREの後に追加

ai_trend_tooltip = '''
const TOOLTIP_AI_TREND: TooltipContent = {
  title: "AI\\u696d\\u7e3e\\u5206\\u6790\\uff08\\u6700\\u592710\\u70b9\\uff09",
  desc: "AI\\u304c\\u6c7a\\u7b97\\u66f8\\u3092\\u8aad\\u307f\\u3001\\u58f2\\u4e0a\\u30fb\\u5229\\u76ca\\u306e\\u30c8\\u30ec\\u30f3\\u30c9\\u3092\\u5206\\u6790\\u3057\\u3066\\u70b9\\u6570\\u5316\\u3057\\u307e\\u3059",
  formula: "3\\u671f\\u9023\\u7d9a\\u5897\\u53ce\\u5897\\u76ca\\u219210\\u70b9\\u3001\\u5897\\u53ce or \\u5897\\u76ca\\u21927\\u70b9\\u3001\\u6a2a\\u3070\\u3044\\u21924\\u70b9\\u3001\\u6e1b\\u53ce\\u6e1b\\u76ca\\u21920\\u70b9",
  intent: "AI\\u304c\\u5ba2\\u89b3\\u7684\\u306b\\u696d\\u7e3e\\u306e\\u6d41\\u308c\\u3092\\u5224\\u5b9a\\u3057\\u307e\\u3059",
};'''

ai_quality_tooltip = '''
const TOOLTIP_AI_QUALITY: TooltipContent = {
  title: "AI\\u7af6\\u4e89\\u512a\\u4f4d\\u6027\\uff08\\u6700\\u592710\\u70b9\\uff09",
  desc: "AI\\u304c\\u4e8b\\u696d\\u306e\\u7af6\\u4e89\\u512a\\u4f4d\\u6027\\u30fb\\u53c2\\u5165\\u969c\\u58c1\\u30fb\\u53ce\\u76ca\\u57fa\\u76e4\\u306e\\u5f37\\u3055\\u3092\\u8a55\\u4fa1\\u3057\\u307e\\u3059",
  formula: "\\u5f37\\u56fa\\u306a\\u512a\\u4f4d\\u6027\\u219210\\u70b9\\u3001\\u4e00\\u5b9a\\u306e\\u512a\\u4f4d\\u6027\\u21927\\u70b9\\u3001\\u5e73\\u5747\\u7684\\u21924\\u70b9\\u3001\\u61f8\\u5ff5\\u21920\\u70b9",
  intent: "\\u4e8b\\u696d\\u304c\\u9577\\u671f\\u7684\\u306b\\u7a3c\\u304e\\u7d9a\\u3051\\u3089\\u308c\\u308b\\u304b\\u3092AI\\u304c\\u5224\\u5b9a\\u3057\\u307e\\u3059",
};'''

# TOOLTIP_RISK_SCOREの直後に追加
risk_end = content.find('};', content.find('const TOOLTIP_RISK_SCORE')) + 2
# 既にTOOLTIP_AI_TRENDがあるか確認
if 'TOOLTIP_AI_TREND' not in content:
    content = content[:risk_end] + ai_trend_tooltip + ai_quality_tooltip + content[risk_end:]
    print('Added TOOLTIP_AI_TREND and TOOLTIP_AI_QUALITY')
else:
    print('TOOLTIP_AI_TREND already exists, skipping')

# AI業績分析バーにツールチップを追加
# 「AI業績分析」のバー行を探して、IndicatorTooltipを追加
# trend_scoreのバー表示部分を探す
if 'TOOLTIP_AI_TREND' in content and 'content={TOOLTIP_AI_TREND}' not in content:
    # AI業績分析のラベル部分を探す
    # パターン: AI\u696d\u7e3e\u5206\u6790 の後にIndicatorTooltipがないケース
    # ラベル定数を探す
    idx = content.find('LABEL_AI_TREND')
    if idx > 0:
        print(f'Found LABEL_AI_TREND at {idx}')
        # JSXでの使用箇所を探す
        jsx_idx = content.find('{LABEL_AI_TREND}', idx + 100)
        if jsx_idx > 0:
            # この後に </span> があるはず、その前にIndicatorTooltipを挿入
            end_span = content.find('</span>', jsx_idx)
            if end_span > 0 and 'TOOLTIP_AI_TREND' not in content[jsx_idx:end_span]:
                content = content[:end_span] + '\n                    <IndicatorTooltip content={TOOLTIP_AI_TREND} />' + content[end_span:]
                print('Added IndicatorTooltip for AI_TREND in JSX')

if 'TOOLTIP_AI_QUALITY' in content and 'content={TOOLTIP_AI_QUALITY}' not in content:
    idx = content.find('LABEL_AI_QUALITY')
    if idx > 0:
        jsx_idx = content.find('{LABEL_AI_QUALITY}', idx + 100)
        if jsx_idx > 0:
            end_span = content.find('</span>', jsx_idx)
            if end_span > 0 and 'TOOLTIP_AI_QUALITY' not in content[jsx_idx:end_span]:
                content = content[:end_span] + '\n                    <IndicatorTooltip content={TOOLTIP_AI_QUALITY} />' + content[end_span:]
                print('Added IndicatorTooltip for AI_QUALITY in JSX')

open('app/page.tsx', 'w', encoding='utf-8').write(content)
print('ALL DONE')
