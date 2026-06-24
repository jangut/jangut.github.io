import http.server, json, os, re, sys, urllib.parse, html as hm
BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, "source", "document")
HTML_PATH = os.path.join(BASE, "index.html")
PORT = int(os.environ.get("PORT", "8080"))
_tree_cache = None

def rj(o): return json.dumps(o, ensure_ascii=False).encode("utf-8")
def send_json(h, code, obj):
    h.send_response(code)
    h.send_header("Content-Type","application/json; charset=utf-8")
    h.send_header("Access-Control-Allow-Origin","*")
    h.end_headers()
    h.wfile.write(rj(obj))
def send_text(h, code, text, ct="text/plain; charset=utf-8"):
    h.send_response(code)
    h.send_header("Content-Type",ct)
    h.send_header("Access-Control-Allow-Origin","*")
    h.end_headers()
    h.wfile.write(text.encode("utf-8"))

def default_tags():
    return [{"name":"\u6280\u672f","icon":"\U0001f527"},{"name":"\u7406\u8bba","icon":"\U0001f4d8"},{"name":"\u60f3\u6cd5","icon":"\U0001f4a1"},{"name":"\u5176\u4ed6","icon":"\u00b7"}]

def parse_tree():
    global _tree_cache
    if _tree_cache: return _tree_cache
    try:
        with open(HTML_PATH,"r",encoding="utf-8") as f: html = f.read()
    except: return {"folders":[],"tags":default_tags()}
    folders = []
    m = re.search(r"<nav\s+class=\"tree\">(.*?)</nav>",html,re.DOTALL)
    if not m:
        _tree_cache = {"folders":[],"tags":default_tags()}; return _tree_cache
    nav_cont = m.group(1)
    fpat = re.compile(r'<div\s+class="folder(\s*open)?">\s*<button\s+class="folder-toggle">(.*?)</button>\s*<ul\s+class="files">(.*?)</ul>\s*</div>',re.DOTALL)
    for fm in fpat.finditer(nav_cont):
        is_open = bool(fm.group(1) and "open" in fm.group(1))
        name = re.sub(r"<[^>]+>","",fm.group(2)).strip()
        name = re.sub(r"^ *\U0001f4c1 *","",name).strip()
        files = []
        ipat = re.compile(r'<li><a\s+href="#"\s+data-md="(.*?)"\s+data-folder="(.*?)"\s+data-file="(.*?)"\s+data-category="(.*?)">',re.DOTALL)
        for fi in ipat.finditer(fm.group(3)):
            files.append({"path":fi.group(1),"title":fi.group(3),"cat":fi.group(4)})
        folders.append({"name":name,"open":is_open,"files":files})
    tags = _parse_tags_from_js(html)
    _tree_cache = {"folders":folders,"tags":tags}
    return _tree_cache

def _parse_tags_from_js(html):
    tags = []
    pat = re.compile(r"category\s*===\s*'([^']+)'\)\s*catIcon\s*=\s*'([^']*)'")
    for m in pat.finditer(html):
        tags.append({"name":m.group(1),"icon":m.group(2) or "\u00b7"})
    return tags if tags else default_tags()

def invalidate_cache():
    global _tree_cache; _tree_cache = None

def scan_docs():
    out = []
    if not os.path.isdir(DOCS): return out
    for fn in sorted(os.listdir(DOCS)):
        if not fn.endswith(".md"): continue
        fp = os.path.join(DOCS, fn)
        title, cat = _extract_meta(fp)
        out.append({"path":"source/document/"+fn,"title":title,"cat":cat})
    return out

def _extract_meta(fp):
    title = cat = None
    try:
        with open(fp,"r",encoding="utf-8") as f: c = f.read()
    except: return os.path.splitext(os.path.basename(fp))[0],"\u5176\u4ed6"
    m = re.match(r"^---\s*\n(.*?)\n---",c,re.DOTALL)
    if m:
        fm = m.group(1)
        tv = re.search(r"^title\s*:\s*(.+)$",fm,re.MULTILINE)
        cv = re.search(r"^category\s*:\s*(.+)$",fm,re.MULTILINE)
        if tv: title = tv.group(1).strip().strip("\"'")
        if cv: cat = cv.group(1).strip().strip("\"'")
    if not title:
        h1 = re.search(r"^#\s+(.+)$",c,re.MULTILINE)
        if h1: title = h1.group(1).strip()
    if not title: title = os.path.splitext(os.path.basename(fp))[0]
    if not cat: cat = "\u5176\u4ed6"
    return title, cat

