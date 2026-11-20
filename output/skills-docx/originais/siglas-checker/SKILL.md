---
name: siglas-checker
description: Auditoria de siglas em seções LaTeX do TCC UniRV conforme Manual UniRV §2.1.12 e §6.4. Detecta termos repetidos sem sigla declarada, definições duplicadas (extenso (SIGLA) repetido), extenso usado após declaração, siglas órfãs (no texto sem entrar na Lista), erros na Lista de Siglas (ordem alfabética, capitalização ≤3/≥4 letras, plural, itálico em estrangeirismos) e siglas proibidas em títulos de tabelas/quadros/figuras. Mostra preview antes/depois e pede aprovação antes de editar. Use quando o usuário disser "revisar siglas", "checar siglas", "verificar lista de siglas", "/siglas-checker", ou enviar arquivo/seção .tex para revisão de siglas no projeto Template (TCC UniRV).
---

# siglas-checker — Auditor de Siglas (Manual UniRV / NBR 14724)

## Contexto do projeto

Este TCC (UniRV, LaTeX/abntex2) usa o ambiente `siglas` em `pretextual/listas.tex` para declarar a Lista de Siglas. As regras vêm do **Manual UniRV §6.4 (p. ~214)** e da **NBR 14724/2024**. O usuário escreve as seções `.tex` em `textual/` e é comum:

- esquecer de declarar uma sigla que aparece muitas vezes;
- definir a sigla "Nome Por Extenso (NPE)" mais de uma vez (a definição só vale na **primeira** ocorrência);
- continuar usando o termo por extenso em vez da sigla depois de já ter sido declarada;
- usar uma sigla no corpo do texto sem que ela conste na Lista de Siglas.

Sua missão: dada uma seção/arquivo `.tex` (ou diretório), apontar todas essas inconsistências, comparando com a Lista de Siglas oficial em `pretextual/listas.tex`.

## Base normativa (Manual UniRV §2.1.12 e §6.4 + NBR 14724/2024)

1. **Sigla × Acrônimo (§6.4)** — Sigla é pronunciada letra a letra (ABNT, IBGE); acrônimo é lido como palavra (Embrapa, UniRV). Ambos vão na mesma Lista de Siglas.

2. **Primeira ocorrência (§6.4 a)**: escrever o nome por extenso seguido da sigla entre parênteses. Exemplos do Manual:
   - `Empresa Brasileira de Correios e Telégrafos (ECT)` (e não EBCT);
   - `Universidade de Rio Verde (UniRV)`;
   - `Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq)`.

3. **Demais ocorrências**: usar apenas a sigla — `IA`, nunca mais "Inteligência Artificial". Reaparecer com o extenso (mesmo seguido da sigla) é erro.

4. **Sigla consagrada (Observação §6.4)** — "deve-se citar apenas a sigla **já existente ou consagrada**, mantendo-se a grafia originalmente criada". **Não inventar siglas**: para Empresa Brasileira de Correios e Telégrafos a sigla é ECT, não EBCT. Quando sugerir uma sigla nova (Verificação D), verificar se já existe uma forma consagrada.

5. **Capitalização (§6.4 b–c)** — depende do nº de letras e da pronúncia:
   - **≤ 3 letras**: SEMPRE maiúsculas. Ex.: `ONU`, `RH`, `IA`, `UI`, `UX`.
   - **≥ 4 letras (c.1)**: todas maiúsculas, quando cada letra é pronunciada separadamente. Ex.: `IBGE`, `BNDE`, `ABNT`.
   - **≥ 4 letras (c.2)**: SÓ a inicial maiúscula, quando forma uma palavra pronunciável (acrônimo). Ex.: `Embrapa`, `Senac`, `Anac`, `Decea`, `Procon`, **`UniRV`**.
   - **Erro comum**: escrever `EMBRAPA` (deveria ser `Embrapa`) ou `Senai` quando todos pronunciam letra a letra. A skill deve sinalizar inconsistências.

