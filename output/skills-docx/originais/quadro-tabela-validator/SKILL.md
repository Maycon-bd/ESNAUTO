---
name: quadro-tabela-validator
description: Valida e corrige tabelas e quadros LaTeX no projeto TamplateLattex segundo o ManualUniRV. Use quando o usuário enviar um trecho LaTeX de tabela/quadro, mencionar /quadro-tabela-validator, "verificar tabela", "validar quadro", "está certo o quadro/tabela?", "esse quadro/tabela está de acordo com o manual?", ou pedir para checar se a representação tabular está correta (quadro vs tabela) e se a formatação atende às exigências do Manual UniRV. Acionar SEMPRE que o usuário enviar código LaTeX de tabular/table/quadro/longtable para validação.
---

# Quadro/Tabela Validator — Validação UniRV

## Quando esta skill é acionada
O usuário enviará:
1. Um trecho LaTeX com um quadro ou tabela (ambientes `table`, `tabular`, `longtable`, `quadro`, etc.).
2. O caminho/localização no projeto: capítulo, seção e/ou subseção dentro de `TamplateLattex/`.
3. (Opcional) O `ManualUniRV.pdf` anexado para reconferência ao final.

Caminho base do projeto: `C:\Users\lokao\Downloads\QuadroEtabela\TamplateLattex\`
Caminho do manual: `C:\Users\lokao\Downloads\QuadroEtabela\ManualUniRV.pdf`

---

## REGRAS DE OURO (inegociáveis)

⚠️ Estas 3 regras valem em TODAS as fases. Violar qualquer uma delas é falha grave da skill.

### REGRA 1 — DUAS ANÁLISES DE FORMATAÇÃO OBRIGATÓRIAS
Toda execução da skill DEVE realizar **DUAS análises distintas** de formatação:
- **Análise A (Fase 2):** validação contra as regras já codificadas nesta skill (`regras-manual.md` + checklist da Fase 2). Não consulta o PDF — usa só o que está documentado na skill.
- **Análise B (Fase 3):** validação extraindo informações DIRETAMENTE do `ManualUniRV.pdf` via `Read` com `pages`, e comparando com a proposta de correção da Análise A. Procura inconsistências entre o que a skill diz e o que o PDF realmente diz.

Se a Análise B encontrar qualquer divergência em relação à Análise A, AJUSTAR a proposta antes de mostrar ao usuário e RELATAR a divergência encontrada.

### REGRA 2 — NÃO INVENTAR, NÃO DEDUZIR, NÃO AUMENTAR
- Toda afirmação sobre regra de formatação deve vir **literalmente** desta skill (`SKILL.md` + `regras-manual.md`) OU **literalmente** do `ManualUniRV.pdf`.
- **PROIBIDO** inferir regras que não estejam escritas. Se algo não está coberto, dizer explicitamente: *"O manual não especifica este ponto"*.
- **PROIBIDO** estender uma regra para casos análogos que não estão escritos.
- **PROIBIDO** "completar" lacunas com bom senso ou prática comum.
- Se a skill contém regra X e o manual não menciona X, indicar que X veio da skill (ex.: decisão registrada pelo usuário, como centralização do bloco) e não do manual.
- Sempre que possível, citar a página do manual (ex.: "pág. 36").

### REGRA 3 — NUNCA ALTERAR SEM PERMISSÃO EXPLÍCITA
- **PROIBIDO** executar `Edit` ou `Write` em qualquer arquivo `.tex` antes que o usuário responda "sim", "pode", "aplique", ou equivalente.
- A proposta de alteração DEVE conter três blocos obrigatórios:
  1. **COMO ESTÁ AGORA** — bloco LaTeX original recebido do usuário, sem modificações.
  2. **COMO VAI FICAR** — bloco LaTeX corrigido proposto.
  3. **O QUE A ALTERAÇÃO VAI RESULTAR** — descrição em linguagem natural do que muda visualmente/estruturalmente e por qual regra (com citação da página do manual quando aplicável).
- Após apresentar os 3 blocos, terminar com a pergunta: *"Posso aplicar essas alterações em `[caminho do arquivo]`?"*
- Aguardar resposta. Sem resposta afirmativa → não tocar em arquivo nenhum.

### REGRA 4 — APENAS FORMATAÇÃO, NUNCA O CONTEÚDO
- **PROIBIDO** alterar, reescrever, traduzir, resumir, completar, corrigir ortografia, "melhorar" ou de qualquer forma modificar as **informações** dentro das células do quadro/tabela.
- O conteúdo das células (textos descritivos, números, datas, rótulos, valores) deve ser preservado **byte a byte**.
- Também é proibido alterar:
  - O texto do título/legenda (apenas a sua estrutura — palavra designativa, numeração, travessão, presença/ausência de ponto final — pode ser ajustada para conformidade).
  - O texto da linha "Fonte:" — apenas a sua estrutura/posição é passível de ajuste.
- O que PODE ser alterado: bordas, alinhamento, negrito do cabeçalho, troca de ambiente (`table` ↔ ambiente de quadro), centralização do bloco, posição de título/fonte, conversão entre tabela e quadro (mantendo todo o conteúdo das células), e formatação tipográfica.
- Se a Fase 1 indicar conversão de tabela → quadro (ou vice-versa), o **conteúdo das células permanece exatamente igual**; somente o tipo do bloco e o estilo de bordas mudam.
- Se identificar erro no conteúdo (ex.: dado errado, palavra trocada), **apenas apontar** no relatório (em uma seção "Observações sobre o conteúdo — fora do escopo desta skill"); **nunca corrigir** no bloco "Como vai ficar".

---

## Protocolo OBRIGATÓRIO em 3 fases

A skill deve seguir EXATAMENTE esta ordem. **Nunca pular fases.**

---

### FASE 1 — IDENTIFICAÇÃO: É QUADRO OU TABELA?

Analisar o conteúdo das células e decidir:

- **Deve ser TABELA** quando o conteúdo é **quantitativo/estatístico**: números, valores monetários, percentuais, medidas, frequências, contagens, dados estatísticos. A finalidade é resumir/sintetizar dados numéricos.
- **Deve ser QUADRO** quando o conteúdo é **qualitativo/descritivo/textual**: descrições, definições, comparações textuais, características, categorias com texto explicativo, listagens conceituais, comparativos de autores/teorias/abordagens. A finalidade é dar visão conjunta sintética de um tema.

Regra-decisor:
- A maioria das células do corpo contém números/medidas? → TABELA.
- A maioria das células do corpo contém texto descritivo/categórico? → QUADRO.
- Caso misto (rótulos curtos + valores numéricos), prevalece o caráter numérico → TABELA.

**Comparar com a representação atual:**
- Se o usuário enviou rotulado como "Tabela" mas o conteúdo é qualitativo → deve virar QUADRO.
- Se enviou como "Quadro" mas o conteúdo é numérico → deve virar TABELA.
- Se a representação atual já é a correta → seguir para Fase 2.

**Relatar a decisão ao usuário** com justificativa baseada no conteúdo das células, ANTES de aplicar qualquer alteração de tipo.

---

### FASE 2 — VALIDAÇÃO DE FORMATAÇÃO

Validar contra TODOS os requisitos do Manual UniRV listados em `regras-manual.md` (na mesma pasta desta skill).

Itens a verificar na ordem:

**A) Estrutura externa**
1. Bloco centralizado horizontalmente na página (`\centering` ou `\begin{center}`).
2. Título acima do bloco, no formato:
   - Tabela: `Tabela N – Título descrevendo natureza, abrangência temporal e geográfica` (sem ponto final).
   - Quadro: `Quadro N – Título descrevendo natureza, abrangência temporal e geográfica` (sem ponto final).
   - Travessão (en-dash " – "), não hífen "-".
   - Numeração progressiva.
3. Linha "Fonte:" abaixo do bloco, obrigatória, em uma das 3 formas:
   - `Fonte: Autor da obra consultada (ano).`
   - `Fonte: Adaptado de Autor da obra consultada (ano).`
   - `Fonte: Nome do autor do trabalho, ano dos dados.`
4. Título e fonte devem **acompanhar a borda esquerda do bloco centralizado**.
5. Legenda/notas abaixo da fonte, se houver.

**B) Estrutura interna do corpo**
6. No mínimo **3 linhas e 2 colunas**.
7. Cabeçalho em **negrito**.
8. Alinhamento dentro das células:
   - Tabela: texto à esquerda; números à direita (preferencialmente alinhados pela vírgula decimal).
   - Quadro: todo o conteúdo à esquerda.
9. Bordas:
   - Tabela: bordas laterais externas **abertas** (sem `|` nas laterais externas); apenas linhas horizontais marcando topo, abaixo do cabeçalho e fundo (estilo IBGE — usar `\toprule`, `\midrule`, `\bottomrule` do `booktabs` ou `\hline` correspondente).
   - Quadro: bordas **fechadas em todos os lados** (moldura completa) + divisórias verticais entre colunas no corpo.
10. Altura das linhas: ajusta-se ao conteúdo (não forçar uniformidade artificial).
11. Largura das colunas: proporcional ao conteúdo (não forçar igualdade).
12. Largura total do bloco: apenas o necessário, não estender artificialmente até as margens.

**C) Tipografia**
13. Fonte do texto no corpo: 12 pt no padrão geral do documento (pode ser menor dentro de tabelas/quadros densos, mas mantenha legibilidade).
14. Cor do texto: preta.

**D) Inserção no texto**
15. O quadro/tabela deve ser **citado no texto** antes de aparecer, em uma das duas formas:
   - Contextualizado: `...conforme pode ser observado na Tabela 1.` / `...no Quadro 1.`
   - Final de frase: `... (Tabela 1).` / `... (Quadro 1).`
16. O bloco deve estar **o mais próximo possível** do parágrafo que o referencia.

**E) Lista pré-textual**
17. Se for tabela → deve ter entrada na **Lista de Tabelas** (`\listoftables` / `main.lot`).
18. Se for quadro → deve ter entrada na **Lista de Ilustrações** (junto com figuras, gráficos, mapas) — NÃO na Lista de Tabelas.

---

### FASE 3 — RECONFERÊNCIA CONTRA O PDF DO MANUAL

Após propor a versão corrigida, **reler trechos relevantes do `ManualUniRV.pdf`** e cruzar com a proposta:

- Páginas 35–37: definições e itens obrigatórios (Tabela, Ilustrações, Quadro).
- Páginas 134–135 (modelo de tese/monografia/dissertação) e 161–162 (modelo de artigo): exemplos visuais de Tabela 1 e Quadro 1.
- Página 207 (seção 5.2.6): regras de citação no texto.
- Páginas 22–23 e 69–70: listas pré-textuais.

Usar a tool `Read` com parâmetro `pages` (ex.: `pages: "35-37"`). Nunca chamar Read sem `pages` — o arquivo é grande demais.

**Procurar especificamente:** inconsistência entre a proposta e o que o manual realmente diz. Se encontrar qualquer divergência, ajustar antes de mostrar ao usuário.

---

## SAÍDA AO USUÁRIO — formato obrigatório

Apresentar nesta ordem:

### 1. Diagnóstico Fase 1 — Tipo (Tabela ou Quadro)
- Decisão: é Tabela ou Quadro?
- Justificativa baseada no conteúdo das células (sem deduzir além do que está escrito nas regras).
- Comparar com o que o usuário enviou: conforme / precisa conversão.

### 2. Análise A (Fase 2) — Validação contra as regras da skill
- Checklist completo dos 18 itens com status: ✓ conforme / ✗ não conforme / ⚠ atenção.
- Para cada ✗ e ⚠, explicar o problema citando a regra origem (item N de `SKILL.md` ou seção de `regras-manual.md`).

### 3. Análise B (Fase 3) — Reconferência direta no `ManualUniRV.pdf`
- Listar as páginas efetivamente lidas via `Read` com `pages`.
- Para cada item validado na Análise A, indicar se o PDF confirma, se diverge, ou se o PDF é silencioso (não menciona).
- Se houver divergência, relatar exatamente onde a skill e o PDF discordam.

### 4. Proposta de alteração — formato obrigatório em 3 BLOCOS
Apresentar SEMPRE os três blocos abaixo, identificando o arquivo-alvo (caminho completo dentro de `TamplateLattex/`):

**Arquivo:** `C:\Users\lokao\Downloads\QuadroEtabela\TamplateLattex\[caminho]`

**BLOCO 1 — Como está agora:**
```latex
[trecho original do usuário, intacto]
```

**BLOCO 2 — Como vai ficar:**
```latex
[trecho corrigido proposto]
```

**BLOCO 3 — O que essa alteração vai resultar:**
- Lista item a item das mudanças (ex.: "troca de hífen por travessão", "remoção de bordas verticais externas", "adição de linha Fonte:").
- Para cada mudança, citar a regra que a justifica (item N do checklist + página do manual quando aplicável).
- Descrever o efeito visual/estrutural esperado (ex.: "tabela passará a ter estilo IBGE com 3 linhas horizontais e sem moldura externa").

### 5. Pedido de permissão
Terminar SEMPRE com a pergunta literal:

> "Posso aplicar essas alterações em `[caminho completo do arquivo]`?"

⚠️ **NUNCA aplicar Edit/Write em arquivos do `TamplateLattex/` sem o usuário responder afirmativamente.**

---

## Convenções LaTeX recomendadas para conformidade

**Tabela (estilo IBGE, sem laterais externas, com booktabs):**
```latex
\begin{table}[H]
    \centering
    \caption{Título da tabela sem ponto final}
    \label{tab:exemplo}
    \begin{tabular}{lrrr}
        \toprule
        \textbf{Descrição} & \textbf{Valor 1 (cm)} & \textbf{Valor 3 (m)} & \textbf{Valor 4 (n)} \\
        \midrule
        Item 1          & 1,00 & 14,01    & 50 \\
        Item 11         & 2,25 & 1.200,05 & 60 \\
        Item 22         & 3,18 & 1,18     & 18 \\
        Item completo   & 4,40 & 28,18    & 4  \\
        \bottomrule
    \end{tabular}
    \\[2pt]
    \begin{flushleft}
        \footnotesize Fonte: Autor da obra consultada (ano).
    \end{flushleft}
