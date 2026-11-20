# Rodada 4 — fontes editoriais e canais complementares

Base examinada: **v010**, SHA256 `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`.
O registro editorial e o hash foram conferidos. Nenhuma edição Word nesta rodada.

## Resultado

Ampliada a investigação de **quatro células em três fontes**: Sharma P1/P4,
Hariharan P4 e Deng P1. Foram recuperados os dois pacotes de origem editorial
do arXiv, inventariados seus membros e lidas passagens pertinentes dos textos,
sem compilar TeX nem executar scripts. A matriz atual mantém **38 sinais ?**.
Este resultado não conclui a meta de recuperar todas as informações.

### Sharma — pesos e comparadores

O histórico oficial do [arXiv 2508.05416](https://arxiv.org/abs/2508.05416)
lista a v1. O pacote arquivado contém texto, bibliografia, classes e imagens;
seu inventário não contém código experimental identificado.

No `samplepaper.tex`, método (linhas217–246), tabela de hiperparâmetros
(328–343) e seleção (564) distinguem parâmetros amostrados e ruído de pesos.
A associação a ReservoirPy não individualiza versão ou lei efetiva de Win/W.
Há referência a inicializadores padrão no rascunho comentado (283), a respeito
do estado inicial. Comentários excluídos da publicação não comprovam o método
executado. Não se aproveitou o texto oculto da imagem do PDF que já havia sido
rejeitado nas revisões anteriores.

Baselines (698–703), resultados (774–784) e discussão/conclusão (1000–1038)
confrontam ESN com Last Value e XGBoost. A discussão de LSTM/Transformer nos
trabalhos relacionados não traz novo contraste quantitativo qualificador.
As passagens consultadas não justificam alterar P1/P4.

**Nova alternativa identificada:** o [registro institucional DFKI](https://www.dfki.de/en/web/research/projects-and-publications/publication/17053)
identifica publicação ICONIP, pp.365–380, e oferece a mesma preprint. A
[editora apresenta capítulo DOI10.1007/978-981-95-4109-6_25](https://link.springer.com/chapter/10.1007/978-981-95-4109-6_25),
online desde17/11/2025. Só a prévia estava acessível; seu resumo tem diferença
de redação. Não foi lido o corpo desse capítulo, nem demonstrada sua equivalência
à preprint. Sua obtenção legítima é uma rota documental aberta para essas células,
sem promessa de que conterá as respostas. Não se altera silenciosamente a versão
do corpus ou a referência da monografia. A abertura do PDF no endereço oficial
`https://link.springer.com/content/pdf/10.1007/978-981-95-4109-6_25.pdf`
também não foi atendida pela ferramenta web. A busca local por Sharma, identificador
arXiv e sufixo do DOI só localizou a preprint conhecida e as evidências desta pesquisa,
sem segunda cópia integral identificada do capítulo publicado.

### Hariharan — comparação quantitativa

O [arXiv 2512.08963](https://arxiv.org/abs/2512.08963) relaciona autores,
título e DOI da publicação EPJ Plus. No pacote de fonte, as tabelas de ações
(linhas392–410) e vento solar (466–482) confrontam Conventional ESN, AEESN,
DeepESN, BrESN e três topologias CESN. Essas variantes não se tornam LSTM/GRU
por conterem redes profundas. A declaração de dados (591) remete ao artigo.

O inventário completo do pacote inclui texto, bibliografia, classes e imagens,
sem script experimental identificado. Nenhuma nova comparação qualificadora foi
recuperada: P4 permanece ?. O fonte foi lido de modo dirigido, em complemento à
leitura anterior do PDF; não se declara nova leitura integral de todo o pacote
nem identidade byte a byte entre preprint e versão publicada.

### Deng — canal do autor

A [ficha oficial DTU](https://orbit.dtu.dk/en/publications/degradation-prediction-of-pemfcs-using-stacked-echo-state-network/)
identifica o manuscrito aceito e DOI10.1109/TTE.2021.3111906. O conteúdo público
do [site do autor, via GitHub](https://github.com/DZH001-energy/DZH001-energy.github.io/blob/main/assets/js/content.js),
foi obtido pelo conector e arquivado em `Deng_site_content.js.txt`. A entrada exata
do artigo vincula o DOI; não oferece código naquela entrada. Os URLs textuais do
arquivo foram inspecionados, sem executar JavaScript ou ler auxiliares alheios à
publicação. O ano2021 do perfil é distinguido do fascículo2022 da revista.

As passagens locais do método separam conexões aleatórias do reservatório e pesos
do autoencoder; nenhuma lei de Win/W foi comprovada por esses canais. P1 permanece ?.
Não localizar um código na ficha e na entrada do autor não prova que inexista em
todos os lugares. A busca web por DOI/código não trouxe um repositório vinculável.

## Alcance e próxima decisão documental

O arquivo `pendencias38_conferidas.json` concilia cada célula restante com a matriz
Word e o hash do PDF correspondente. É inventário, não declaração de nova leitura
de todas elas. Os registros de leituras anteriores continuam preservados.

Para avançar sem repetir leituras já registradas, as alternativas precisam fornecer
**informação específica não presente nas evidências atuais**: versão publicada
integral de Sharma; procedimento efetivo de pesos/ambiente de Kumar; tratamento
efetivo dos dados de Abebe; ou suplemento/código expressamente associado às demais
fontes. Artigos de outros autores e exemplos genéricos de bibliotecas não suprem
esses detalhes. Nenhum contato externo foi feito; rascunhos de perguntas existentes
na rodada3 permanecem apenas rascunhos.

## Verificação e preservação

`registrar_rodada.py` confere SHA256 da v010, localiza o quadro35×6 no OOXML,
concilia as170células e as38insuficiências e verifica os hashes dos PDFs vinculados.
Os arquivos novos têm hashes no manifesto. Nenhuma versão Word foi criada por
esta auditoria. Não houve treinamento, busca genética, testeDM, execução de código
de terceiros ou alteração nos resultados existentes. Não há renderização Word nova
porque não houve edição; as inspeções anteriores não foram reapresentadas como novas.
