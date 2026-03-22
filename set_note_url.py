note_url = "https://note.com/dreamy_okapi3047/n/n0fafb7449d15"

# page.tsx
content = open('app/page.tsx', 'r', encoding='utf-8').read()
count1 = content.count('href="#"')
content = content.replace('href="#"', 'href="' + note_url + '"')
open('app/page.tsx', 'w', encoding='utf-8').write(content)
print("page.tsx: replaced %d links" % count1)

# about/page.tsx
content2 = open('app/about/page.tsx', 'r', encoding='utf-8').read()
count2 = content2.count('href="#"')
content2 = content2.replace('href="#"', 'href="' + note_url + '"')
open('app/about/page.tsx', 'w', encoding='utf-8').write(content2)
print("about/page.tsx: replaced %d links" % count2)

print("DONE")
