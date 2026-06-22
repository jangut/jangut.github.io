const fs = require("fs");
const path = "C:/Git/repositories/jangut.github.io";

// 读取两份数据（去BOM）
let idx = JSON.parse(fs.readFileSync(path+"/source/index.json","utf8").replace(/^\uFEFF/,""));
let music = JSON.parse(fs.readFileSync(path+"/source/music.json","utf8").replace(/^\uFEFF/,""));

let html = fs.readFileSync(path+"/game/note-slice.html","utf8");

// 1. 替换 SONGS = {} 为索引（已内嵌）
// 2. 在 };\n 后面加 _ALL_NOTES + 合并循环
const idxStr = JSON.stringify(idx, null, 2);
const musicStr = JSON.stringify(music, null, 2);
const insertAfter = "const SONGS = " + idxStr + ";";

const notesBlock = "\n\n// 全部乐谱（内嵌）\n" +
  "const _ALL_NOTES = " + musicStr + ";\n\n" +
  "// 合并乐谱到 SONGS\n" +
  "for(const k of Object.keys(_ALL_NOTES)){\n" +
  "  if(SONGS[k]) SONGS[k].notes = _ALL_NOTES[k].notes;\n" +
  "}\n";

html = html.replace(
  "const SONGS = " + idxStr + ";\n// 缓存全部乐谱",
  "const SONGS = " + idxStr + ";" + notesBlock + "// 缓存全部乐谱"
);

// 3. 删除 _allSongs 变量
html = html.replace("let _allSongs=null;\n", "");

// 4. 简化卡片点击（去掉异步fetch）
html = html.replace(
  "card.addEventListener('click',async()=>{\n" +
  "      selectedSong=key;\n" +
  "      document.querySelectorAll('.song-card').forEach(c=>c.classList.remove('selected'));\n" +
  "      card.classList.add('selected');\n" +
  "      if(!SONGS[key].notes) try {\n" +
  "        if(!_allSongs){const r=await fetch('../source/music.json');_allSongs=await r.json();}\n" +
  "        if(!SONGS[key])SONGS[key]={};\n" +
  "        SONGS[key].notes=_allSongs[key].notes;\n" +
  "      } catch(e){}\n" +
  "    });",
  "card.addEventListener('click',()=>{\n" +
  "      selectedSong=key;\n" +
  "      document.querySelectorAll('.song-card').forEach(c=>c.classList.remove('selected'));\n" +
  "      card.classList.add('selected');\n" +
  "    });"
);

// 5. 简化 btn-play
html = html.replace(
  "document.getElementById('btn-play').addEventListener('click',async()=>{\n" +
  "    audioCtx.resume();\n" +
  "    if(!SONGS[selectedSong]||!SONGS[selectedSong].notes) try {\n" +
  "      if(!_allSongs){const r=await fetch('../source/music.json');_allSongs=await r.json();}\n" +
  "      if(!SONGS[selectedSong])SONGS[selectedSong]={};\n" +
  "      SONGS[selectedSong].notes=_allSongs[selectedSong].notes;\n" +
  "    } catch(e){}\n" +
  "    startGame(selectedSong);\n" +
  "  });",
  "document.getElementById('btn-play').addEventListener('click',()=>{ audioCtx.resume(); startGame(selectedSong); });"
);

fs.writeFileSync(path+"/game/note-slice.html", html, "utf8");
console.log("Done. Embedded " + Object.keys(music).length + " songs, total " + html.length + " bytes");