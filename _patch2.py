import sys

file_path = 'C:\\Git\\repositories\\jangut.github.io\\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# TOC functions to insert before '// Sidebar md links'
toc_functions = '''
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
  }

'''

# Insert before '// Sidebar md links'
marker = '// Sidebar md links'
idx = c.index(marker)
c = c[:idx] + toc_functions + c[idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

# Verify
with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

print('function buildTOC:', 'function buildTOC' in c)
print('function showTOC:', 'function showTOC' in c)
print('function hideTOC:', 'function hideTOC' in c)
print('tocToggle.addEventListener:', 'tocToggle.addEventListener' in c)
print('origSwitch:', 'origSwitch' in c)
print('tocPanel in body:', 'tocPanel' in c)
print('toc-toggle CSS:', 'toc-toggle' in c)
print('setTimeout(buildTOC):', 'setTimeout(buildTOC' in c)