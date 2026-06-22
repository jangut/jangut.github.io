import re
path = 'C:/Git/repositories/jangut.github.io/game/note-slice.html'
with open(path, encoding='utf-8') as f:
  data = f.read()
cat_map = {'小星星':'入门','生日快乐':'入门','少女的祈祷':'经典','欢乐颂':'经典','绿袖子':'经典','卡农主题':'经典','铃儿响叮当':'入门','茉莉花':'国风','七里香':'国风','童线':'流行','晴天':'流行','简单爱':'流行','夜曲':'流行','小幸运':'流行','追光者':'流行','海阔天空':'摇滚','光辉岁月':'摇滚','真的爱你':'摇滚','平凡之路':'摇滚','梦中的婚礼':'流行'}
lines = data.split('\n')
fixed = 0
for i in range(len(lines)):
  m = re.search(r"name:'([^']+)'", lines[i])
  if m:
    name = m.group(1)
    cat = cat_map.get(name)
    if cat and ',cat:' not in lines[i]:
      lines[i] = lines[i].replace("name:'" + name + "'", "name:'" + name + "',cat:'" + cat + "'")
      fixed += 1
data = '\n'.join(lines)
old = 'const order=["入门","国风","流行","摇滚","经典"];'
if old in data:
  data = data.replace(old, 'const order=["入门","国风","流行","摇滚","经典","其他"];')
with open(path, 'w', encoding='utf-8') as f:
  f.write(data)
print('Fixed ' + str(fixed) + ' songs')