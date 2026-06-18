import os

data_file = r'd:\MAYCON\PROJETOS\ESNAUTO\Scripts\results\Run_20260617_160122_Prod\scenarios\AlgGen PETR4 ESN_mae_otim40x60 com factor 10000_2 (2563) Win GED e W Normal\Dados PETR4 ESN_mae_otim40x60 com_factor 10000_2.csv'

with open(data_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find the last valid data line (line 27884 = index 27883)
# It's the line with Contar = 27883
target_idx = None
for i in range(len(lines)-1, -1, -1):
    stripped = lines[i].strip()
    if not stripped:
        continue
    parts = stripped.split('\t')
    if len(parts) >= 2:
        try:
            int(parts[1].strip('"'))
            target_idx = i
            break
        except ValueError:
            pass

print(f"Target line index: {target_idx} (line {target_idx+1})")
print(f"Line content: {lines[target_idx].strip()[:100]}")

# Add #MELHOR marker at end of line
if '#MELHOR' not in lines[target_idx]:
    lines[target_idx] = lines[target_idx].rstrip('\r\n') + '\t#MELHOR\r\n'
    with open(data_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Marker #MELHOR added successfully!")
else:
    print("Marker already present.")

print(f"\nFinal line: {lines[target_idx].strip()[:150]}")
