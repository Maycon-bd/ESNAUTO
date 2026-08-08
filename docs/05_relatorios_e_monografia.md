# 📄 Componente 5: Relatórios e Documentos Acadêmicos

Este componente engloba a **documentação acadêmica e relatórios técnicos** produzidos ao longo do Trabalho de Conclusão de Curso (TCC). Inclui a monografia oficial, relatórios de reestruturação de código e relatórios de resultados experimentais formatados em Markdown e Word.

---

## 📂 Arquivos Integrantes do Componente

```
ESNAUTO/
├── reports/                             # Pasta central de relatórios acadêmicos
│   ├── Relatorio_Automacao_ESN.md       # Relatório técnico de arquitetura
│   ├── Relatorio_Automacao_ESN.docx     # Relatório técnico em MS Word
│   └── MayconGarciaSilva_monografia.docx# Monografia oficial do TCC
│
├── resultados_validacao_teste.md        # Relatório estatístico dos 12 cenários
└── resultados_validacao_teste2.md       # Cópia/Espelho de segurança dos resultados
```

---

## 📝 Detalhamento de Cada Arquivo

### 1. `reports/MayconGarciaSilva_monografia.docx`
- **Caminho**: [reports/MayconGarciaSilva_monografia.docx](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/reports/MayconGarciaSilva_monografia.docx)
- **Formato**: Documento Microsoft Word (`.docx`)
- **Função**: **Monografia Oficial de TCC** do aluno Maycon Garcia Silva.
- **Conteúdo**: Texto acadêmico completo estruturado em Introdução, Fundamentação Teórica (Echo State Networks e Algoritmos Genéticos), Metodologia (preparação de dados PETR4 2000-2020), Resultados e Discussões (análise dos 12 cenários) e Conclusão.

---

### 2. `reports/Relatorio_Automacao_ESN.md` e `Relatorio_Automacao_ESN.docx`
- **Caminho MD**: [reports/Relatorio_Automacao_ESN.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/reports/Relatorio_Automacao_ESN.md)
- **Caminho DOCX**: [reports/Relatorio_Automacao_ESN.docx](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/reports/Relatorio_Automacao_ESN.docx)
- **Função**: **Relatório Técnico de Arquitetura e Automação**.
- **Conteúdo**: Documenta formalmente a reestruturação física do workspace, a passagem de parâmetros via CLI para os scripts R e Python, e o funcionamento do pipeline de automação batch e do R Shiny Studio.

---

### 3. `resultados_validacao_teste.md`
- **Caminho**: [resultados_validacao_teste.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/resultados_validacao_teste.md)
- **Função**: **Relatório Consolidado de Resultados Experimentais**.
- **Conteúdo**: Apresenta a análise estatística comparativa detalhada dos 12 cenários de simulação (3 Rodadas × 4 Combinações de distribuições de pesos $W_{in}$ e $W$).

#### 📊 Principais Destaques Contidos no Relatório:
- **Tabela Comparativa Completa**: Apresenta MAE e RMSE nas partições de Validação e Teste para os 12 cenários.
- **🥇 Melhor no Teste (MAE)**: `Run 3 | Win Normal | W Normal` (MAE Teste: `0.327472`).
- **🥇 Melhor no Teste (RMSE)**: `Run 3 | Win Uniforme | W Uniforme` (RMSE Teste: `0.497529`).
- **🎯 Melhor na Validação**: `Run 2 | Win GED | W Uniforme` (MAE Validação: `0.262317`).
- **⚡ Melhor no GA**: `Run 2 | Win GED | W Normal` (Fitness: `-0.237537`).

---

### 4. `resultados_validacao_teste2.md`
- **Caminho**: [resultados_validacao_teste2.md](file:///g:/Outros%20computadores/Meu%20computador/TFC1/ESNAUTO/resultados_validacao_teste2.md)
- **Função**: **Cópia / Espelho de Backup**.
- **Conteúdo**: Mantém a réplica sincronizada do relatório de resultados para garantia de redundância no projeto.
