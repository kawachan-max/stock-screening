content = open('app/page.tsx', 'r', encoding='utf-8').read()
count = 0

# ===== TOOLTIP_CHEAP_SCORE (割安度) =====
old = content[content.find('const TOOLTIP_CHEAP_SCORE'):content.find('};', content.find('const TOOLTIP_CHEAP_SCORE'))+2]
new = '''const TOOLTIP_CHEAP_SCORE: TooltipContent = {
  title: "\\u5272\\u5b89\\u5ea6\\u30b9\\u30b3\\u30a2\\uff08\\u6700\\u592730\\u70b9\\uff09",
  desc: "\\u30cd\\u30c3\\u30c8\\u30ad\\u30e3\\u30c3\\u30b7\\u30e5\\u6bd4\\u7387\\uff08NC\\u6bd4\\u7387\\uff09\\u3068PER\\u3067\\u5272\\u5b89\\u5ea6\\u3092\\u70b9\\u6570\\u5316\\u3057\\u307e\\u3059",
  formula: "NC\\u6bd4\\u7387\\u30b9\\u30b3\\u30a2\\uff08\\u6700\\u592720\\u70b9\\uff09\\uff0bPER\\u30b9\\u30b3\\u30a2\\uff08\\u6700\\u592710\\u70b9\\uff09",
  intent: "\\u6e05\\u539f\\u9054\\u90ce\\u5f0f\\u306e\\u6838\\u5fc3\\u3002NC\\u6bd4\\u7387\\u3068PER\\u304c\\u4f4e\\u3044\\u307b\\u3069\\u5272\\u5b89\\u5ea6\\u304c\\u9ad8\\u304f\\u8a55\\u4fa1\\u3055\\u308c\\u307e\\u3059",
};'''
content = content.replace(old, new)
count += 1
print(f'{count}. CHEAP_SCORE fixed')

# ===== TOOLTIP_GROWTH_SCORE (成長性) =====
old = content[content.find('const TOOLTIP_GROWTH_SCORE'):content.find('};', content.find('const TOOLTIP_GROWTH_SCORE'))+2]
new = '''const TOOLTIP_GROWTH_SCORE: TooltipContent = {
  title: "\\u6210\\u9577\\u6027\\u30b9\\u30b3\\u30a2\\uff08\\u6700\\u592720\\u70b9\\uff09",
  desc: "\\u58f2\\u4e0a\\u30fb\\u5229\\u76ca\\u306e\\u589e\\u53ce\\u589e\\u76ca\\u3068\\u6210\\u9577\\u7387\\u3067\\u6210\\u9577\\u6027\\u3092\\u8a55\\u4fa1\\u3057\\u307e\\u3059",
  formula: "3\\u671f\\u9023\\u7d9a\\u589e\\u53ce(5)\\uff0b\\u58f2\\u4e0a\\u6210\\u9577\\u7387(5)\\uff0b3\\u671f\\u9023\\u7d9a\\u589e\\u76ca(5)\\uff0b\\u5229\\u76ca\\u6210\\u9577\\u7387(5)",
  intent: "\\u4e2d\\u9577\\u671f\\u306b\\u6210\\u9577\\u304c\\u7d9a\\u3044\\u3066\\u3044\\u308b\\u304b\\u3092\\u898b\\u308b\\u9805\\u76ee\\u3067\\u3059",
};'''
content = content.replace(old, new)
count += 1
print(f'{count}. GROWTH_SCORE fixed')

