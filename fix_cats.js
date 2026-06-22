const fs=require("fs");
const path="C:/Git/repositories/jangut.github.io/game/note-slice.html";
let data=fs.readFileSync(path,"utf8");
console.log("File length:",data.length);

const catMap={"小星星":"入门","生日快乐":"入门","少女的祈祷":"经典","欢乐颂":"经典","绿袖子":"经典","卡农":"经典","茉莉花":"国风","七里香":"国风","成都":"国风","梦中的婚礼":"流行","童话":"流行","晴天":"流行","简单爱":"流行","夜曲":"流行","小幸运":"流行","追光者":"流行","海阔天空":"摇滚","光辉岁月":"摇滚","真的爱你":"摇滚","平凡之路":"摇滚"};

// Test a known line
let test = data.match(/童话.*bpm:/);
console.log("Test match for 童话:", test ? test[0] : "NOT FOUND");

// Test the regex
let test2 = data.match(/name:'童话',bpm:/);
console.log("Regex test for 童话:", test2 ? test2[0] : "NOT FOUND");

let lines=data.split("\n");
let fixed=0;
for(let i=0;i<lines.length;i++){
  let m=lines[i].match(/name:'([^']+)',bpm:/);
  if(m){let name=m[1];let cat=catMap[name];
    if(cat&&!lines[i].includes(",cat:")){
      lines[i]=lines[i].replace(/(name:'[^']+'),bpm:/,"$1,cat:'"+cat+"',bpm:");fixed++;}}
}
data=lines.join("\n");
data=data.replace('const order=["入门","国风","流行","摇滚","经典"];','const order=["入门","国风","流行","摇滚","经典","其他"];');
fs.writeFileSync(path,data,"utf8");
console.log("Fixed "+fixed+" songs");
