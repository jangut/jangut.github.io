import sys
file_path = 'C:\\Git\\repositories\\jangut.github.io\\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Debug
print("1. editor-body HTML:", '<div class="editor-body">' in c)
print("2. toc-panel:", '<div class="toc-panel"' in c)
print("3. editor-main HTML wrapper:", '<div class="editor-main">' in c)
print("4. editor-main CSS:", '.editor-main' in c)
print("5. toc-toggle margin:", 'margin-left: auto' in c)
print("6. toc-panel absolute:", 'position: absolute' in c)

# Steps 3-5 from previous run
# Find the first occurrence of HTML editor-body (not CSS)
html_body = '<div class="editor-body">'
# Find it after the style tag to skip the CSS section
style_end_pos = c.find('</style>')
idx = c.find(html_body, style_end_pos)
print("editor-body HTML tag at index:", idx)

if idx > 0:
    # Check it's not already wrapped
    # Look 100 chars before idx for 'editor-main'
    area_before = c[max(0,idx-100):idx]
    if 'editor-main' not in area_before:
        # Replace with wrapper
        c = c[:idx] + '<div class="editor-main">' + c[idx:]

# Close editor-body before toc-panel
toc_div = '<div class="toc-panel" id="tocPanel">'
toc_idx = c.find(toc_div, style_end_pos)
if toc_idx > 0:
    # Find the line before toc-panel that should close editor-body
    # We need to insert </div> right before toc_panel opens
    before_text = c[max(0,toc_idx-400):toc_idx]
    last_div_close = before_text.rfind('</div>')
    if last_div_close >= 0:
        # Found the </div> that closes editor-body-inner
        # Insert a new </div> after it to close editor-body
        real_idx = max(0,toc_idx-400) + last_div_close + 6
        insert_text = '\n      </div>'
        c = c[:real_idx] + insert_text + c[real_idx:]
        print("Inserted editor-body close before toc-panel")

# Add editor-main CSS
editor_css_end = '''  .editor-body{
    flex: 1;
    overflow-y: auto;
    background: var(--bg-void);
    display: flex;
    justify-content: center;
  }'''
css_idx = c.find(editor_css_end)
if css_idx > 0:
    # Check if editor-main CSS already exists
    if '.editor-main' not in c[:css_idx]:
        editor_main_css = '''
  .editor-main {
    flex: 1;
    display: flex;
    min-height: 0;
    min-width: 0;
  }'''
        c = c[:css_idx] + editor_main_css + c[css_idx:]
        print("Added editor-main CSS")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)
print()
print("After fixes:")
print("- editor-main HTML wrapper:", '<div class="editor-main">' in c)
print("- editor-body close before toc:", 'toc-panel' in c)
print("- editor-main CSS:", '.editor-main' in c)
print("- toc-toggle margin:", 'margin-left: auto' in c)
print("- toc-panel absolute:", 'position: absolute' in c)