#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_doc.py — 自动将 Markdown 文章添加到 blog 网站侧边栏

用法:
    python add_doc.py                     # 扫描 source/document/ 所有 .md
    python add_doc.py source/document/文件名.md   # 只添加指定文件

Markdown 文件支持 YAML frontmatter:
---
title: 文章标题
category: 技术     # 可选: 技术 / 理论 / 其他（默认）
folder: 控制理论     # 可选: 侧边栏文件夹名，默认用文件所在子目录名
---
"""

import re
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, 'source', 'document')
HTML_PATH = os.path.join(BASE_DIR, 'index.html')

CAT_CLASSES = {
    '技术': 'cat-tech',
    '理论': 'cat-theory',
}


def extract_meta(md_path):
    """从 Markdown 文件提取 title, category, folder"""
    title = category = folder = None
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f'  \u2717 \u8bfb\u53d6\u5931\u8d25: {e}')
        return None, None, None

    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if m:
        fm = m.group(1)
        tv = re.search(r'^title\s*:\s*(.+)$', fm, re.MULTILINE)
        cv = re.search(r'^category\s*:\s*(.+)$', fm, re.MULTILINE)
        fv = re.search(r'^folder\s*:\s*(.+)$', fm, re.MULTILINE)
        if tv:
            title = tv.group(1).strip().strip("\"'")
        if cv:
            category = cv.group(1).strip().strip("\"'")
        if fv:
            folder = fv.group(1).strip().strip("\"'")

    if not title:
        h1 = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1:
            title = h1.group(1).strip()
    if not title:
        title = os.path.splitext(os.path.basename(md_path))[0]

    rel_dir = os.path.relpath(os.path.dirname(md_path), DOCS_DIR)
    if not folder:
        folder = rel_dir if rel_dir != '.' else '\u672a\u5206\u7c7b'

    if not category:
        category = '\u5176\u4ed6'

    return title.strip(), category.strip(), folder.strip()


def build_entry(md_rel, folder, title, category):
    """构建 li 条目 HTML"""
    cc = CAT_CLASSES.get(category, 'cat-other')
    md_file = os.path.splitext(os.path.basename(md_rel))[0]
    return (
        '            <li><a href="#" '
        f'data-md="{md_rel}" '
        f'data-folder="{folder}" '
        f'data-file="{md_file}" '
        f'data-category="{category}">'
        '<span class="file-dot">\u00b7</span>'
        f'{title}'
        f'<span class="doc-cat {cc}">{category}</span></a></li>'
    )


def find_or_create_folder(html, folder):
    """查找文件夹位置，不存在则创建。返回 (html, insert_pos)。"""
    pat = re.compile(
        r'(<button\s+class="folder-toggle">'
        r'<span\s+class="chev">\u25b8</span>'
        r'<span\s+class="folder-icon">\U0001f4c1</span>\s*'
        + re.escape(folder) +
        r'\s*</button>\s*<ul\s+class="files">)\s*'
    )
    m = pat.search(html)
    if m:
        return html, m.end()

    # 文件夹不存在，在游戏链接之前创建
    insert_m = re.search(r'(<a\s+href="game/index\.html)', html)
    if not insert_m:
        print(f'  \u2717 \u627e\u4e0d\u5230\u63d2\u5165\u4f4d\u7f6e')
        return html, -1

    folder_html = (
        f'\n        <div class="folder">\n'
        f'          <button class="folder-toggle">'
        f'<span class="chev">\u25b8</span>'
        f'<span class="folder-icon">\U0001f4c1</span> {folder}</button>\n'
        f'          <ul class="files">\n'
        f'          </ul>\n'
        f'        </div>\n'
    )
    pos = insert_m.start()
    html = html[:pos] + folder_html + html[pos:]

    # 重新定位新文件夹的插入点
    m2 = pat.search(html)
    if m2:
        return html, m2.end()
    return html, -1


def add_doc(md_path):
    """处理单个 md 文件"""
    md_rel = os.path.relpath(md_path, BASE_DIR).replace('\\', '/')
    title, category, folder = extract_meta(md_path)
    if not title:
        print(f'  \u2717 \u5199\u4f5c\u5355\u5143\u672a\u547d\u540d\u8df3\u8fc7: {md_rel}')
        return False

    print(f'  \u6807\u9898: {title}')
    print(f'  \u5206\u7c7b: {category}')
    print(f'  \u6587\u4ef6\u5939: {folder}')

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    if f'data-md="{md_rel}"' in html:
        print(f'  \u26a0\ufe0f \u5df2\u5728\u4fa7\u8fb9\u680f\u4e2d\uff0c\u8df3\u8fc7')
        return False

    html, pos = find_or_create_folder(html, folder)
    if pos < 0:
        return False

    entry = '\n' + build_entry(md_rel, folder, title, category)
    html = html[:pos] + entry + html[pos:]

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'  \u2705 \u5df2\u6dfb\u52a0\u5230\u300c{folder}\u300d\u6587\u4ef6\u5939')
    return True


def main():
    args = sys.argv[1:]
    if args:
        files = [os.path.join(BASE_DIR, a) for a in args]
    else:
        files = []
        for root, dirs, fnames in os.walk(DOCS_DIR):
            for fn in fnames:
                if fn.endswith('.md'):
                    files.append(os.path.join(root, fn))
        files.sort()

    if not files:
        print('\u6ca1\u6709\u627e\u5230 Markdown \u6587\u4ef6\u3002')
        return

    succ = 0
    for fp in files:
        fp = os.path.abspath(fp)
        if not os.path.isfile(fp):
            print(f'  \u2717 \u6587\u4ef6\u4e0d\u5b58\u5728: {fp}')
            continue
        print(f'\n\U0001f4c4 {os.path.relpath(fp, BASE_DIR)}')
        if add_doc(fp):
            succ += 1

    print(f'\n\u5b8c\u6210: {succ}/{len(files)} \u4e2a\u6587\u4ef6\u5df2\u5904\u7406')


if __name__ == '__main__':
    main()
