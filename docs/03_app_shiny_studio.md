# 🖥️ Componente 3: ESNAUTO Benchmark Studio (R Shiny Web App)

O **ESNAUTO Benchmark Studio** é uma aplicação web interativa desenvolvida em **R Shiny** com uma interface moderna (UI/UX premium) para visualização, ajuste de parâmetros e comparação em tempo real entre a **Echo State Network (ESN)** e modelos clássicos de Deep Learning Recorrente (**LSTM** e **GRU**).

---

## 📂 Arquivos Integrantes do Componente

```
ESNAUTO/
└── app/
    ├── app.R                          # Arquivo principal (UI + Server)
    │
    ├── modules/                       # Módulos isolados por responsabilidade
    │   ├── mod_esn.R                  # Módulo interativo da ESN
    │   ├── mod_lstm.R                 # Módulo interativo da rede LSTM
    │   ├── mod_gru.R                  # Módulo interativo da rede GRU
    │   └── mod_comparacao.R           # Módulo de comparação unificada
    │
    ├── utils/                         # Funções auxiliares
    │   ├── data_prep.R                # Carregamento e particionamento dos dados
    │   └── metrics.R                  # Cálculo de métricas financeiras e estatísticas
    │
    └── www/                           # Recursos estáticos de design
        └── custom.css                 # CSS customizado com visual Dark/Glassmorphism
```

---

## 🚀 Como Executar o App R Shiny

Abra o console do R ou terminal e execute:

```bash
Rscript -e "shiny::runApp('app')"
```
Ou abra o arquivo `app/app.R` no RStudio e clique no botão **Run App**.

---

## 📝 Detalhamento de Cada Arquivo

### 1. `app/app.R`
- **Caminho**: [app/app.R](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/app/app.R)
- **Função**: Ponto de entrada da aplicação Shiny. Define a estrutura de navegação superior (`navbarPage`) e conecta o servidor aos módulos.

#### 🎨 Abas Navegáveis:
1. **📊 Dados PETR4**: Carregamento da série histórica e configuração dos splits (Treino/Validação/Teste).
2. **🧠 ESN (Reservoir)**: Execução interativa da ESN e ajuste dos hiperparâmetros do reservatório.
3. **📈 LSTM Network**: Treinamento e avaliação da rede Long Short-Term Memory.
4. **📉 GRU Network**: Treinamento e avaliação da rede Gated Recurrent Unit.
5. **⚡ Comparação Geral**: Painel consolidado lado a lado das 3 arquiteturas.

---

### 2. Módulos da Aplicação (`app/modules/`)

#### A. `app/modules/mod_esn.R`
- **Caminho**: [app/modules/mod_esn.R](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/app/modules/mod_esn.R)
- **Função**: Controla a interface gráfica e a execução em tempo real da **Echo State Network**.
- **Recursos**: Sliders para alteração da taxa de vazão ($a$), raio espectral ($sr$), tempo de lavagem ($initLen$), tamanho do reservatório ($tam\_reservoir$) e regularização Ridge ($reg$). Exibe instantaneamente os gráficos de ajuste e resíduos.

#### B. `app/modules/mod_lstm.R`
- **Caminho**: [app/modules/mod_lstm.R](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/app/modules/mod_lstm.R)
- **Função**: Implementa a interface e a lógica de treinamento para a rede recorrente profunda **LSTM** (Long Short-Term Memory). Permite configurar número de unidades, épocas, tamanho do lote (batch size) e taxa de aprendizado.

#### C. `app/modules/mod_gru.R`
- **Caminho**: [app/modules/mod_gru.R](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/app/modules/mod_gru.R)
- **Função**: Controla a interface e o pipeline da rede **GRU** (Gated Recurrent Unit), oferecendo parâmetros configuráveis de camadas, épocas e taxas de convergência.

#### D. `app/modules/mod_comparacao.R`
- **Caminho**: [app/modules/mod_comparacao.R](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/app/modules/mod_comparacao.R)
- **Função**: Consolida os resultados das 3 redes em um painel comparativo único.
- **Recursos**: Tabela comparativa de métricas ($R^2$, MAE, RMSE, MAPE), gráficos de predição sobrepostos e análise visual de resíduos.

---

### 3. Utilitários e Estilos (`app/utils/` e `app/www/`)

#### A. `app/utils/data_prep.R`
- **Caminho**: [app/utils/data_prep.R](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/app/utils/data_prep.R)
- **Função**: Carrega e prepara a série temporal de preços da PETR4 (2000–2020). Responsável pela normalização MinMax/Z-score e pelo particionamento temporal dos dados (Treino: 50%, Validação: 25%, Teste: 25%).

#### B. `app/utils/metrics.R`
- **Caminho**: [app/utils/metrics.R](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/app/utils/metrics.R)
- **Função**: Coleção de funções matemáticas para o cálculo preciso das estatísticas de desempenho:
  - **MAE**: Erro Médio Absoluto ($\text{MAE} = \frac{1}{N} \sum |y - \hat{y}|$)
  - **RMSE**: Raiz do Erro Quadrático Médio ($\text{RMSE} = \sqrt{\frac{1}{N} \sum (y - \hat{y})^2}$)
  - **MAPE**: Erro Percentual Absoluto Médio
  - **R²**: Coeficiente de Determinação

#### C. `app/www/custom.css`
- **Caminho**: [app/www/custom.css](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/app/www/custom.css)
- **Função**: Folha de estilos CSS customizada para garantir uma experiência visual premium. Aplica paleta de cores escuras modernas, cards com efeito glassmorphism, tipografia customizada e botões responsivos.
