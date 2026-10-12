"""Bigrams de títulos com proveniência e contagem binária por documento."""
from collections import Counter
from pathlib import Path
import json
import re
import unicodedata
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/bibliometria_reconstrucao"
# Lista explícita: palavras de ligação são filtradas depois de formar pares
# adjacentes, para não criar ligações artificiais entre palavras distantes.
STOPWORDS = set("a an and are as at be been being by for from has have in into is it its of on or that the their these this to was were with without using through".split())


def main():
    base = json.loads((OUT / "base_reconstruida.json").read_text(encoding="utf-8"))
    records = []
    for r in base["records"]:
        title = r["title"]
        origin = r["origem_metadados"]
        if r["id"] == "D07":
            pdf = PdfReader(ROOT / "Artigos citados" / r["arquivo_pdf"])
            page = pdf.pages[1].extract_text() or ""
            text = re.sub(r"\s+", " ", page)
            title = "Application of machine learning algorithm to predict the behavior of stocks marketed in Brazil"
            assert title in text, "Título inglês de Costa e Lunkes não confirmado"
            origin = "Título inglês declarado no PDF, página 2; não é tradução produzida para a análise"
        cleaned = unicodedata.normalize("NFKC", title).lower()
        tokens = re.findall(r"[a-z]+", cleaned)
        pairs = {f"{a} {b}" for a, b in zip(tokens, tokens[1:])
                 if a not in STOPWORDS and b not in STOPWORDS}
        records.append({"id": r["id"], "titulo_original_base": r["title"],
                        "titulo_analisado": title, "origem_titulo": origin,
                        "tokens": tokens, "bigrams": sorted(pairs)})
    counts = Counter(pair for r in records for pair in r["bigrams"])
    freq = [{"expressao": pair, "documentos": counts[pair],
             "ids": [r["id"] for r in records if pair in r["bigrams"]]}
            for pair in sorted(counts, key=lambda p: (-counts[p], p))]
    assert len(records) == 34 and len({r["id"] for r in records}) == 34
    assert all(len(x["ids"]) == x["documentos"] for x in freq)
    result = {"n_documentos": len(records), "unidade": "Presença de par de palavras por documento",
              "minimo_grafico": 2, "stemming": False, "expansao_acronimos": False,
              "stopwords": sorted(STOPWORDS), "records": records, "frequencias": freq}
    (OUT / "expressoes_titulos.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"documentos": len(records), "recorrentes": [x for x in freq if x["documentos"] >= 2]}, ensure_ascii=True))


if __name__ == "__main__":
    main()
