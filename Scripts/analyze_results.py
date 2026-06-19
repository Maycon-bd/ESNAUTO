"""
analyze_results.py — FASE 2 do Pipeline ESN/GA
Analisa os CSVs de resultados de todos os cenários de uma sessão,
ranqueia por fitness e salva ranking.json para uso nas fases seguintes.

Uso:
    python analyze_results.py <session_dir>
    python analyze_results.py <session_dir> --log <pipeline_log_path>
"""

import os
import sys
import json
import argparse
from datetime import datetime


# ──────────────────────────────────────────────
# Logger simples compatível com pipeline.py
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

    def info(self, msg):   self._write(msg)
    def ok(self, msg):     self._write(f"OK — {msg}")
    def error(self, msg):  self._write(f"ERRO — {msg}")
    def warn(self, msg):   self._write(f"AVISO — {msg}")


# ──────────────────────────────────────────────
# Leitura dos arquivos de fitness
# ──────────────────────────────────────────────
def parse_fitness_file(filepath):
    """
    Lê o arquivo 'melhores_fitness' de um cenário e retorna
    os dados da última linha válida (melhor solução encontrada pelo AG).
    Retorna None se o arquivo não puder ser lido.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        last_valid = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            # Pula linhas de cabeçalho (coluna 1 não é número)
            try:
                int(parts[0].strip('"'))
            except ValueError:
                continue
            try:
                fitness = float(parts[6].strip('"'))
                last_valid = {
                    "epoca":        int(parts[0].strip('"')),
                    "a":            float(parts[1].strip('"')),
                    "sr":           float(parts[2].strip('"')),
                    "initLen":      int(parts[3].strip('"')),
                    "tam_reservoir":int(parts[4].strip('"')),
                    "reg":          float(parts[5].strip('"')),
                    "fitness":      fitness,
                }
            except (ValueError, IndexError):
                continue

        return last_valid
    except Exception as e:
        return None


def get_last_epoch_from_file(filepath):
    """
    Retorna o número da última época registrada em um arquivo de matrizes
    (Win, W ou Wout), ignorando cabeçalhos repetidos.
    """
    last_epoch = None
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            try:
                ep = int(parts[1].strip('"'))
                last_epoch = ep
            except ValueError:
                continue
    except Exception:
        pass
    return last_epoch


# ──────────────────────────────────────────────
# Função principal de análise
# ──────────────────────────────────────────────
def analyze(session_dir, logger):
    scenarios_dir = os.path.join(session_dir, "scenarios")
    if not os.path.isdir(scenarios_dir):
        logger.error(f"Pasta de cenários não encontrada: {scenarios_dir}")
        return None

    cenarios = sorted([
        d for d in os.listdir(scenarios_dir)
        if os.path.isdir(os.path.join(scenarios_dir, d))
    ])

    if not cenarios:
        logger.error("Nenhum cenário encontrado na pasta de scenarios.")
        return None

    logger.info(f"Encontrados {len(cenarios)} cenários para análise.")

    resultados = []

    for folder in cenarios:
        folder_path = os.path.join(scenarios_dir, folder)

        # Encontrar arquivo de fitness
        fitness_file = None
        for f in os.listdir(folder_path):
            if "melhores_fitness" in f and f.endswith(".csv"):
                fitness_file = os.path.join(folder_path, f)
                break

        if not fitness_file:
            logger.warn(f"Arquivo melhores_fitness não encontrado em: {folder}")
            continue

        dados = parse_fitness_file(fitness_file)
        if not dados:
            logger.warn(f"Não foi possível ler fitness de: {folder}")
            continue

        # Extrair distribuições do nome da pasta
        win_dist = "Desconhecida"
        w_dist   = "Desconhecida"
        run_num  = "?"
        name = folder

        # Extrai run number
        import re
        run_match = re.search(r"factor \d+_(\d+)", name)
        if run_match:
            run_num = run_match.group(1)

        # Extrai distribuições Win e W
        win_match = re.search(r"Win (\w+) e W (\w+)$", name)
        if win_match:
            win_dist = win_match.group(1)
            w_dist   = win_match.group(2)

        # Encontrar arquivos de matrizes e última época
        win_file = wout_file = w_file = None
        for f in os.listdir(folder_path):
            fl = f.lower()
            if "petr4 win esn" in fl and f.endswith(".csv"):
                win_file = os.path.join(folder_path, f)
            elif "petr4 w reserv" in fl and f.endswith(".csv"):
                w_file = os.path.join(folder_path, f)
            elif "petr4 wout esn" in fl and f.endswith(".csv"):
                wout_file = os.path.join(folder_path, f)

        ultima_epoca_matrizes = None
        if win_file:
            ultima_epoca_matrizes = get_last_epoch_from_file(win_file)

        resultado = {
            "folder":                folder,
            "folder_path":           folder_path,
            "run":                   run_num,
            "win_dist":              win_dist,
            "w_dist":                w_dist,
            "fitness":               dados["fitness"],
            "a":                     dados["a"],
            "sr":                    dados["sr"],
            "initLen":               dados["initLen"],
            "tam_reservoir":         dados["tam_reservoir"],
            "reg":                   dados["reg"],
            "epoca_melhor_fitness":  dados["epoca"],
            "epoca_matrizes":        ultima_epoca_matrizes,
            "win_file":              win_file,
            "w_file":                w_file,
            "wout_file":             wout_file,
        }
        resultados.append(resultado)
        logger.info(
            f"  Run {run_num} | Win {win_dist:9s} | W {w_dist:9s} | "
            f"Fitness={dados['fitness']:.15f} | Época melhor={dados['epoca']}"
        )

    if not resultados:
        logger.error("Nenhum resultado válido encontrado.")
        return None

    # Ordenar por fitness (menos negativo = melhor MAE)
    resultados_sorted = sorted(resultados, key=lambda x: x["fitness"], reverse=True)

    melhor_geral = resultados_sorted[0]
    logger.ok(
        f"Melhor geral: Run {melhor_geral['run']} | "
        f"Win {melhor_geral['win_dist']} | W {melhor_geral['w_dist']} | "
        f"Fitness={melhor_geral['fitness']:.15f}"
    )

    # Melhor por distribuição Win
    melhor_por_win = {}
    for dist in set(r["win_dist"] for r in resultados):
        candidatos = [r for r in resultados if r["win_dist"] == dist]
        melhor_por_win[dist] = max(candidatos, key=lambda x: x["fitness"])

    # Melhor por distribuição W
    melhor_por_w = {}
    for dist in set(r["w_dist"] for r in resultados):
        candidatos = [r for r in resultados if r["w_dist"] == dist]
        melhor_por_w[dist] = max(candidatos, key=lambda x: x["fitness"])

    ranking = {
        "session_dir":       session_dir,
        "total_cenarios":    len(resultados),
        "melhor_geral":      melhor_geral,
        "melhor_por_win":    melhor_por_win,
        "melhor_por_w":      melhor_por_w,
        "ranking_completo":  resultados_sorted,
    }

    # Salvar ranking.json
    ranking_path = os.path.join(session_dir, "ranking.json")
    with open(ranking_path, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)
    logger.ok(f"ranking.json salvo em: {ranking_path}")

    return ranking


# ──────────────────────────────────────────────
# Entry point standalone
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Fase 2 — Análise de Resultados ESN/GA")
    parser.add_argument("session_dir", help="Caminho da pasta da sessão (Run_YYYYMMDD_...)")
    parser.add_argument("--log", default=None, help="Caminho do arquivo pipeline.log")
    args = parser.parse_args()

    logger = PhaseLogger("FASE 2", args.log)
    logger.info("INÍCIO — Analisando resultados de todos os cenários")

    start = datetime.now()
    ranking = analyze(args.session_dir, logger)
    elapsed = datetime.now() - start

    if ranking is None:
        logger.error(f"Análise falhou. Tempo: {elapsed}")
        sys.exit(1)

    logger.info(f"CONCLUÍDO — Tempo: {elapsed}")


if __name__ == "__main__":
    main()
