import sys
file_path = 'C:\\Git\\repositories\\jangut.github.io\\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert TOC CSS before </style>
toc_css = '''
  .toc-panel {
    position: sticky;
    top: 0;
    width: 220px;
    min-width: 220px;
    flex-shrink: 0;
    background: var(--bg-panel);
    border-left: 1px solid var(--line);
    display: none;
    flex-direction: column;
    overflow: hidden;
    height: 100%;
    align-self: flex-start;
  }
  .toc-panel.open {
    display: flex;
  }
  .toc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px 10px;
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    border-bottom: 1px solid var(--line);
    flex-shrink: 0;
  }
  .toc-close {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 16px;
    padding: 2px 6px;
    border-radius: 4px;
    line-height: 1;
  }
  .toc-close:hover {
    background: var(--bg-elevated);
    color: var(--text-primary);
  }
  .toc-body {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
  }
  .toc-item {
    display: block;
    padding: 7px 18px;
    font-size: 13px;
    line-height: 1.4;
    color: var(--text-secondary);
    text-decoration: none;
    border-left: 2px solid transparent;
    transition: all .12s;
    cursor: pointer;
  }
  .toc-item:hover {
    color: var(--text-primary);
    background: var(--bg-elevated);
    border-left-color: var(--accent-cyan);
  }
  .toc-item.active {
    color: var(--accent-cyan);
    border-left-color: var(--accent-cyan);
    background: var(--accent-cyan-dim);
  }
  .toc-item.level-3 {
    padding-left: 30px;
    font-size: 12px;
  }
  .toc-empty {
    padding: 24px 18px;
    text-align: center;
    color: var(--text-muted);
    font-size: 12px;
    font-family: var(--mono);
  }
  .toc-toggle {
    display: flex;
    align-items: center;
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    font-size: 14px;
    padding: 9px 12px;
    border-radius: 8px 8px 0 0;
    margin: 4px 4px 0 0;
    transition: color .15s, background .15s;
    white-space: nowrap;
  }
  .toc-toggle:hover {
    color: var(--text-secondary);
    background: var(--bg-elevated);
  }
  .toc-toggle.active {
    color: var(--accent-cyan);
  }
'''
content = content.replace('</style>', toc_css + '</style>', 1)
print('1. CSS inserted:', 'toc-panel' in content)

# 2. Insert TOC toggle button after home tab
old_tab = '''<button class="tab active" data-panel="panel-index"><span class="file-dot" style="color:var(--accent-cyan)">●</span>首页</button>'''
new_tab = old_tab + '\n        <button class="toc-toggle" id="tocToggle" title="显示/隐藏目录">📑</button>'
content = content.replace(old_tab, new_tab, 1)
print('2. Toggle inserted:', 'tocToggle' in content)

# 3. Insert TOC panel HTML after editor-body-inner closing div
toc_panel = '''
        <div class="toc-panel" id="tocPanel">
          <div class="toc-header">
            <span>&#x1F4D1; 目录</span>
            <button class="toc-close" id="tocClose" title="关闭目录">&#x2715;</button>
          </div>
          <div class="toc-body" id="tocBody"></div>
        </div>'''
content = content.replace(
    '</div>\n      </div>\n\n      <div class="statusbar">',
    '</div>' + toc_panel + '\n      </div>\n\n      <div class="statusbar">'
)
print('3. Panel inserted:', 'tocPanel' in content)

# 4. TOC JS functions
toc_js = '''

  // === TOC (目录) ===
  var tocVisible = false;

  function buildTOC() {
    var panel = document.querySelector('.panel.active');
    if (!panel) return;
    var headings = panel.querySelectorAll('h2, h3');
    var container = document.getElementById('tocBody');
    if (!container) return;
    if (headings.length === 0) {
      container.innerHTML = '<div class="toc-empty">无目录</div>';
      return;
    }
    var html = '';
    headings.forEach(function(h, idx) {
      var level = h.tagName === 'H2' ? 2 : 3;
      var text = h.textContent.trim();
      if (!text) return;
      var id = 'toc-h-' + idx;
      h.id = id;
      html += '<a class="toc-item level-' + level + '" data-toc-id="' + id + '">' + text + '</a>';
    });
    container.innerHTML = html;

    container.querySelectorAll('.toc-item').forEach(function(item) {
      item.addEventListener('click', function() {
        var target = document.getElementById(this.dataset.tocId);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          container.querySelectorAll('.toc-item.active').forEach(function(a) { a.classList.remove('active'); });
          this.classList.add('active');
        }
      });
    });
  }

  function showTOC() {
    buildTOC();
    var tp = document.getElementById('tocPanel');
    var tt = document.getElementById('tocToggle');
    if (tp) tp.classList.add('open');
    if (tt) tt.classList.add('active');
    tocVisible = true;
  }

  function hideTOC() {
    var tp = document.getElementById('tocPanel');
    var tt = document.getElementById('tocToggle');
    if (tp) tp.classList.remove('open');
    if (tt) tt.classList.remove('active');
    tocVisible = false;
  }

  function toggleTOC() {
    if (tocVisible) { hideTOC(); }
    else { showTOC(); }
  }

  document.getElementById('tocToggle').addEventListener('click', toggleTOC);
  document.getElementById('tocClose').addEventListener('click', hideTOC);

  // Auto-show TOC when switching to a doc panel
  var origSwitch = window.switchToPanel;
  if (origSwitch) {
    window.switchToPanel = function(panelId) {
      origSwitch(panelId);
      if (panelId && panelId.indexOf('panel-doc-') !== -1) {
        setTimeout(function() { buildTOC(); showTOC(); }, 100);
      } else {
        hideTOC();
      }
    };
  }'''

# Insert TOC functions before "// Sidebar md links"
content = content.replace(
    '  }\n\n\n  // Sidebar md links',
    '  }\n\n  // === TOC ===\n  function initTOC() {\n    var tt = document.getElementById(\'tocToggle\');\n    var tc = document.getElementById(\'tocClose\');\n    if (tt) tt.addEventListener(\'click\', toggleTOC);\n    if (tc) tc.addEventListener(\'click\', hideTOC);\n\n    var os = window.switchToPanel;\n    if (os) {\n      window.switchToPanel = function(pid) {\n        os(pid);\n        if (pid && pid.indexOf(\'panel-doc-\') !== -1) {\n          setTimeout(function() { buildTOC(); showTOC(); }, 100);\n        } else {\n          hideTOC();\n        }\n      };\n    }\n  }\n  initTOC();\n\n  // Sidebar md links'
)
print('4. TOC JS inserted:', 'initTOC' in content)

# Add hideTOC() call in closeDoc
content = content.replace(
    "switchToPanel('panel-index');\n    }",
    "switchToPanel('panel-index');\n      hideTOC();\n    }"
)
print('5. hideTOC in closeDoc:', content.count('hideTOC()') > 1)

# Add buildTOC after renderMathInElement
content = content.replace(
    'renderMathInElement(panel, {delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}]});\n        }',
    'renderMathInElement(panel, {delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}]});\n        }\n        setTimeout(buildTOC, 100);'
)
print('6. buildTOC after render:', 'setTimeout(buildTOC' in content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\\nAll done!')