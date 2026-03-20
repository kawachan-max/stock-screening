content = open('app/page.tsx', 'r', encoding='utf-8').read()

# TOOLTIP_NC: 素現金→純現金, 時価経額→時価総額
content = content.replace('\\u7D20\\u73FE\\u91D1', '\\u7D14\\u73FE\\u91D1')
content = content.replace('\\u6642\\u4FA1\\u7D4C\\u984D', '\\u6642\\u4FA1\\u7DCF\\u984D')
print('NC fixed')

# TOOLTIP_MARKETCAP: 値学→価値, 株企業数→株式数, 市場未登見ゾーン→小型株ゾーン
content = content.replace('\\u5024\\u5B66', '\\u4FA1\\u5024')
content = content.replace('\\u682A\\u4F01\\u696D\\u6570', '\\u682A\\u5F0F\\u6570')
content = content.replace('\\u5E02\\u5834\\u672A\\u767B\\u898B\\u30BE\\u30FC\\u30F3', '\\u5C0F\\u578B\\u682A\\u30BE\\u30FC\\u30F3')
print('MARKETCAP fixed')

# TOOLTIP_PBR: 正味費産→正味資産
content = content.replace('\\u6B63\\u5473\\u8CBB\\u7523', '\\u6B63\\u5473\\u8CC7\\u7523')
print('PBR fixed')

# TOOLTIP_CHEAP_SCORE: 達郃→達郎
content = content.replace('\\u9054\\u90C3', '\\u9054\\u90CE')
print('CHEAP_SCORE fixed')

# TOOLTIP_ROE: 15%以下→15%以上
content = content.replace('15%\\u4EE5\\u4E0B\\uFF1D\\u30D0\\u30D5', '15%\\u4EE5\\u4E0A\\uFF1D\\u30D0\\u30D5')
content = content.replace('15%\\u4EE5\\u4E0B\\uFF1D\\u512A\\u826F', '15%\\u4EE5\\u4E0A\\uFF1D\\u512A\\u826F')
print('ROE fixed')

# TOOLTIP_RISK_SCORE: 出来量→出来高
content = content.replace('\\u51FA\\u6765\\u91CF', '\\u51FA\\u6765\\u9AD8')
print('RISK出来高 fixed')

# TOOLTIP_RISK_SCORE intent: 等筋銘柄を排除→危険な銘柄を排除
# まず現在のintent部分を探して置換
old_intent = '\\u7B49\\u7B4B\\u9298\\u67C4\\u3092\\u6392\\u9664'
new_intent = '\\u5371\\u967A\\u306A\\u9298\\u67C4\\u3092\\u6392\\u9664'
if old_intent in content:
    content = content.replace(old_intent, new_intent)
    print('等筋→危険 fixed (pattern 1)')
else:
    # 別パターンで探す
    import re
    # intent行を探して丸ごと置換
    old_pat = r'(intent: "\\u3069.*?\\u6e1b\\u70b9\\u3002)([^"]*)(\\u3092\\u6392\\u9664\\u3059\\u308b\\u305f\\u3081\\u306e\\u4ed5\\u7d44\\u307f")'
    match = re.search(old_pat, content)
    if match:
        print('Found intent pattern:', repr(match.group(2)))
        new_mid = '\\u5371\\u967a\\u306a\\u9298\\u67c4'
        content = content[:match.start(2)] + new_mid + content[match.end(2):]
        print('等筋→危険 fixed (pattern 2)')
    else:
        print('WARNING: 等筋 pattern not found, searching broadly...')
        # 全てのintent行周辺を表示
        idx = content.find('u6e1b\\u70b9\\u3002')
        while idx > 0:
            print('  context:', repr(content[idx:idx+120]))
            idx = content.find('u6e1b\\u70b9\\u3002', idx+1)

open('app/page.tsx', 'w', encoding='utf-8').write(content)
print('ALL DONE')
