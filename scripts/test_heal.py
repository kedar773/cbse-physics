import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

test_file = r"E:\physics_cbse\Class_12\Electrostatics_20260903_2109\08_speed_hacks_examiner_traps_and_points_to_remember.md"

with open(test_file, 'r', encoding='utf-8') as f:
    text = f.read()

def heal_markdown(content):
    # 1. Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # 2. Heal split markdown tables
    # Find patterns where | col1 | is followed by $$ math $$ and then | col3 | col4 | col5 |
    lines = content.split('\n')
    new_lines = []
    i = 0
    healed_count = 0
    while i < len(lines):
        line = lines[i].strip()
        # Look for table row starting and ending with | and having only 1 cell: | **Something** |
        if line.startswith('|') and line.endswith('|') and line.count('|') == 2 and not line.startswith('| :'):
            col1 = line.strip('|').strip()
            # Scan forward for $$ math $$
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip() == '$$':
                math_lines = []
                j += 1
                while j < len(lines) and lines[j].strip() != '$$':
                    math_lines.append(lines[j].strip())
                    j += 1
                if j < len(lines) and lines[j].strip() == '$$':
                    j += 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and lines[j].strip().startswith('|') and lines[j].strip().endswith('|'):
                        rem = lines[j].strip().lstrip('|').strip()
                        formula = ' '.join(math_lines).strip()
                        new_lines.append(f"| {col1} | ${formula}$ | {rem}")
                        i = j + 1
                        healed_count += 1
                        continue
        # Also de-indent accidental 4-space code blocks that start with bullets or bold
        if re.match(r'^\s{4,8}(\*|-|\d+\.|\*\*)\s*', lines[i]):
            clean_line = re.sub(r'^\s{4,8}', '  ', lines[i])
            new_lines.append(clean_line)
        else:
            new_lines.append(lines[i])
        i += 1
        
    return healed_count, '\n'.join(new_lines)

cnt, healed = heal_markdown(text)
print(f"Total table rows healed: {cnt}")

# Check sample lines around table
lines = healed.split('\n')
for idx, l in enumerate(lines[140:160], 141):
    print(f"{idx}: {l}")
