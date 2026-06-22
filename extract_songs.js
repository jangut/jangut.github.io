const fs = require('fs');
let html = fs.readFileSync('C:/Git/repositories/jangut.github.io/game/note-slice.html', 'utf8');
// 找到 const SONGS = { ... };
const start = html.indexOf('const SONGS = {');
let depth = 0, pos = start;
while(pos < html.length) {
  const c = html[pos];
  if(c === '{') depth++;
  if(c === '}') depth--;
  if(depth === 0 && pos > start && html[pos] === '}'){
    // 检查后面是否跟着 ';'
    if(html[pos+1] === ';'){ pos+=2; break; }
  }
  pos++;
}
const songsJS = html.substring(start, pos);
// 用 eval 提取数据
const SONGS = eval('(' + songsJS.substring(14) + ')');
// 转换为 JSON
const json = JSON.stringify(SONGS, null, 2)
  .replace(/"(\w+)":/g, '$1:') // 去掉属性名的引号
  .replace(/"(bpm|diff|cat|name|color)":/g, '"$1":') // 保留这几个
  .replace(/: "([^"]+)"/g, ":'$1'"); // 值用单引号
fs.writeFileSync('C:/Git/repositories/jangut.github.io/source/music.txt', 'const SONGS = ' + json + ';\n', 'utf8');
console.log('Done, size: ' + json.length);
