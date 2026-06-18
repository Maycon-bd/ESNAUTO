import os

base = r'd:\MAYCON\PROJETOS\ESNAUTO\Scripts\results\Run_20260617_160122_Prod\scenarios\AlgGen PETR4 ESN_mae_otim40x60 com factor 10000_2 (2563) Win GED e W Normal'

TARGET_EPOCH = 938  # last epoch in Win/W files for this scenario
BEST_EPOCH   = 117  # epoch with best Fitness in bestSol file

# Best parameters (from melhores_fitness epoch 117)
a             = "0.870902030197374"
sr            = "0.406802420062409"
initLen       = "9"
tam_reservoir = "27"
reg           = "2.2289743444227e-05"
dist_win      = "GED mean=14.573152, sd=8.032086, nu=7.686645"
dist_w        = "Normal mean=0, sd=1"

def extract_epoch_rows(filepath, epoch_num):
    """Extract all rows for a given epoch. Returns list of (row_idx, values_list)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    rows = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        col1 = parts[0].strip('"')
        col2 = parts[1].strip('"')
        try:
            row_idx = int(col1)
            ep = int(col2)
        except ValueError:
            continue
        if ep == epoch_num:
            # values start at col3 onwards (skip last if it's a string like GED...)
            vals = []
            for v in parts[2:]:
                v = v.strip('"')
                try:
                    float(v)
                    vals.append(v)
                except ValueError:
                    break  # distribution string at the end
            rows[row_idx] = vals
    return rows

# Extract Win (2 rows x 27 cols)
win_rows = extract_epoch_rows(
    os.path.join(base, 'Dados PETR4 Win ESN_mae_otim40X60 com_factor 10000_2.csv'),
    TARGET_EPOCH
)
print(f"Win rows found: {sorted(win_rows.keys())} | sizes: {[len(win_rows[k]) for k in sorted(win_rows.keys())]}")

# Extract W (27 rows x 27 cols)
w_rows = extract_epoch_rows(
    os.path.join(base, 'Dados PETR4 W reservatório ESN_mae_otim40X60 com_factor 10000_2.csv'),
    TARGET_EPOCH
)
print(f"W rows found: {sorted(w_rows.keys())} | sizes: {[len(w_rows[k]) for k in sorted(w_rows.keys())]}")

# Extract Wout (1 row x 29 cols = tam_reservoir+2)
wout_rows = extract_epoch_rows(
    os.path.join(base, 'Dados PETR4 Wout ESN_mae_otim40X60 com_factor 10000_2.csv'),
    TARGET_EPOCH
)
print(f"Wout rows found: {sorted(wout_rows.keys())} | sizes: {[len(wout_rows[k]) for k in sorted(wout_rows.keys())]}")

# --- Build Win matrix (nrow=tam_reservoir, ncol=2) ---
# In R: matrix(nrow=N, ncol=2, c(...)) fills column-major
# Row 1 of Win file = first column of matrix
# Row 2 of Win file = second column of matrix
win_col1 = win_rows[1]  # 27 values
win_col2 = win_rows[2]  # 27 values
win_all = win_col1 + win_col2

# --- Build W matrix (nrow=tam_reservoir, ncol=tam_reservoir) ---
# Each row in file corresponds to a row in the matrix (but R uses col-major fill)
# The file stores by row: row 1, row 2, ..., row 27
# R matrix col-major: we need values column by column
# So we need to transpose: collect all rows, then output column by column
n = int(tam_reservoir)
w_matrix = []
for i in range(1, n+1):
    w_matrix.append(w_rows[i])

# Verify dimensions
print(f"W matrix: {len(w_matrix)} rows x {len(w_matrix[0])} cols")

# For R col-major fill: go col by col
w_vals_colmajor = []
for col in range(n):
    for row in range(n):
        w_vals_colmajor.append(w_matrix[row][col])

# --- Build Wout (1 row x (tam_reservoir+2)) ---
wout_vals = []
for i in sorted(wout_rows.keys()):
    wout_vals.extend(wout_rows[i])

print(f"Win total values: {len(win_all)} (expected {n*2})")
print(f"W total values: {len(w_vals_colmajor)} (expected {n*n})")
print(f"Wout total values: {len(wout_vals)} (expected {n+2})")

# --- Format R code ---
def fmt_vec(vals, indent=44):
    sp = ' ' * indent
    per_line = 10
    lines_out = []
    for i in range(0, len(vals), per_line):
        chunk = ', '.join(vals[i:i+per_line])
        lines_out.append(sp + chunk)
    return ',\n'.join(lines_out)

r_code = f"""
##Dados treinados e validados (dados brutos) com factor 10000_2, ({2563}) otimizado por MAE v. 2.8.1.2 Maycon G Silva
##Melhor cenário: Run 2, Win GED e W Normal | Fitness = -0.23753732723132 | Época = {BEST_EPOCH}
#tourSelection, spCrossover, raMutation, keepBest=T, pmutation=0.1, elitism = 1, optim=F
a             = {a}
sr            =\t{sr}\t
initLen       =\t{initLen}
tam_reservoir =\t{tam_reservoir}
reg           =\t{reg}
#Win = Distribuição {dist_win}
Win           = matrix(nrow = tam_reservoir, ncol = 2, c( {', '.join(win_all[:10])},
{fmt_vec(win_all[10:], 44)},
                                                          {', '.join(win_all[n:n+10])},
{fmt_vec(win_all[n+10:], 44)}))

#W   = Distribuição {dist_w}
W             = matrix(nrow = tam_reservoir, ncol = tam_reservoir, c({', '.join(w_vals_colmajor[:10])},
{fmt_vec(w_vals_colmajor[10:], 44)}))

Wout          = matrix(nrow = 1, ncol = (tam_reservoir+2), c( {wout_vals[0]},
"""
for v in wout_vals[1:]:
    r_code += f"                                                              {v},\n"
r_code = r_code.rstrip(',\n') + "))\n"

print("\n" + "="*60)
print("R CODE BLOCK:")
print("="*60)
print(r_code)

# Save to file
with open(r'd:\MAYCON\PROJETOS\ESNAUTO\scratch_rblock.txt', 'w', encoding='utf-8') as f:
    f.write(r_code)
print("\nSaved to scratch_rblock.txt")
