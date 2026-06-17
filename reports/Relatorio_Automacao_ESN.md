# Relatório de Organização e Nova Arquitetura de Simulações ESN

Este relatório descreve a reestruturação física e a nova arquitetura de salvamento das simulações da rede neural **Echo State Network (ESN)** otimizada com **Algoritmo Genético (GA)** para prever os dados de fechamento das ações da PETR4. 

Esta reorganização foi realizada para garantir que o workspace permaneça limpo, os resultados antigos fiquem arquivados e as novas simulações sejam salvas em uma estrutura intuitiva e autosuficiente, ideal para comparação acadêmica no TCC.

---

## 📁 Arquitetura do Workspace Reestruturado

A estrutura de arquivos foi dividida em responsabilidades claras:

```
d:\MAYCON\PROJETOS\ESNAUTO\
├── automate_simulations.py        # Centraliza o orquestrador em Python
├── run_simulations.bat            # Atalho interativo para rodar a automação
│
├── reports/                       # Centraliza os relatórios do TCC
│   ├── Relatorio_Automacao_ESN.md
│   ├── Relatorio_Automacao_ESN.docx
│   └── MayconGarciaSilva_monografia.docx
│
└── Scripts/                       # Scripts e dados de simulação
    ├── acoes_petr4_esn.R          # Nome simplificado e limpo para o script R
    │
    ├── data/                      # Dados de entrada (imutáveis)
    │   ├── PETR4_close com factor_2000-2020.txt
    │   └── PETR4_close com factor_2000-2020_com data.csv
    │
    └── results/                   # Resultados estruturados
        │
        ├── archive/               # HISTÓRICO: Guarda resultados e zips antigos
        │   ├── outputs/           # Antigas pastas movidas da raiz
        │   └── [Antigos PDFs, Zips e Pastas de simulação...]
        │
        └── Run_YYYYMMDD_HHMMSS_{Mode}/ # Nova execução (Gerada automaticamente)
            ├── pdfs/              # Cópia direta dos PDFs da execução (fácil comparação visual)
            ├── zips/              # Arquivos ZIP prontos para envio ao orientador
            └── scenarios/         # Pastas brutas de cada cenário com seus respectivos CSVs e logs
                ├── AlgGen PETR4 ESN_mae_otim40x60 com factor 10000_1 (...) Win Normal e W Normal/
                └── ...
```

---

## 🛠️ Modificações Realizadas

### 1. Script R (`acoes_petr4_esn.R`)
* **Nome Simplificado**: O script R original (`acoes-petr4 brutos com factor v2.8.1.1 para Maycon Garcia Silva.R`) foi renomeado para `acoes_petr4_esn.R`.
* **Argumento do Diretório de Saída (`output_dir`)**: Foi adicionado o suporte ao 5º argumento de linha de comando. Se informado, todos os arquivos CSV gerados pela simulação (`Dados PETR4...csv`) são gravados diretamente no respectivo diretório do cenário utilizando `file.path()`.
* **Gerenciamento Nativo de Plotagem**: 
  * O script agora cria e abre o arquivo PDF diretamente no diretório final de destino:
    `pdf(file.path(output_dir, paste0(basename(output_dir), ".pdf")), width=10, height=7)`
  * Ao final da execução, o R chama explicitamente `dev.off()` para salvar os gráficos.
  * O PDF resultante agora contém tanto os gráficos de histograma/boxplot iniciais (página 1) quanto a curva de evolução de fitness do GA (páginas seguintes), tudo agrupado em um único documento PDF para o cenário.

### 2. Orquestrador Python (`automate_simulations.py`)
* **Pasta de Sessão Única**: A cada execução da automação, é gerada uma pasta de sessão com a data e hora atual (ex: `Run_20260617_130000_Prod/`).
* **Estruturação Automática**: A automação cria as subpastas `scenarios/`, `pdfs/` e `zips/` dentro da pasta de sessão.
* **Simplificação do Fluxo**: A complexa rotina do Python de buscar e mover arquivos gerados na raiz de `Scripts/` foi eliminada. Agora, o orquestrador apenas:
  1. Cria a pasta do cenário em `scenarios/`.
  2. Passa a pasta do cenário como argumento de saída para o R.
  3. Copia o PDF gerado diretamente do cenário para `pdfs/` (facilitando visualizações rápidas).
  4. Compacta o diretório do cenário em formato `.zip` e o salva diretamente em `zips/`.

### 3. Script Batch de Execução Rápida (`run_simulations.bat`)
* Criado um script batch interativo no diretório raiz. Permite ao usuário rodar a automação em modo teste ou produção através de um menu de seleção de forma simples.

---

## 🚀 Como Executar as Simulações na Nova Arquitetura

Você pode abrir o terminal e rodar diretamente:

### 1. Rodar Teste Rápido (200 iterações, rodadas 1, 2, 3)
```bash
python automate_simulations.py --test
```
Ou dê dois cliques no arquivo `run_simulations.bat` no seu gerenciador de arquivos do Windows e escolha a opção `1`.

### 2. Executar Simulações Oficiais do TCC (10.000 iterações, rodadas 1, 2, 3)
```bash
python automate_simulations.py
```
Ou dê dois cliques no arquivo `run_simulations.bat` e escolha a opção `2`.
