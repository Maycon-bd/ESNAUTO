# Regras de Citação ABNT/LaTeX e Ilustrações

## Citações (NBR 10520/2023)

### Citação indireta (paráfrase)
```latex
Segundo \citeonline{chave}, [texto]...
[texto]... \cite{chave}.
```
Gera: (AUTOR, ano) conforme abntex2cite.

### Citação direta curta (até 3 linhas)
```latex
``[trecho citado]'' \cite[p.~X]{chave}.
```

### Citação direta longa (mais de 3 linhas)
```latex
\begin{citacao}
[Texto citado integralmente] \cite[p.~X]{chave}.
\end{citacao}
```

### Citação de fonte secundária (apud)
```latex
\apud{chaveOriginal}{chaveFonte}
```

### Atribuição de autoria no texto
Formas corretas de atribuir afirmações:
- `Segundo \citeonline{chave},`
- `De acordo com \citeonline{chave1} e \citeonline{chave2},`
- `Conforme \citeonline{chave} (p.~X),`
- `\citeonline{chave} afirma que`
- `\citeonline{chave} concluiu que`
- `Os resultados de \citeonline{chave} indicam que`

---

## Entradas BibTeX (referencias.bib)

Use o `@type` correto para cada fonte:

| Tipo | Quando usar |
|---|---|
| `@article` | Artigo de periódico |
| `@inproceedings` | Artigo de anais/conferência |
| `@book` | Livro |
| `@incollection` | Capítulo de livro |
| `@mastersthesis` | Dissertação de mestrado |
| `@phdthesis` | Tese de doutorado |
| `@misc` com `url=` e `urldate=` | Recurso online |

---

## Rastreabilidade obrigatória

Após cada parágrafo com informação originada de artigos externos:

```latex
%% FONTE: [Título do artigo] / [Autores] / [Ano]
%% Seção: [nome da seção ou capítulo no artigo]
%% Página: [número]
%% Trecho: "[trecho original ou paráfrase próxima]"
```

Quando faltar material para cobrir um ponto obrigatório:

```latex
%% LACUNA: [descrição do tema não coberto pelos artigos fornecidos]
%% AÇÃO: [buscar artigo adicional sobre este tema e inserir aqui]
```

---

## Regras de Ilustrações (ABNT NBR 14724/2024)

### Tipos e quando usar

| Tipo | Quando usar | Formatação LaTeX |
|---|---|---|
| **Tabela** | Dados estatísticos/quantitativos; mín. 3 linhas x 2 colunas; SEM fechamento lateral | `table` + `tabular`, `\caption{}` acima, `\legend{}` abaixo |
| **Quadro** | Dados qualitativos/descritivos; COM fechamento lateral; largura 16 cm | `table` com `\hline` em todas as bordas |
| **Figura** | Representações visuais, esquemas, mapas conceituais | `figure`, `\caption{}` acima, `\legend{}` abaixo |
| **Gráfico** | Dados numéricos em formato visual (barras, linha, pizza, radar, etc.) | `figure` com imagem gerada externamente |
| **Fluxograma** | Sequência de etapas com decisões | `figure` com imagem gerada externamente |

### Itens obrigatórios em qualquer elemento visual

1. **Palavra designativa + número progressivo por tipo** (cada tipo conta separado): `Tabela 1`, `Figura 1`, `Quadro 1`
2. **Título**: sem ponto-final, fonte 10, espaçamento simples, justificado — **acima** do elemento
3. O próprio elemento visual
4. **Fonte**: logo abaixo, fonte 10, espaçamento simples, **com ponto-final**:
   - Produção própria: `Fonte: [Nome do autor], [ano].`
   - Adaptado: `Fonte: Adaptado de [AUTOR] ([ano]).`
   - De terceiros: `Fonte: [AUTOR] ([ano]).`

### Chamada obrigatória no texto

Todo elemento visual deve ser referenciado no texto **antes** de aparecer:
- `(ver Tabela 1)`, `conforme a Figura 2`, `como demonstrado no Quadro 3`
- Nunca insira um elemento sem chamada prévia no parágrafo que o antecede

### Mínimo de ilustrações

Ao menos **1 elemento visual a cada 2-3 páginas** de texto corrido. Uma seção sem ilustrações perde credibilidade perante a banca.

### Comentário de sugestão no LaTeX

Quando identificar onde uma ilustração seria valiosa, insira no código LaTeX no local exato:

```latex
%% ILUSTRACAO SUGERIDA
%% Tipo: [Grafico de barras | Quadro | Tabela | Figura | Fluxograma | Mapa de calor | etc.]
%% Posicao: [acima | abaixo] do paragrafo anterior
%% Titulo sugerido: [titulo sem ponto-final, conforme ABNT]
%% O que ilustra: [qual afirmacao ou dado do paragrafo esta ilustracao reforca]
%% Conteudo: [descrever exatamente o que deve constar - eixos, colunas, categorias, valores]
%% Fonte: [Elaborado pelo autor, [ano]. | Adaptado de AUTOR (ano). | AUTOR (ano).]
%% Justificativa: [por que este elemento visual e valioso aqui para a banca]
```

### Guia de tipos de gráfico por contexto

| Tipo | Contexto típico neste TCC |
|---|---|
| Gráfico de barras | Comparar número de artigos por ferramenta, por abordagem, por metodologia ágil |
| Gráfico de linha | Evolução do número de publicações sobre IA + prototipação por ano |
| Gráfico de pizza | Distribuição por abordagem (código × visual), por tipo de ferramenta (máx. 5-6 fatias) |
| Gráfico de radar | Comparar ferramentas em dimensões: autonomia, aplicabilidade ágil, complexidade de adoção |
| Gráfico de funil | Funil PRISMA da RSL: artigos encontrados → triados → elegíveis → incluídos |
| Mapa de calor | Ferramentas × características (quais automatizam o quê); ferramentas × fases ágeis |
| Fluxograma | Protocolo da RSL (Kitchenham); fluxo de uso de uma ferramenta de IA |
| Tabela | Síntese dos artigos selecionados com colunas do formulário de extração |
| Quadro | Comparação de características das ferramentas; síntese de abordagens |
