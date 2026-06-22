const fs = require("fs");
const txt = fs.readFileSync("C:/Git/repositories/jangut.github.io/source/music.txt", "utf8");

const result = {};
let cat = "", song = null;

for (const line of txt.split("\n")) {
  // 分类标题（2空格 + 短文字）
  const cm = line.match(/^\s{2}(\S+)\s*$/);
  if (cm && !line.includes(",") && cm[1].length < 6) { cat = cm[1]; continue; }
  
  // 歌曲标题
  const sm = line.match(/^\[([^\]]+)\]\s+(.+?)\s+BPM:(\d+)\s+难度:(\S+)\s+色:([#\w]+)\s+音符:(\d+)/);
  if (sm) {
    if (song) result[song.key] = { name:song.name, bpm:song.bpm, diff:song.diff, color:song.color, cat:song.cat, notes:song.notes };
    song = { key:sm[1], name:sm[2].trim(), bpm:+sm[3], diff:sm[4], color:sm[5], cat, notes:[] };
    continue;
  }
  
  // 音符行（含逗号、缩进）
  if (song && line.includes(",") && line.match(/^\s{2}/)) {
    for (const n of line.trim().split(/\s+/)) {
      const p = n.split(",");
      if (p.length >= 2) {
        const note = [p[0], +p[1]];
        if (p[2]) note.push(p[2]);
        song.notes.push(note);
      }
    }
  }
}
if (song) result[song.key] = { name:song.name, bpm:song.bpm, diff:song.diff, color:song.color, cat:song.cat, notes:song.notes };

const json = JSON.stringify(result, null, 2);
fs.writeFileSync("C:/Git/repositories/jangut.github.io/source/music.json", json, "utf8");
// 验证
JSON.parse(json);
const total = Object.values(result).reduce((s,x)=>s+x.notes.length, 0);
console.log("Recovered " + Object.keys(result).length + " songs, " + total + " total notes, " + json.length + " bytes");