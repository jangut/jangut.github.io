const fs = require("fs");
const path = require("path");
const all = JSON.parse(fs.readFileSync("C:/Git/repositories/jangut.github.io/source/music.txt","utf8"));

// 创建 songs 目录
const songsDir = "C:/Git/repositories/jangut.github.io/source/songs";
if (!fs.existsSync(songsDir)) fs.mkdirSync(songsDir);

const index = {};
const SEMI_MIN = 47, SEMI_MAX = 83;

for (const [key, song] of Object.entries(all)) {
  // 计算预览条
  const preview = song.notes.slice(0,24).map(([n])=>{
    const t = ((noteToSemi(n)-SEMI_MIN)/(SEMI_MAX-SEMI_MIN));
    return Math.round(3+t*23);
  });
  
  // 写单曲文件（含全部音符）
  fs.writeFileSync(songsDir + "/" + key + ".json", JSON.stringify(song, null, 2), "utf8");
  
  // 索引只保留元数据 + 预览条
  index[key] = {
    name: song.name, bpm: song.bpm, diff: song.diff,
    color: song.color, cat: song.cat,
    notes_len: song.notes.length,
    preview: preview
  };
}

fs.writeFileSync("C:/Git/repositories/jangut.github.io/source/index.json", JSON.stringify(index, null, 2), "utf8");
console.log("Split " + Object.keys(index).length + " songs");

function noteToSemi(n){
  const m={C:0,"C#":1,D:2,"D#":3,E:4,F:5,"F#":6,G:7,"G#":8,A:9,"A#":10,B:11};
  const note=n.match(/^([A-G]#?)(\d+)$/);
  if(!note) return 60;
  return m[note[1]]+(parseInt(note[2])+1)*12;
}