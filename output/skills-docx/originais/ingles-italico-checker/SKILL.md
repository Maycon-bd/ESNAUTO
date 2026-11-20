---
name: ingles-italico-checker
description: Revisa uma seção LaTeX do TCC e identifica todas as palavras em inglês (estrangeirismos) que NÃO estão envolvidas por \textit{}. Apresenta a lista das ocorrências encontradas, mostra um preview do diff com a correção (envolvendo cada palavra em \textit{}) e pergunta se o usuário aprova a aplicação antes de editar o arquivo. Use sempre que o usuário disser "revisar inglês em itálico", "checar estrangeirismos", "verificar palavras em inglês", "/ingles-italico-checker", ou enviar uma seção/arquivo .tex pedindo para conferir se os termos em inglês estão em itálico. Acionar SEMPRE que o usuário mencionar revisão de itálico, estrangeirismos ou termos em inglês em qualquer arquivo do projeto Template (TCC UniRV).
---

# ingles-italico-checker — Revisor de Estrangeirismos em Itálico

## Contexto do projeto

Este TCC (UniRV, LaTeX/abntex2) segue a regra do **Manual UniRV (seção 6.2, p. 212)**: "os estrangeirismos devem ser grafados em itálico" via `\textit{...}`. O usuário escreve em português e marca termos em inglês manualmente; é comum esquecer algumas ocorrências. Sua missão é encontrar essas omissões em uma seção (um ou mais arquivos `.tex`) que o usuário enviar.

## Base normativa (Manual UniRV + NBR 10520/2023)

**Regra geral** — estrangeirismos em itálico.

**Exceção 1 — termos já aportuguesados NÃO levam itálico.** O Manual UniRV cita explicitamente como exemplos: `download`, `feedback`, `marketing`, `on-line`, `bullying`, `campus`. A fonte oficial adotada pela UniRV é a Lista de Estrangeirismos da Secom/Senado Federal: https://www12.senado.leg.br/manualdecomunicacao/verbetes-acessorio/estrangeirismos-grafados-sem-italico-ou-aspas

**Exceção 2 — abreviaturas latinas de citação SEMPRE em itálico** (NBR 10520/2023, reforçado no Manual UniRV): `et al.`, `apud`, `ibid.`, `ibidem`, `idem` (`id.`), `opus citatum` (`op. cit.`), `loco citato` (`loc. cit.`), `passim`, `sequentia` (`et seq.`), `conferre` (`cf.`).

**Ênfase em citação literal** — se houver grifo (itálico) adicionado dentro de `\enquote{}` ou `\begin{quote}`, o autor da obra exige a marca `grifo nosso` (quando o itálico foi adicionado pelo usuário) ou `grifo do autor` (quando o itálico já estava no original). Não altere itálicos dentro de citações literais — apenas sinalize se faltar a marcação `grifo nosso`/`grifo do autor`.

## Entrada esperada

O usuário fornecerá:
- Um caminho de arquivo `.tex` (ex.: `textual/2-referencial_teorico/1-revisao-literatura.tex`), OU
- Um diretório (ex.: `textual/1-introducao/`), OU
- Um trecho de código LaTeX colado direto na conversa.

Se o caminho for ambíguo, peça confirmação antes de prosseguir.

## Protocolo de execução (siga na ordem)

### Passo 1 — Leia o conteúdo
Use `Read` para o(s) arquivo(s) indicado(s). Se for um diretório, use `Glob` para listar todos os `.tex` antes.

### Passo 2 — Identifique candidatos a estrangeirismos

Procure por palavras/expressões em inglês **fora** de `\textit{...}`. Para isso, percorra o texto e ignore:

- Conteúdo dentro de `\textit{...}`, `\emph{...}`, `\textbf{\textit{...}}`.
- Comandos LaTeX (`\cite`, `\citeonline`, `\ref`, `\label`, `\input`, `\section`, `\chapter`, etc.) e seus argumentos chave-valor.
- Blocos `\begin{lstlisting}...\end{lstlisting}` e `\verb|...|`.
- Comentários (linhas começando com `%`, e o restante de uma linha após `%` não escapado).
- URLs dentro de `\href{...}{...}` e `\url{...}`.
- Conteúdo de `\footnote{...}` só para o argumento de comandos como `\href`, mas o texto narrativo de notas de rodapé DEVE ser verificado normalmente.
- Chaves bibliográficas de `\cite{chaveDoAutor2024}` — a chave não é texto narrativo.

