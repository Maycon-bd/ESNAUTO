# 📊 Componente 4: Gestão de Dados e Estrutura de Resultados

Este componente compreende a **base de dados histórica de entrada imutável** (ações da PETR4 entre 2000 e 2020) e a **arquitetura física de pastas e arquivos de saída** onde são gravados os logs, matrizes, relatórios e pacotes de entrega de cada simulação.

---

## 📂 Arquivos Integrantes do Componente

```
ESNAUTO/
├── Scripts/
│   ├── data/                                  # Bases de dados históricas
│   │   ├── PETR4_close com factor_2000-2020.txt
│   │   └── PETR4_close com factor_2000-2020_com data.csv
│   │
│   └── results/                               # Resultados das sessões de simulação
│       ├── archive/                           # Histórico antigo de execuções
│       └── Run_YYYYMMDD_HHMMSS_{Mode}/        # Sessão gerada dinamicamente
│           ├── pdfs/                          # PDFs compilados por cenário
│           ├── zips/                          # Arquivos compactados por cenário
│           ├── scenarios/                     # Dados brutos dos 12 cenários
│           └── entrega/                       # Resultados e ZIP final consolidado
│
└── resultados_tcc/                            # Gráficos e txt oficiais consolidados
    ├── grafico_teste_corrigido.png
    ├── grafico_validacao_corrigido.png
    └── resultados_ESN_PETR4.txt
```

---

## 📝 Detalhamento das Bases de Dados (`Scripts/data/`)

### 1. `Scripts/data/PETR4_close com factor_2000-2020.txt`
- **Formato**: Arquivo texto plano (vetor numérico de valores por linha)
- **Conteúdo**: Preços diários de fechamento das ações da Petrobras (PETR4) ajustados por proventos, dividendos e desdobramentos (fator) no período de **03/01/2000 a 28/12/2020**.
- **Utilidade**: Utilizado como entrada numérica direta nas simulações batch executadas pelo script R `acoes_petr4_esn.R`.

### 2. `Scripts/data/PETR4_close com factor_2000-2020_com data.csv`
- **Formato**: CSV indexado por data (`Data`, `Fechamento_Ajustado`)
- **Conteúdo**: Mesma série temporal financeira de PETR4 contendo a marcação temporal exata de cada pregão da B3.
- **Utilidade**: Utilizado pela aplicação **ESNAUTO Benchmark Studio (R Shiny)** para plotagem gráfica com eixos temporais reais.

---

## 📁 Estrutura de Resultados por Sessão (`Scripts/results/`)

A cada execução da automação (`automate_simulations.py`), o sistema cria uma pasta isolada identificada por carimbo de data/hora:

### 1. Subpasta `scenarios/`
Contém 12 subpastas correspondentes às 3 rodadas dos 4 cenários de distribuições de pesos ($W_{in}$ e $W$):
- Exemplo: `AlgGen PETR4 ESN_mae_otim40x60 com factor 10000_1 (...) Win Normal e W Normal/`
- Arquivos internos:
  - `Dados PETR4 ESN_mae_otim...csv`: Série predita vs. real na validação.
  - `Dados PETR4 resumo fitness...csv`: Evolução da função fitness por geração do GA.
  - `matriz_Win_epoca_{epoca}.txt`: Matriz de entrada numérica da melhor época.
  - `matriz_W_epoca_{epoca}.txt`: Matriz do reservatório numérica da melhor época.
  - `{nome_cenario}.pdf`: PDF com gráficos de fitness e distribuição inicial.

### 2. Subpastas `pdfs/` e `zips/`
- `pdfs/`: Armazena cópias diretas de todos os PDFs dos 12 cenários da sessão para comparação visual ágil.
- `zips/`: Armazena a compactação individual de cada cenário para arquivamento.

### 3. Subpasta `entrega/` (Gerada no Pós-Processamento)
Gerada automaticamente pela Fase 4 (`package_results.py`):
- `resultados_validacao_teste.txt`: Relatório compilado com o ranking do melhor cenário e hiperparâmetros.
- `grafico_validacao.png`: Gráfico de alinhamento da partição de validação em alta resolução.
- `grafico_teste.png`: Gráfico de alinhamento da partição Out-of-Sample de teste em alta resolução.
- `entrega_YYYYMMDD_HHMMSS.zip`: Pacote ZIP final pronto para submissão acadêmica.

---

## 🖼️ Pasta de Resultados Consolidados do TCC (`resultados_tcc/`)

Armazena os artefatos oficiais selecionados e corrigidos para apresentação na monografia:
- **`grafico_validacao_corrigido.png`**: Gráfico oficial da partição de validação com paleta acadêmica.
- **`grafico_teste_corrigido.png`**: Gráfico oficial da partição de teste com paleta acadêmica.
- **`resultados_ESN_PETR4.txt`**: Registro numérico oficial dos hiperparâmetros ótimos selecionados para o TCC.
