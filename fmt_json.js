const fs = require("fs");
const data = JSON.parse(fs.readFileSync("C:/Git/repositories/jangut.github.io/source/music.json", "utf8"));

function fmt(notes) {
  const groups = [];
  let group = [], beat = 0;
  for (const x of notes) {
    let s = "[" + JSON.stringify(x[0]) + "," + x[1];
    if (x[2]) s += "," + JSON.stringify(x[2]);
    s += "]";
    group.push(s);
    beat += x[1] || 0.25;
    if (beat >= 3.5 || group.length >= 8) {
      groups.push("    " + group.join(", "));
      group = []; beat = 0;
    }
  }
  if (group.length) groups.push("    " + group.join(", "));
  return "[\n" + groups.join(",\n") + "\n  ]";
}

var out = "{\n";
var keys = Object.keys(data);
for (var i = 0; i < keys.length; i++) {
  var k = keys[i], s = data[k];
  out += "  " + JSON.stringify(k) + ": {\n";
  out += "    \"name\": " + JSON.stringify(s.name) + ",\n";
  out += "    \"bpm\": " + s.bpm + ",\n";
  out += "    \"diff\": " + JSON.stringify(s.diff) + ",\n";
  out += "    \"color\": " + JSON.stringify(s.color) + ",\n";
  out += "    \"cat\": " + JSON.stringify(s.cat) + ",\n";
  out += "    \"notes\": " + fmt(s.notes) + "\n";
  out += "  }" + (i < keys.length - 1 ? "," : "") + "\n";
}
out += "}\n";

JSON.parse(out); // validate
fs.writeFileSync("C:/Git/repositories/jangut.github.io/source/music.json", out, "utf8");
console.log("Valid JSON, " + out.length + " bytes");