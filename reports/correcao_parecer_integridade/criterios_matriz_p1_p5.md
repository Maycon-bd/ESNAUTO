# Critérios da recodificação P1–P5

Esta recodificação substitui a interpretação binária da matriz da v001. Mantém os
cinco temas, mas explicita os objetos e distingue evidência direta e secundária.
Não transforma o corpus recuperado em amostra representativa de toda a literatura.

| Dimensão | Informação exigida |
|---|---|
| P1 | Distribuição probabilística explicitamente ligada à geração dos elementos de Win ou W de um modelo ESN/RC. Registrar qual matriz, escala e eventual transformação. Uma sequência caótica é uma regra de geração, não automaticamente uma distribuição probabilística identificada. |
| P2 | Procedimento para escolher hiperparâmetros de ESN/RC: busca, otimização, sensibilidade com critério de seleção ou seleção manual explicitada. Listar valores fixos ou treinar Wout não basta. Ajustar outra arquitetura não satisfaz P2. |
| P3 | Operação concreta de preparação de séries temporais: retornos, diferenças, normalização, limpeza, imputação, ajuste corporativo ou construção de atributos/janelas. A partição treino/teste isoladamente não basta. Séries não financeiras são admissíveis, com domínio identificado. Ajustar distribuição IID não equivale a preparar uma série temporal. |
| P4 | Comparação quantitativa de previsão envolvendo LSTM, GRU ou Transformer. Mera menção, ilustração de arquitetura, lista bibliográfica ou comparação só entre variantes ESN não basta. Transformer não é chamado de arquitetura recorrente. |
| P5 | Mercado e ativo/índice financeiro identificados e vinculados à análise. A expressão genérica 'mercado financeiro' não basta. Séries simuladas associadas a preços financeiros não equivalem a previsão de preços observados. |

## Estados de cada célula

- **D**: evidência direta localizada no método, análise de dados ou experimento da
  própria fonte. Não implica reprodução independente nem aprovação da qualidade.
- **S**: discussão substantiva secundária ou comparação numérica importada de
  outro estudo. A evidência deve ser explicitada, sem contá-la como novo experimento.
- **?**: a passagem consultada não permite fechar o critério. Inclui informação
  insuficiente, objeto ambíguo e ausência de uma passagem qualificadora no escopo
  lido. Não significa que o conteúdo inexista na obra ou na literatura.
- **—**: não se aplica ao objeto efetivamente estudado. Justificar pela descrição
  do método/objeto, e não por busca automática de palavras.
- **PENDENTE**: célula ainda não recodificada. É estado de trabalho e não deve ser
  apresentado no quadro final como resultado da leitura.

Em estudos de revisão ou teóricos, passagens conceituais recebem S quando atendem
substantivamente ao critério. Um exemplo executado pela própria fonte pode receber D.
Em P4, a comparação inteiramente importada recebe S mesmo em artigo experimental.
Em P5, a associação explícita entre condições iniciais simuladas e um ativo recebe S,
sem ser contada como previsão direta de uma série financeira observada. Incluem-se
modelos RC físicos relacionados à ESN, identificando o tipo de reservatório; seus
ganhos físicos não são automaticamente leis probabilísticas de pesos de uma ESN.

A identificação de famílias probabilísticas em uma ESN sem individualização da
matriz é registrada como informação pertinente, mas não prova a lei de Win.
Distribuições de amostragem de hiperparâmetros e ruído de observação permanecem
separadas das distribuições dos pesos. Conteúdo de figuras reproduzidas de outras
fontes não é convertido em procedimento executado pelos autores do artigo.

## Evidência e fechamento

Cada célula registra fonte, hash do PDF, página física/seção, síntese da passagem,
escopo da leitura e limite. Os estados são decisões de leitura humana documentada;
o script apenas monta arquivos e confere consistência, sem inferir códigos por palavras.

Só recalcular a Tabela 1, o Quadro 1, a Figura 1 e as conclusões dependentes depois
da recodificação de todas as 170 células. Apresentar D e S separadamente e conservar
? e — na legenda. Frequências contam documentação localizada segundo estes critérios,
não prevalência dos métodos no universo científico. Não usar ? como prova de lacuna.
