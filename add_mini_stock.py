content = open('app/about/page.tsx', 'r', encoding='utf-8').read()

# STANCE_FOOTの定数の後に新しい定数を追加
old = 'STANCE_FOOT = "'
idx = content.find(old)
# STANCE_FOOTの定義の終わりを見つける
end = content.find('";', idx) + 2

# 新しい定数を追加
new_const = '''
const STANCE_MINI = "\\u203b \\u5c0f\\u578b\\u682a\\u306f1\\u5358\\u5143\\u304c\\u9ad8\\u984d\\u306a\\u9298\\u67c4\\u3082\\u3042\\u308a\\u307e\\u3059\\u3002S\\u682a\\u30fb\\u30df\\u30cb\\u682a\\u306a\\u3069\\u306e\\u5358\\u5143\\u672a\\u6e80\\u682a\\u3092\\u6d3b\\u7528\\u3059\\u308c\\u3070\\u30011\\u682a\\u304b\\u3089\\u5c11\\u984d\\u3067\\u5206\\u6563\\u6295\\u8cc7\\u304c\\u53ef\\u80fd\\u3067\\u3059\\u3002\\u79c1\\u81ea\\u8eab\\u3082SBI\\u8a3c\\u5238\\u306eS\\u682a\\u3092\\u6d3b\\u7528\\u3057\\u3066\\u3044\\u307e\\u3059\\u3002";
'''

content = content[:end] + new_const + content[end:]

# JSXでSTANCE_FOOTの表示の後にSTANCE_MINIを追加
old_jsx = 'STANCE_FOOT}</p>'
new_jsx = 'STANCE_FOOT}</p>\n            <p className="text-xs text-gray-500 mt-3 bg-gray-50 p-3 rounded-lg">{STANCE_MINI}</p>'
content = content.replace(old_jsx, new_jsx, 1)

open('app/about/page.tsx', 'w', encoding='utf-8').write(content)
print("DONE")