6. **Sigla de origem estrangeira (§6.4 d)** — duas situações:
   - Quando existir forma traduzida em português: usar a **dupla**, formato: `Extenso Estrangeiro (SIGLA)/Extenso em Português (SIGLA-PT)`. Exemplos do Manual:
     - `United Nations (UN)/Nações Unidas (NU)`;
     - `Acquired Immunological Deficiency Syndrome (Aids)/Síndrome de Imunodeficiência Adquirida (Sida)`.
   - Quando não houver tradução ou a forma original já for convencionada: manter apenas a sigla estrangeira. Ex.: `FAO`.

7. **Lista de Siglas (§2.1.12)** — "Lista alfabética das abreviaturas e siglas utilizadas no texto, seguidas das palavras ou expressões correspondentes grafadas por extenso (em maiúsculo e minúsculo, quando for o caso)."
   - **Obrigatoriedade**: o Manual apresenta dupla redação — §2.1.12 fala em "**mais de dez itens**" (= 11+), enquanto os modelos de páginas dizem "**10 ou mais itens**". Critério seguro: **≥ 10 itens torna obrigatória**. Avisar o usuário quando a lista estiver entre 8 e 11 (zona de atenção).
   - **Formato dos itens**: `SIGLA – Nome por extenso` (en-dash com espaços). No LaTeX abntex2 (`\item[SIGLA] -- Extenso`), `--` é renderizado como en-dash. Sinalizar uso de hífen simples ou travessão `---`.
   - **Ordem alfabética estrita por sigla**.

8. **Termo estrangeiro no extenso da Lista**: deve vir em `\textit{}`, opcionalmente seguido da tradução entre parênteses (sem itálico). Ex.: `\textit{Large Language Model} (grande modelo de linguagem)`.

9. **Siglas no plural (norma editorial)**: acrescenta-se `s` minúsculo sem apóstrofo — `LLMs`, `APIs`. Nunca `LLM's` nem `LLMS`.

10. **Não usar ponto entre letras** — `ABNT`, não `A.B.N.T.`.

11. **Proibido usar siglas em títulos (§3, observações repetidas em Tabelas, Quadros e Ilustrações)** — "não utilizar siglas nos títulos das tabelas / quadros / ilustrações". Verificar `\caption{...}` de `table`, `quadro`, `figure`, etc., e os títulos numerados (`Tabela 1 — ...`, `Quadro 2 — ...`, `Figura 3 — ...`).

12. **Abreviaturas latinas de citação (§6.2 + NBR 10520/2023)** — `et al.`, `apud`, `ibid.`, `ibidem`, `opus citatum`, `idem` permanecem em itálico. **Não são tratadas por esta skill** (são alvo do `ingles-italico-checker`); apenas mencionar caso o usuário pergunte sobre formatação.

## Entrada esperada

O usuário fornecerá:
- Caminho de arquivo `.tex` (ex.: `textual/2-referencial_teorico/1-revisao-literatura.tex`), OU
- Diretório (ex.: `textual/3-metodologia/`), OU
- Trecho de código LaTeX colado direto na conversa.

Se for ambíguo, peça confirmação antes de prosseguir.

## Protocolo de execução (siga na ordem)

### Passo 1 — Carregue a Lista de Siglas oficial

**Sempre** comece lendo `pretextual/listas.tex`. Extraia todos os itens `\item[SIGLA] -- Extenso ...` dentro do bloco `\begin{siglas} ... \end{siglas}` e construa um dicionário:

```
{
  "ABNT":  "Associação Brasileira de Normas Técnicas",
  "GUI":   "Graphical User Interface",
  "IA":    "Inteligência Artificial",
  ...
}
```

Guarde também a ordem em que aparecem (para validar ordem alfabética).

### Passo 2 — Leia o(s) arquivo(s) alvo

Use `Read` para o(s) arquivo(s) indicado(s). Se for um diretório, use `Glob` (`**/*.tex`) primeiro. Ignore:

- Comentários (`%...`).
- Comandos LaTeX e seus argumentos: `\cite{...}`, `\citeonline{...}`, `\ref{...}`, `\label{...}`, `\input{...}`, `\include{...}`, `\section{...}` (mas o **texto** das seções deve ser analisado).
- Blocos `\begin{lstlisting}...\end{lstlisting}`, `\verb|...|`.
- URLs em `\href{url}{...}` e `\url{...}`.
- Chaves bibliográficas (`Silva2024` em `\cite{Silva2024}` não conta).

