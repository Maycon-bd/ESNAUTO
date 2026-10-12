"""Inventário local de evidências para reconstrução bibliográfica.

DOIs encontrados são candidatos, pois um PDF também pode citar DOIs alheios.
Não atribui autores, anos ou citações ausentes e não simula exportação Scopus.
"""
from pathlib import Path
import hashlib
import json
import re

from pypdf import PdfReader


def main():
    root = Path(__file__).resolve().parents[1]
    folder = root / "Artigos citados"
    output = root / "reports" / "bibliometria_reconstrucao"
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for path in sorted(folder.glob("*.pdf")):
        record = {"arquivo": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        try:
            pdf = PdfReader(path)
            texts = [(page.extract_text() or "") for page in pdf.pages[:4]]
            text = "\n".join(texts)
            metadata = pdf.metadata or {}
            candidates = {}
            for page_no, content in enumerate(texts, start=1):
                for match in re.finditer(r"10\.\d{4,9}/[^\s<>\"]+", content, flags=re.I):
                    doi = match.group().rstrip(".,;]")
                    candidates.setdefault(doi, {"doi_candidato": doi, "pagina": page_no,
                        "contexto": content[max(0, match.start()-100):match.end()+100]})
            markers = []
            for match in re.finditer(r"\b(?:key\s*words?|index\s+terms|palavras[-\s]chave)\b", text, flags=re.I):
                markers.append(text[match.start():match.start()+550])
            record.update({"paginas": len(pdf.pages), "caracteres_primeiras_paginas": len(text),
                "titulo_embutido_nao_validado": str(metadata.get("/Title", "")),
                "autor_embutido_nao_validado": str(metadata.get("/Author", "")),
                "dois_candidatos": list(candidates.values()),
                "trechos_marcadores_palavras_chave": markers[:3],
                "texto_inicial_para_conferencia": text[:1500],
                "status": "Extração inicial; identificação e metadados ainda precisam de validação"})
        except Exception as exc:
            record["erro"] = str(exc)
        records.append(record)
    summary = {"pdfs": len(records), "com_texto_extraido": sum(r.get("caracteres_primeiras_paginas", 0) > 200 for r in records),
               "com_candidato_doi": sum(bool(r.get("dois_candidatos")) for r in records),
               "com_marcador_keywords": sum(bool(r.get("trechos_marcadores_palavras_chave")) for r in records),
               "erros": sum("erro" in r for r in records)}
    data = {"origem": "PDFs locais de Artigos citados; primeiras quatro páginas",
            "resumo": summary, "registros": records}
    (output / "inventario_pdfs.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == "__main__":
    main()
