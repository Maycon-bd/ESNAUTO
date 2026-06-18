import os

# O melhor é o da última linha do arquivo de dados do cenário Run2 (2563) Win GED e W Normal
# conforme explicado: pegar a ultima linha do arquivo W (epoca 938) e buscar no arquivo principal
# Mas a logica real: pegar a ultima linha do arquivo Win/W/Wout e verificar o Contar na ultima linha do ESN data

data_file = r'd:\MAYCON\PROJETOS\ESNAUTO\Scripts\results\Run_20260617_160122_Prod\scenarios\AlgGen PETR4 ESN_mae_otim40x60 com factor 10000_2 (2563) Win GED e W Normal\Dados PETR4 ESN_mae_otim40x60 com_factor 10000_2.csv'

with open(data_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print(f"Header: {lines[0].strip()[:200]}")

# Find last valid data line (before any repeated header)
last_valid_line = None
last_valid_linenum = None
for i, line in enumerate(lines):
    stripped = line.strip()
    if not stripped:
        continue
    parts = stripped.split('\t')
    if len(parts) >= 2:
        col2 = parts[1].strip('"')
        try:
            int(col2)
            last_valid_line = stripped
            last_valid_linenum = i + 1
        except ValueError:
            pass

print(f"\nLast valid data line #{last_valid_linenum}:")
print(last_valid_line[:300])

# Parse columns
parts = last_valid_line.split('\t')
cols = ['Parâmetro', 'Contar', 'a', 'sr', 'initLen', 'tam_reservoir', 'reg',
        'MAE_treino40%', 'MAE_valida60%', 'Otimiza', 'old_Otimiza', 'RMSE_treino', 'RMSE_valida', 'RMSE_t0.4+RMSE_v0.6']

print("\nParsed values:")
for col, val in zip(cols, parts):
    print(f"  {col}: {val.strip(chr(34))}")
