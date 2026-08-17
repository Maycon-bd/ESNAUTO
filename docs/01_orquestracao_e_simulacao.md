# ⚙️ Componente 1: Orquestração e Simulação Batch ESN + GA

Este componente é responsável pelo **disparo automatizado**, **orquestração em lote (batch)** e **treinamento da Echo State Network (ESN)** otimizada via **Algoritmo Genético (GA)**. Ele garante que as 12 simulações experimentais do TCC sejam executadas com reprodutibilidade, isolamento de resultados e sem poluição visual no ambiente.

---

## 📂 Arquivos Integrantes do Componente

```
ESNAUTO/
├── automate_simulations.py        # Orquestrador central em Python
├── run_simulations.bat            # Atalho interativo para Windows
└── Scripts/
    ├── acoes_petr4_esn.R          # Script R parametrizado ESN + GA
    └── gerar_graficos_corrigidos.R# Script R auxiliar de geração de gráficos
```

---

## 📝 Detalhamento de Cada Arquivo

### 1. `automate_simulations.py`
- **Caminho**: [`automate_simulations.py`](../automate_simulations.py)
- **Linguagem**: Python 3 (Biblioteca Padrão)
- **Função**: Orquestrador principal do sistema. Gerencia o ciclo de vida das simulações sequenciais dos 4 cenários experimentais repetidos em 3 rodadas (totalizando 12 simulações por execução).

#### 🔑 Principais Funcionalidades:
- **Criação de Sessão Única**: A cada disparo, gera uma pasta de execução com data/hora em `Scripts/results/Run_YYYYMMDD_HHMMSS_{Mode}/`.
- **Gerenciamento de Subpastas**: Cria automaticamente `scenarios/`, `pdfs/` e `zips/` dentro da sessão.
- **Invocação do Rscript**: Detecta o binário `Rscript.exe` no sistema Windows ou Linux (incluindo busca automática em `C:\Program Files\R`) e dispara o script `acoes_petr4_esn.R` com 5 argumentos CLI.
- **Cópias e Compactação**: Ao final de cada cenário, realiza a cópia direta do PDF gerado para a pasta `pdfs/` e empacota o cenário em um arquivo `.zip` individual em `zips/`.

#### 💻 Parâmetros de Linha de Comando:
```bash
# Rodar em modo teste rápido (200 gerações GA)
python automate_simulations.py --test

# Rodar em modo produção (10.000 gerações GA em todas as 3 rodadas)
python automate_simulations.py

# Rodar apenas uma rodada específica em produção (ex: rodada 2)
python automate_simulations.py --run 2

# Definir número customizado de gerações do GA (ex: 5000)
python automate_simulations.py --itera 5000
```

---

### 2. `run_simulations.bat`
- **Caminho**: [`run_simulations.bat`](../run_simulations.bat)
- **Linguagem**: Batch Script (Windows CMD)
- **Função**: Interface amigável de linha de comando para uso no Windows. Evita a necessidade de digitar comandos longos no terminal.

#### 🕹️ Opções do Menu Interativo:
1. `1`: Executa a suíte de testes rápidos com 200 gerações (`python automate_simulations.py --test`).
2. `2`: Executa a bateria de produção com 10.000 gerações (`python automate_simulations.py`).
3. `3`: Cancela a operação e encerra.

---

### 3. `Scripts/acoes_petr4_esn.R`
- **Caminho**: [`Scripts/acoes_petr4_esn.R`](../Scripts/acoes_petr4_esn.R)
- **Linguagem**: R (v4.0+)
- **Função**: Script numérico central que implementa o modelo ESN (Echo State Network) e a otimização de hiperparâmetros via Algoritmo Genético (pacote `GA`).

#### 🎛️ Argumentos Recebidos via CLI (`commandArgs`):
1. `win_dist`: Distribuição da matriz de pesos de entrada $W_{in}$ (`Normal`, `Uniforme`, `GED`).
2. `w_dist`: Distribuição da matriz de pesos do reservatório $W$ (`Normal`, `Uniforme`).
3. `num_iter`: Número máximo de gerações do GA (ex: 200 ou 10000).
4. `run_id`: Identificador da rodada (`1`, `2` ou `3`).
5. `output_dir`: Caminho absoluto onde todos os CSVs, logs de fitness, matrizes e o PDF final devem ser gravados.

#### 🧬 Hiperparâmetros Otimizados pelo GA:
- **Taxa de Vazão ($a$)**: $[0.01, 1.00]$ — Inércia dos neurônios do reservatório.
- **Raio Espectral ($sr$)**: $[0.01, 0.99]$ — Escalamento dos autovalores de $W$.
- **Período de Lavagem ($initLen$)**: $[1, 200]$ — Passos descartados para eliminação de estados transientes.
- **Tamanho do Reservatório ($tam\_reservoir$)**: $[3, 50]$ — Quantidade de neurônios no reservatório.
- **Regularização Ridge ($reg$)**: $[10^{-7}, 10^{-2}]$ — Penalidade da regressão de saída $W_{out}$.

#### 📤 Arquivos Gerados por Cenário:
- `Dados PETR4 ESN_mae_otim40x60 com factor {iter}_{run} ... .csv`: CSV contendo predições e valores reais da partição de validação.
- `Dados PETR4 resumo fitness ... .csv`: Histórico da curva de evolução de fitness por época do GA.
- `matriz_Win_epoca_{epoca}.txt`: Matriz de entrada extraída na melhor época.
- `matriz_W_epoca_{epoca}.txt`: Matriz de conexões do reservatório extraída na melhor época.
- `{nome_do_cenario}.pdf`: PDF compilado contendo o histograma da série temporal e os gráficos da curva de evolução de fitness.

---

### 4. `Scripts/gerar_graficos_corrigidos.R`
- **Caminho**: [`Scripts/gerar_graficos_corrigidos.R`](../Scripts/gerar_graficos_corrigidos.R)
- **Linguagem**: R
- **Função**: Script auxiliar pós-simulação para a plotagem em alta resolução (PNG 300 DPI) das curvas de predição *Validação* vs. *Valores Reais* e *Teste Out-of-Sample* vs. *Valores Reais*. Utiliza correções visuais e paletas de cores otimizadas para a monografia do TCC.