\end{table}
```

**Quadro (bordas fechadas, divisórias verticais):**
```latex
\begin{table}[H]
    \centering
    \caption{Quadro N – Título descrevendo natureza e abrangência}
    \label{qua:exemplo}
    \begin{tabular}{|l|l|}
        \hline
        \textbf{Período} & \textbf{Descrição} \\
        \hline
        2005-2010 & Texto descritivo... \\
        \hline
        2006-2012 & Texto descritivo... \\
        \hline
        2008-2015 & ... \\
        \hline
        2010-2017 & Texto descritivo... \\
        \hline
    \end{tabular}
    \\[2pt]
    \begin{flushleft}
        \footnotesize Fonte: Autor da obra consultada (ano).
    \end{flushleft}
\end{table}
```

Observação: se o projeto define um ambiente próprio `quadro` (verifique `config/pacotes.tex` e `config/formatacao.tex`), use o ambiente do projeto em vez do `table`.

---

## Comportamento esperado

- Nunca pular nenhuma das 3 fases.
- Sempre executar AS DUAS análises de formatação (Análise A — skill, Análise B — PDF). Não aceitar atalhos.
- Não inventar, não deduzir, não estender regras. Se algo não está escrito, dizer "o manual não especifica".
- Sempre justificar cada decisão citando a regra-origem (item do checklist e/ou página do manual).
- Sempre apresentar a proposta de alteração nos 3 blocos obrigatórios (antes / depois / resultado).
- Sempre pedir permissão antes de aplicar edição em arquivos `.tex`. Sem resposta afirmativa, não executar Edit/Write.
- Alterar **somente a formatação**. O conteúdo das células (textos, números, datas, rótulos) é intocável — preservar byte a byte. Se notar erro no conteúdo, apenas apontar como observação fora do escopo, sem corrigir.
- Se faltar informação (ex.: localização exata dentro de `TamplateLattex/`), perguntar antes de prosseguir.
- Se o `ManualUniRV.pdf` não estiver acessível, alertar o usuário e NÃO prosseguir com a Análise B — informar que a validação ficou incompleta. Não substituir a Análise B por inferência.
