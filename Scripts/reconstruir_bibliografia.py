"""Reconstrói registros locais, com enriquecimento Crossref e rastreabilidade."""
from pathlib import Path
import argparse
import datetime
import difflib
import hashlib
import html
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request

from docx import Document
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/bibliometria_reconstrucao"
# Relação conferida entre os PDFs, a referência original e as palavras-chave declaradas.
SEEDS = [
 (516, "Asymmetric generalized", "AR algorithms; asymmetric generalized error distribution; generalized error distribution; maximum likelihood estimation; probability; statistics; symmetric distribution"),
 (517, "Comparing MAE", "Stock price forecasting; Financial Time Series; ESN"),
 (518, "A Comprehensive Survey", ""),
 (520, "BovDB:", "B3; Data set; Stocks; Time series"),
 (521, "Quantum Temporal", ""),
 (523, "Same Error", ""),
 (524, "Aplicação de algoritmo", "machine learning; portfolio selection; technical analysis; fundamental analysis"),
 (525, "Degradation prediction", "Proton exchange membrane fuel cells; prognostics prediction; stacked echo state network; genetic algorithm; projection-encoding"),
 (527, "On Financial", "time series; regression; distribution; volatility; goodness-of-fit"),
 (529, "Modelling Financial Returns", "daily financial returns; excess kurtosis; skewness; finite mixtures of GED"),
 (528, "Modelling Financial Returns", ""),
 (530, "Training Multilayer", "stock market; machine learning; multilayer perceptron; financial data; artificial intelligence; artificial neural networks; online trading; big data; social science data; evolutionary algorithms; optimization"),
 (532, "Multivariate time", ""),
 (533, "FPGA-Accelerated", "reservoir computing; echo state network; recurrent neural network; chaotic systems; hardware accelerator; field programmable gate array"),
 (537, "Echo state network", ""),
 (538, "Forecasting Crude", "Crude oil prices; Time series analysis; Reservoir computing; Financial market prediction; Forecasting"),
 (541, "Enhancing Trading", "S&P 500; sentiment analysis; large language model; time-series forecasting; trading"),
 (540, "Forecasting stock", ""),
 (543, "Explorations in", ""),
 (544, "Conditional Heteroskedasticity", ""),
 (546, "Forecasting Financial", ""),
 (548, "Minimizing Chaos", "neural network; deep learning; Lorenz system; echo state network; reservoir computing; prediction"),
 (549, "Echo State Networks", "chaotic time series; cryptocurrency forecasting; echo state networks; lyapunov exponent"),
 (550, "Echo State Network Optimization", "Echo State Network; methods; Optimization; parameters; Reservoir Computing; SLR"),
 (551, "Comparison of LSTM", "LSTM; GRU; gold prices; forecasting; recurrent neural networks; performance evaluation"),
 (552, "Stock Price Forecasting", "Stock data forecast; echo state network; deep learning"),
 (553, "Stocks price prediction", "Stocks price; Sparrow search algorithm; Echo state network"),
 (554, "Approach Based", "Stock Exchange Prediction; Autoregressive Models & Linear Models"),
 (547, "Novel hybrid", "Volatility prediction; Echo state network; Heterogeneous autoregressive model; Particle swarm optimization"),
 (555, "Artificial intelligence", "artificial intelligence (AI); autoregressive integrated moving average artificial neural network (ARIMA-ANN) (time-series forecasting); generative adversarial network (GAN); K-means long short-term memory (LSTM); stock senti wordnet (SSWN); hybrid quantum neural network (HQNN); spectral GPT"),
 (556, "Enhanced Multistep", "Optical reservoir computing; Parallel data processing; Multivariate forecasting; Multistep prediction"),
 (557, "Stock market index", "Financial market prediction; Stock market index prediction; Financial time series; Reservoir computing; Deep learning"),
 (558, "Comparative Analysis", "Artificial intelligence; stock forecasting; LSTM; GRU Model; Transformer; Tesla"),
 (559, "Application of ESN", "Compressed sensing; ESN; Reserve pool; Time series"),
]
ALIASES = {"esn": "echo state network", "echo state networks": "echo state network",
 "recurrent neural networks": "recurrent neural network", "gru model": "gru",
 "stock data forecast": "stock price forecasting", "stock forecasting": "stock price forecasting"}


