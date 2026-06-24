import http.server, json, os, re, sys, urllib.parse, html as hm

BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, 'source', 'document')

def parse_tree():
    with open(os.path.join(BASE,'index.html'), encoding='utf-8') as f:
        h = f.read()
    folders = []
    # Split on folder divs (more robust than single regex)
    parts = h.split('<div class="folder')
    for part in parts[1:]:
        is_open = ' open"' in part[:20]
        fb = re.search(r'<button class="folder-toggle">.*?<span class="folder-icon">[^<]*</span>\s*(.*?)</button>', part)
        if not fb: continue
        name = fb.group(1).strip()
        files = []
        for fm in re.finditer(
            r'<li><a href="#" data-md="([^"]*)"[^>]*>'
            r'<span class="file-dot">[^<]*</span>([^<]+?)'
            r'<span class="doc-cat[^"]*"[^>]*>([^<]*)</span></a></li>',
            part, re.DOTALL
        ):
            files.append({
                'path': fm.group(1),
                'title': hm.unescape(fm.group(2)).strip(),
                'cat': fm.group(3).strip()
            })
        folders.append({'name': name, 'open': is_open, 'files': files})
    gm = re.search(r'<a href="(game/index\.html)" class="sidebar-game-link">', h)
    lb = re.search(r'<div class="label">([^<]*)</div>', h[h.find('sidebar-footer'):])
    return {
        'folders': folders,
        'game': gm.group(1) if gm else '',
        'label': hm.unescape(lb.group(1)).strip() if lb else ''
    }


def scan_docs():
    """扫描 source/document/ 返回 .md 列表"""
    files = []
    for fn in os.listdir(DOCS):
        if not fn.endswith('.md'): continue
        fp = os.path.join(DOCS, fn)
        with open(fp, encoding='utf-8') as f:
            text = f.read()
        title = fn.replace('.md','')
        cat = '其他'
        m = re.search(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
        if m:
            fm = m.group(1)
            tv = re.search(r'^title\s*:\s*(.+)$', fm, re.MULTILINE)
            cv = re.search(r'^category\s*:\s*(.+)$', fm, re.MULTILINE)
            if tv: title = tv.group(1).strip().strip("\"'")
            if cv: cat = cv.group(1).strip().strip("\"'")
        files.append({'path': 'source/document/'+fn, 'title': title, 'cat': cat})
    return sorted(files, key=lambda x: x['title'])

def rebuild_html(tree):
    with open(os.path.join(BASE,'index.html'), encoding='utf-8') as f:
        h = f.read()
    start = h.find('<div class="root-label">')
    end = h.find('</nav>', start)
    cats = {'\u6280\u672f': 'cat-tech', '\u7406\u8bba': 'cat-theory'}
    nt = '        <div class="root-label"><span class="chev">\u25be</span> blog/</div>\n'
    for fld in tree['folders']:
        op = ' open' if fld['open'] else ''
        nt += f'        <div class="folder{op}">\n'
        nt += f'          <button class="folder-toggle"><span class="chev">\u25b8</span><span class="folder-icon">\U0001f4c1</span> {fld["name"]}</button>\n'
        nt += '          <ul class="files">\n'
        for f in fld['files']:
            cc = cats.get(f['cat'], 'cat-other')
            icon = '\U0001F527' if f['cat'] == '\u6280\u672f' else '\U0001F4D8' if f['cat'] == '\u7406\u8bba' else '\u00b7'
            nt += f'            <li><a href="#" data-md="{f["path"]}" data-folder="{fld["name"]}" data-file="{f["title"]}" data-category="{f["cat"]}"><span class="file-dot">{icon}</span>{f["title"]}<span class="doc-cat {cc}">{f["cat"]}</span></a></li>\n'
        nt += '          </ul>\n        </div>\n'
    nt += f'        <a href="{tree["game"]}" class="sidebar-game-link">\n          <span style="width:20px;text-align:center">\U0001f3ae</span>\n          \u6e38\u620f\u76d2\u5b50\n        </a>\n'
    h = h[:start] + nt + h[end:]
    lbm = re.search(r'(<div class="label">)[^<]*(</div>)', h[h.find('sidebar-footer'):])
    if lbm and tree.get('label'):
        pos = h.find('sidebar-footer') + lbm.start(1)
        h = h[:pos] + lbm.group(1) + tree['label'] + lbm.group(2) + h[pos+len(lbm.group(0)):]
    with open(os.path.join(BASE,'index.html'), 'w', encoding='utf-8') as f:
        f.write(h)

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        p = urllib.parse.urlparse(self.path)
        if p.path == '/api/tree':
            self.json(parse_tree())
        elif p.path == '/api/docs':
            self.json(scan_docs())
        elif p.path == '/':
            self.send_response(200)
            self.send_header('Content-Type','text/html;charset=utf-8')
            self.end_headers()
            ui_path = os.path.join(BASE, os.path.dirname(__file__), 'manager_ui.html')
            alt = os.path.join(BASE, 'manager_ui.html')
            for fp in [ui_path, alt]:
                if os.path.exists(fp):
                    self.wfile.write(open(fp,'rb').read())
                    return
            self.wfile.write(b'manager_ui.html not found')
        else:
            super().do_GET()
    def do_POST(self):
        p = urllib.parse.urlparse(self.path)
        n = int(self.headers.get('Content-Length',0))
        b = json.loads(self.rfile.read(n)) if n else {}
        if p.path == '/api/save':
            rebuild_html(b)
            self.json({'ok':True})
        else:
            self.json({'error':'not found'}, 404)
    def json(self, d, c=200):
        self.send_response(c)
        self.send_header('Content-Type','application/json;charset=utf-8')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps(d,ensure_ascii=False).encode())

UI_HTML = '''
<!DOCTYPE html>
<html>
</html>
'''

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv)>1 else 8080
    http.server.HTTPServer(('0.0.0.0',port), H).serve_forever()