def rebuild_html(tree):
    try:
        with open(HTML_PATH,"r",encoding="utf-8") as f: html = f.read()
    except: return False
    tags = tree.get("tags",default_tags())
    def ic(cat):
        for t in tags:
            if t["name"]==cat: return t.get("icon","\u00b7")
        return "\u00b7"
    th = '<nav class="tree">\n        <div class="root-label"><span class="chev">\u25be</span> blog/</div>\n'
    for fol in tree.get("folders",[]):
        oc = " open" if fol.get("open",True) else ""
        fn = fol.get("name","\u672a\u547d\u540d")
        th += '        <div class="folder%s">\n          <button class="folder-toggle"><span class="chev">\u25b8</span><span class="folder-icon">\U0001f4c1</span> %s</button>\n          <ul class="files">\n' % (oc, hm.escape(fn))
        for fi in fol.get("files",[]):
            p = fi.get("path",""); t = fi.get("title",""); ca = fi.get("cat","\u5176\u4ed6")
            th += '            <li><a href="#" data-md="%s" data-folder="%s" data-file="%s" data-category="%s"><span class="file-dot">%s</span>%s</a></li>\n' % (hm.escape(p), hm.escape(fn), hm.escape(t), hm.escape(ca), ic(ca), hm.escape(t))
        th += '          </ul>\n        </div>\n'
    th += '        <a href="game/index.html" class="sidebar-game-link">\n          <span style="width:20px;text-align:center">\U0001f3ae</span>\n          \u6e38\u620f\u76d2\u5b50\n        </a>\n</nav>'
    html = re.sub(r'<nav\s+class="tree">.*?</nav>',th,html,count=1,flags=re.DOTALL)
    new_js = "    var catIcon = '\u25cb';"
    for i,t in enumerate(tags):
        kw = "if" if i==0 else "else if"
        new_js += "\n    %s (category === '%s') catIcon = '%s';" % (kw, t["name"], t["icon"])
    html = re.sub(r'var\s+catIcon\s*=\s*\'[^\']*\'\s*;(?:\s*(?:else\s+)?if\s*\(\s*category\s*===\s*\'[^\']*\'\)\s*catIcon\s*=\s*\'[^\']*\';\s*)*',new_js,html,count=1)
    with open(HTML_PATH,"w",encoding="utf-8") as f: f.write(html)
    invalidate_cache()
    return True

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,fmt,*a):
        sys.stderr.write("[manager] %s\n" % (fmt%a))
    def do_GET(self):
        p = urllib.parse.urlparse(self.path); path = p.path
        if path == "/": self._serve_ui()
        elif path == "/api/tree": send_json(self,200,parse_tree())
        elif path == "/api/docs": send_json(self,200,scan_docs())
        elif path.startswith("/api/read/"):
            fp = urllib.parse.unquote(path[len("/api/read/"):])
            full = os.path.join(BASE,fp)
            if not fp or not os.path.isfile(full):
                send_json(self,404,{"error":"not found"}); return
            try:
                with open(full,"r",encoding="utf-8") as f: content = f.read()
                send_json(self,200,{"content":content})
            except: send_json(self,500,{"error":"read error"})
        else: self._serve_static(path)
    def do_POST(self):
        p = urllib.parse.urlparse(self.path)
        if p.path in ("/api/save","/api/upload"):
            length = int(self.headers.get("Content-Length",0))
            body = self.rfile.read(length) if length else b"{}"
            try: data = json.loads(body)
            except: data = {}
            if p.path == "/api/save":
                send_json(self,200,{"ok":rebuild_html(data)})
            else:
                name = data.get("name",""); content = data.get("content","")
                if not name: send_json(self,400,{"ok":False,"error":"no name"}); return
                safe = re.sub(r'[<>:"/\\|?*]',"_",name)
                dest = os.path.join(DOCS,safe)
                try:
                    with open(dest,"w",encoding="utf-8") as f: f.write(content)
                    send_json(self,200,{"ok":True,"path":"source/document/"+safe})
                    invalidate_cache()
                except: send_json(self,500,{"ok":False,"error":"write error"})
        else: send_json(self,404,{"error":"not found"})
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
    def _serve_ui(self):
        ui_path = os.path.join(BASE,"manager_ui.html")
        if os.path.isfile(ui_path):
            with open(ui_path,"r",encoding="utf-8") as f:
                send_text(self,200,f.read(),"text/html; charset=utf-8")
        else: send_text(self,404,"manager_ui.html not found")
    def _serve_static(self,path):
        import mimetypes
        fp = os.path.join(BASE,path.lstrip("/"))
        if os.path.isfile(fp):
            with open(fp,"rb") as f: data = f.read()
            ct,_ = mimetypes.guess_type(fp)
            send_text(self,200,data.decode("utf-8","replace"),ct or "application/octet-stream")
        else: send_text(self,404,"not found")

if __name__ == "__main__":
    srv = http.server.HTTPServer(("0.0.0.0",PORT),H)
    print("Blog Manager running at http://localhost:%d" % PORT)
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\nstopped"); srv.server_close()
