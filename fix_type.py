content = open('app/page.tsx', 'r', encoding='utf-8').read()

old = 'Record<keyof NonNullable<Row["risk_checks"]>, TooltipContent>'
count = content.count(old)
print(f'Found: {count}')

if count > 0:
    content = content.replace(old, 'Record<string, TooltipContent>')
    open('app/page.tsx', 'w', encoding='utf-8').write(content)
    print('DONE')
else:
    # Try with escaped quotes
    old2 = "Record<keyof NonNullable<Row['risk_checks']>, TooltipContent>"
    count2 = content.count(old2)
    print(f'Alt found: {count2}')
    if count2 > 0:
        content = content.replace(old2, 'Record<string, TooltipContent>')
        open('app/page.tsx', 'w', encoding='utf-8').write(content)
        print('DONE')
    else:
        # Search for any Record<keyof pattern
        idx = content.find('Record<keyof')
        if idx > 0:
            print(f'Found Record<keyof at {idx}:')
            print(repr(content[idx:idx+80]))
        else:
            print('NOT FOUND - already fixed?')
