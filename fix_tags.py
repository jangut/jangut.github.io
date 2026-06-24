import re

with open("manager_ui.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where af() starts (line 131)
for i, line in enumerate(lines):
    if "function af" in line:
        print(f"af() at line {i}")
        # Insert renderTags, addTag, renderLibrary before af()
        new_funcs = """function renderTags(){
  var e=document.getElementById('tagList');
  if(!e)return;
  if(!T.tags)T.tags=[
    {name:'\u6280\u672f',icon:'\U0001F527'},
    {name:'\u7406\u8bba',icon:'\U0001F4D8'},
    {name:'\u60f3\u6cd5',icon:'\U0001F4A1'},
    {name:'\u5176\u4ed6',icon:'\u00b7'}
  ];
  var h='';
  T.tags.forEach(function(t,j){
    h+='<div class="tr">';
    h+='<input class="tn" value="'+t.name+'" onchange="T.tags['+j+'].name=this.value;R()" placeholder="\u540d\u79f0">';
    h+='<input class="ti" value="'+t.icon+'" onchange="T.tags['+j+'].icon=this.value;R()" placeholder="\u56fe\u6807">';
    h+='<span class="dx" onclick="T.tags.splice('+j+',1);renderTags();R()">\u2715</span>';
    h+='</div>';
  });
  e.innerHTML=h;
}
function addTag(){
  if(!T.tags)T.tags=[];
  T.tags.push({name:'\u65b0\u6807\u7b7e',icon:'\U0001F4CC'});
  renderTags();R();
}
function renderLibrary(){
  var el=document.getElementById('libList');
  if(!el)return;
  fetch('/api/docs').then(function(r){return r.json()}).then(function(d){
    var h='';
    d.forEach(function(x){
      h+='<div class="lib-item" onclick="preview(\''+x.path+'\',\''+x.title+'\')">';
      h+='<span class="tag '+(x.cat==='\u6280\u672f'?'t':x.cat==='\u7406\u8bba'?'l':x.cat==='\u60f3\u6cd5'?'i':'o')+'">'+x.cat+'</span>';
      h+=x.title+'</div>';
    });
    if(!d.length)h='<div style="padding:8px;color:#667084;font-size:11px">\u6ca1\u6709\u6587\u4ef6</div>';
    el.innerHTML=h;
  });
}
"""
        lines.insert(i, new_funcs)
        break
else:
    print("af() not found")

with open("manager_ui.html", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Tags & library functions added")
