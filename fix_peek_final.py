import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix left peek (sidebar-peek) — should be plain 文件
html = html.replace(
    '<button class="sidebar-peek" id="sidebarPeek" aria-label="打开侧边栏">\n      <span class="peek-label toc-label">📑目录</span>',
    '<button class="sidebar-peek" id="sidebarPeek" aria-label="打开侧边栏">\n      <span class="peek-label">\U0001F5C2\U0000FE0F\u6587\u4EF6</span>'
)

# Fix right peek (toc-peek) — should be vertical 目录  
html = html.replace(
    '<button class="toc-peek" id="tocPeek" title="显示目录">\n      <span class="peek-label toc-label">📑目录</span>',
    '<button class="toc-peek" id="tocPeek" title="显示目录">\n      <span class="peek-label toc-label">\U0001F4D1\u76EE\u5F55</span>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('fixed')