**O que CONSIDERAR como estrangeirismo a corrigir (envolver em `\textit{}`):**
- Palavras inglesas usadas como substantivos comuns no fluxo do texto: `stakeholders`, `framework(s)`, `prompt(s)`, `wireframe(s)`, `mockup(s)`, `backlog`, `sketch(es)`, `layout(s)`, `template(s)`, `widget(s)`, `expertise`, `dashboard`, `deadline`, `briefing`, `insight(s)`, `workflow`, `pipeline`, `cluster`, `query/queries`, `script(s)`, `plugin(s)`, `bug(s)`, `release`, `feature(s)`, `dataset(s)`, `output`, `input`, `parser`, `crawler`, `survey`, `benchmark`, `crowdsourcing`, `cloud`, `streaming`, `gateway`, `endpoint`, `token(s)`, `embedding(s)`.
- **Abreviaturas latinas de citação (SEMPRE em itálico, regra reforçada pelo Manual UniRV e NBR 10520/2023)**: `et al.`, `apud`, `ibid.`, `ibidem`, `idem` (`id.`), `op. cit.`, `opus citatum`, `loc. cit.`, `loco citato`, `passim`, `et seq.`, `sequentia`, `cf.`, `conferre`.
- Outras expressões latinas: `in loco`, `a priori`, `a posteriori`, `ad hoc`, `lato sensu`, `stricto sensu`, `in vitro`, `in vivo`, `sui generis`, `per capita` (este último é controverso — sinalize).
- Títulos em inglês de obras/conferências/journals em texto corrido (fora de `\cite{...}`).
- Termos técnicos expandidos em inglês: `Large Language Models`, `Natural Language Processing`, `Machine Learning`, `Deep Learning`, `Computer Vision`, `Quasi-Gold Standard`, `Preferred Reporting Items for Systematic Reviews and Meta-Analyses`, `User Experience`, `User Interface`.

**O que NÃO marcar — termos aportuguesados, conforme Manual UniRV §6.2 e Lista da Secom:**

Lista explícita de exemplos do Manual UniRV (NÃO levam itálico): `download`, `feedback`, `marketing`, `on-line` (e a variante `online`), `bullying`, `campus`.

Outros termos amplamente reconhecidos como aportuguesados pela Lista da Secom (NÃO levam itálico): `site`, `web`, `link`, `e-mail`, `internet`, `mouse`, `chip`, `pixel`, `software`, `hardware`, `design`, `designer`, `show`, `shopping`, `pendrive`, `smartphone`, `tablet`, `notebook`, `know-how`, `workshop`, `play-off`, `playboy`, `slogan`, `status`, `stress`, `gay`. Em caso de dúvida sobre se um termo está nessa lista, **inclua-o como "⚠️ controverso — verificar na Lista da Secom"** e deixe o usuário decidir.

**O que NÃO marcar — outras exclusões:**
- Siglas em maiúsculas: `IA`, `LLM`, `LLMs`, `GPT`, `GPT-4`, `PRISMA`, `RSL`, `API`, `URL`, `HTTP`, `PDF`, `JSON`, `IEEE`, `ACM`, `IBGE`, `UN`, `FAO`, `AIDS`. (Manual UniRV §6.4 não exige itálico em siglas, mesmo estrangeiras.)
- Nomes próprios (produtos, ferramentas, empresas, modelos): `Gemini`, `PaLM`, `Figma`, `Sketch` (quando é o nome do app), `Parsifal`, `Overleaf`, `GitHub`, `Google`, `Microsoft`, `OpenAI`, `Anthropic`, `Claude`, `ChatGPT`, `Adobe`, `Photoshop`.
- Palavras dentro de citação direta literal (`\enquote{...}` ou `\begin{quote}...\end{quote}`) — citação literal preserva o original. **Não altere**; apenas avise se houver itálico adicionado pelo usuário sem a marca `grifo nosso` ou `grifo do autor` (Manual UniRV §5.1).
- Nomes de autores em `\citeonline{...}`/`\cite{...}` (já tratado pelo template).
- Argumentos de `\href{url}{...}`, `\url{...}`, `\label{...}`, `\ref{...}`.

