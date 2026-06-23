import sys
lines = open("C:\\Git\\repositories\\jangut.github.io\\_fix_toc2.py", "r", encoding="utf-8").readlines()
# Fix line 132 (0-indexed: 131)
if len(lines) > 131:
    old = lines[131]
    lines[131] = old.replace("'tocPeek').classList'", "'tocPeek'")
    print("Fixed:", lines[131][:60])
with open("C:\\Git\\repositories\\jangut.github.io\\_fix_toc2.py", "w", encoding="utf-8") as f:
    f.writelines(lines)