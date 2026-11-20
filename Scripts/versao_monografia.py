"""Controle local de versões editoriais; usa somente a biblioteca padrão Python."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sys
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REGISTRO = ROOT / 'docs/assistencia_monografia/versao_vigente.json'
ARQUIVO = ROOT / 'reports/monografia/versoes'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def relativo(path):
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def local(path):
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        raise ValueError('O caminho registrado precisa permanecer dentro do projeto.')
    return resolved


def ler():
    if not REGISTRO.exists():
        raise ValueError('Registro não inicializado. Use iniciar uma única vez.')
    return json.loads(REGISTRO.read_text(encoding='utf-8'))


def vigente(registro):
    return next(v for v in registro['versoes'] if v['id'] == registro['vigente'])


def conferir(versao):
    path = local(versao['arquivo'])
    if sha(path.read_bytes()) != versao['sha256']:
        raise ValueError(f"Conteúdo alterado fora do controle: {versao['id']} ({path}). "
                         'Preserve a cópia alterada e recupere o snapshot original antes de continuar; '
                         'não atualize o hash para esconder a alteração.')
    return path


@contextmanager
def exclusao():
    lock = REGISTRO.with_suffix('.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = lock.open('x', encoding='utf-8')
    except FileExistsError:
        raise ValueError(f'Outro registro está em andamento ou foi interrompido: {lock}. '
                         'Confira o processo antes de remover um bloqueio abandonado.') from None
    try:
        with handle:
            handle.write(datetime.now(timezone.utc).isoformat())
        yield
    finally:
        lock.unlink()


def salvar(registro):
    tmp = REGISTRO.with_name(REGISTRO.name + '.' + uuid.uuid4().hex + '.tmp')
    with tmp.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)
        f.write('\n')
        f.flush()
    tmp.replace(REGISTRO)


def validar_docx(path):
    if path.suffix.lower() != '.docx':
        raise ValueError('É necessário fornecer um arquivo .docx.')
    data = path.read_bytes()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        if not {'[Content_Types].xml', 'word/document.xml'}.issubset(z.namelist()):
            raise ValueError('O arquivo não contém a estrutura DOCX esperada.')
        if z.testzip():
            raise ValueError('O arquivo DOCX está corrompido.')
    return data


def publicar(args, inicial=False):
    source = Path(args.arquivo).resolve()
    data = validar_docx(source)
    with exclusao():
        if inicial:
            if REGISTRO.exists():
                raise ValueError('O registro já existe; iniciar não pode sobrescrevê-lo.')
            registro = {'schema_version': 1, 'vigente': None, 'versoes': []}
            parent = None
        else:
            registro = ler()
            parent = vigente(registro)
            conferir(parent)
            if args.base != parent['id']:
                raise ValueError(f"Base desatualizada: foi informada {args.base}; "
                                 f"a vigente é {parent['id']}. Compare e incorpore as alterações "
                                 'posteriores antes de registrar. Não há mesclagem automática de Word.')
            if sha(data) == parent['sha256']:
                raise ValueError('O Word é idêntico ao vigente. Auditoria sem edição não cria versão.')
        evidencias = []
        for item in args.evidencia:
            p = local(item)
            evidencias.append({'arquivo': relativo(p), 'sha256': sha(p.read_bytes())})
        version = f"v{len(registro['versoes']) + 1:03d}"
        folder = ARQUIVO / version
        folder.mkdir(parents=True, exist_ok=False)
        target = folder / f'MayconGarciaSilva_monografia_{version}.docx'
        with target.open('xb') as f:
            f.write(data)
        entry = {
            'id': version,
            'anterior': parent['id'] if parent else None,
            'arquivo': relativo(target),
            'sha256': sha(data),
            'registrada_em_utc': datetime.now(timezone.utc).isoformat(),
            'origem_importada': str(source),
            'responsavel': args.responsavel,
            'resumo': args.resumo,
            'estado_editorial': args.estado,
            'validacao_declarada': args.validacao,
            'evidencias': evidencias,
            'pendencias': args.pendencia if inicial or args.pendencia else list(parent['pendencias']),
        }
        registro['versoes'].append(entry)
        registro['vigente'] = version
        salvar(registro)
        print(json.dumps({'id': version, 'arquivo': str(target), 'sha256': entry['sha256']},
                         ensure_ascii=False, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='comando', required=True)
    current = subs.add_parser('atual', help='Confere hash e mostra a versão vigente.')
    current.add_argument('--json', action='store_true')
    subs.add_parser('historico', help='Mostra a cadeia de versões registradas.')
    check = subs.add_parser('verificar', help='Confere snapshots registrados.')
    check.add_argument('--todos', action='store_true')
    work = subs.add_parser('preparar', help='Cria uma cópia de trabalho sem sobrescrever arquivo.')
    work.add_argument('--destino', required=True)
    for command in ['iniciar', 'registrar']:
        sub = subs.add_parser(command)
        sub.add_argument('--arquivo', required=True)
        if command == 'registrar':
            sub.add_argument('--base', required=True)
        sub.add_argument('--resumo', required=True)
        sub.add_argument('--responsavel', required=True)
        sub.add_argument('--estado', choices=['em_revisao', 'conferida'], default='em_revisao')
        sub.add_argument('--validacao', required=True,
                         help='Descreva o que foi e o que não foi verificado; não é certificação.')
        sub.add_argument('--evidencia', action='append', default=[])
        sub.add_argument('--pendencia', action='append', default=[],
                         help='No registro seguinte, se omitida, herda as pendências. '
                              'Se fornecida, substitui a lista; justifique resoluções no resumo.')
    args = parser.parse_args(argv)
    if args.comando in ['iniciar', 'registrar']:
        publicar(args, inicial=args.comando == 'iniciar')
        return
    registro = ler()
    version = vigente(registro)
    if args.comando == 'historico':
        for item in registro['versoes']:
            print(f"{item['id']} <- {item['anterior'] or 'importação'} | "
                  f"{item['estado_editorial']} | {item['resumo']}")
    elif args.comando == 'verificar':
        items = registro['versoes'] if args.todos else [version]
        for item in items:
            conferir(item)
            print(item['id'] + ': SHA256 confere')
    elif args.comando == 'atual':
        path = conferir(version)
        result = dict(version, caminho_absoluto=str(path))
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Vigente: {version['id']} ({version['estado_editorial']})\n{path}\n"
                  f"SHA256: {version['sha256']}\nValidação: {version['validacao_declarada']}")
            for p in version['pendencias']:
                print('Pendente: ' + p)
    elif args.comando == 'preparar':
        data = conferir(version).read_bytes()
        dest = local(args.destino)
        if dest.is_relative_to(ARQUIVO.resolve()) or dest.suffix.lower() != '.docx':
            raise ValueError('A cópia de trabalho deve ser .docx e ficar fora de versoes/.')
        sidecar = dest.with_suffix(dest.suffix + '.origem.json')
        if dest.exists() or sidecar.exists():
            raise ValueError('Destino ou registro de origem já existe; use um nome novo.')
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as f:
            f.write(data)
        with sidecar.open('x', encoding='utf-8') as f:
            json.dump({'base': version['id'], 'sha256_origem': version['sha256'],
                       'arquivo_origem': version['arquivo']}, f, ensure_ascii=False, indent=2)
        print(f"Cópia: {dest}\nBase para registrar: {version['id']}\nOrigem: {sidecar}")


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, StopIteration, zipfile.BadZipFile) as exc:
        print('ERRO: ' + str(exc), file=sys.stderr)
        sys.exit(1)