### Passo 3 — Apresente a lista ao usuário

Formato obrigatório:

```
## Palavras em inglês fora de \textit{} encontradas

Total: N ocorrências em M arquivo(s).

### arquivo.tex
| # | Linha | Palavra/Expressão | Contexto | Observação |
|---|-------|-------------------|----------|------------|
| 1 | 42    | stakeholders      | "...envolver stakeholders e refinar..." | — |
| 2 | 87    | et al.            | "(Silva et al., 2024)"                  | expressão latina |
| 3 | 103   | design            | "...processo de design de interfaces..." | ⚠️ controverso |
```

Agrupe por arquivo. Use o número da linha real do arquivo. Inclua um trecho curto de contexto (~60 caracteres).

### Passo 4 — Mostre o preview da alteração

Antes de qualquer edição, apresente um diff visual em blocos de código com prefixo `-` (antes) e `+` (depois) para CADA ocorrência:

```diff
arquivo.tex:42
- ...essa prática para envolver stakeholders e refinar requisitos...
+ ...essa prática para envolver \textit{stakeholders} e refinar requisitos...
```

Se houver muitas ocorrências (>10), agrupe e mostre o diff completo de uma vez por arquivo, mas mantenha numeração para que o usuário possa rejeitar itens específicos.

### Passo 5 — Solicite aprovação

Use a ferramenta `AskUserQuestion` com a pergunta:

> "Aprovo as alterações acima? Posso aplicar todas, aplicar apenas algumas (você me diz quais números), ou cancelar?"

Opções:
- **Aplicar todas** — segue para o passo 6 com todas.
- **Aplicar parcialmente** — pergunte quais números (`1, 3, 5-7`) e aplique só esses.
- **Cancelar** — não edita nada, encerra.

### Passo 6 — Aplique as edições aprovadas

Use `Edit` (com `old_string`/`new_string` exatos, preservando indentação) para cada item aprovado. Faça uma edição por ocorrência para garantir unicidade do `old_string` — se a frase aparecer mais de uma vez, expanda o contexto até ficar única.

Ao terminar, reporte em uma linha: `✅ N alterações aplicadas em M arquivo(s).`

## Regras gerais de comportamento

- **NUNCA edite sem aprovação explícita** — o passo 5 é obrigatório.
- **NUNCA toque em** `\enquote{...}`, `\begin{quote}...\end{quote}`, comentários `%`, ou comandos LaTeX.
- Se o usuário enviar trecho colado (não arquivo), pule o passo 6 e apenas mostre o trecho corrigido pronto para ele copiar.
- Se não encontrar nenhuma ocorrência, responda em uma linha: `✅ Nenhum estrangeirismo fora de \textit{} encontrado em [arquivo].`
- Seja conciso nas mensagens entre passos — o foco é a lista, o diff e a pergunta de aprovação.
- **Falsos positivos detectados no template do usuário**: o arquivo `textual/3-metodologia/7-extracao-dados.tex` contém `\textit{on-line}`. Conforme Manual UniRV §6.2, `on-line` é aportuguesado e NÃO deveria estar em itálico — se você encontrar esse padrão (palavra aportuguesada DENTRO de `\textit{}`), reporte como **"⚠️ itálico indevido"** numa seção separada da lista e ofereça a correção inversa (remover o `\textit{}`).

## Referências oficiais a citar quando o usuário pedir justificativa

- Manual UniRV §6.2 (p. 212) — "EMPREGO DE PALAVRAS ESTRANGEIRAS"
- ABNT NBR 10520/2023 — abreviaturas latinas de citação
- Lista da Secom/Senado: https://www12.senado.leg.br/manualdecomunicacao/verbetes-acessorio/estrangeirismos-grafados-sem-italico-ou-aspas
