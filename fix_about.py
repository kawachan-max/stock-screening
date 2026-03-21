content = open('app/about/page.tsx', 'r', encoding='utf-8').read()

# ===== 1. CATCH_7〜8の後に、清原式×バフェット流の説明を追加 =====
# CATCH_8の後に新しい定数を追加

new_consts_after_catch8 = '''
const HYBRID_TITLE = "\\u306a\\u305c\\u300c\\u6e05\\u539f\\u5f0f\\u00d7\\u30d0\\u30d5\\u30a7\\u30c3\\u30c8\\u6d41\\u300d\\u306a\\u306e\\u304b\\uff1f";
const HYBRID_1 = "\\u6e05\\u539f\\u5f0f\\uff1a\\u30cd\\u30c3\\u30c8\\u30ad\\u30e3\\u30c3\\u30b7\\u30e5\\u6bd4\\u7387\\u3067\\u300c\\u5272\\u5b89\\u3067\\u653e\\u7f6e\\u3055\\u308c\\u305f\\u5c0f\\u578b\\u682a\\u300d\\u3092\\u767a\\u898b\\u3059\\u308b";
const HYBRID_2 = "\\u30d0\\u30d5\\u30a7\\u30c3\\u30c8\\u6d41\\uff1aROE\\u30fbROIC\\u30fb\\u53ce\\u76ca\\u5b89\\u5b9a\\u6027\\u3067\\u300c\\u6210\\u9577\\u6027\\u3068\\u4e8b\\u696d\\u306e\\u8cea\\u300d\\u3092\\u78ba\\u8a8d\\u3059\\u308b";
const HYBRID_3 = "\\u3053\\u306e\\u30cf\\u30a4\\u30d6\\u30ea\\u30c3\\u30c9\\u306b\\u3088\\u308a\\u3001\\u4f55\\u5e74\\u3082\\u5272\\u5b89\\u306e\\u307e\\u307e\\u653e\\u7f6e\\u3055\\u308c\\u308b\\u3060\\u3051\\u306e\\u682a\\u3092\\u907f\\u3051\\u3089\\u308c\\u307e\\u3059\\u3002\\u307e\\u305fROE\\u304c\\u9ad8\\u3044\\u4f01\\u696d\\u306f\\u3001\\u512a\\u308c\\u305f\\u53ce\\u76ca\\u529b\\u304b\\u3089\\u914d\\u5f53\\u5897\\u3084\\u81ea\\u793e\\u682a\\u8cb7\\u3044\\u306e\\u53ef\\u80fd\\u6027\\u3082\\u9ad8\\u307e\\u308a\\u307e\\u3059\\u3002";
'''

# CATCH_8定義の後に挿入
catch8_end = content.find('";', content.find('const CATCH_8')) + 2
if 'HYBRID_TITLE' not in content:
    content = content[:catch8_end] + new_consts_after_catch8 + content[catch8_end:]
    print('1. Added HYBRID constants')

# ===== 2. STANCE修正: 中長期→数年単位、高配当活用、NC比率順の選択肢 =====
# STANCE_BODYを置換
old_stance = content[content.find('const STANCE_BODY'):content.find('";', content.find('const STANCE_BODY'))+2]
new_stance = 'const STANCE_BODY = "\\u30cd\\u30c3\\u30c8\\u30ad\\u30e3\\u30c3\\u30b7\\u30e5\\u6bd4\\u7387\\u304c\\u9ad8\\u304f\\u3001\\u4eee\\u306b\\u5012\\u7523\\u3057\\u3066\\u3082\\u640d\\u3057\\u306b\\u304f\\u3044\\u30ec\\u30d9\\u30eb\\u306e\\u5272\\u5b89\\u682a\\u3092\\u3001\\u30b3\\u30a2\\u30b5\\u30c6\\u30e9\\u30a4\\u30c8\\u6226\\u7565\\u306e\\u30b5\\u30c6\\u30e9\\u30a4\\u30c8\\u679a\\u3068\\u3057\\u3066\\u3001\\u8907\\u6570\\u9298\\u67c4\\u306b\\u5206\\u6563\\u3057\\u3001\\u6570\\u5e74\\u5358\\u4f4d\\u3067\\u4fdd\\u6709\\u3059\\u308b\\u4e2d\\u9577\\u671f\\u6295\\u8cc7\\u3002\\u305d\\u306e\\u3046\\u3061\\u3069\\u308c\\u304b\\u304c\\u30c6\\u30f3\\u30d0\\u30ac\\u30fc\\u306b\\u306a\\u308c\\u3070\\u3044\\u3044\\u3002";'
content = content.replace(old_stance, new_stance)
print('2. Updated STANCE_BODY')

