content = open('app/about/page.tsx', 'r', encoding='utf-8').read()
content = content.replace('chr(34)+chr(34)+chr(59)', '""')
open('app/about/page.tsx', 'w', encoding='utf-8').write(content)
print('DONE')
