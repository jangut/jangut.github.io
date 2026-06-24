with open("manager_ui.html", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(134, 150):
    print(f"{i}: {lines[i].rstrip()}")
