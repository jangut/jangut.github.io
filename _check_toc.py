import sys
lines = open("C:\\Git\\repositories\\jangut.github.io\\index.html", "r", encoding="utf-8").read().split("\n")
for i, l in enumerate(lines):
    if 'tocToggle' in l:
        print(f"tabbar TOC btn [{i}]:", l.strip())
for i, l in enumerate(lines):
    if 'editor-main' in l and 'class=' in l:
        print(f"editor-main [{i}]:", l.strip())
for i, l in enumerate(lines):
    if 'toc-panel' in l and 'class=' in l:
        print(f"toc-panel [{i}]:", l.strip())
for i, l in enumerate(lines):
    if 'position: absolute' in l:
        print(f"ABSOLUTE RESIDUE [{i}]:", l.strip())
for i, l in enumerate(lines):
    if 'margin-left: auto' in l:
        print(f"margin-left: [{i}]:", l.strip())