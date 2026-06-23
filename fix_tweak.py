import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Lower peek opacity: 0.18 → 0.10
html = html.replace('    opacity: 0.18;', '    opacity: 0.10;')

# 2. Add label back to sidebar footer
# Find the cat-wrap inside sidebar-footer
html = html.replace(
    '<div class="sidebar-footer">\n        <div class="cat-wrap"',
    '<div class="sidebar-footer">\n        <div class="label">\u732b\u732b</div>\n        <div class="cat-wrap"'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
