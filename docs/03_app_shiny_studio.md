# 🖥️ Componente 3: ESNAUTO Benchmark Studio (R Shiny Web App)

O **ESNAUTO Benchmark Studio** é uma aplicação web interativa desenvolvida em **R Shiny** com uma interface moderna (UI/UX premium) para visualização, otimização genética em tempo real, ajuste de parâmetros e comparação simultânea entre a **Echo State Network (ESN)** e modelos clássicos de Deep Learning Recorrente (**LSTM** e **GRU**).

---

## 📂 Arquivos Integrantes do Componente

```
ESNAUTO/
└── app/
    ├── app.R                          # Orquestrador Master (UI + Server + Botão Universal + Live Widget)
    │
    ├── modules/                       # Módulos isolados por responsabilidade
    │   ├── mod_esn.R                  # Módulo interativo da ESN (Presets, Custom e GA Live)
    │   ├── mod_lstm.R                 # Módulo interativo da rede LSTM (Keras 3 / TensorFlow)
    │   ├── mod_gru.R                  # Módulo interativo da rede GRU (Keras 3 / TensorFlow)
    │   └── mod_comparacao.R           # Módulo de comparação unificada, custo-benefício e histórico CSV
    │
    ├── utils/                         # Funções e Motores de IA
    │   ├── ga_engine.R                # Motor Live GA (Cromossomo 55-bits + LHS + Cataclismo Adaptativo + IPC Flags)
    │   ├── esn_core.R                 # Módulo analítico de treino Ridge, validação e teste cego out-of-sample
    │   ├── history_tracker.R          # Gerenciador persistente de histórico em CSV e recordes globais
    │   ├── data_prep.R                # Carregamento, particionamento e catálogo de distribuições
    │   └── metrics.R                  # Cálculo de métricas financeiras (MAE, RMSE, MAPE, R², tempo)
    │
    └── www/                           # Recursos estáticos de design
        └── custom.css                 # CSS customizado (Live Widget, botões 52px, tema dark/light)
```

---

## 🚀 Como Executar o App R Shiny

Abra o console do R ou terminal PowerShell e execute:

```powershell
& 'C:\Program Files\R\R-4.6.0\bin\Rscript.exe' -e "shiny::runApp('app', port = 8080, host = '127.0.0.1')"
```
Ou abra o arquivo `app/app.R` no RStudio e clique no botão **Run App**.

---

## ⚡ Botão Universal Unificado de Benchmark

No topo da aplicação, o **Hero Banner Global** disponibiliza o botão master:
> **`⚡ EXECUTAR BENCHMARK COMPLETO (ESN + GA + LSTM + GRU)`**

Ao clicar, abre-se um modal de configuração permitindo escolher:

### 1. Perfis de Execução da ESN:
* 🏆 **Opção A — Produção Completa (Padrão TCC Oficial)**: 10.000 Gerações, critério de parada `run = 3500`, população = 10.
* 🔬 **Opção B — Otimização Rápida de Demonstração**: 60 a 500 Gerações (~30s a 2min).
* ⚙️ **Opção C — GA Personalizado**: Slider de 100 a 15.000 Gerações, população e tolerância de parada configuráveis.
* ⚡ **Opção D — Preset Histórico Instantâneo**: Inferência com os melhores hiperparâmetros clássicos do TCC (~5s).

### 2. Atalhos de Seleção por Onda Estratégica:
* `⚡ 4 Cenários TCC`: $W_{in} \in \{\text{GED}, \text{Normal}, \text{Uniforme}\}$, $W \in \{\text{Normal}, \text{Uniforme}\}$.
* `🌊 Onda 1: Caudas Pesadas`: $W_{in} \in \{\text{Pearson V}, \text{t-Student}, \text{Laplace}\}$, $W \in \{\text{Normal}, \text{Uniforme}, \text{t-Student}\}$.
* `🌊 Onda 2: Shocks & Assimetrias`: $W_{in} \in \{\text{Cauchy}, \text{t-Student Assimétrica}, \text{Laplace}\}$, $W \in \{\text{Normal}, \text{Cauchy}, \text{Laplace}\}$.
* `🌊 Onda 3: Esparsidade & Snedecor`: $W_{in} \in \{\text{Normal Esparsa}, \text{GED}\}$, $W \in \{\text{Normal Esparsa}, \text{F-Snedecor}, \text{GED}\}$.
* `🌊 Onda 4: Híbridos`: Combinações cruzadas com normalização espectral e esparsidade.

