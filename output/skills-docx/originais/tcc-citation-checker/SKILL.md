---
name: "tcc-citation-checker"
description: "Verifica fidelidade de citações em TCCs seguindo 5 regras essenciais: limite de 700 caracteres por parágrafo, clareza de mensagem, rastreabilidade completa com comentários, coerência interna do trabalho, e leitura integral das fontes sem dedução."
---

# TCC Citation Checker

Skill para verificar a fidelidade de citações em TCCs escritos em LaTeX, comparando o trecho
do TCC com a publicação original citada. Todas as reescritas seguem 5 regras essenciais:
**limite de 700 caracteres por parágrafo**, **clareza de mensagem**, **rastreabilidade com
comentários obrigatórios**, **coerência interna verificada**, **leitura integral das fontes**.

## O que o usuário fornece

- **Trecho do TCC** (em LaTeX ou texto puro) contendo a citação a ser verificada
- **Publicação citada** (PDF anexado ou texto colado) da qual a citação foi retirada

Se o usuário não fornecer algum desses dois elementos, peça antes de prosseguir.

---

## Fluxo de execução

### Passo 1 — Leitura e extração (Regra 5: Leitura integral, sem dedução)

**OBRIGATÓRIO**: Antes de prosseguir, você DEVE ler a publicação citada completamente, do início
ao fim. Não deduza o conteúdo, não busque apenas palavras-chave. Esta leitura integral evita
erros de interpretação e garante que você conhece o contexto real do que o autor escreveu.

1. Leia o trecho do TCC fornecido e identifique:
   - A afirmação principal que depende da citação
   - O autor/obra citado (ex: `\cite{autor2020}`)
   - O contexto argumentativo no trabalho (por que essa citação está sendo usada)

2. Leia a publicação citada INTEGRALMENTE (PDF ou texto) — não apenas busque a palavra-chave.
   Localize os trechos que fundamentam a afirmação do TCC e entenda o contexto completo em que
   o autor original escreveu aquelas palavras.

3. (Opcional mas recomendado) Consulte outras seções do TCC para verificar se há informações
   relacionadas que possam gerar incoerência interna.

---

### Passo 2 — Classificação da fidelidade

Compare o que o trecho do TCC afirma com o que a publicação realmente diz.
Classifique em uma das três categorias:

#### ✅ 100% Condizente
- A afirmação do TCC representa fielmente a ideia do autor
- O contexto e o sentido estão preservados
- Não há distorção, exagero ou simplificação indevida

#### ⚠️ Parcialmente Condizente
- A ideia geral está correta, mas há imprecisões, exageros, generalizações indevidas,
  ou o contexto foi ligeiramente distorcido
- A citação é parcialmente válida mas precisa de ajuste

#### ❌ Equivocado
- O trecho do TCC afirma algo que o autor não disse, contradiz o autor, ou usa a
  citação fora de contexto de forma enganosa
- A citação não suporta a afirmação feita

---

### Passo 3 — Explicação detalhada (Regra 2: Clareza de mensagem)

Após classificar, explique o diagnóstico com CLAREZA ABSOLUTA. Cada frase deve deixar evidente
o ponto que está sendo feito. Evite explicações vagas, suposições ou frases que deixem dúvida
sobre o que você quis dizer.

- **O que o TCC afirma**: resuma a afirmação do trecho em linguagem clara e direta
- **O que o autor realmente diz**: cite trecho(s) relevante(s) da publicação original
  (em bloco recuado, com indicação de página se disponível)
- **Onde está a divergência** (se houver): aponte com precisão o ponto problemático —
  uma palavra específica, uma generalização indevida, um contexto diferente, etc.

A explicação deve ser inequívoca: o leitor não deve ficar em dúvida sobre qual é o problema ou
sobre a recomendação que você está fazendo.

Exemplo de formato:

```
📄 O que o TCC afirma:
"[resumo claro da afirmação]"

📚 O que o autor diz (p. X):
"[trecho relevante da publicação]"

🔍 Diagnóstico:
[explicação precisa da concordância ou divergência, deixando claro qual é o problema específico]
```

---

### Passo 4 — Correção (se necessário) — Regras 1, 3, 4

Se a classificação for ⚠️ ou ❌, execute este passo com atenção às 5 regras essenciais.

#### 4a. Instrução de correção
Explique **o que precisa mudar** para o trecho ficar fiel ao autor:
- O que deve ser removido, suavizado ou contextualizado
- O que pode ser mantido
- Como preservar o argumento do TCC sem distorcer a fonte

#### 4b. Verificação de coerência interna (Regra 4: Coerência com o resto do trabalho)

**ANTES de reescrever**, você DEVE:

