import os
import sys
import subprocess
import shutil
import argparse
import random
from datetime import datetime

# Configurações globais
SCRIPT_R_NAME = "acoes_petr4_esn.R"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "Scripts")
RESULTS_DIR = os.path.join(SCRIPTS_DIR, "results")

# Cenários de simulação aprovados para o TCC
SCENARIOS = [
    {"win": "Normal",   "w": "Normal"},
    {"win": "Uniforme", "w": "Uniforme"},
    {"win": "GED",      "w": "Uniforme"},
    {"win": "GED",      "w": "Normal"},
]

def get_rscript_path():
    # 1. Tenta encontrar no PATH do sistema
    if shutil.which("Rscript") is not None:
        return "Rscript"
    
    # 2. Tenta encontrar no diretório padrão do Windows para R
    pf_r = r"C:\Program Files\R"
    if os.path.exists(pf_r):
        for version in sorted(os.listdir(pf_r), reverse=True):
            # Tenta na pasta bin padrão
            rscript_path = os.path.join(pf_r, version, "bin", "Rscript.exe")
            if os.path.exists(rscript_path):
                return rscript_path
            # Tenta também na pasta x64 dentro de bin
            rscript_path_x64 = os.path.join(pf_r, version, "bin", "x64", "Rscript.exe")
            if os.path.exists(rscript_path_x64):
                return rscript_path_x64
                
    return "Rscript"

def print_banner(text):
    print("=" * 60)
    print(f" {text}")
    print("=" * 60)

