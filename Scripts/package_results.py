"""
package_results.py — FASE 4 do Pipeline ESN/GA
Copia todos os arquivos de resultado para a pasta 'entrega/'
e cria um ZIP final nomeado com a data atual.

Uso:
    python package_results.py <session_dir>
    python package_results.py <session_dir> --log <pipeline_log_path>
"""

import os
import sys
import shutil
import argparse
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
# Empacotamento
# ──────────────────────────────────────────────
def package(session_dir, logger):
    entrega_dir = os.path.join(session_dir, "entrega")
    os.makedirs(entrega_dir, exist_ok=True)

    # 1. Arquivos obrigatórios esperados
    arquivos_obrigatorios = [
        os.path.join(entrega_dir, "resultados_validacao_teste.txt"),
        os.path.join(entrega_dir, "grafico_validacao.png"),
        os.path.join(entrega_dir, "grafico_teste.png"),
    ]

    faltando = []
    for arq in arquivos_obrigatorios:
        if os.path.exists(arq):
            size_kb = os.path.getsize(arq) / 1024
            logger.ok(f"Arquivo presente: {os.path.basename(arq)} ({size_kb:.1f} KB)")
        else:
            logger.warn(f"Arquivo não encontrado: {os.path.basename(arq)}")
            faltando.append(arq)

    if faltando:
        logger.warn(f"{len(faltando)} arquivo(s) não encontrado(s). O ZIP será criado mesmo assim.")

    # 2. Copiar ranking.json para entrega
    ranking_src = os.path.join(session_dir, "ranking.json")
    ranking_dst = os.path.join(entrega_dir, "ranking_cenarios.json")
    if os.path.exists(ranking_src):
        shutil.copy2(ranking_src, ranking_dst)
        logger.ok("ranking_cenarios.json copiado para entrega/")
    else:
        logger.warn("ranking.json não encontrado — será omitido do ZIP.")

    # 3. Copiar pipeline.log para entrega
    log_src = os.path.join(session_dir, "pipeline.log")
    log_dst = os.path.join(entrega_dir, "pipeline.log")
    if os.path.exists(log_src):
        shutil.copy2(log_src, log_dst)
        logger.ok("pipeline.log copiado para entrega/")

    # 4. Copiar ZIPs individuais dos cenários (da pasta zips/)
    zips_dir = os.path.join(session_dir, "zips")
    if os.path.isdir(zips_dir):
        cenarios_zips = [f for f in os.listdir(zips_dir) if f.endswith(".zip")]
        if cenarios_zips:
            cenarios_zip_dir = os.path.join(entrega_dir, "cenarios_zips")
            os.makedirs(cenarios_zip_dir, exist_ok=True)
            for z in cenarios_zips:
                shutil.copy2(os.path.join(zips_dir, z), os.path.join(cenarios_zip_dir, z))
            logger.ok(f"{len(cenarios_zips)} ZIPs de cenários copiados para entrega/cenarios_zips/")
        else:
            logger.warn("Nenhum ZIP de cenário encontrado na pasta zips/")
    else:
        logger.warn("Pasta zips/ não encontrada — ZIPs individuais não serão incluídos.")

    # 5. Criar ZIP final
    datahora = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_nome = f"ESN_PETR4_TCC_Maycon_{datahora}"
    zip_path = os.path.join(session_dir, zip_nome)

    logger.info(f"Criando ZIP final: {zip_nome}.zip ...")
    try:
        shutil.make_archive(zip_path, "zip", entrega_dir)
        zip_file = zip_path + ".zip"
        size_mb  = os.path.getsize(zip_file) / (1024 * 1024)
        logger.ok(f"ZIP criado: {os.path.basename(zip_file)} ({size_mb:.2f} MB)")
    except Exception as e:
        logger.error(f"Falha ao criar ZIP: {e}")
        return False

    # 6. Resumo final
    logger.info("-" * 50)
    logger.info("PACOTE FINAL GERADO:")
    logger.info(f"  Pasta entrega: {entrega_dir}")
    logger.info(f"  ZIP final:     {zip_file}")
    logger.info("-" * 50)
    logger.info("Conteúdo da entrega/:")
    for root, dirs, files in os.walk(entrega_dir):
        level = root.replace(entrega_dir, "").count(os.sep)
        indent = "  " * (level + 1)
        for file in files:
            fpath = os.path.join(root, file)
            size_kb = os.path.getsize(fpath) / 1024
            logger.info(f"{indent}{file} ({size_kb:.1f} KB)")

    return True


def main():
    parser = argparse.ArgumentParser(description="Fase 4 — Empacotamento de Resultados ESN/GA")
    parser.add_argument("session_dir", help="Caminho da pasta da sessão")
    parser.add_argument("--log", default=None, help="Caminho do pipeline.log")
    args = parser.parse_args()

    logger = PhaseLogger("FASE 4", args.log)
    logger.info("INÍCIO — Empacotando resultados para entrega")

    start = datetime.now()
    ok = package(args.session_dir, logger)
    elapsed = datetime.now() - start

    if not ok:
        logger.error(f"Fase 4 falhou. Tempo: {elapsed}")
        sys.exit(1)

    logger.info(f"CONCLUÍDO — Tempo: {elapsed}")


if __name__ == "__main__":
    main()
