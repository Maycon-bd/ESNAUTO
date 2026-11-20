# Formato de Entrega

Após autorização do usuário, entregue em **três blocos**:

---

## BLOCO 1 — Código LaTeX

O código completo e pronto para copiar no arquivo `.tex` correspondente, incluindo:

- Comando de abertura da seção/subseção
- Todo o texto em LaTeX com parágrafos, citações e ambientes corretos
- Comentários de rastreabilidade `%% FONTE:` após cada parágrafo com informação externa
- Indicações `%% LACUNA:` onde informação faltou
- Comentários `%% ILUSTRACAO SUGERIDA` inseridos no local exato, com todos os campos preenchidos

**Nunca entregue código com `\begin` sem `\end` correspondente.**

---

## BLOCO 2 — Entradas BibTeX

Todas as entradas prontas para copiar no `referencias.bib`, uma para cada artigo citado no texto. Use o `@type` correto (ver `references/regras-citacao.md`).

Só gere este bloco se houver novas referências não presentes no bib atual.

---

## BLOCO 3 — Arquivo Markdown de Resultado

Gere o conteúdo completo de um arquivo `escrita_[nome-da-secao].md` com a seguinte estrutura:

```markdown
# Escrita — [NOME DA SECAO/SUBSECAO]
**TCC UniRV | Data de geração:** [data]
**Artigos utilizados:** [lista com título, autores e ano de cada artigo citado]

---

## Texto gerado (versão legível)

[Todo o texto da seção em português puro, sem comandos LaTeX, para leitura e revisão humana]

---

## Rastreabilidade por parágrafo

[Para cada parágrafo: número do parágrafo → artigo de origem → seção → página → trecho original]

---

## Lacunas identificadas

[Lista de todos os %% LACUNA: encontrados, com descrição e ação necessária]

---

## Ilustrações sugeridas

| # | Tipo | Título sugerido | Posição | O que ilustra | Conteúdo resumido | Fonte |
|---|---|---|---|---|---|---|
| 1 | [tipo] | [título] | [após parágrafo N] | [afirmação] | [dados/eixos] | [origem] |

---

## Limitações dos estudos utilizados

[Lista das limitações conceituais e metodológicas dos estudos utilizados]

---

## Checklist de entrega

- [ ] Todo parágrafo tem pelo menos uma citação atribuída
- [ ] Nenhuma afirmação foi feita sem atribuição de autoria
- [ ] Cada parágrafo tem %% FONTE: com artigo, seção, página e trecho
- [ ] As citações estão no formato ABNT correto (autor-data)
- [ ] O código LaTeX está sintaticamente correto
- [ ] Não há \begin sem \end correspondente
- [ ] Nenhuma informação foi inventada ou presumida
- [ ] As lacunas estão sinalizadas com %% LACUNA:
- [ ] As entradas BibTeX estão completas com o @type correto
- [ ] Nenhum termo proibido foi usado no texto
- [ ] Toda afirmação é factual ou inferência explicitamente anunciada
- [ ] A auto-revisão foi executada por completo
- [ ] O texto está em português brasileiro, voz impessoal, 3a pessoa
- [ ] Nenhum padrão de escrita de IA foi usado (ex: " - " como conector)
- [ ] O texto não reproduz 100% nenhuma fonte (sem plágio)
- [ ] Toda ilustração sugerida tem comentário completo com todos os campos
- [ ] Todo elemento visual tem chamada prévia no parágrafo anterior
- [ ] A numeração de cada tipo é progressiva e independente por tipo
- [ ] Há no mínimo 1 ilustração sugerida a cada 2-3 páginas de texto
```