# STANCE_FOOTを置換（高配当活用・NC比率順の選択肢を追加）
old_foot = content[content.find('const STANCE_FOOT'):content.find('";', content.find('const STANCE_FOOT'))+2]
new_foot = 'const STANCE_FOOT = "\\u30e9\\u30f3\\u30ad\\u30f3\\u30b0\\u4e0a\\u4f4d\\uff1d\\u3059\\u3050\\u4e0a\\u304c\\u308b\\u9298\\u67c4\\u3067\\u306f\\u3042\\u308a\\u307e\\u305b\\u3093\\u3002\\u300c\\u5272\\u5b89\\u3067\\u653e\\u7f6e\\u3055\\u308c\\u3066\\u3044\\u308b\\u6709\\u671b\\u5019\\u88dc\\u300d\\u3067\\u3059\\u3002\\u914d\\u5f53\\u5229\\u56de\\u308a\\u3082\\u8868\\u793a\\u3057\\u3066\\u3044\\u308b\\u306e\\u3067\\u3001\\u3059\\u3067\\u306b\\u9ad8\\u914d\\u5f53\\u306b\\u306a\\u3063\\u3066\\u3044\\u308b\\u9298\\u67c4\\u304b\\u3089\\u9577\\u671f\\u4fdd\\u6709\\u3059\\u308b\\u3068\\u3044\\u3046\\u6d3b\\u7528\\u3082\\u53ef\\u80fd\\u3067\\u3059\\u3002\\u307e\\u305f\\u3001\\u6e05\\u539f\\u5f0f\\u306b\\u91cd\\u70b9\\u3092\\u7f6e\\u304f\\u65b9\\u306f\\u3001\\u30b9\\u30b3\\u30a2\\u306b\\u3088\\u308b\\u30e9\\u30f3\\u30ad\\u30f3\\u30b0\\u3067\\u306f\\u306a\\u304f\\u3001\\u30cd\\u30c3\\u30c8\\u30ad\\u30e3\\u30c3\\u30b7\\u30e5\\u6bd4\\u7387\\u306e\\u9ad8\\u3044\\u9806\\u306b\\u9298\\u67c4\\u3092\\u9078\\u3076\\u3053\\u3068\\u3082\\u3067\\u304d\\u307e\\u3059\\u3002";'
content = content.replace(old_foot, new_foot)
print('3. Updated STANCE_FOOT')

# ===== 3. 金融セクター除外の注記を追加 =====
new_finance_note = '''
const FINANCE_NOTE_TITLE = "\\u91d1\\u878d\\u30bb\\u30af\\u30bf\\u30fc\\u306b\\u3064\\u3044\\u3066";
const FINANCE_NOTE = "\\u9280\\u884c\\u30fb\\u4fdd\\u967a\\u30fb\\u4e0d\\u52d5\\u7523\\u306a\\u3069\\u91d1\\u878d\\u30bb\\u30af\\u30bf\\u30fc\\u306f\\u3001\\u30cd\\u30c3\\u30c8\\u30ad\\u30e3\\u30c3\\u30b7\\u30e5\\u6bd4\\u7387\\u306e\\u7b97\\u51fa\\u65b9\\u6cd5\\u304c\\u4e00\\u822c\\u4e8b\\u696d\\u4f1a\\u793e\\u3068\\u7570\\u306a\\u308b\\u305f\\u3081\\u3001\\u672c\\u30e9\\u30f3\\u30ad\\u30f3\\u30b0\\u306e\\u5bfe\\u8c61\\u5916\\u3068\\u3057\\u3066\\u3044\\u307e\\u3059\\u3002\\u91d1\\u878d\\u30bb\\u30af\\u30bf\\u30fc\\u5411\\u3051\\u306e\\u30b9\\u30af\\u30ea\\u30fc\\u30cb\\u30f3\\u30b0\\u306f\\u4eca\\u5f8c\\u5225\\u30bf\\u30d6\\u3067\\u63d0\\u4f9b\\u4e88\\u5b9a\\u3067\\u3059\\u3002";
'''

