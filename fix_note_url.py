content = open('app/page.tsx', 'r', encoding='utf-8').read()

old_url = "note.com/kawachan_max"
new_url = "note.com/dreamy_okapi3047/n/n0fafb7449d15"

count = content.count(old_url)
print("Found old URL: %d times" % count)

content = content.replace(old_url, new_url)

open('app/page.tsx', 'w', encoding='utf-8').write(content)
print("DONE")
