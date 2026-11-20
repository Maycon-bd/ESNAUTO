# Contexto do TCC

## Identificação

- **Título:** Prototipação de Interfaces com Suporte de Inteligência Artificial em Processos Ágeis: Uma Revisão Sistemática da Literatura
- **Curso:** Engenharia de Software
- **Instituição:** UniRV — Universidade de Rio Verde
- **Tipo de pesquisa:** Revisão Sistemática da Literatura (RSL), conduzida conforme as diretrizes de Kitchenham et al. (2009)

---

## Problema e lacuna

Ferramentas de prototipação são amplamente utilizadas no apoio ao design de interfaces em contextos de desenvolvimento ágil. A introdução de técnicas de inteligência artificial nesse domínio tem possibilitado a automatização de etapas como geração de telas, sugestão de componentes e adaptação de fluxos de navegação. No entanto, há pouca sistematização na literatura sobre as abordagens utilizadas, seus mecanismos de funcionamento e seus limites de aplicação. Esta lacuna justifica a condução de uma revisão sistemática da literatura.

---

## Questão de pesquisa central

Quais ferramentas, bibliotecas ou frameworks utilizam inteligência artificial para apoiar a prototipagem de interfaces em processos ágeis de desenvolvimento de software, e quais são suas principais características, abordagens, limitações e aplicações?

---

## Objetivo geral

Realizar uma revisão sistemática da literatura para identificar, classificar e analisar ferramentas, frameworks e bibliotecas que utilizam inteligência artificial para apoiar a prototipação de interfaces em processos ágeis de desenvolvimento de software.

## Objetivos específicos

1. Identificar as principais ferramentas, bibliotecas e frameworks com suporte de IA voltadas à prototipação de interfaces
2. Classificar as abordagens encontradas em categorias: baseadas em código × baseadas em componentes visuais
3. Analisar as funcionalidades, métodos de uso, limitações e objetivos das ferramentas identificadas
4. Comparar os benefícios e limitações das abordagens automatizadas com IA frente a métodos tradicionais de prototipação
5. Propor diretrizes e boas práticas para seleção e uso dessas ferramentas em contextos ágeis de desenvolvimento

---

## Resultados esperados da RSL

- Mapeamento das soluções existentes (ferramentas, bibliotecas, frameworks), com caracterização de suas abordagens
- Identificação das **abordagens predominantes**: baseadas em código vs. baseadas em componentes visuais
- Levantamento dos **modelos de IA empregados** por cada solução
- Identificação dos **contextos de aplicação** mais recorrentes na literatura
- Descrição de **como as ferramentas automatizam etapas do design**: geração de telas, wireframes, sugestão de componentes, recomendações de layout, preenchimento de código, adaptação de fluxos de navegação
- Mapeamento das **limitações técnicas e metodológicas** de cada abordagem
- Apontamento das **lacunas existentes na literatura** sobre o tema
- Diretrizes práticas para seleção e uso em cenários ágeis, considerando: autonomia da ferramenta, aplicabilidade ao contexto ágil e complexidade de adoção

---

## Estrutura dos capítulos

| Capítulo | Arquivo(s) .tex |
|---|---|
| Cap. 1 — Introdução | textual/1-introducao/1-contexto.tex, 2-problema.tex, 3-trabalhos-relacionados.tex, 4-objetivo-geral.tex, 5-objetivos-especificos.tex, 6-justificativa.tex, 7-hipoteses.tex |
| Cap. 2 — Revisão de Literatura | textual/2-revisao/1-revisao-literatura.tex, 2-estado-da-arte.tex, 3-trabalhos-relacionados-busca.tex |
| Cap. 3 — Metodologia | textual/3-metodologia/1-classificacao-pesquisa.tex, 2-criterios-avaliacao.tex |
| Cap. 4 — Resultados | textual/4-resultados/1-tabulacao-analise.tex |
| Cap. 5 — Conclusão | textual/5-conclusao/1-conclusao.tex |

---

## Formulário de extração de dados (30 campos)

Cada artigo selecionado é analisado segundo os seguintes campos:

**Dados bibliográficos**
- Título do artigo | Autor(es) | Ano de publicação | Veículo de publicação | País(es) dos autores

**Sobre a proposta do artigo**
- O que o artigo se propôs a fazer
- Proposta ou avaliação prática (o artigo propõe algo novo ou avalia algo existente?)
- Método de avaliação utilizado

**Sobre a ferramenta/solução analisada**
- Ferramenta/biblioteca/framework identificada
- Classificação da abordagem (baseada em código × baseada em componentes visuais)
- Modelo de IA utilizado
- O que a ferramenta automatiza (tarefas específicas do design)
- Nível de independência da IA (grau de autonomia)
- Como a ferramenta é utilizada (fluxo de uso)
- Interação usuário-ferramenta

**Sobre o encaixe com processos ágeis**
- Encaixe no processo ágil
- Fase ágil em que a ferramenta atua
- Etapas de design e desenvolvimento ágil suportadas
- Projetada explicitamente para processos ágeis? (sim/não/parcialmente)
- Aplicabilidade ao cenário ágil

**Análise crítica**
- Vantagens relatadas
- Desvantagens relatadas
- Limites técnicos e metodológicos
- Comparação com prototipação tradicional
- Testes com usuários reais (realizou ou não)
- Público-alvo da ferramenta
- Tipos de projetos/cenários de uso
- Sugestões/regras de uso propostas pelos autores

**Síntese e contribuição**
- Contribuição final do artigo
- Desafios da área identificados pelo estudo

---

## Implicações críticas para a escrita

- Este é um trabalho de **RSL pura** — não há sistema desenvolvido, experimento conduzido pelo autor, coleta de dados primários ou validação com usuários. Toda afirmação deve remeter à literatura revisada.
- A classificação binária **baseadas em código × baseadas em componentes visuais** é a taxonomia central do trabalho.
- Ao mencionar tarefas automatizadas por IA, use os termos do vocabulário central: "geração de telas", "sugestão de componentes", "recomendações de layout", "adaptação de fluxos de navegação", "preenchimento de código".
- Ao analisar critérios de adequação de ferramentas, use os três critérios definidos: **autonomia, aplicabilidade ao contexto ágil e complexidade de adoção**.
- Os **30 campos do formulário de extração** são a estrutura analítica do trabalho.
