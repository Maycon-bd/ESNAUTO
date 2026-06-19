"""
inject_and_test.py — FASE 3 do Pipeline ESN/GA
Lê o ranking.json, extrai os parâmetros e matrizes do melhor cenário,
gera um script R temporário e o executa via Rscript para obter
os resultados de validação e teste.

Uso:
    python inject_and_test.py <session_dir>
    python inject_and_test.py <session_dir> --log <pipeline_log_path>
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from datetime import datetime


# ──────────────────────────────────────────────
# Logger
# ──────────────────────────────────────────────
class PhaseLogger:
    def __init__(self, phase_name, log_path=None):
        self.phase = phase_name
        self.log_path = log_path

    def _write(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] [{self.phase}] {msg}"
        print(line)
        if self.log_path:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")

    def info(self, msg):  self._write(msg)
    def ok(self, msg):    self._write(f"OK — {msg}")
    def error(self, msg): self._write(f"ERRO — {msg}")
    def warn(self, msg):  self._write(f"AVISO — {msg}")


# ──────────────────────────────────────────────
# Extração de matrizes
# ──────────────────────────────────────────────
def extract_epoch_rows(filepath, epoch_num):
    """Extrai todas as linhas de uma época específica de um arquivo de matriz."""
    rows = {}
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue
            try:
                row_idx = int(parts[0].strip('"'))
                ep      = int(parts[1].strip('"'))
            except ValueError:
                continue
            if ep == epoch_num:
                vals = []
                for v in parts[2:]:
                    v = v.strip('"')
                    try:
                        float(v)
                        vals.append(v)
                    except ValueError:
                        break
                rows[row_idx] = vals
    except Exception as e:
        pass
    return rows


def get_last_epoch(filepath):
    """Retorna o número da última época em um arquivo de matriz."""
    last_ep = None
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) < 2:
                    continue
                try:
                    ep = int(parts[1].strip('"'))
                    last_ep = ep
                except ValueError:
                    continue
    except Exception:
        pass
    return last_ep


def build_r_matrix_win(win_file, epoch, tam_reservoir):
    """Constrói o código R para a matriz Win (nrow=tam_reservoir, ncol=2)."""
    rows = extract_epoch_rows(win_file, epoch)
    if not rows or 1 not in rows or 2 not in rows:
        return None, None
    col1 = rows[1]   # primeira coluna da matriz (nrow linhas)
    col2 = rows[2]   # segunda coluna
    all_vals = col1 + col2
    vals_str = ", ".join(all_vals)
    r_code = (
        f"Win <- matrix(nrow = tam_reservoir, ncol = 2, c(\n"
        f"  {vals_str}))\n"
    )
    return r_code, rows


def build_r_matrix_w(w_file, epoch, tam_reservoir):
    """Constrói o código R para a matriz W (nrow=ncol=tam_reservoir), col-major."""
    rows = extract_epoch_rows(w_file, epoch)
    if not rows:
        return None
    n = tam_reservoir
    matrix = [rows.get(i, []) for i in range(1, n + 1)]

    # Transposição para col-major (R preenche por coluna)
    vals_colmajor = []
    for col in range(n):
        for row in range(n):
            if col < len(matrix[row]):
                vals_colmajor.append(matrix[row][col])
            else:
                vals_colmajor.append("0")

    vals_str = ", ".join(vals_colmajor)
    r_code = (
        f"W <- matrix(nrow = tam_reservoir, ncol = tam_reservoir, c(\n"
        f"  {vals_str}))\n"
    )
    return r_code


def build_r_matrix_wout(wout_file, epoch):
    """Constrói o código R para a matriz Wout."""
    rows = extract_epoch_rows(wout_file, epoch)
    if not rows:
        return None
    all_vals = []
    for i in sorted(rows.keys()):
        all_vals.extend(rows[i])
    vals_str = ",\n  ".join(all_vals)
    r_code = (
        f"Wout <- matrix(nrow = 1, ncol = (tam_reservoir + 2), c(\n"
        f"  {vals_str}))\n"
    )
    return r_code
# ──────────────────────────────────────────────
# Detecção do Rscript
# ──────────────────────────────────────────────
def get_rscript_path():
    if shutil.which("Rscript"):
        return "Rscript"
    pf_r = r"C:\Program Files\R"
    if os.path.exists(pf_r):
        for version in sorted(os.listdir(pf_r), reverse=True):
            for sub in ["bin", os.path.join("bin", "x64")]:
                candidate = os.path.join(pf_r, version, sub, "Rscript.exe")
                if os.path.exists(candidate):
                    return candidate
    return "Rscript"


# ──────────────────────────────────────────────
# Geração do script R temporário
# ──────────────────────────────────────────────
def generate_r_script(best, output_dir, data_dir, logger, graph_val_name, graph_test_name):
    """
    Gera um script R completo e autossuficiente para rodar
    validação e teste com os parâmetros do cenário.
    """
    win_file  = best["win_file"]
    w_file    = best["w_file"]
    wout_file = best["wout_file"]
    epoch     = best["epoca_matrizes"]
    n         = best["tam_reservoir"]

    if not epoch:
        logger.error("Época de matrizes não encontrada no ranking.")
        return None

    r_win  = build_r_matrix_win(win_file, epoch, n)
    r_w    = build_r_matrix_w(w_file, epoch, n)
    r_wout = build_r_matrix_wout(wout_file, epoch)

    if r_win[0] is None or r_w is None or r_wout is None:
        logger.error("Falha ao extrair uma ou mais matrizes (Win/W/Wout).")
        return None

    r_win_code = r_win[0]

    out_dir_r  = output_dir.replace("\\", "\\\\")
    data_dir_r = data_dir.replace("\\", "\\\\")
    win_dist   = best.get("win_dist", "?")
    w_dist     = best.get("w_dist", "?")
    fitness    = best.get("fitness", "?")
    run_num    = best.get("run", "?")

    r_script = f"""
