# Protocolo de validação estatística por sementes

Este protocolo foi adicionado após a revisão do artigo submetido ao ACDSA 2027, que apontou limitação na validação estatística dos experimentos estocásticos. O objetivo é medir a variabilidade produzida pela geração aleatória das matrizes \(W_{in}\) e \(W\), mantendo fixos os hiperparâmetros históricos das configurações analisadas.

## Primeira bateria

Três configurações históricas são avaliadas:

| Cenário | ID histórico | \(W_{in}\) | \(W\) | a | sr | initLen | Nx | lambda |
|---|---|---|---|---:|---:|---:|---:|---:|
| Controle | GA_RUN_0046 | Normal | Normal | 0.316 | 0.017 | 57 | 3 | 2.97e-5 |
| Menor MAE observado | GA_RUN_0030 | Laplace | Normal | 0.112 | 0.215 | 57 | 22 | 5.72e-5 |
| Menor RMSE observado | GA_RUN_0033 | Laplace | Cauchy | 0.924 | 0.652 | 97 | 28 | 2.98e-5 |

Os valores acima são os hiperparâmetros documentados nos relatórios oficiais das Ondas 2 e 4. Nesta etapa eles são mantidos fixos. Não há nova busca genética.

## Sementes

Por padrão são usadas 30 sementes consecutivas, iniciando em 202700. As mesmas sementes são usadas nos três cenários, permitindo comparações pareadas.

Exemplo:

```powershell
Rscript Scripts/run_seed_validation.R --asset PETR4 --seeds 30 --seed-base 202700
```

No Windows, também é possível executar:

```text
run_seed_validation.bat
```

## Separação treino, validação e teste

A bateria usa a divisão cronológica já definida pelo projeto.

A avaliação é feita em duas etapas:

1. **Treino -> validação:** a leitura Ridge é ajustada apenas no conjunto de treino e avaliada na validação.
2. **Treino+validação -> teste:** após a etapa de validação, a leitura é reajustada sobre a sequência contígua de treino+validação e então avaliada no teste final.

Esse fluxo evita a concatenação artificial treino+teste usada em partes do pipeline histórico e preserva o contexto temporal imediatamente anterior ao teste.

O conjunto de teste não é usado para escolher cenário, seed ou hiperparâmetros nesta nova bateria. As três configurações são definidas antes da execução.

## Distribuições congeladas

Para evitar que futuras alterações no catálogo de distribuições mudem o experimento, a rotina fixa explicitamente:

- Normal: média 0, desvio-padrão 1;
- Laplace: média 0, desvio-padrão 1;
- Cauchy: location 0, scale 1.

## Saídas

Cada execução cria uma pasta em:

```text
Scripts/results/seed_validation/<ATIVO>_<timestamp>/
```

Arquivos principais:

- `seed_results_raw.csv`: uma linha por cenário/seed;
- `seed_results_summary.csv`: média, mediana, desvio-padrão, IC95%, mínimo e máximo;
- `pairwise_wilcoxon_test.csv`: comparações pareadas por seed com correção de Holm;
- `manifest.json` ou `manifest.R`: protocolo, partições, seeds e parâmetros;
- `matrices/<cenario>/seed_<seed>.rds`: Win, W, W escalada, Wout e hiperparâmetros;
- opcionalmente `predictions/`: previsões ponto a ponto quando `--save-predictions true`.

As métricas registradas são MAE, RMSE e R² em validação e teste, além do tempo de ajuste/avaliação.

## Interpretação

Esta bateria responde especificamente à pergunta:

> As vantagens observadas de Laplace × Normal e Laplace × Cauchy permanecem quando apenas a realização aleatória do reservatório muda?

Ela não testa ainda a variabilidade do próprio Algoritmo Genético, porque os hiperparâmetros permanecem fixos.

Se a diferença entre as distribuições persistir de forma consistente ao longo das seeds, o resultado fortalece a evidência sobre inicialização probabilística. Se as distribuições apresentarem desempenho sobreposto, isso indicará que parte do recorde pontual pode ser explicada pela variabilidade estocástica do reservatório.

## Próximas etapas

Depois desta primeira bateria:

1. analisar distribuições e boxplots de MAE/RMSE;
2. verificar magnitude das diferenças e testes pareados;
3. decidir se é necessário repetir a busca GA completa por seed;
4. repetir o protocolo em VALE3 e em um terceiro ativo;
5. posteriormente repetir LSTM/GRU com múltiplas sementes se a comparação estatística entre arquiteturas for mantida no artigo.

## Observação sobre os hiperparâmetros históricos

Os relatórios versionados registram alguns parâmetros com precisão arredondada. Caso os arquivos brutos originais das execuções GA_RUN_0030, GA_RUN_0033 e GA_RUN_0046 sejam recuperados com precisão maior, os valores fixados neste protocolo devem ser substituídos pelos valores exatos antes da bateria definitiva destinada à publicação.
