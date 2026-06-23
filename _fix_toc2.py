import sys

file_path = "C:\\Git\\repositories\\jangut.github.io\\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
lines = content.split("\n")

# 1. Remove the toc-toggle button from tabbar (remove line 757, 0-indexed)
# Find and remove the toc-toggle line
for i, l in enumerate(lines):
    if 'toc-toggle' in l and 'id="tocToggle"' in l:
        togg_line = i
        break

print(f"toc-toggle at line: {togg_line}")
lines = lines[:togg_line] + lines[togg_line+1:]

# 2. Add toc-peek button after sidebar-peek close
for i, l in enumerate(lines):
    if 'sidebar-peek' in l and '</button>' in l:
        peek_close = i
        break

print(f"sidebar-peek close at line: {peek_close}")

toc_peek_html = [
    '',
    '      <button class="toc-peek" id="tocPeek" title="显示目录">',
    '        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>',
    '      </button>',
    '',
]
lines = lines[:peek_close+1] + toc_peek_html + lines[peek_close+1:]

content_new = "\n".join(lines)

# 3. Update JS references: tocToggle -> tocPeek
# The addEventListener line
old_js1 = "document.getElementById('tocToggle').addEventListener('click', toggleTOC);"
new_js1 = "document.getElementById('tocPeek').addEventListener('click', toggleTOC);"
content_new = content_new.replace(old_js1, new_js1)

# The showTOC function
old_js2 = "    var tt = document.getElementById('tocToggle');"
new_js2 = "    var tt = document.getElementById('tocPeek');"
content_new = content_new.replace(old_js2, new_js2)

# 4. Replace toc-toggle CSS with toc-peek CSS
toc_peek_css = '''  .toc-peek {
    display: flex;
    position: fixed;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 22px;
    height: 44px;
    background: var(--bg-panel);
    border: 1px solid var(--line);
    border-right: none;
    border-radius: 6px 0 0 6px;
    color: var(--text-muted);
    cursor: pointer;
    z-index: 25;
    align-items: center;
    justify-content: center;
    padding: 0;
  }
  .toc-peek:hover { opacity: .8; }
  .toc-peek.hidden { display: none; }
  .toc-peek svg { width: 14px; height: 14px; }
'''

# Find and remove the old toc-toggle CSS blocks
toggle_start = content_new.find('.toc-toggle {')
toggle_hover_start = content_new.find('.toc-toggle:hover')
toggle_active_start = content_new.find('.toc-toggle.active')

toggle_hover_end = content_new.find('}', toggle_hover_start) + 1
toggle_active_end = content_new.find('}', toggle_active_start) + 1

# Remove all three blocks and insert toc-peek CSS at toggle_start
# The .toc-toggle.active block might not exist after earlier modifications
# Let's handle it gracefully
end_of_old_css = max(toggle_hover_end - 1, toggle_active_end - 1)
# Find the next line after the last block
# Actually, let's just remove from toggle_start to toggle_active_end
end = max(toggle_hover_end, toggle_active_end)
# But there might be .toc-toggle.active block too
# Find the next selector after all toggle blocks
search_from = toggle_active_start + 10 if toggle_active_start > 0 else toggle_hover_start + 10
next_select = content_new.find('\n  .', search_from)
if next_select > 0:
    cleanup = content_new[toggle_start:next_select+1]
    # Check what we're removing
    print("Removing CSS block:")
    print(cleanup[:200] + "...")
    content_new = content_new[:toggle_start] + toc_peek_css + '\n' + content_new[next_select+1:]

# Also remove any margin-left:auto from old toc-toggle CSS that might remain
content_new = content_new.replace('margin: 4px 4px 0 auto;\n  }\n\n  .toc-peek', '.toc-peek')

# 5. Update showTOC/hideTOC to show/hide the peek button
# In showTOC: after making tp visible, hide the peek
showTOC_idx = content_new.find('function showTOC() {')
if showTOC_idx > 0:
    # Find the line where tocVisible = true is set
    visible_line = content_new.find('tocVisible = true;', showTOC_idx)
    if visible_line > 0:
        # Find the start of that line
        line_start = content_new.rfind('\n', 0, visible_line) + 1
        indent = content_new[line_start:visible_line].rstrip()
        insert = indent + 'document.getElementById(\'tocPeek\').classList.add(\'hidden\');\n'
        content_new = content_new[:visible_line] + insert + content_new[visible_line:]

# In hideTOC: after making tp invisible, show the peek
hideTOC_idx = content_new.find('function hideTOC() {')
if hideTOC_idx > 0:
    visible_line2 = content_new.find('tocVisible = false;', hideTOC_idx)
    if visible_line2 > 0:
        line_start2 = content_new.rfind('\n', 0, visible_line2) + 1
        indent2 = content_new[line_start2:visible_line2].rstrip()
        insert2 = indent2 + 'document.getElementById(\'tocPeek\').classList.remove(\'hidden\');\n'
        content_new = content_new[:visible_line2] + insert2 + content_new[visible_line2:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content_new)

print("\nAll done!")
print("Has toc-peek button:", 'tocPeek' in content_new)
print("Has toc-peek CSS:", '.toc-peek {' in content_new)
print("No toc-toggle in HTML:", 'toc-toggle' not in content_new or 'class="toc-toggle"' not in content_new)
print("Has peek show/hide:", 'tocPeek' in content_new)
