const fs = require("fs");
const path = "C:/Git/repositories/jangut.github.io";

// 读 index.json（去掉BOM）
let idx = fs.readFileSync(path+"/source/index.json", "utf8").replace(/^\uFEFF/, "");
idx = JSON.parse(idx);

// 生成 JS 对象字面量
let idxStr = JSON.stringify(idx, null, 2);

// 读 HTML
let html = fs.readFileSync(path+"/game/note-slice.html", "utf8");

// 1. 嵌入索引
html = html.replace(
  "const SONGS = {};",
  "const SONGS = " + idxStr + ";"
);

// 2. 删除 loadSongs 函数
const s = html.indexOf("// 从 index.json 加载歌曲");
const e = html.indexOf("\n\n", html.indexOf("buildSongList();")) + 1;
if (s > 0 && e > s) {
  html = html.substring(0, s - 1) + html.substring(e);
}

// 3. 替换调用
html = html.replace(
  "syncSliderLabels();\nloadSongs();",
  "syncSliderLabels();\ndocument.getElementById(\"load-overlay\").classList.add(\"hidden\");\nbuildSongList();"
);

// 4. 安全超时改成1秒
html = html.replace("5000;", "2000;");

fs.writeFileSync(path+"/game/note-slice.html", html, "utf8");
console.log("Embedded " + Object.keys(idx).length + " songs");