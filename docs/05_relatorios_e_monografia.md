# 📄 Componente 5: Relatórios e Documentos Acadêmicos

Este componente engloba a **documentação acadêmica e relatórios técnicos** produzidos ao longo do Trabalho de Conclusão de Curso (TCC). Inclui a monografia oficial, a seção metodológica pronta para o artigo, relatórios de reestruturação de código e relatórios de resultados experimentais formatados em Markdown e Word.

---

## 📂 Arquivos Integrantes do Componente

```
ESNAUTO/
├── docs/
│   └── 06_secao_artigo_tfc_otimizacao_ga.md # Texto acadêmico pronto para inclusão no TFC/Artigo
│
├── reports/                                 # Pasta central de relatórios acadêmicos
│   ├── Relatorio_Automacao_ESN.md           # Relatório técnico de arquitetura
│   ├── Relatorio_Automacao_ESN.docx         # Relatório técnico em MS Word
│   └── MayconGarciaSilva_monografia.docx    # Monografia oficial do TCC
│
├── resultados_validacao_teste.md            # Relatório estatístico dos 12 cenários
└── resultados_validacao_teste2.md           # Cópia/Espelho de segurança dos resultados
```

---

## 📝 Detalhamento de Cada Arquivo

### 1. `docs/06_secao_artigo_tfc_otimizacao_ga.md` ⭐ (NOVO - Seção Pronta para o Artigo)
- **Caminho**: [`docs/06_secao_artigo_tfc_otimizacao_ga.md`](06_secao_artigo_tfc_otimizacao_ga.md)
- **Função**: **Texto formal e equações matemáticas prontas para colar no Artigo/Monografia**.
- **Conteúdo**:
  - Formulação matemática do cromossomo de 59 bits ($a$, $sr$, $initLen$, $tam\_reservoir$, $reg$).
  - Justificativa e equações da **Amostragem por Hipercubo Latino (LHS)**.
  - Formulação do **Mecanismo Anti-Estagnação por Cataclismo (CHC Adaptativo)** para escapar de mínimos locais e buscar o mínimo global.
  - Função de Aptidão Ponderada (40% Treino / 60% Validação).
  - Tabela comparativa oficial de resultados no Teste Cego (*Out-of-Sample*): ESN vs LSTM vs GRU.
  - Análise de Custo-Benefício Computacional e referências em formato ABNT/IEEE (Jaeger, Eshelman, Goldberg, McKay, Hochreiter, Cho).

---

### 2. `reports/MayconGarciaSilva_monografia.docx`
- **Caminho**: [`reports/MayconGarciaSilva_monografia.docx`](../reports/MayconGarciaSilva_monografia.docx)
- **Formato**: Documento Microsoft Word (`.docx`)
- **Função**: **Monografia Oficial de TCC** do aluno Maycon Garcia Silva.

---

### 3. `reports/Relatorio_Automacao_ESN.md` e `Relatorio_Automacao_ESN.docx`
- **Caminho MD**: [`reports/Relatorio_Automacao_ESN.md`](../reports/Relatorio_Automacao_ESN.md)
- **Caminho DOCX**: [`reports/Relatorio_Automacao_ESN.docx`](../reports/Relatorio_Automacao_ESN.docx)
- **Função**: **Relatório Técnico de Arquitetura e Automação**.

---

### 4. `resultados_validacao_teste.md`
- **Caminho**: [`resultados_validacao_teste.md`](../resultados_validacao_teste.md)
- **Função**: **Relatório Consolidado de Resultados Experimentais** dos 12 cenários de simulação batch.
