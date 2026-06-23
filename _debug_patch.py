import sys
file_path = 'C:\\Git\\repositories\\jangut.github.io\\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 4: Insert TOC JS - find the location more carefully
marker = '  }\n\n\n  // Sidebar md links'
if marker in content:
    idx = content.index(marker)
    print('Found marker at index:', idx)
else:
    # Try different variations
    for m in ['  }\n\n  // Sidebar md links', '  }\n  // Sidebar md links', '  }  // Sidebar md links', '  }\n\n\n\n  // Sidebar md links']:
        if m in content:
            marker = m
            idx = content.index(marker)
            print('Found alt marker at index:', idx)
            break
    else:
        print('Markers NOT FOUND')
        # Search near
        sm = content.find('Sidebar md links')
        if sm > 0:
            print('Sidebar md links at:', sm)
            print('Context:', repr(content[sm-60:sm+30]))

# Step 5: Find closeDoc ending
close_marker = "switchToPanel('panel-index');\n    }"
if close_marker in content:
    print('closeDoc marker found')
else:
    # Try variations
    close_alt = ["switchToPanel('panel-index');\n      hideTOC();\n    }", "switchToPanel('panel-index');\n    }"]
    for cm in close_alt:
        if cm in content:
            print('Found alt close marker')
            break
    else:
        # Search for switchToPanel near panel-index
        st = content.find("switchToPanel('panel-index')")
        if st > 0:
            print('switchToPanel(panel-index) at:', st)
            print('Context:', repr(content[st:st+80]))