# ===== TOOLTIP_QUALITY_DETAIL (事業の質・収益性) =====
old = content[content.find('const TOOLTIP_QUALITY_DETAIL'):content.find('};', content.find('const TOOLTIP_QUALITY_DETAIL'))+2]
new = '''const TOOLTIP_QUALITY_DETAIL: TooltipContent = {
  title: "\\u4e8b\\u696d\\u306e\\u8cea\\u30fb\\u53ce\\u76ca\\u6027\\uff08\\u6700\\u592715\\u70b9\\uff09",
  desc: "ROE\\u3068ROIC\\u306e\\u6c34\\u6e96\\u3068\\u55b6\\u696d\\u5229\\u76ca\\u7387\\u306e\\u5b89\\u5b9a\\u6027\\u3067\\u4e8b\\u696d\\u306e\\u8cea\\u3092\\u8a55\\u4fa1\\u3057\\u307e\\u3059",
  formula: "ROE\\u30b9\\u30b3\\u30a2(5)\\uff0bROIC\\u30b9\\u30b3\\u30a2(5)\\uff0b\\u53ce\\u76ca\\u5b89\\u5b9a\\u6027\\u30b9\\u30b3\\u30a2(5)",
  intent: "\\u55b6\\u696d\\u5229\\u76ca\\u306e\\u7d9a\\u304f\\u5b9f\\u7e3e\\u3092\\u898b\\u306a\\u304c\\u3089\\u3001\\u5229\\u76ca\\u306e\\u8cea\\u3092\\u8a55\\u4fa1\\u3057\\u307e\\u3059",
};'''
content = content.replace(old, new)
count += 1
print(f'{count}. QUALITY_DETAIL fixed')

# ===== TOOLTIP_SHAREHOLDER_SCORE (株主還元余地) =====
old = content[content.find('const TOOLTIP_SHAREHOLDER_SCORE'):content.find('};', content.find('const TOOLTIP_SHAREHOLDER_SCORE'))+2]
new = '''const TOOLTIP_SHAREHOLDER_SCORE: TooltipContent = {
  title: "\\u682a\\u4e3b\\u9084\\u5143\\u4f59\\u5730\\u30b9\\u30b3\\u30a2\\uff08\\u6700\\u592710\\u70b9\\uff09",
  desc: "\\u914d\\u5f53\\u6027\\u5411\\u3068\\u30ad\\u30e3\\u30c3\\u30b7\\u30e5\\u306e\\u589e\\u52a0\\u3001\\u589e\\u914d\\u30fb\\u81ea\\u793e\\u682a\\u8cb7\\u3044\\u306e\\u5b9f\\u7e3e\\u3001PBR\\u5bfe\\u5fdc\\u3092\\u8a55\\u4fa1\\u3057\\u307e\\u3059",
  formula: "\\u914d\\u5f53\\u6027\\u5411(3)\\uff0b\\u30ad\\u30e3\\u30c3\\u30b7\\u30e5\\u7a4d\\u307f\\u4e0a\\u304c\\u308a(3)\\uff0b\\u9084\\u5143\\u65b9\\u91dd\\u5909\\u5316(2)\\uff0b\\u6771\\u8a3cPBR\\u5bfe\\u5fdc(2)",
  intent: "\\u9084\\u5143\\u4f59\\u5730\\u304c\\u5927\\u304d\\u3044\\u9298\\u67c4\\u306f\\u3001\\u4eca\\u5f8c\\u306e\\u914d\\u5f53\\u5897\\u3084\\u682a\\u4fa1\\u4e0a\\u6607\\u306e\\u304d\\u3063\\u304b\\u3051\\u306b\\u306a\\u308a\\u307e\\u3059",
};'''
content = content.replace(old, new)
count += 1
print(f'{count}. SHAREHOLDER_SCORE fixed')

# ===== TOOLTIP_BONUS (ボーナス) =====
old = content[content.find('const TOOLTIP_BONUS'):content.find('};', content.find('const TOOLTIP_BONUS'))+2]
new = '''const TOOLTIP_BONUS: TooltipContent = {
  title: "\\u30dc\\u30fc\\u30ca\\u30b9\\uff08\\u6700\\u59275\\u70b9\\uff09",
  desc: "\\u55b6\\u696dCF3\\u671f\\u9023\\u7d9a\\u30d7\\u30e9\\u30b9\\u30013\\u671f\\u9023\\u7d9a\\u589e\\u914d\\u3001\\u4e0a\\u65b9\\u4fee\\u6b63\\u3001\\u9ad8\\u914d\\u5f53\\uff0b\\u4f4ePBR\\u3001\\u8d85\\u5272\\u5b89\\u30b3\\u30f3\\u30dc\\u306e5\\u6761\\u4ef6\\u3067\\u52a0\\u70b9",
  formula: "\\u55b6\\u696dCF\\u5b89\\u5b9a\\uff0b\\u589e\\u914d\\uff0b\\u4e0a\\u65b9\\u4fee\\u6b63\\uff0b\\u5272\\u5b89\\u30b3\\u30f3\\u30dc\\u52a0\\u70b9",
  intent: "\\u5b9f\\u7e3e\\u3068\\u5b89\\u5b9a\\u6027\\u304c\\u78ba\\u8a8d\\u3067\\u304d\\u308b\\u9298\\u67c4\\u306b\\u8ffd\\u52a0\\u70b9\\u3092\\u4e0e\\u3048\\u307e\\u3059",
};'''
content = content.replace(old, new)
count += 1
print(f'{count}. BONUS fixed')