1. Revisar outras seções do TCC que já estão prontas para verificar se há informações
   relacionadas que possam gerar inconsistência com a reescrita proposta
2. Garantir que a nova redação não entra em contradição com o que já foi escrito em outro lugar
3. Conferir se os termos, conceitos e definições usados em outras partes do trabalho são
   consistentes com a redação que você vai propor

Se encontrar inconsistência, sinalize antes de fazer a reescrita e proponha uma solução coerente.

#### 4c. Reescrita proposta — Regra 1: Limite de 700 caracteres por parágrafo

Reescreva o trecho do TCC em LaTeX, com as seguintes exigências:
- Fiel ao que o autor realmente afirma
- Parafraseado (não cópia direta da publicação)
- Mantém o fluxo argumentativo do TCC
- Preserva o comando `\cite{}` original
- **LIMITE DE 700 CARACTERES POR PARÁGRAFO**: cada parágrafo da reescrita não deve
  exceder 700 caracteres (incluindo espaços). Se ultrapassar, divida o conteúdo em mais
  parágrafos ou reescreva de forma mais concisa.
- **Nunca use traço (" — " ou " - ") como recurso estilístico** — reescreva a frase
  de forma que a ideia caiba sem esse recurso (use ponto, vírgula, dois-pontos ou
  reestruture a oração)
- **Evite padrões de escrita típicos de IA**, como enumerações com travessão,
  frases com estrutura "X; Y; Z", paralelismos excessivos ou vocabulário
  excessivamente formal e uniforme

#### 4d. Comentário de rastreabilidade (Regra 3: Rastreabilidade completa)

**OBRIGATÓRIO**: Antes do bloco de código LaTeX com a reescrita, inclua um comentário de
rastreabilidade no seguinte formato:

```latex
%% FONTE: [título completo da publicação] / [autor(es)] / [ano]
%% Seção: [nome ou número da(s) seção(ões) de onde os trechos foram extraídos]
%% Página: [número(s) de página(s) correspondente(s) a cada seção listada]
%% Trecho: "[trecho exato extraído da publicação, copiado palavra por palavra]"
%% Trecho: "[outro trecho exato, se houver mais de um trecho relevante]"
```

Regras obrigatórias do comentário de rastreabilidade:
- Cada `%% Trecho:` deve conter **texto copiado LITERALMENTE** da publicação, sem paráfrase
  — o objetivo é que o pesquisador possa fazer Ctrl+C / Ctrl+V do trecho e localizá-lo na
  publicação original
- Liste apenas trechos que fundamentam a ideia inserida no texto do TCC — nenhum trecho
  irrelevante
- A ordem de `%% Seção:` e `%% Página:` deve corresponder entre si (primeira seção = primeira página)
- Se a publicação estiver em inglês, os trechos devem estar em inglês (idioma original)
- O comentário é uma ferramenta de auditoria para rastreabilidade acadêmica — não é opcional

Apresente o comentário de rastreabilidade seguido do bloco de código LaTeX com a reescrita.

---

### Passo 5 — Verificação de plágio e conformidade às 5 regras

Após propor a reescrita, faça uma análise em três níveis:

#### 5a. Verificação do limite de 700 caracteres por parágrafo (Regra 1)

Para cada parágrafo da reescrita:
1. Conte os caracteres (incluindo espaços, mas excluindo quebras de parágrafo)
2. Se algum parágrafo exceder 700 caracteres, sinalize: "Parágrafo [número] ultrapassa 700 caracteres"
3. Reescreva o parágrafo para ficar dentro do limite, dividindo em mais parágrafos se necessário

#### 5b. Verificação do texto reescrito contra plágio

Compare a reescrita proposta com:
1. O trecho original do TCC
2. O trecho da publicação citada

Verifique:
- **Estrutura sintática**: as frases têm estrutura diferente do original?
- **Vocabulário**: as palavras-chave foram substituídas por sinônimos adequados?
- **Fraseado**: não há sequências de 4+ palavras idênticas ao original?
- **Estilo**: o texto evita marcadores de escrita de IA (travessões, paralelismos
  excessivos, enumerações com hífen)?

#### 5c. Verificação do comentário de rastreabilidade (Regra 3)

Confirme que cada `%% Trecho:` está **EXATAMENTE IGUAL** ao texto da publicação original:
- Verifique palavra por palavra — ortografia, capitalização, pontuação
- Se qualquer palavra estiver diferente, corrija o comentário antes de entregar
- O comentário é ferramenta de auditoria: se estiver errado, o pesquisador não conseguirá
  localizar o trecho e a rastreabilidade falha

#### 5d. Verificação de coerência interna (Regra 4)