# ============================================================
# Script R gerado automaticamente pelo pipeline — FASE 3
# Melhor cenário: Run {run_num} | Win {win_dist} | W {w_dist}
# Fitness = {fitness}
# ============================================================

setwd("{data_dir_r}")

library(pracma)

# Dados
data_fac <- as.matrix(read.csv2(
  'PETR4_close com factor_2000-2020.txt', header=FALSE))
data <- as.numeric(data_fac)

data_date_fac <- as.matrix(read.csv2(
  'PETR4_close com factor_2000-2020_com data.csv', header=FALSE))
data_date_fac1 <- as.Date(data_date_fac[1:5198, 1])
data_date_1    <- data_date_fac1

# Partições
treino <- 2600
valida <- 1299
teste  <- 1299

inSize <- outSize <- 1

# Hiperparâmetros do melhor cenário
a             <- {best['a']}
sr            <- {best['sr']}
initLen       <- {best['initLen']}
tam_reservoir <- {best['tam_reservoir']}
reg           <- {best['reg']}

# Matrizes
{r_win_code}
{r_w}
{r_wout}

# ── VALIDAÇÃO ──────────────────────────────────
treino_valida <- data[1:(treino + valida)]

rhoW <- abs(eigen(W, only.values=TRUE)$values[1])
W    <- sr * W / rhoW

X  <- matrix(0, 1 + inSize + tam_reservoir, treino - initLen)
Yt <- matrix(treino_valida[(initLen+2):(treino+1)], 1)
x  <- rep(0, tam_reservoir)

for (t in 1:treino) {{
  u <- treino_valida[t]
  x <- (1-a)*x + a*tanh(Win %*% rbind(1,u) + W %*% x)
  if (t > initLen) X[, t-initLen] <- rbind(1, u, x)
}}

Y <- matrix(0, outSize, valida)
u <- treino_valida[treino + 1]
for (t in 1:valida) {{
  x    <- (1-a)*x + a*tanh(Win %*% rbind(1,u) + W %*% x)
  y    <- Wout %*% rbind(1, u, x)
  Y[, t] <- y
  u    <- treino_valida[treino + t + 1]
}}

Ytr <- matrix(0, outSize, treino)
u   <- treino_valida[1]
for (j in 1:treino) {{
  x      <- (1-a)*x + a*tanh(Win %*% rbind(1,u) + W %*% x)
  y      <- Wout %*% rbind(1, u, x)
  Ytr[, j] <- y
  u            <- treino_valida[j+1]
}}

mae_treino_v  <- mean(abs(treino_valida[2:treino] - Ytr[outSize, 1:(treino-1)]))
mae_valida_v  <- mean(abs(treino_valida[(treino+2):(treino+valida)] - Y[outSize, 1:(valida-1)]))
rmse_treino_v <- sqrt(mean((treino_valida[2:treino] - Ytr[outSize, 1:(treino-1)])^2))
rmse_valida_v <- sqrt(mean((treino_valida[(treino+2):(treino+valida)] - Y[outSize, 1:(valida-1)])^2))
Y_val <- Y