# DISCLAIMER定数の前に追加
if 'FINANCE_NOTE_TITLE' not in content:
    disclaimer_pos = content.find('const DISCLAIMER_TITLE')
    content = content[:disclaimer_pos] + new_finance_note + '\n' + content[disclaimer_pos:]
    print('4. Added FINANCE_NOTE constants')

# ===== 4. HOWTO_SCORE_DESCを新配点に合わせる =====
old_howto = content[content.find('const HOWTO_SCORE_DESC'):content.find('";', content.find('const HOWTO_SCORE_DESC'))+2]
new_howto = 'const HOWTO_SCORE_DESC = "\\u5272\\u5b89\\u5ea6(30)\\u30fb\\u6210\\u9577\\u6027(20)\\u30fb\\u53ce\\u76ca\\u6027(15)\\u30fbAI\\u696d\\u7e3e\\u5206\\u6790(10)\\u30fbAI\\u7af6\\u4e89\\u512a\\u4f4d\\u6027(10)\\u30fb\\u682a\\u4e3b\\u9084\\u5143\\u4f59\\u5730(10)\\u30fb\\u30dc\\u30fc\\u30ca\\u30b9(5)\\u30fb\\u30ea\\u30b9\\u30af\\u6e1b\\u70b9(-30)\\u306e\\u5408\\u8a08\\u3002\\u9ad8\\u3044\\u307b\\u3069\\u5272\\u5b89\\u304b\\u3064\\u512a\\u826f\\u306a\\u9298\\u67c4";'
content = content.replace(old_howto, new_howto)
print('5. Updated HOWTO_SCORE_DESC')

# ===== 5. FEATURE_2を新配点に合わせる =====
old_feature2 = content[content.find('const FEATURE_2'):content.find('";', content.find('const FEATURE_2'))+2]
new_feature2 = 'const FEATURE_2 = "\\u5272\\u5b89\\u5ea6\\u00d7\\u6210\\u9577\\u6027\\u00d7\\u53ce\\u76ca\\u6027\\u00d7\\u682a\\u4e3b\\u9084\\u5143\\u3092\\u30b9\\u30b3\\u30a2\\u5316\\u3057\\u3066\\u9806\\u4f4d\\u4ed8\\u3051";'
content = content.replace(old_feature2, new_feature2)
print('6. Updated FEATURE_2')

# ===== 6. JSXにハイブリッド説明セクションを追加 =====
# CATCH_8の表示の後、FEATUREセクションの前にハイブリッドセクションを挿入
# JSXを直接編集するのは難しいので、CATCHセクションの閉じタグ後に指示を出す
# → これはCursorに任せる方が安全

# ===== 7. JSXに金融セクター注記セクションを追加 =====
# → これもCursorに任せる方が安全

open('app/about/page.tsx', 'w', encoding='utf-8').write(content)
print('\nALL DONE - Constants updated')
print('\n=== IMPORTANT ===')
print('JSX sections need to be added by Cursor:')
print('1. Add HYBRID section (HYBRID_TITLE, HYBRID_1, HYBRID_2, HYBRID_3) after CATCH section')
print('2. Add FINANCE_NOTE section (FINANCE_NOTE_TITLE, FINANCE_NOTE) before DISCLAIMER section')
