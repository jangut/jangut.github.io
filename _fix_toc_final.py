import sys

file_path = "C:\\Git\\repositories\\jangut.github.io\\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Remove toc-toggle from tabbar
c = c.replace(
    '        <button class="toc-toggle" id="tocToggle" title="显示/隐藏目录">📑</button>\n',
    ''
)

# 2. Add toc-peek after sidebar-peek close
c = c.replace(
    '      </button>\n\n      <div class="editor-main">',
    '      </button>\n\n      <button class="toc-peek" id="tocPeek" title="显示目录">\n        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>\n      </button>\n\n      <div class="editor-main">'
)

# 3. Replace CSS
old_css = "  .toc-toggle {"
new_css = '  .toc-peek {\n    display: flex;\n    position: fixed;\n    right: 0;\n    top: 50%;\n    transform: translateY(-50%);\n    width: 22px;\n    height: 44px;\n    background: var(--bg-panel);\n    border: 1px solid var(--line);\n    border-right: none;\n    border-radius: 6px 0 0 6px;\n    color: var(--text-muted);\n    cursor: pointer;\n    z-index: 25;\n    align-items: center;\n    justify-content: center;\n    padding: 0;\n  }\n  .toc-peek:hover { opacity: .8; }\n  .toc-peek.hidden { display: none; }\n  .toc-peek svg { width: 14px; height: 14px; }'

# Find toc-toggle CSS block and replace all related blocks
idx = c.find(old_css)
if idx >= 0:
    # Find end of .toc-toggle:hover block
    hover_start = c.find(".toc-toggle:hover", idx)
    active_start = c.find(".toc-toggle.active", idx)
    # Find end of last block
    if active_start > 0:
        end = c.find("}", active_start) + 1
    elif hover_start > 0:
        end = c.find("}", hover_start) + 1
    else:
        end = c.find("}", idx) + 1
    
    # Clean up: include trailing whitespace
    after_end = end
    while after_end < len(c) and c[after_end] in '\n\r ':
        after_end += 1
    c = c[:idx] + new_css + '\n' + c[after_end:]

# 4. Update JS references (use simple pattern matching)
c = c.replace(
    "document.getElementById('tocToggle').addEventListener('click', toggleTOC);",
    "document.getElementById('tocPeek').addEventListener('click', toggleTOC);"
)
c = c.replace(
    "    var tt = document.getElementById('tocToggle');",
    "    var tt = document.getElementById('tocPeek');"
)

# 5. Add hidden class toggle in showTOC/hideTOC
c = c.replace(
    "    if (tt) { tt.classList.add('hidden'); }\n    tocVisible = true;",
    "    if (tt) { tt.classList.add('hidden'); }\n    tocVisible = true;"
)
c = c.replace(
    "    if (tt) tt.classList.remove('active');\n    tocVisible = false;",
    "    if (tt) { tt.classList.remove('hidden'); }\n    tocVisible = false;"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(c)

print("Done")
v = open(file_path, "r", encoding="utf-8").read()
print("No toc-toggle:", 'class="toc-toggle"' not in v)
print("Has toc-peek:", 'class="toc-peek"' in v)
print("Has toc-peek CSS:", ".toc-peek {" in v)
print("Has addEventListener:", "tocPeek').addEventListener" in v)
print("Has hidden class logic:", "classList.add('hidden')" in v)