cat("##VALIDACAO##\\n")
cat(paste("MAE_treino_val =", mae_treino_v, "\\n"))
cat(paste("MAE_valida     =", mae_valida_v, "\\n"))
cat(paste("RMSE_treino_val=", rmse_treino_v, "\\n"))
cat(paste("RMSE_valida    =", rmse_valida_v, "\\n"))

# ── TESTE ──────────────────────────────────────
treina_testa <- c(data[1:treino], data[(treino+valida+1):(treino+valida+teste)])

rhoW <- abs(eigen(W, only.values=TRUE)$values[1])
W    <- sr * W / rhoW

X  <- matrix(0, 1 + inSize + tam_reservoir, treino - initLen)
Yt <- matrix(treina_testa[(initLen+2):(treino+1)], 1)
x  <- rep(0, tam_reservoir)

for (t in 1:treino) {{
  u <- treina_testa[t]
  x <- (1-a)*x + a*tanh(Win %*% rbind(1,u) + W %*% x)
  if (t > initLen) X[, t-initLen] <- rbind(1, u, x)
}}

Y <- matrix(0, outSize, teste)
u <- treina_testa[treino + 1]
for (t in 1:teste) {{
  x    <- (1-a)*x + a*tanh(Win %*% rbind(1,u) + W %*% x)
  y    <- Wout %*% rbind(1, u, x)
  Y[, t] <- y
  u    <- treina_testa[treino + t + 1]
}}

Ytr <- matrix(0, outSize, treino)
u   <- treina_testa[1]
for (j in 1:treino) {{
  x      <- (1-a)*x + a*tanh(Win %*% rbind(1,u) + W %*% x)
  y      <- Wout %*% rbind(1, u, x)
  Ytr[, j] <- y
  u      <- treina_testa[j+1]
}}

mae_treino  <- mean(abs(treina_testa[2:treino] - Ytr[outSize, 1:(treino-1)]))
mae_teste   <- mean(abs(treina_testa[(treino+2):(treino+teste)] - Y[outSize, 1:(teste-1)]))
rmse_treino <- sqrt(mean((treina_testa[2:treino] - Ytr[outSize, 1:(treino-1)])^2))
rmse_teste  <- sqrt(mean((treina_testa[(treino+2):(treino+teste)] - Y[outSize, 1:(teste-1)])^2))

cat("##TESTE##\\n")
cat(paste("MAE_treino  =", mae_treino, "\\n"))
cat(paste("MAE_teste   =", mae_teste, "\\n"))
cat(paste("RMSE_treino =", rmse_treino, "\\n"))
cat(paste("RMSE_teste  =", rmse_teste, "\\n"))

# ── GRÁFICOS ───────────────────────────────────
dir.create("{out_dir_r}", showWarnings=FALSE, recursive=TRUE)

png(file.path("{out_dir_r}", "{graph_val_name}"), width=1200, height=700, res=120)
  plot(ylim=c(0,50),
       ylab="Precos observados e previstos com factor (R$)",
       xlab="Data",
       data_date_1[(treino+1):(treino+valida)],
       treino_valida[(treino+1):(treino+valida)],
       type='l', col='green', lwd=2)
  lines(data_date_1[(treino+1):(treino+valida)], c(Y_val), col='black', lwd=1)
  title(main=paste("Validacao — ESN PETR4 | Win {win_dist} | W {w_dist} | N={n}"))
  legend('topright', legend=c('Serie alvo','Serie prevista'),
         col=c('green','black'), lty=1, bty='n')
dev.off()

png(file.path("{out_dir_r}", "{graph_test_name}"), width=1200, height=700, res=120)
  plot(ylim=c(10,90),
       ylab="Precos observados com factor e previstos com factor (R$)",
       xlab="Data",
       data_date_fac1[(treino+1):(treino+valida)],
       treina_testa[(treino+1):(treino+teste)],
       type='l', col='green', lwd=2)
  lines(data_date_fac1[(treino+1):(treino+valida)], c(Y), col='black', lwd=1)
  title(main=paste("Teste — ESN PETR4 | Win {win_dist} | W {w_dist} | N={n}"))
  legend('topleft', legend=c('Serie alvo','Serie prevista'),
         col=c('green','black'), lty=1, bty='n')
dev.off()