# ===== TOOLTIP_RISK_SCORE (リスク減点) =====
old = content[content.find('const TOOLTIP_RISK_SCORE'):content.find('};', content.find('const TOOLTIP_RISK_SCORE'))+2]
new = '''const TOOLTIP_RISK_SCORE: TooltipContent = {
  title: "\\u30ea\\u30b9\\u30af\\u6e1b\\u70b9\\uff08\\u6700\\u5927\\u7d0430\\u70b9\\uff09",
  desc: "\\u8ca1\\u52d9\\u5065\\u5168\\u6027\\u30fbFCF\\u30fb\\u6d41\\u52d5\\u6027\\u30fb\\u5229\\u76ca\\u306e\\u8cea\\u306a\\u3069\\u3092\\u7dcf\\u5408\\u7684\\u306b\\u8a55\\u4fa1\\u3057\\u6e1b\\u70b9\\u3057\\u307e\\u3059",
  formula: "\\u51fa\\u6765\\u9ad8\\u30ea\\u30b9\\u30af(-3)\\uff0b\\u4e00\\u904e\\u6027\\u5229\\u76ca(-4)\\uff0bROE\\u4f4e\\u4f4d(-2)\\uff0b\\u81ea\\u5df1\\u8cc7\\u672c(-3)\\uff0b\\u9577\\u671f\\u8ca0\\u50b5(-4)\\uff0bFCF(-4)\\uff0b\\u8907\\u6570\\u00d7\\u8ffd\\u52a0\\u30da\\u30ca\\u30eb\\u30c6\\u30a3",
  intent: "\\u3069\\u308c\\u3060\\u3051\\u826f\\u3044\\u30b9\\u30b3\\u30a2\\u3067\\u3082\\u30ea\\u30b9\\u30af\\u304c\\u9ad8\\u3051\\u308c\\u3070\\u6e1b\\u70b9\\u3002\\u5371\\u967a\\u306a\\u9298\\u67c4\\u3092\\u6392\\u9664\\u3059\\u308b\\u305f\\u3081\\u306e\\u4ed5\\u7d44\\u307f",
};'''
content = content.replace(old, new)
count += 1
print(f'{count}. RISK_SCORE fixed')

# ===== TOOLTIP_NC (ネットキャッシュ比率) =====
old = content[content.find('const TOOLTIP_NC'):content.find('};', content.find('const TOOLTIP_NC'))+2]
new = '''const TOOLTIP_NC: TooltipContent = {
  title: "\\u30cd\\u30c3\\u30c8\\u30ad\\u30e3\\u30c3\\u30b7\\u30e5\\u6bd4\\u7387",
  desc: "\\u4f1a\\u793e\\u304c\\u6301\\u3064\\u73fe\\u91d1\\u304b\\u3089\\u8ca0\\u50b5\\u3092\\u5f15\\u3044\\u305f\\u7d14\\u73fe\\u91d1\\u304c\\u6642\\u4fa1\\u7dcf\\u984d\\u306e\\u4f55\\u500d\\u304b\\u3092\\u793a\\u3059\\u6307\\u6a19\\u30021.0\\u4ee5\\u4e0a\\uff1d\\u682a\\u4fa1\\u3088\\u308a\\u73fe\\u91d1\\u304c\\u591a\\u3044\\u8d85\\u5272\\u5b89\\u72b6\\u614b",
  formula: "\\u7d14\\u73fe\\u91d1 \\u00f7 \\u6642\\u4fa1\\u7dcf\\u984d",
  intent: "1.0\\u4ee5\\u4e0a\\uff1d\\u8d85\\u5272\\u5b89",
};'''
content = content.replace(old, new)
count += 1
print(f'{count}. NC fixed')

open('app/page.tsx', 'w', encoding='utf-8').write(content)
print(f'\\nALL DONE: {count} tooltips fixed')
