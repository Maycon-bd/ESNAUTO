"""Extrai texto OOXML e registra a identidade das fontes sem alterar originais.

Não julga validade científica nem layout. Sem rede, R, Word ou treino de modelos.
--check confere o snapshot existente sem escrever; o modo padrão o atualiza.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs/assistencia_monografia/fontes.json"
OUTPUT = ROOT / "reports/assistencia_monografia"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def local_path(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f"Caminho fora do projeto: {relative}")
    return path


def snapshot():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    rows = []
    ids = set()
    for item in catalog["fontes"]:
        if item["id"] in ids:
            raise ValueError(f"ID duplicado: {item['id']}")
        ids.add(item["id"])
        path = local_path(item["path"])
        row = dict(item)
        row["exists"] = path.is_dir() if item["tipo"] == "directory" else path.is_file()
        if row["exists"]:
            if item["tipo"] == "file":
                row.update(sha256=digest(path), bytes=path.stat().st_size)
            else:
                row["pdfs"] = [
                    {"path": p.relative_to(ROOT).as_posix(), "sha256": digest(p)}
                    for p in sorted(path.glob("*.pdf"))
                ]
        rows.append(row)
    base = next(r for r in rows if r["id"] == catalog["base_editorial_id"])
    if not base["exists"]:
        raise ValueError("Base editorial ausente")
    with ZipFile(local_path(base["path"])) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        paragraphs = []
        for index, node in enumerate(document.findall(".//w:p", NS), 1):
            text = "".join(t.text or "" for t in node.findall(".//w:t", NS))
            paragraphs.append({"id": f"P{index:04d}", "text": text})
        base["paragraphs_including_tables"] = len(paragraphs)
        base["has_comments_part"] = "word/comments.xml" in archive.namelist()
    result = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "catalog_sha256": digest(CATALOG),
        "base_editorial_id": catalog["base_editorial_id"],
        "sources": rows,
        "scope": "Identidade e extração textual; não valida ciência, fontes citadas ou layout",
    }
    return result, paragraphs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    current, paragraphs = snapshot()
    missing = [r["path"] for r in current["sources"] if not r["exists"]]
    if missing:
        print("Fontes catalogadas ausentes:\n" + "\n".join(missing))
        return 1
    manifest = OUTPUT / "snapshot_fontes.json"
    if args.check:
        if not manifest.is_file():
            print("Snapshot ausente; execute primeiro sem --check.")
            return 1
        previous = json.loads(manifest.read_text(encoding="utf-8"))
        # generated_utc muda a cada chamada; não participa da comparação.
        current.pop("generated_utc")
        previous.pop("generated_utc", None)
        if current != previous:
            print("Fontes ou catálogo mudaram. Reavalie a auditoria antes de renovar o snapshot.")
            return 1
        expected = "\n".join(f"{p['id']}: {p['text']}" for p in paragraphs) + "\n"
        text_path = OUTPUT / "monografia_base_texto.txt"
        if not text_path.is_file() or text_path.read_text(encoding="utf-8") != expected:
            print("Extração textual ausente ou divergente.")
            return 1
        print(f"OK: {len(current['sources'])} fontes; base e extração preservadas.")
        return 0
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUTPUT / "monografia_base_texto.txt").write_text(
        "\n".join(f"{p['id']}: {p['text']}" for p in paragraphs) + "\n", encoding="utf-8"
    )
    print(f"Snapshot: {manifest.relative_to(ROOT)}")
    print(f"Texto: {len(paragraphs)} parágrafos, incluindo células e vazios.")
    print("Os identificadores Pxxxx só valem para o hash registrado da base editorial.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
