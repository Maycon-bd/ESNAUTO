# Análise e adaptação das cinco skills

## Resultado e escopo

Foram preparadas cinco skills novas, com sufixo `-docx`, para Word/DOCX e Google Docs quando houver ferramentas compatíveis. Os nomes diferentes permitem coexistir com as versões de LaTeX. As versões recebidas foram preservadas em `originais/`; a monografia e a configuração de skills instaladas não foram alteradas.

As versões revisadas estão em `adaptadas/`, cada uma com SKILL.md e referências próprias. Os ZIPs individuais e o pacote conjunto são entregáveis portáteis; sua criação não equivale à instalação ou ativação automática no Codex.

## Mudanças por skill

| Recebida | Problemas encontrados | Tratamento na adaptação |
|---|---|---|
| quadro-tabela-validator | Projeto/caminhos de outro usuário; remissões ao manual geral; corpo 12 pt; quadro com grade; proibição de toda linha vertical; mínimo e listas tratados sem contexto | Perfil específico FASOFT; 11 pt no corpo/cabeçalho; 10 pt no título/fonte; quadro de 16 cm sem grade no corpo; separações de cabeçalho; imagens das páginas 53–54 e ambiguidade registrada |
| ingles-italico-checker | Busca por comandos em vez de estilo efetivo; listas de exceções maiores que as comprovadas; páginas antigas | Itálico nativo/herdado e palavras entre segmentos; exceções documentadas; outros termos dependem de consulta; citações diretas e funções tipográficas preservadas |
| tcc-writer | Persona com credenciais fictícias; contexto fixo de outro TCC sobre prototipação; estruturas de arquivos e bibliografia LaTeX; cota de ilustrações; regras editoriais apresentadas como absolutas | Contexto do trabalho efetivo; estilos e citações nativos; rastreabilidade em comentários/relatório; limite de 700 mantido como preferência editorial, não norma; sem cota artificial de ilustrações |
| siglas-checker | Lista externa fixa; exclusão de siglas comuns; regras de criação/normalização mecânicas; limiar conservador de 10 sem respaldo neste guia | Lista no documento; parte textual em ordem; grafia consagrada; mais de dez = 11+ na redação específica do PDF 24; tensão com nota geral de listas registrada |
| tcc-citation-checker | Saída em código; comentários obrigatórios em LaTeX; somente três classificações; critério de quatro palavras e selo de aprovação como teste de plágio | Evidência por afirmação; estado não verificável; preservação de campos; leitura efetivamente realizada declarada; sem certificado de originalidade |

## Correção principal de quadros/tabelas

Fonte: Guia Oficial de Padronização Científica da Faculdade de Engenharia de Software – UniRV, 1ª edição, v.1.0.2 (PDF recebido com 76 páginas). Toda paginação citada neste relatório indica posição no PDF, pois os modelos têm números impressos de exemplo.

As páginas 53 e 54 contêm instruções gráficas que não aparecem na extração de texto. A análise visual foi indispensável:

| Item | Tabela — PDF 53 | Quadro — PDF 54 |
|---|---|---|
| Título | 10 pt, simples, justificado, sem ponto-final | Igual |
| Cabeçalho | 11 pt, negrito; separações internas no cabeçalho | Anotação equivalente; divergência entre texto e desenho sobre divisória vertical |
| Corpo | 11 pt, simples, sem grade interna | Igual |
| Contorno | Sem laterais externas | Com laterais externas |
| Largura fixa | Não especificada no modelo | 16 cm |
| Fonte dos dados | 10 pt, simples, ponto-final | Igual |
| Siglas no título | Proibidas na anotação | Proibidas na anotação |

A largura de 16 cm mencionada pela skill writer original tem respaldo neste guia específico. Já a ordem de fechar todas as células do quadro é incompatível com a instrução de corpo sem traços internos. A regra da skill antiga de usar apenas três linhas horizontais em toda a tabela também omite as divisórias verticais do cabeçalho mostradas no modelo.

O quadro tem ambiguidade real: a anotação do cabeçalho pede linhas internas, mas a imagem não mostra claramente uma separação vertical. Isso foi mantido como ponto de decisão, sem transformar a dúvida em grade obrigatória no corpo.

O guia recomenda listas próprias por tipo de ilustração (PDF 23). Assim, Lista de Quadros é adequada; a regra anterior de exigir lista genérica de ilustrações foi removida. O guia pede referência no texto e proximidade do elemento (PDF 32); chamada anterior é preferência operacional, não uma ordem absoluta extraída dessa passagem.

## Recursos e portabilidade

Cada skill inclui orientações de acesso e preservação de Word/Google Docs, localização sem linhas fictícias, escopo de autorização e verificação estrutural/visual. Referências visuais pertinentes acompanham as skills que as utilizam. O PDF completo fica no pacote conjunto para reconferência e sua identidade está em `fontes.json`.

Os recursos de contexto e vocabulário de prototipação da writer recebida não foram transportados como contexto ativo: pertencem a outro trabalho. As instruções de entrega e citação foram reescritas para documentos; os cenários de avaliação foram adaptados para entradas DOCX, fontes insuficientes e preservação de mecanismos nativos.

## Verificação e limites

Foi feita conferência das referências relativas, nomes/frontmatter, conteúdo dos ZIPs e ausência de dependências de projetos LaTeX nas versões adaptadas. A leitura visual das páginas 53–54 fundamenta o perfil tabular; páginas 48, 71–72 foram conferidas visualmente para siglas/estrangeirismos. A validação técnica e seus resultados estão em `VALIDACAO.md`.

Não foi executada uma revisão da monografia usando as skills, nem um teste de edição em Google Docs. As skills instruem a descobrir os recursos disponíveis e a declarar limitações; não afirmam que o conector instalado suporta todo tipo de formatação.