### 3. Perfil de Treinamento Deep Learning:
* 🏆 **DL Produção (Padrão Oficial)**: **80 épocas** (~40s) — garante convergência e comparação justa com a ESN.
* ⚡ **DL Rápido**: 25 épocas (~15s).
* ⚙️ **DL Personalizado**: 10 a 200 épocas e timesteps ajustáveis.

---

## 🎛️ Widget Flutuante Interativo de Controle ao Vivo (Live Controller)

Fixado no **canto inferior direito** da interface durante qualquer execução:
1. **Badge Dinâmico**: `🟢 Executando (X%)` / `⏸️ Pausado` / `⏹️ Cancelando`.
2. **Progresso em Tempo Real**: Geração atual, fitness do líder, cataclismos ocorridos e estágio atual.
3. **Barra Gradiente Fluida**: Atualizada a cada geração do GA e a cada época do Deep Learning.
4. **Botão Dinâmico de Pausa/Retomada (`btn_pause_toggle_js`)**:
   - Durante a execução: exibe **`⏸️ Pausar`** (roxo/aviso).
   - Ao ser clicado: congela o GA no exato ponto da geração e muda instantaneamente para **`▶️ Retomar`** (verde).
   - Ao ser clicado novamente: retoma o processamento e volta a exibir **`⏸️ Pausar`**.
5. **Botão de Interrupção Segura (`⏹️ Cancelar & Salvar`)**:
   - Interrompe o GA com segurança sem perder os cálculos já realizados.
   - Avalia o melhor indivíduo encontrado até a geração atual na partição de validação e teste.
   - Salva o registro imediatamente no arquivo `Scripts/results/historico_otimizacoes_ga.csv` com a tag `(Cancelado)`.

---

## ⚙️ Arquitetura de Comunicação em Tempo Real

Para contornar o comportamento síncrono *single-threaded* do R durante o loop de CPU do GA:
* **Bomba de Rede WebSocket**: Inserido `httpuv::service(10)` no monitor de cada geração (`monitor_ga_cataclisma`) para descarregar a fila de pacotes TCP/WebSocket da rede instantaneamente.
* **Servidor HTTP Local de Controle (Portas 8089–8092)**: Permite que o JavaScript no navegador faça chamadas `fetch(..., {mode: 'no-cors'})` diretamente para o R sem depender apenas da fila interna do Shiny.
* **Sinalização IPC por Arquivos de Flag**: Flags atômicas no diretório temporário (`ga_cancelar.flag` e `ga_pausar.flag`) garantem resposta em tempo inferior a 1 milissegundo.

---

## 💥 Calibração Adaptativa do Cataclismo (Hipermutação CHC)

O operador de Cataclismo evita estagnação no espaço de $2^{55} \approx 3{,}60 \times 10^{16}$ estados. O gatilho de estagnação $\theta_{\text{limiar}}$ calibra-se automaticamente conforme o tamanho do horizonte:

| Horizonte de Gerações | Limiar sem Melhora ($\theta_{\text{limiar}}$) | Comportamento do Algoritmo |
| :--- | :--- | :--- |
| **$\le 500$ gerações** | **30 gerações** | Sensibilidade alta para screening ágil. |
| **$1.000$ a $4.999$ gerações** | **50 gerações** | Equilíbrio entre refinamento local e saltos quânticos. |
| **$5.000$ a $9.999$ gerações** | **80 gerações** | Exploração aprofundada de cada bacia de atração. |
| **$\ge 10.000$ gerações** | **100 gerações** | **Exploração exaustiva e refinamento máximo** antes do próximo cataclismo. |

---

## 📜 Histórico e Persistência de Resultados

Todas as execuções do GA são consolidadas em:
- [`Scripts/results/historico_otimizacoes_ga.csv`](../Scripts/results/historico_otimizacoes_ga.csv)
- **Novo Recorde Mundial Global**: Caso uma combinação supere o melhor MAE de teste de todos os tempos, as matrizes numéricas $W_{in}$, $W$ e $W_{out}$ e os parâmetros ótimos são exportados automaticamente em:
  `Scripts/results/melhor_recorde_global/`