### Passo 3 — Detecte inconsistências (7 verificações)

#### Verificação A — Definição duplicada da mesma sigla
Padrão `Extenso (SIGLA)` ou `Extenso \textit{(SIGLA)}`. Liste TODAS as ocorrências do padrão para cada sigla; a **partir da segunda**, sinalize como **"definição duplicada"** — deve virar apenas a sigla.

> Regex sugerida: `[\wÀ-ÿ\s]+\s*\(([A-Z][A-Za-z]{1,7})\)` e cruzar com o dicionário do passo 1.

#### Verificação B — Sigla declarada mas extenso ainda em uso
Para cada sigla do dicionário, procure o **nome por extenso** (case-insensitive) no texto APÓS a primeira ocorrência da sigla. Se aparecer, sinalize como **"extenso após declaração"** — deve ser substituído pela sigla.

> Atenção: ignorar ocorrências dentro de `\textit{}` quando o extenso é estrangeiro e está sendo usado como conceito explicativo entre parênteses (raro; sinalize como dúvida).

#### Verificação C — Sigla usada no texto sem estar na Lista
Encontre tokens em CAIXA ALTA (2-7 letras, opcionalmente com dígitos) que se repitam ≥ 2 vezes. Filtre o que NÃO entra:
- Já está no dicionário do passo 1.
- É nome próprio/marca (`PRISMA`, `GPT`, `IEEE`, `ACM`, `IBGE`, `USA`, `JSON`, `PDF`, `HTTP`, `API`, `URL` — mantenha uma lista interna).
- Aparece dentro de `\cite{}` ou similar.

Se sobrar: **"sigla não declarada"** — sugerir adicionar à Lista.

#### Verificação D — Termo extenso repetido sem virar sigla
Encontre expressões nominais em maiúsculas iniciais (Title Case ou maiúsculas) com 2-5 palavras que se repitam ≥ 3 vezes (ex.: "Revisão Sistemática da Literatura", "Processamento de Linguagem Natural", "Aprendizado de Máquina"). Para cada candidato:
- Se já está na Lista de Siglas pelo extenso: pular (Verificação B cuida).
- Caso contrário: sinalizar como **"candidato a sigla"** — sugerir sigla (iniciais das palavras significativas) e propor inclusão na Lista.

#### Verificação E — Inconsistências na própria Lista de Siglas
Verifique em `pretextual/listas.tex`:
- **Ordem alfabética** estrita por sigla.
- **Itálico em termos estrangeiros**: extenso em inglês/outra língua deve estar em `\textit{}`.
- **Plural com apóstrofo** (`LLM's` em vez de `LLMs`) — erro.
- **Pontos entre letras** (`A.B.N.T.`) — erro.
- **Capitalização inadequada (§6.4 b–c)**:
  - Sigla ≤ 3 letras NÃO em maiúsculas (ex.: `Ia` em vez de `IA`) — erro.
  - Sigla ≥ 4 letras com pronúncia palavra-a-palavra mas grafada como acrônimo (ex.: `Ibge`) — erro.
  - Acrônimo (palavra pronunciável) em tudo maiúsculas (ex.: `EMBRAPA`, `UNIRV`) — sinalizar como possível erro; perguntar ao usuário se a sigla é lida como palavra.
- **Separador** entre sigla e extenso: deve ser `--` (en-dash) — sinalizar hífen simples `-` ou travessão `---`.
- **Total de siglas**: se < 10, lembrar que a Lista é OPCIONAL; se ≥ 10, é OBRIGATÓRIA. Se estiver entre 8 e 11, avisar o usuário do limite (Manual UniRV tem dupla redação: §2.1.12 diz ">10", exemplos dizem "≥10" — recomenda-se o critério mais seguro).

#### Verificação F — Sigla estrangeira sem equivalente em português (§6.4 d)
Para cada item na Lista cujo extenso esteja em `\textit{}` (= estrangeiro) e que tenha equivalente comum em português, verificar se segue o formato dual do Manual:

