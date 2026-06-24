import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Restore article div class (remove content-view)
html = html.replace(
    '<div class="content-view article-body" style="max-width:780px;margin:0 auto;padding:24px;">' + "'" + ' + marked.parse(text) + ' + "'" + '</div>',
    '<div class="article-body" style="max-width:780px;margin:0 auto;padding:24px;">' + "'" + ' + marked.parse(text) + ' + "'" + '</div>'
)

# 2. Change all CSS selectors
html = html.replace('.content-view.article-body', '.article-body')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('fixed')
