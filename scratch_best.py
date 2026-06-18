import os
import csv

scenarios_dir = r'd:\MAYCON\PROJETOS\ESNAUTO\Scripts\results\Run_20260617_160122_Prod\scenarios'

best_global_fitness = float('inf')
best_global_info = {}

print("=== Verificando todos os cenários ===\n")

for folder in sorted(os.listdir(scenarios_dir)):
    folder_path = os.path.join(scenarios_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    
    for file in os.listdir(folder_path):
        if 'melhores_fitness' in file:
            path = os.path.join(folder_path, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse tab-delimited, skip repeated header lines
            lines = content.strip().split('\n')
            last_valid = None
            for line in lines:
                line = line.strip()
                if not line or 'Época' in line or line.startswith('"Época"'):
                    continue
                parts = line.split('\t')
                if len(parts) >= 7:
                    try:
                        fitness = float(parts[6].strip('"'))
                        last_valid = parts
                    except ValueError:
                        pass
            
            if last_valid:
                fitness = float(last_valid[6].strip('"'))
                a   = last_valid[1].strip('"')
                sr  = last_valid[2].strip('"')
                iL  = last_valid[3].strip('"')
                tr  = last_valid[4].strip('"')
                reg = last_valid[5].strip('"')
                
                print(f"Cenário: {folder}")
                print(f"  Epoch: {last_valid[0].strip('\"')} | a={a} | sr={sr} | initLen={iL} | tam_reservoir={tr} | Reg={reg} | Fitness={fitness}")
                print()
                
                if fitness < best_global_fitness:
                    best_global_fitness = fitness
                    best_global_info = {
                        'folder': folder,
                        'folder_path': folder_path,
                        'fitness': fitness,
                        'a': a,
                        'sr': sr,
                        'initLen': iL,
                        'tam_reservoir': tr,
                        'reg': reg,
                    }

print("=" * 60)
print(f"MELHOR CENÁRIO:")
print(f"  Folder: {best_global_info.get('folder')}")
print(f"  Fitness: {best_global_info.get('fitness')}")
print(f"  a = {best_global_info.get('a')}")
print(f"  sr = {best_global_info.get('sr')}")
print(f"  initLen = {best_global_info.get('initLen')}")
print(f"  tam_reservoir = {best_global_info.get('tam_reservoir')}")
print(f"  Reg = {best_global_info.get('reg')}")