cat("##GRAFICOS_OK##\\n")
"""
    return r_script


def run_scenario_test(scen, output_dir, data_dir, session_dir, logger, rscript_exec):
    win_dist   = scen.get("win_dist", "?")
    w_dist     = scen.get("w_dist", "?")
    run_num    = scen.get("run", "?")
    
    graph_val_name = f"grafico_validacao_{win_dist}_{w_dist}_run{run_num}.png"
    graph_test_name = f"grafico_teste_{win_dist}_{w_dist}_run{run_num}.png"
    
    r_script = generate_r_script(scen, output_dir, data_dir, logger, graph_val_name, graph_test_name)
    if r_script is None:
        return None

    r_script_name = f"ESN_test_{win_dist}_{w_dist}_run{run_num}_temp.R"
    r_log_name = f"ESN_test_{win_dist}_{w_dist}_run{run_num}_temp.log"
    r_script_path = os.path.join(session_dir, r_script_name)
    r_log_path = os.path.join(session_dir, r_log_name)
    
    with open(r_script_path, "w", encoding="utf-8") as f:
        f.write(r_script)

    try:
        result = subprocess.run(
            [rscript_exec, r_script_path],
            capture_output=True,
            text=True,
            timeout=600  # 10 min max
        )
        stdout = result.stdout
        stderr = result.stderr

        with open(r_log_path, "w", encoding="utf-8") as f:
            f.write("=== STDOUT ===\n")
            f.write(stdout)
            f.write("\n=== STDERR ===\n")
            f.write(stderr)

        if result.returncode != 0:
            logger.error(f"Rscript para Run {run_num} | Win {win_dist} | W {w_dist} retornou erro {result.returncode}")
            return None

        # Parsear métricas do stdout
        metrics = {}
        secao = None
        for line in stdout.splitlines():
            if "##VALIDACAO##" in line:
                secao = "val"
            elif "##TESTE##" in line:
                secao = "test"
            elif "=" in line and secao:
                clean = line.strip().strip('[1] "').rstrip('"').strip()
                if "=" in clean:
                    key, val = clean.split("=", 1)
                    metrics[f"{secao}_{key.strip()}"] = val.strip()
        
        try:
            os.remove(r_script_path)
        except Exception:
            pass

        return metrics
    except Exception as e:
        logger.error(f"Erro ao executar Rscript para Run {run_num} | Win {win_dist} | W {w_dist}: {e}")
        return None


# ──────────────────────────────────────────────
# Execução principal
# ──────────────────────────────────────────────
def inject_and_test(session_dir, logger):
    session_dir = os.path.abspath(session_dir)
    # Carregar ranking.json
    ranking_path = os.path.join(session_dir, "ranking.json")
    if not os.path.exists(ranking_path):
        logger.error(f"ranking.json não encontrado em: {session_dir}")
        logger.error("Execute a FASE 2 (analyze_results.py) antes desta fase.")
        return False

    with open(ranking_path, "r", encoding="utf-8") as f:
        ranking = json.load(f)

    scenarios = ranking.get("ranking_completo", [])
    if not scenarios:
        logger.error("Nenhum cenário encontrado no ranking_completo.")
        return False

    # Diretório de saída
    output_dir = os.path.join(session_dir, "entrega")
    os.makedirs(output_dir, exist_ok=True)

    # Detectar pasta de dados
    base_dir  = os.path.dirname(os.path.dirname(session_dir))  # ESNAUTO/Scripts
    data_dir  = os.path.join(base_dir, "data")
    if not os.path.exists(data_dir):
        logger.error(f"Pasta de dados não encontrada: {data_dir}")
        return False

    rscript_exec = get_rscript_path()
    logger.info(f"Rscript detectado: {rscript_exec}")

    # Ordenar os cenários para o relatório na mesma ordem das tabelas do Matheus
    def sort_key(scen):
        combo_order = {
            ("Normal", "Normal"): 1,
            ("Uniforme", "Uniforme"): 2,
            ("GED", "Uniforme"): 3,
            ("GED", "Normal"): 4
        }
        combo = (scen["win_dist"], scen["w_dist"])
        order = combo_order.get(combo, 99)
        try:
            run = int(scen["run"])
        except ValueError:
            run = 99
        return (order, run)

    scenarios_sorted = sorted(scenarios, key=sort_key)
    logger.info(f"Iniciando a simulação e injeção de todos os {len(scenarios_sorted)} cenários...")

    resultados_scenarios = []
    
    for idx, scen in enumerate(scenarios_sorted, 1):
        logger.info(f"[{idx}/{len(scenarios_sorted)}] Processando: Run {scen['run']} | Win {scen['win_dist']} | W {scen['w_dist']}")
        metrics = run_scenario_test(scen, output_dir, data_dir, session_dir, logger, rscript_exec)
        if metrics:
            full_data = scen.copy()
            full_data.update(metrics)
            resultados_scenarios.append(full_data)
        else:
            logger.error(f"Falha ao executar teste para cenário {scen['folder']}")

    if not resultados_scenarios:
        logger.error("Nenhum cenário pôde ser testado com sucesso.")
        return False

    # Converter métricas de texto para float para ordenação/seleção corretas
    for r in resultados_scenarios:
        for k in ["val_MAE_valida", "val_RMSE_valida", "test_MAE_teste", "test_RMSE_teste", "val_MAE_treino_val", "test_MAE_treino"]:
            if k in r:
                try:
                    r[f"{k}_float"] = float(r[k])
                except ValueError:
                    r[f"{k}_float"] = float('inf')
            else:
                r[f"{k}_float"] = float('inf')

    # Melhor cenário por MAE de Teste
    best_test_mae = min(resultados_scenarios, key=lambda x: x["test_MAE_teste_float"])
    # Melhor cenário por MAE de Validação
    best_val_mae = min(resultados_scenarios, key=lambda x: x["val_MAE_valida_float"])
    # Melhor cenário escolhido pelo GA (ranking original["melhor_geral"])
    best_ga_fitness = ranking["melhor_geral"]
    # Encontrar esse correspondente na nossa lista com as métricas calculadas
    best_ga_match = next((r for r in resultados_scenarios if r["folder"] == best_ga_fitness["folder"]), best_ga_fitness)

    logger.info("---")
    logger.info(f"Melhor por MAE de Teste: Run {best_test_mae['run']} | Win {best_test_mae['win_dist']} | W {best_test_mae['w_dist']} | MAE={best_test_mae['test_MAE_teste']}")
    logger.info(f"Melhor por MAE de Validação: Run {best_val_mae['run']} | Win {best_val_mae['win_dist']} | W {best_val_mae['w_dist']} | MAE={best_val_mae['val_MAE_valida']}")
    logger.info(f"Melhor por Fitness do GA: Run {best_ga_match.get('run')} | Win {best_ga_match.get('win_dist')} | W {best_ga_match.get('w_dist')} | Fitness={best_ga_match.get('fitness')}")
    logger.info("---")

    # Copiar os gráficos do melhor cenário por MAE de Teste para grafico_validacao.png e grafico_teste.png
    best_val_graph_src = os.path.join(output_dir, f"grafico_validacao_{best_test_mae['win_dist']}_{best_test_mae['w_dist']}_run{best_test_mae['run']}.png")
    best_test_graph_src = os.path.join(output_dir, f"grafico_teste_{best_test_mae['win_dist']}_{best_test_mae['w_dist']}_run{best_test_mae['run']}.png")
    
    if os.path.exists(best_val_graph_src):
        shutil.copy2(best_val_graph_src, os.path.join(output_dir, "grafico_validacao.png"))
        logger.ok("grafico_validacao.png criado (copiado do melhor cenário de teste)")
    else:
        logger.warn(f"Gráfico de validação de origem não encontrado: {best_val_graph_src}")
        
    if os.path.exists(best_test_graph_src):
        shutil.copy2(best_test_graph_src, os.path.join(output_dir, "grafico_teste.png"))
        logger.ok("grafico_teste.png criado (copiado do melhor cenário de teste)")
    else:
        logger.warn(f"Gráfico de teste de origem não encontrado: {best_test_graph_src}")

    # Escrever relatório consolidado
    txt_path = os.path.join(output_dir, "resultados_validacao_teste.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("         RESULTADOS ESN — PETR4 TCC Maycon G Silva\n")
        f.write(f"         Relatório Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        f.write("--- TABELA COMPARATIVA DOS 12 CENÁRIOS ---\n")
        f.write("As métricas a seguir foram obtidas avaliando as matrizes ótimas nas partições de validação e teste.\n\n")
        
        f.write("| Run | Distribuição Win | Distribuição W | MAE (Validação) | RMSE (Validação) | MAE (Teste) | RMSE (Teste) |\n")
        f.write("|-----|------------------|----------------|-----------------|------------------|-------------|--------------|\n")
        for r in resultados_scenarios:
            f.write(
                f"| {r['run']:3s} | {r['win_dist']:16s} | {r['w_dist']:14s} | "
                f"{r.get('val_MAE_valida', '?'):15s} | {r.get('val_RMSE_valida', '?'):16s} | "
                f"{r.get('test_MAE_teste', '?'):11s} | {r.get('test_RMSE_teste', '?'):12s} |\n"
            )
        f.write("\n")

        # Escrever melhor de teste
        f.write("--- MELHOR CENÁRIO DE TESTE (Menor MAE de Teste) ---\n")
        f.write(f"Cenário:      Run {best_test_mae['run']} | Win {best_test_mae['win_dist']} | W {best_test_mae['w_dist']}\n")
        f.write(f"Época GA:     {best_test_mae['epoca_melhor_fitness']}\n")
        f.write(f"Hiperparâmetros:\n")
        f.write(f"  a             = {best_test_mae['a']}\n")
        f.write(f"  sr            = {best_test_mae['sr']}\n")
        f.write(f"  initLen       = {best_test_mae['initLen']}\n")
        f.write(f"  tam_reservoir = {best_test_mae['tam_reservoir']}\n")
        f.write(f"  reg           = {best_test_mae['reg']}\n")
        f.write(f"Resultados:\n")
        f.write(f"  MAE  Validação = {best_test_mae.get('val_MAE_valida', '?')}\n")
        f.write(f"  RMSE Validação = {best_test_mae.get('val_RMSE_valida', '?')}\n")
        f.write(f"  MAE  Teste     = {best_test_mae.get('test_MAE_teste', '?')}\n")
        f.write(f"  RMSE Teste     = {best_test_mae.get('test_RMSE_teste', '?')}\n\n")

        # Escrever melhor de validação
        f.write("--- MELHOR CENÁRIO DE VALIDAÇÃO (Menor MAE de Validação) ---\n")
        f.write(f"Cenário:      Run {best_val_mae['run']} | Win {best_val_mae['win_dist']} | W {best_val_mae['w_dist']}\n")
        f.write(f"Época GA:     {best_val_mae['epoca_melhor_fitness']}\n")
        f.write(f"Resultados:\n")
        f.write(f"  MAE  Validação = {best_val_mae.get('val_MAE_valida', '?')}\n")
        f.write(f"  RMSE Validação = {best_val_mae.get('val_RMSE_valida', '?')}\n")
        f.write(f"  MAE  Teste     = {best_val_mae.get('test_MAE_teste', '?')}\n")
        f.write(f"  RMSE Teste     = {best_val_mae.get('test_RMSE_teste', '?')}\n\n")

        # Escrever melhor do GA
        f.write("--- CENÁRIO SELECIONADO PELO GA (Melhor Fitness) ---\n")
        f.write(f"Cenário:      Run {best_ga_match.get('run')} | Win {best_ga_match.get('win_dist')} | W {best_ga_match.get('w_dist')}\n")
        f.write(f"Fitness GA:   {best_ga_match.get('fitness')}\n")
        f.write(f"Época GA:     {best_ga_match.get('epoca_melhor_fitness')}\n")
        f.write(f"Resultados:\n")
        f.write(f"  MAE  Validação = {best_ga_match.get('val_MAE_valida', '?')}\n")
        f.write(f"  RMSE Validação = {best_ga_match.get('val_RMSE_valida', '?')}\n")
        f.write(f"  MAE  Teste     = {best_ga_match.get('test_MAE_teste', '?')}\n")
        f.write(f"  RMSE Teste     = {best_ga_match.get('test_RMSE_teste', '?')}\n")

    logger.ok(f"Relatório geral com os 12 cenários salvo com sucesso em: {txt_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Fase 3 — Injeção e Teste ESN/GA")
    parser.add_argument("session_dir", help="Caminho da pasta da sessão")
    parser.add_argument("--log", default=None, help="Caminho do pipeline.log")
    args = parser.parse_args()

    logger = PhaseLogger("FASE 3", args.log)
    logger.info("INÍCIO — Injetando parâmetros de todos os cenários e rodando R")

    start = datetime.now()
    ok = inject_and_test(args.session_dir, logger)
    elapsed = datetime.now() - start

    if not ok:
        logger.error(f"Fase 3 falhou. Tempo: {elapsed}")
        sys.exit(1)

    logger.info(f"CONCLUÍDO — Tempo: {elapsed}")

if __name__ == "__main__":
    main()