Certifique-se de que a reescrita proposta:
- Não contradiz outras seções do trabalho já redigidas
- Usa os mesmos termos e conceitos definidos em outras partes
- Mantém a coerência argumentativa e conceitual do TCC

#### Critério de aprovação final:

A reescrita é aprovada quando TODOS os critérios abaixo são atendidos:
- ✅ Nenhum parágrafo ultrapassa 700 caracteres
- ✅ Nenhuma sequência de 4+ palavras consecutivas coincide com a publicação original
- ✅ A estrutura das frases é visivelmente diferente
- ✅ O sentido e a fidelidade ao autor estão preservados
- ✅ O comentário de rastreabilidade contém apenas trechos literais e localizáveis
- ✅ A redação é coerente com o restante do trabalho
- ✅ As mensagens são claras, sem ambiguidades

Ao final, apresente o resultado com o selo:
```
✅ Reescrita aprovada — texto parafraseado, rastreabilidade verificada,
700 caracteres respeitado, coerência interna confirmada.
```

---

## Formato de saída completo

```
## Verificação de Citação

**Classificação:** [✅ 100% Condizente | ⚠️ Parcialmente Condizente | ❌ Equivocado]

---

### 📄 O que o TCC afirma
[resumo]

### 📚 O que o autor diz
[trecho da publicação, com página se disponível]

### 🔍 Diagnóstico
[explicação]

---

### ✏️ Correção sugerida
[o que deve mudar]

### 📝 Trecho reescrito (LaTeX)
\`\`\`latex
%% FONTE: [título] / [autor(es)] / [ano]
%% Seção: [seção(ões)]
%% Página: [página(s)]
%% Trecho: "[trecho literal da publicação]"
%% Trecho: "[outro trecho literal, se houver]"

[trecho reescrito em LaTeX]
\`\`\`

### 🔎 Verificação de plágio
[análise de similaridade do texto reescrito]
[verificação da exatidão dos trechos no comentário de rastreabilidade]

✅ Reescrita aprovada — texto parafraseado e rastreabilidade verificada.
```

---

## 5 Regras Essenciais de Qualidade (Resumo Executivo)

Todas as reescritas propostas por esta skill seguem obrigatoriamente estas 5 regras:

1. **Limite de 700 caracteres por parágrafo**: cada parágrafo da reescrita nunca deve
   ultrapassar 700 caracteres (incluindo espaços). Esta regra garante clareza, concisão
   e legibilidade.

2. **Clareza de mensagem**: toda explicação e recomendação deve ser inequívoca, sem deixar
   dúvidas. Evite frases vagas, suposições ou linguagem ambígua. O leitor deve entender
   imediatamente qual é o problema ou a recomendação.

3. **Rastreabilidade completa**: todo trecho que dependa de uma publicação ou PDF deve incluir
   comentário de rastreabilidade obrigatório em LaTeX. Os trechos literais devem ser exatos,
   permitindo auditoria acadêmica e verificação de plágio.

4. **Coerência interna**: antes de qualquer reescrita, verificar o restante do trabalho para
   garantir que a nova redação não contradiz o que já foi escrito. Termos, conceitos e
   argumentações devem ser consistentes em todo o TCC.

5. **Leitura integral das fontes**: nunca deduza, invente ou busque apenas palavras-chave.
   Leia a publicação completa, do início ao fim, para entender o contexto real do que o
   autor escreveu.

---

## Notas importantes

- **Leitura completa**: Sempre leia a publicação integralmente — não deduza, não invente,
  não busque apenas palavras-chave. O contexto real é essencial para classificação correta.

- **Rastreabilidade obrigatória**: Toda reescrita que cite uma publicação ou PDF exige
  comentário de rastreabilidade em LaTeX com trechos literais exatos — não é opcional.

- **Verificação de coerência**: Antes de qualquer reescrita, revise outras seções do TCC
  para evitar inconsistências internas. Um trabalho coerente é fundamental.

- **Limite de 700 caracteres**: Este é um limite inegociável. Se um parágrafo ultrapassar
  700 caracteres, sinalize e reescreva para caber dentro do limite. Qualidade de redação
  exige concisão.

- **Clareza acima de tudo**: Sua explicação deve ser inequívoca. O leitor não pode ficar
  em dúvida sobre qual é o problema ou a recomendação.

- Se a publicação for em inglês e o TCC em português, leve isso em conta na comparação —
  traduções imprecisas são uma fonte comum de equívoco.

- Se o usuário não forneceu o PDF da publicação e o título/DOI for identificável no `\cite{}`,
  pergunte se ele pode anexar — não tente verificar sem a fonte original completa.

- Mantenha um tom construtivo e didático: o objetivo é ajudar o estudante a melhorar o TCC,
  não apenas apontar erros. Explicações claras e orientações precisas levam a aprendizado.