def main():
    # Parsing de argumentos via argparse
    parser = argparse.ArgumentParser(description="Automação de simulações ESN - TCC")
    parser.add_argument("--test", "-t", action="store_true", help="Rodar em modo teste rápido com 200 iterações")
    parser.add_argument("--run", "-r", type=str, default=None, help="Número da rodada/execução (substitui o '_1' final). Se omitido, roda as rodadas 1, 2 e 3 sequencialmente.")
    parser.add_argument("--itera", "-i", type=int, default=10000, help="Número total de iterações do GA (padrão: 10000)")
    args = parser.parse_args()

    # Define número de iterações
    iterations = 200 if args.test else args.itera
    
    # Define a lista de rodadas
    if args.run is not None:
        run_numbers = [args.run]
    else:
        run_numbers = ["1", "2", "3"]

    # Criação do diretório estruturado da sessão
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode_tag = "Test" if args.test else "Prod"
    session_name = f"Run_{timestamp}_{mode_tag}"
    session_dir = os.path.join(RESULTS_DIR, session_name)
    scenarios_dir = os.path.join(session_dir, "scenarios")
    pdfs_dir = os.path.join(session_dir, "pdfs")
    zips_dir = os.path.join(session_dir, "zips")
    
    os.makedirs(scenarios_dir, exist_ok=True)
    os.makedirs(pdfs_dir, exist_ok=True)
    os.makedirs(zips_dir, exist_ok=True)

    print_banner(f"INICIANDO AUTOMAÇÃO DE SIMULAÇÕES ESN - TCC")
    print(f"Modo: {'TESTE (200 iterações)' if args.test else f'PRODUÇÃO ({iterations} iterações)'}")
    print(f"Rodadas (Runs) a serem executadas: {', '.join(run_numbers)}")
    print(f"Caminho Base: {BASE_DIR}")
    print(f"Caminho dos Resultados da Sessão: {session_dir}")
    print(f"Cenários definidos por rodada: {len(SCENARIOS)}")
    for i, sc in enumerate(SCENARIOS, 1):
        print(f"  {i}. Win: {sc['win']} | W: {sc['w']}")
    print("-" * 60)

    # Execução sequencial de cada rodada
    for run_number in run_numbers:
        print_banner(f"INICIANDO RODADA DE SIMULAÇÃO: {run_number}")
        
        for index, sc in enumerate(SCENARIOS, 1):
            win_dist = sc["win"]
            w_dist = sc["w"]
            
            # Gerar o ID aleatório de 4 dígitos para este cenário (ex: 4943, 5991, 6102, 9220)
            random_id = random.randint(1000, 9999)
            
            # Nomenclatura exata solicitada pelo usuário para a pasta e zip
            folder_name = f"AlgGen PETR4 ESN_mae_otim40x60 com factor {iterations}_{run_number} ({random_id}) Win {win_dist} e W {w_dist}"
            scenario_dir = os.path.join(scenarios_dir, folder_name)
            os.makedirs(scenario_dir, exist_ok=True)

            print_banner(f"Executando Rodada {run_number} - Cenário {index}/{len(SCENARIOS)}: Win {win_dist} e W {w_dist} (ID {random_id})")
            print(f"Salvando diretamente em: {scenario_dir}")
            
            # Montar comando Rscript usando caminho dinâmico detectado e passando o diretório de destino
            rscript_exec = get_rscript_path()
            cmd = [rscript_exec, SCRIPT_R_NAME, win_dist, w_dist, str(iterations), run_number, scenario_dir]
            print(f"Executando: {' '.join(cmd)}")
            print(f"Diretório de trabalho: {SCRIPTS_DIR}")
            print("Aguarde a finalização do processo (isso pode demorar)...")

            # Arquivo de log para salvar tudo que o script R printar
            log_file_path = os.path.join(scenario_dir, "run.log")
            
            try:
                with open(log_file_path, "w", encoding="utf-8") as log_file:
                    # Executa o subprocesso redirecionando stdout e stderr para o log
                    process = subprocess.Popen(
                        cmd, 
                        cwd=SCRIPTS_DIR, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        text=True, 
                        bufsize=1
                    )
                    
                    # Exibe a saída do R em tempo real no terminal da automação e salva no arquivo
                    for line in process.stdout:
                        sys.stdout.write(f"[R] {line}")
                        sys.stdout.flush()
                        log_file.write(line)
                    
                    process.wait()

                if process.returncode != 0:
                    print(f"\n[ERRO] O script R retornou código de erro: {process.returncode}")
                    print(f"Verifique o arquivo de log para detalhes: {log_file_path}")
                else:
                    print("\n[OK] Simulação concluída com sucesso no R!")

            except Exception as e:
                print(f"\n[ERRO] Falha ao executar o processo R: {e}")
                continue

            # Organização dos arquivos de saída (cópia de PDF e compactação de ZIP)
            print("\nOrganizando arquivos de saída...")
            
            # 1. Copiar o PDF para a pasta global de PDFs da sessão (para visualização rápida)
            pdf_filename = f"{folder_name}.pdf"
            pdf_src = os.path.join(scenario_dir, pdf_filename)
            pdf_dest = os.path.join(pdfs_dir, pdf_filename)
            if os.path.exists(pdf_src):
                try:
                    shutil.copy(pdf_src, pdf_dest)
                    print(f"  PDF copiado para a pasta consolidada: pdfs/{pdf_filename}")
                except Exception as e:
                    print(f"  [ERRO] Não foi possível copiar o PDF: {e}")
            else:
                print("  [AVISO] PDF do gráfico não encontrado na pasta do cenário.")

            # 2. Criar o arquivo ZIP do cenário na pasta global de ZIPs da sessão
            zip_dest_without_ext = os.path.join(zips_dir, folder_name)
            try:
                shutil.make_archive(zip_dest_without_ext, 'zip', scenario_dir)
                print(f"  Arquivo compactado criado: zips/{folder_name}.zip")
            except Exception as e:
                print(f"  [ERRO] Não foi possível criar o arquivo ZIP: {e}")

            print(f"Finalizado cenário: {folder_name}\n" + "-" * 60)

    print_banner("AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"Todos os resultados salvos de forma organizada na pasta da sessão:")
    print(f"  {session_dir}")

if __name__ == "__main__":
    main()
