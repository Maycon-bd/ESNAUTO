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

---

## 👨‍💻 Autoria, Propósito & Legado Acadêmico

### 1. Autoria do Software
- **Autor e Desenvolvedor:** **Maycon Garcia Silva**
- **Trabalho Acadêmico:** Trabalho de Conclusão de Curso (TFC) — Modelagem Preditiva de Séries Financeiras com ESN e Deep Learning.
- **Licença & Acesso:** Código acadêmico aberto para pesquisa, extensão e melhoria contínua.

### 2. Por que uma Aplicação Web Executada Localmente (Localhost / Desktop R Shiny)?
A aplicação foi projetada como um **site web executado em ambiente local (127.0.0.1:8080)**. Embora a hospedagem em servidores de nuvem pública seja comum na web, para o escopo deste projeto a execução local apresenta vantagens técnicas determinantes:
1. **Poder Computacional Irrestrito**: Simulações genéticas com até 15.000 gerações e treinamento de redes neurais profundas (LSTM/GRU com 80 épocas) exigem 100% dos núcleos de CPU e acesso direto à memória RAM/GPU da estação de trabalho, sem limites de *timeout* ou quotas restritivas de serviços em nuvem gratuitos.
2. **I/O de Alta Velocidade e Gravação Atômica**: Gravação em tempo real de matrizes de pesos com dezenas de milhares de elementos e logs linha a linha em disco local sem sobrecarga de rede.
3. **Controle Físico e Latência Zero**: O acoplamento entre o loop de inferência em C/R e o front-end Shiny através do servidor local e IPC Flags garante resposta instantânea para pausar, retomar e cancelar sem perda de dados.

### 3. Legado para os Futuros Orientandos do Laboratório
Este software e seu código-fonte foram intencionalmente estruturados de forma **modular, limpa e amplamente documentada** para servir como ponto de partida e legado para os **futuros alunos e orientandos do orientador**, facilitando a continuidade e expansão desta linha de pesquisa:
- **Novas Distribuições de Matrizes**: O catálogo em `app/utils/data_prep.R` possui arquitetura desacoplada via `registrar_distribuicao()`, permitindo adicionar novas distribuições estocásticas em poucas linhas.
- **Novas Topologias de Reservoir Computing**: A estrutura analítica de `ga_engine.R` e `esn_core.R` permite plugar facilmente variações como *Deep Echo State Networks (Deep-ESN)*, *Leaky ESN* e reservatórios com topologias de mundo pequeno (*Small-World Networks*).
- **Novas Metaheurísticas de Otimização**: A função de fitness e a interface de cromossomo de 55 bits podem ser herdadas para comparação com *Particle Swarm Optimization (PSO)*, *Differential Evolution (DE)* ou *Bayesian Optimization*.
- **Outras Séries Temporais Financeiras**: O particionamento em `app/app.R` permite carregar novos ativos (ex: VALE3, IBOV, Criptomoedas, Commodities) e re-executar todo o benchmark instantaneamente.

---

## 🛠️ Stack Tecnológico Utilizado & Referências Oficiais de Software

O desenvolvimento deste software integra um ecossistema científico e de engenharia de ponta:

| Tecnologia / Pacote | Versão / Função no Projeto | Referência Bibliográfica Oficial |
| :--- | :--- | :--- |
| **R Language & Environment** | Motor estatístico, matricial e inferência numérica | **R CORE TEAM**. *R: A Language and Environment for Statistical Computing*. Vienna, Austria: R Foundation for Statistical Computing, 2024. Disponível em: <https://www.R-project.org/>. |
| **R Shiny Framework** | Interface web interativa reativa e servidor WebSocket | **CHANG, W. et al.** *shiny: Web Application Framework for R*. R package version 1.9.1, 2024. Disponível em: <https://CRAN.R-project.org/package=shiny>. |
| **GA (Genetic Algorithms)** | Otimização estocástica e operadores evolutivos | **SCRUCCA, L.** *GA: A Package for Genetic Algorithms in R*. Journal of Statistical Software, v. 53, n. 4, p. 1–37, 2013. DOI: 10.18637/jss.v053.i04. |
| **httpuv** | Biblioteca de servidor HTTP assíncrono e WebSocket | **CHENG, J. et al.** *httpuv: HTTP and WebSocket Server Library for R*. R package version 1.6.15, 2024. Disponível em: <https://CRAN.R-project.org/package=httpuv>. |
| **Keras 3 & TensorFlow** | Treinamento e inferência de redes neurais LSTM e GRU | **CHOLLET, F. et al.** *Keras: Deep Learning for humans*. GitHub, 2015. / **ABADI, M. et al.** *TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems*, 2016. |
| **pracma** | Funções matemáticas e pseudoinversa de Moore-Penrose | **BORCHERS, H. W.** *pracma: Practical Numerical Math Functions*. R package version 2.4.4, 2023. Disponível em: <https://CRAN.R-project.org/package=pracma>. |
| **lhs** | Amostragem por Hipercubo Latino para Geração 0 | **CARNELL, R.** *lhs: Latin Hypercube Samples*. R package version 1.1.6, 2022. Disponível em: <https://CRAN.R-project.org/package=lhs>. |
| **Python 3** | Orquestração batch, scripts de injeção e teste fora da amostra | **VAN ROSSUM, G.; DRAKE, F. L.** *Python 3 Reference Manual*. Scotts Valley, CA: CreateSpace, 2009. |
| **Vanilla CSS & UI/UX** | Design system com Glassmorphism, Micro-animações e Responsividade | **WORLD WIDE WEB CONSORTIUM (W3C)**. *Cascading Style Sheets (CSS) Snapshot 2023*. W3C Working Group Note, 2023. |

