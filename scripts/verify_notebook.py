import os
import re
import sys

base = r"E:\physics_cbse\physics_html_notebook"

def check_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    dirname = os.path.dirname(file_path)
    links = re.findall(r'(?:href|src)=["\']([^#"\'\s]+)["\']', content)
    missing = []
    
    for l in links:
        if l.startswith('http') or l.startswith('mailto:') or l.startswith('data:'):
            continue
        target = os.path.normpath(os.path.join(dirname, l))
        if not os.path.exists(target):
            missing.append((l, target))
            
    return len(links), missing

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

total_links = 0
all_missing = []

for root, dirs, files in os.walk(base):
    for file in files:
        if file.endswith('.html'):
            f_path = os.path.join(root, file)
            lc, miss = check_file(f_path)
            total_links += lc
            all_missing.extend(miss)

print(f"Total links/assets checked across all HTML files: {total_links}")
print(f"Missing assets/links: {len(all_missing)}")
if all_missing:
    for m in all_missing[:10]:
        print("  Missing:", m)
else:
    print("[SUCCESS] All links and local assets verified 100% valid!")
