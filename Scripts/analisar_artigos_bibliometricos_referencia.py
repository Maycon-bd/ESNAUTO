"""Extrai páginas e identifica figuras dos dois artigos fornecidos pelo autor."""
from pathlib import Path
import json
import re
from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/bibliometria_reconstrucao/referencias_graficas"
OUT.mkdir(parents=True, exist_ok=True)
DOWNLOADS = Path("C:/Users/User/Downloads")
INPUTS = {"ENMC": "*XXV ENMC*publicado.pdf", "KBS": "*Knowledge Based Systems*Cardoso*publicado.pdf"}

for label, pattern in INPUTS.items():
    paths = list(DOWNLOADS.glob(pattern))
    if len(paths) != 1:
        raise RuntimeError(f"Arquivo ambíguo: {label}: {paths}")
    path = paths[0]
    reader = PdfReader(path)
    pages = [(p.extract_text() or "") for p in reader.pages]
    (OUT / f"{label}_texto.txt").write_text("\n\n".join(f"[PÁGINA PDF {i}]\n{t}" for i, t in enumerate(pages, 1)), encoding="utf-8")
    descriptions = []
    for i, text in enumerate(pages, 1):
        for match in re.finditer(r"(?:Fig(?:ure|ura)?\.?|Table|Tabela)\s*\d+\s*[.:–-]?", text, flags=re.I):
            descriptions.append({"pagina": i, "trecho": text[max(0,match.start()-50):match.start()+800]})
    (OUT / f"{label}_inventario.json").write_text(json.dumps({"arquivo": str(path), "paginas": len(pages), "figuras_e_tabelas": descriptions}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(label, len(pages), "páginas", "referências a figuras/tabelas", len(descriptions))
    preview = OUT / "previas"
    preview.mkdir(exist_ok=True)
    rendering = pdfium.PdfDocument(str(path))
    selected = (6, 7, 8) if label == "ENMC" else (6, 7)
    for page_no in selected:
        page = rendering[page_no-1]
        bitmap = page.render(scale=1.5)
        bitmap.to_pil().save(preview / f"{label}_pagina_{page_no}.png")
        bitmap.close()
        page.close()
    rendering.close()