```
\textit{Foreign Extended} (FOR) (extenso em português)
```
ou — mais conforme ao Manual — o duplo:

```
\textit{Foreign Extended} (FOR)/Extenso em Português (POR-PT)
```

Exemplo do Manual: `United Nations (UN)/Nações Unidas (NU)`. Se o extenso em inglês tiver tradução amplamente usada em PT (ex.: `Large Language Model` → "grande modelo de linguagem"), sugerir a versão dual. Quando a sigla original em inglês já estiver consagrada (`FAO`, `GUI`, `UX`, `UI`), aceitar o formato simples com tradução entre parênteses.

#### Verificação G — Siglas usadas em títulos (§3 — proibição)
"Não utilizar siglas nos títulos das tabelas / quadros / ilustrações." Verificar:
- `\caption{...}` dentro de `\begin{table}`, `\begin{quadro}`, `\begin{figure}`, `longtable`, etc.
- Linhas começando com `Tabela N -`, `Quadro N -`, `Figura N -` se houver títulos manuais.

Se encontrar uma sigla declarada (do dicionário) dentro de um `\caption`, sinalizar como **"sigla proibida em título"** e sugerir substituir pelo extenso.

### Passo 4 — Apresente o relatório

Formato obrigatório, em PT-BR:

```
## Auditoria de Siglas — N inconsistências encontradas

### Lista de Siglas oficial (pretextual/listas.tex)
9 siglas declaradas. Status: OPCIONAL (< 10) / OBRIGATÓRIA (≥ 10).

### A. Definição duplicada (re-introduz "Extenso (SIGLA)" depois da 1ª vez)
| # | Arquivo | Linha | Sigla | Trecho |
|---|---------|-------|-------|--------|
| 1 | 2-referencial.tex | 87 | IA | "...na Inteligência Artificial (IA) moderna..." |

### B. Extenso usado após declaração da sigla
| # | Arquivo | Linha | Sigla | Extenso encontrado | Trecho |
|---|---------|-------|-------|--------------------|--------|
| 2 | 3-metodologia.tex | 42 | RSL | "Revisão Sistemática da Literatura" | "...durante a Revisão Sistemática da Literatura aplicada..." |

### C. Siglas usadas no texto sem estar na Lista
| # | Sigla | Ocorrências | Sugestão de extenso | Arquivos |
|---|-------|-------------|---------------------|----------|
| 3 | NLP   | 5 vezes     | Natural Language Processing | 2-referencial.tex, 4-resultados.tex |

### D. Candidatos a sigla (termo repetido sem declaração)
| # | Termo | Ocorrências | Sugestão de sigla | Arquivos |
|---|-------|-------------|-------------------|----------|
| 4 | Processamento de Linguagem Natural | 6 | PLN | 2-referencial.tex |

### E. Problemas na Lista de Siglas
| # | Item | Problema | Correção |
|---|------|----------|----------|
| 5 | LLM | Extenso "Large Language Model" sem `\textit{}` | Envolver em `\textit{}` |
| 6 | UNIRV | Capitalização — é acrônimo, deve ser `UniRV` | Trocar para `UniRV` |

### F. Sigla estrangeira sem formato dual (§6.4 d)
| # | Sigla | Extenso atual | Formato sugerido |
|---|-------|---------------|------------------|
| 7 | LLM | \textit{Large Language Model} (grande modelo de linguagem) | OK (sigla original consagrada) — sem ação |

### G. Sigla usada em título de tabela/quadro/figura (proibido)
| # | Arquivo | Linha | Local | Sigla | Sugestão |
|---|---------|-------|-------|-------|----------|
| 8 | 4-resultados.tex | 120 | \caption | IA | Trocar pelo extenso "Inteligência Artificial" |
```

Sempre agrupe por verificação (A, B, C, D, E, F, G). Use número global crescente.

### Passo 5 — Mostre o preview da alteração (antes/depois)

Para CADA item, mostre um bloco diff:

```diff
arquivo.tex:87  [A. Definição duplicada]
- ...na Inteligência Artificial (IA) moderna, observa-se...
+ ...na IA moderna, observa-se...
```

