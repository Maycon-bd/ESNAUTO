# Apresentação e roteiro sincronizados com a v010

Base editorial conferida no registro antes da edição e antes da entrega: v010,
`reports/monografia/versoes/v010/MayconGarciaSilva_monografia_v010.docx`.
SHA256: `1da5ea82344c177d75af723362017e3e558bbb127bd9995f7ec0cbd6964f81ed`.

Os arquivos finais estão em `entrega`. A monografia e as apresentações anteriores
foram preservadas. Não foi criada nova versão editorial Word da monografia.

## Alterações

- Rodapés, notas e roteiro passam a identificar v010; as notas registram o hash
  da base examinada.
- Localizadores antigos Pnnnn foram substituídos por seções, elementos e páginas
  impressas da v010, conforme a paginação reconciliada em
  `reports/auditoria_formatacao_20261102/conferencia.json` e
  `reports/busca_lacunas_20261101/paginacao_candidata.json`.
- Corrigidas as fontes de consulta dos slides 9 e 14: a figura ilustrativa
  pertence à seção 4.2, com Figura 6 na página 57.
- Preservadas as falas das notas da apresentação visual. No roteiro, a expressão
  “A tabela mostra” foi sincronizada para “Os gráficos mostram” no slide 12.
  Esse era o único descompasso de fala com a versão visual já existente.
- Mantidos os resultados e os limites científicos, a separação entre histórico,
  rodada DM e lote ilustrativo, os 23 segmentos e os 1.500 segundos planejados.
  O tempo real de gravação depende de ensaio e ritmo de fala.

## Conferências

O PowerPoint abriu e renderizou os 23 slides. Foram reconhecidos 82 links de
navegação e 23 transições por clique, sem avanço por tempo. Os 10 gráficos
nativos, suas planilhas, relações, mídias e demais componentes foram preservados
byte a byte. A importação pelo Artifact Tool e os validadores de pacote,
geometria, fontes e gráficos passaram.

As imagens finais foram examinadas. Na comparação com as imagens da apresentação
anterior, a capa é idêntica e as únicas diferenças nos outros 22 slides ficam
nos caracteres da versão no rodapé; o restante é pixel a pixel idêntico.

O roteiro mantém 13 páginas. Todas foram renderizadas e abertas para inspeção;
sem cortes ou sobreposições observados. O conversor LibreOffice empacotado não
está disponível, e duas rotas de exportação PDF do Word não responderam. A
alternativa bem-sucedida foi obter as 13 páginas diretamente do Word por
`Page.EnhMetaFileBits`, rasterizá-las e alimentar o `render_docx.py` com um PDF
de QA dessas mesmas páginas atuais. Nenhum PDF de versão anterior foi reutilizado.
As instâncias de automação que travaram foram identificadas e encerradas;
a impressora padrão do usuário permaneceu inalterada.

As evidências, scripts, hashes e recibos ficam em `build`, especialmente
`rastreabilidade.json`, `validacao_final.json`, `conferencia_final.json` e
`entrega_verificada.json`. Esta atualização não executou experimentos nem
constitui nova validação científica integral.