def clean(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", html.unescape(s))).strip()


def normalized_title(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())


def request_metadata(doi, title, cache):
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    if not doi:
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.title": title, "rows": 3})
    else:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ESNAUTO-Bibliografia/1.0 (academic metadata reconstruction)"})
        with urllib.request.urlopen(req, timeout=40) as response:
            data = json.load(response)
        payload = {"url": url, "data_recuperacao": datetime.date.today().isoformat(), "resposta": data}
        cache.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload
    except Exception as exc:
        return {"url": url, "erro": str(exc)}


def bibescape(s):
    return clean(str(s)).replace("\\", " ").replace("{", "(").replace("}", ")").replace("%", r"\%").replace("&", r"\&")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("documento", type=Path)
    parser.add_argument("--online", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True, parents=True)
    cache_dir = OUT / "crossref_bruto"
    cache_dir.mkdir(exist_ok=True)
    doc = Document(args.documento)
    inventory = json.loads((OUT / "inventario_pdfs.json").read_text(encoding="utf-8"))["registros"]
    assert len(inventory) == len(SEEDS) == 34
    results = []
    for i, (pdf, (paragraph, prefix, keywords)) in enumerate(zip(inventory, SEEDS), start=1):
        ref = doc.paragraphs[paragraph].text
        assert prefix.casefold() in ref.casefold(), (i, ref)
        start = ref.casefold().index(prefix.casefold())
        tail = ref[start:]
        title, _, remainder = tail.partition(". ")
        authors = [clean(x).rstrip(".") for x in ref[:start].strip().rstrip(".").split(";")]
        year_match = re.search(r"\b(19\d{2}|20\d{2})[ab]?\b", remainder)
        assert year_match, ref
        year = int(year_match.group(1))
        original_year = year
        doi_match = re.search(r"DOI:\s*(10\.\S+)", ref, flags=re.I)
        doi = doi_match.group(1).rstrip(".") if doi_match else ""
        source = remainder.split(", v.")[0].split(", 202")[0]
        doc_type = "article"
        notes = []
        if i in (2, 10, 33): doc_type = "inproceedings"
        if i in (11, 19): doc_type = "phdthesis" if i == 11 else "mastersthesis"
        if i in (5, 6, 17, 23, 24): doc_type = "misc"
        if i == 5:
            year = 2026
            source = "arXiv:2512.06630v2"
            notes.append("DOI de exemplo no template IEEE do PDF foi rejeitado.")
            notes.append("Rodapé do PDF: arXiv:2512.06630v2, 13 Feb 2026; a monografia informa 2025.")
        if i == 6:
            year, source = 2026, "arXiv:2603.02620v1"
            notes.append("Rodapé do PDF: arXiv:2603.02620v1, 3 Mar 2026; a monografia informa 2025.")
        if i == 10: source = "51st Scientific Meeting of the Italian Statistical Society (SIS 2022)"
        if i == 11: source = "Università degli Studi G. d'Annunzio Chieti-Pescara"
        if i == 19: source = "University of Groningen"
        if i == 17: source = "arXiv:2507.09739v1"
        if i == 23: source = "arXiv:2508.05416; preprint"
        if i == 24:
            year, doi, source = 2022, "10.21203/rs.3.rs-1909702/v1", "Research Square; preprint v1"
            notes.append("PDF v1 de 2022; a monografia cita publicação de 2023. Análise usa a versão disponível.")
        if i == 10: notes.append("Ano 2022 conforme referência e edição SIS 2022; a Tabela 2 informa 2023b.")
        if i == 11: notes.append("Tese de doutorado, e não artigo.")
        if i == 19: notes.append("Dissertação de mestrado, e não artigo.")
        if i == 20: notes.append("Metadados locais apoiados na referência do DOCX; PDF inicial requer OCR.")
        if year < 2021: notes.append("Referência anterior ao recorte; mantida como fonte complementar para análise do conjunto.")
        record = {"id": f"D{i:02d}", "arquivo_pdf": pdf["arquivo"], "sha256_pdf": pdf["sha256"],
            "referencia_original": ref, "paragrafo_docx": paragraph,
            "title": title, "authors": authors, "year": year, "ano_referencia_monografia": original_year, "doi": doi,
            "source": source, "type": doc_type, "abstract": "", "notes": notes,
            "keywords_originais": keywords.split("; ") if keywords else [],
            "keywords_normalizadas": sorted(set(ALIASES.get(clean(k).lower(), clean(k).lower()) for k in keywords.split("; "))) if keywords else [],
            "origem_keywords": "Transcrição conferida dos trechos Keywords/Index Terms do PDF" if keywords else "Ausente nas páginas iniciais inspecionadas; não inferido",
            "origem_metadados": "Referência do DOCX e conferência das páginas iniciais do PDF",
            "grupo_temporal": "2021–2026" if year >= 2021 else "Referências anteriores ao recorte",
            "identificacao_status": "Conferência local; enriquecimento externo pendente"}
        # Palavras-chave nunca são substituídas por assuntos/tags do índice externo.
        cache = cache_dir / f"{record['id']}.json"
        if args.online or cache.exists():
            payload = request_metadata(doi, title, cache)
            if "resposta" in payload:
                message = payload["resposta"]["message"]
                candidates = message.get("items", []) if "items" in message else [message]
                candidates.sort(key=lambda m: difflib.SequenceMatcher(None, normalized_title(title), normalized_title(m.get("title", [""])[0])).ratio(), reverse=True)
                match = candidates[0] if candidates else {}
                ext_title = match.get("title", [""])[0]
                similarity = difflib.SequenceMatcher(None, normalized_title(title), normalized_title(ext_title)).ratio()
                record["crossref"] = {"consulta": payload["url"], "data": payload["data_recuperacao"], "similaridade_titulo": round(similarity, 4), "cache": str(cache.relative_to(ROOT))}
                ext_authors = [clean(a.get("family", "") + ", " + a.get("given", "")) for a in match.get("author", []) if a.get("family")]
                surname = normalized_title(authors[0].split(",")[0])
                author_agrees = any(surname in normalized_title(a) for a in ext_authors)
                if similarity >= 0.94 and author_agrees:
                    record["identificacao_status"] = "Título e primeiro autor reconciliados com Crossref"
                    record["title"] = clean(ext_title)
                    record["authors"] = ext_authors
                    if doc_type == "misc" and not doi:
                        record["doi_versao_relacionada_crossref"] = match.get("DOI", "")
                        record["notes"].append("Registro Crossref relacionado não foi usado como DOI da versão preprint local.")
                    else:
                        record["doi"] = match.get("DOI", doi)
                    if match.get("container-title") and doc_type not in ("misc", "phdthesis", "mastersthesis"):
                        record["source"] = clean(match["container-title"][0])
                    if doc_type != "misc" or doi:
                        record["abstract"] = clean(re.sub(r"<[^>]*>", " ", match.get("abstract", "")))
                    parts = match.get("published", {}).get("date-parts", [[]])[0]
                    record["ano_crossref"] = parts[0] if parts else None
                    if record["ano_crossref"] and record["ano_crossref"] != year:
                        record["notes"].append(f"Ano Crossref {record['ano_crossref']} difere de {year}; ano local preservado para a versão do PDF.")
                    record["origem_metadados"] += "; título/autores/DOI conferidos em Crossref"
                else:
                    record["notes"].append("Resultado Crossref não aceito automaticamente: título ou autoria não reconciliados.")
            else:
                record["erro_consulta"] = payload.get("erro", "")
            if args.online: time.sleep(0.15)
        results.append(record)
        print(record["id"], record["identificacao_status"], flush=True)
    data = {"origem": "Reconstrução a partir dos PDFs e da monografia, com conferência Crossref quando disponível",
        "n": len(results), "n_com_keywords": sum(bool(r["keywords_originais"]) for r in results),
        "dicionario_normalizacao": ALIASES, "documento_sha256": hashlib.sha256(args.documento.read_bytes()).hexdigest(), "records": results}
    (OUT / "base_reconstruida.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    bib = []
    for r in results:
        fields = {"author": " and ".join(r["authors"]), "title": r["title"], "year": r["year"],
            "journal" if r["type"] == "article" else "booktitle" if r["type"] == "inproceedings" else "school" if "thesis" in r["type"] else "howpublished": r["source"],
            "doi": r["doi"], "url": "https://doi.org/" + r["doi"] if r["doi"] else "",
            "author_keywords": "; ".join(r["keywords_normalizadas"]), "abstract": r["abstract"],
            "annote": "Base reconstruída de PDFs locais; metadados com cobertura parcial. " + " ".join(r["notes"])}
        lines = [f"@{r['type']}{{{r['id']},"] + [f"{k}={{{bibescape(v)}}}," for k, v in fields.items() if v != ""] + ["}"]
        bib.append("\n".join(lines))
    (OUT / "artigos_reconstruidos.bib").write_text("\n\n".join(bib) + "\n", encoding="utf-8")
    print(f"Base reconstruída: {len(results)} registros; {data['n_com_keywords']} com palavras-chave declaradas.")


if __name__ == "__main__":
    main()