```diff
arquivo.tex:42  [B. Extenso após declaração]
- ...durante a Revisão Sistemática da Literatura aplicada ao tema...
+ ...durante a RSL aplicada ao tema...
```

Para verificações C e D, mostre também o diff proposto em `pretextual/listas.tex`:

```diff
pretextual/listas.tex
  \item[LLM]   -- \textit{Large Language Model} (grande modelo de linguagem)
+ \item[NLP]   -- \textit{Natural Language Processing} (processamento de linguagem natural)
  \item[RSL]   -- Revisão Sistemática da Literatura
```

(respeitando ordem alfabética).

### Passo 6 — Solicite aprovação

Use `AskUserQuestion`:

> "Aprovo as alterações acima? Posso aplicar todas, aplicar apenas algumas (você me diz quais números), ou cancelar?"

Opções:
- **Aplicar todas** — segue para o passo 7.
- **Aplicar parcialmente** — pergunte os números (`1, 3, 5-7`) e aplique só esses.
- **Cancelar** — encerra sem editar.

### Passo 7 — Aplique as edições aprovadas

Use `Edit` (com `old_string`/`new_string` exatos, preservando indentação) para cada item aprovado. Faça uma edição por ocorrência, ampliando o contexto do `old_string` até ficar única.

**Importante**: ao adicionar uma nova entrada em `pretextual/listas.tex`, insira na posição alfabética correta e siga o mesmo padrão de alinhamento (`\item[XXX]   -- ...`).

Ao terminar, reporte em uma linha:
`✅ N alterações aplicadas em M arquivo(s) + lista atualizada com K nova(s) sigla(s).`

## Regras gerais de comportamento

- **NUNCA edite sem aprovação explícita** — o passo 6 é obrigatório.
- **NUNCA toque em** citação literal (`\enquote{...}`, `\begin{quote}...\end{quote}`), comentários `%`, ou comandos.
- Se o usuário enviar trecho colado (não arquivo), pule o passo 7 e mostre o trecho corrigido pronto para copiar.
- Se nenhuma inconsistência for encontrada: `✅ Nenhuma inconsistência de siglas encontrada em [arquivo].`
- Seja conciso entre passos — o foco é o relatório, o diff e a aprovação.
- Quando sugerir uma sigla nova (verificação D), justifique brevemente a sigla escolhida (ex.: "PLN = iniciais de Processamento de Linguagem Natural").
- Em caso de conflito (uma sigla sugerida já é usada para outra coisa), avisar e pedir ao usuário para escolher.

## Referências oficiais a citar quando o usuário pedir justificativa

- **Manual UniRV §2.1.12** (p. 23) — "Lista de siglas": obrigatória com mais de 10 itens, ordem alfabética.
- **Manual UniRV §6.4** (p. 213-214) — "Sigla e acrônimo": regras de primeira ocorrência, capitalização (≤3 vs ≥4 letras, c.1 vs c.2), sigla consagrada, formato dual para siglas estrangeiras.
- **Manual UniRV §3** (observações nos modelos de Tabelas/Quadros/Ilustrações) — proibição de siglas em títulos.
- **Manual UniRV §6.2** (p. 212) — Estrangeirismos e abreviaturas latinas (`et al.`, `apud`, `ibid.`, `opus citatum`) em itálico (NBR 10520/2023). Escopo do `ingles-italico-checker`, não desta skill.
- **ABNT NBR 14724/2024** — Trabalhos acadêmicos: apresentação.
- **ABNT NBR 10520/2023** — Citações em documentos.

## Skills relacionadas (não duplicar trabalho)

- **`ingles-italico-checker`** — cobre estrangeirismos em itálico no texto corrido (§6.2). Esta skill (`siglas-checker`) só verifica o itálico do **extenso dentro da Lista de Siglas** e do **extenso na primeira ocorrência no texto**. Se o usuário pedir revisão de itálico em geral, sugira a outra skill.
- **`quadro-tabela-validator`** — formato visual de tabelas/quadros. A presente skill apenas detecta sigla em `\caption{...}`; problemas de formatação ficam com a outra.
- **`tcc-writer`** — escrita/edição geral de trechos. Se precisar reescrever um parágrafo inteiro depois de aplicar correções, encaminhar para essa skill.
