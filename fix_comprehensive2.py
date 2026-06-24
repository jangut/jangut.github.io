import re

with open("manager_ui.html", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Add missing .tr / .tn / .ti CSS
if ".tr{" not in c:
    c = c.replace(
        ".fl{display:flex;align-items:center;gap:6px;padding:5px 0;font-size:13px;border-bottom:1px solid #1a2535}",
        ".fl{display:flex;align-items:center;gap:6px;padding:5px 0;font-size:13px;border-bottom:1px solid #1a2535}\n"
        + ".tr{display:flex;align-items:center;gap:6px;padding:5px 0;font-size:13px;border-bottom:1px solid #1a2535}\n"
        + ".tn{flex:1;border:none;background:transparent;color:#9db0c3;font-size:13px;outline:none}\n"
        + ".tn:focus{outline:1px solid #4cf7ff;border-radius:3px;padding:1px 4px;color:#f0f4f8}\n"
        + ".ti{flex:0 0 40px;border:none;background:transparent;color:#9db0c3;font-size:13px;outline:none;text-align:center}\n"
        + ".ti:focus{outline:1px solid #4cf7ff;border-radius:3px;color:#f0f4f8}\n"
        + ".tr .dx{color:#ff6b6b;cursor:pointer;opacity:.4;flex-shrink:0;padding:2px 4px}\n"
        + ".tr .dx:hover{opacity:1}"
    )
    print("tr CSS added")
else:
    print("tr CSS exists")

# 2. Unify .lib-item with .fl
c = c.replace(
    ".lib-item{padding:4px 8px;border-radius:4px;cursor:pointer;font-size:12px;color:#9db0c3;margin:2px 0}",
    ".lib-item{padding:5px 0;cursor:pointer;font-size:13px;color:#9db0c3;border-bottom:1px solid #1a2535}"
)
c = c.replace(
    ".lib-item:hover{background:#1a2535;color:#f0f4f8}",
    ".lib-item:hover{color:#f0f4f8}"
)

# 3. Unify headers
c = c.replace(
    ".lib-h{padding:8px 10px;cursor:pointer;font-size:12px;color:#667084;display:flex;align-items:center;gap:6px}",
    ".lib-h{cursor:pointer;font-size:13px;color:#667084;display:flex;align-items:center;gap:6px;margin-bottom:8px;text-transform:uppercase;letter-spacing:.06em}"
)
c = c.replace(
    ".lib-h:hover{background:#1a2535}",
    ".lib-h:hover{color:#9db0c3}"
)
c = c.replace(
    ".sec h3{font-size:13px;color:#667084;margin-bottom:10px}",
    ".sec h3{font-size:13px;color:#667084;margin-bottom:8px;text-transform:uppercase;letter-spacing:.06em}"
)

# 4. Add .tag.i for 想法
c = c.replace(
    ".lib-item .tag.o{background:rgba(102,112,133,.12);color:#667084}",
    ".lib-item .tag.o{background:rgba(102,112,133,.12);color:#667084}\n.lib-item .tag.i{background:rgba(255,148,232,.15);color:#ff94e8}"
)

with open("manager_ui.html", "w", encoding="utf-8") as f:
    f.write(c)

# Verify
for s in [".tr{", ".tn", ".ti", "renderTags", "renderLibrary", ".lib-item{padding:5px 0"]:
    ok = s in open("manager_ui.html", encoding="utf-8").read()
    print(f"{'OK' if ok else 'NO'}: {s[:40]}")
