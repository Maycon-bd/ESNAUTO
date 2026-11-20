# Edição do vídeo da apresentação

## Gravação editada

Versão atual com cinco alertas do Windows tratados:
`exportados/ESNAUTO_apresentacao_v005.mp4` (**24min36s**).
Legendas opcionais: `exportados/ESNAUTO_apresentacao_v005.srt`.
Imagem e legendas idênticas às da v004. Detalhes em
`exportados/ESNAUTO_apresentacao_v005_edicao.md`.

Versão anterior com o rodapé de fonte coberto pela cor do fundo:
`exportados/ESNAUTO_apresentacao_v004.mp4` (**24min36s**).
Legendas opcionais: `exportados/ESNAUTO_apresentacao_v004.srt`.
Áudio e texto das legendas idênticos aos da v003.

Versão anterior com refinamento de hesitações, orientações na demonstração e legendas
opcionais: `exportados/ESNAUTO_apresentacao_v003.mp4` (**24min36s**).
Legendas: `exportados/ESNAUTO_apresentacao_v003.srt`. Ative ou desative a faixa
em português no player; o SRT também pode ser carregado separadamente.
Detalhes: `exportados/ESNAUTO_apresentacao_v003_edicao.md`.

Versão com correção de voz distante em 10:31–13:06:
`exportados/ESNAUTO_apresentacao_25min_v002_audio_corrigido.mp4`.

Primeira edição preservada: `exportados/ESNAUTO_apresentacao_25min_v001.mp4`.
Duração conferida: **24min50,233s**, com áudio ajustado e slides preservados.
O registro das alterações está em `exportados/ESNAUTO_apresentacao_25min_v001_edicao.md`.

## Ferramentas

Ambiente local separado dos scripts de pesquisa e da monografia. As ferramentas
estão instaladas nesta pasta, sem depender de instalação global ou de API paga.

Coloque uma cópia da gravação em `entrada/`. Guarde também o arquivo original.
Os arquivos produzidos ficam em `exportados/`.

No PowerShell, dentro desta pasta:

```powershell
. ./ativar.ps1
ffmpeg -version
ffprobe -version
whisper --help
hyperframes --help
npm run studio
```

Transcrição em português, com arquivos TXT, SRT, VTT, TSV e JSON:

```powershell
./transcrever.ps1 -Arquivo './entrada/gravacao.mp4'
```

O modelo padrão é `base`, multilíngue, já baixado e testado. É possível escolher `-Modelo small`
para uma transcrição mais exigente; o modelo será baixado no primeiro uso.
O Whisper usa CPU neste ambiente. A transcrição precisa de revisão humana,
especialmente para nomes, siglas e termos do trabalho.

Teste do Remotion:

```powershell
npm run render:teste
```

Teste do HyperFrames com o modelo inicial oficial:

```powershell
. ./ativar.ps1
hyperframes render hyperframes-teste -o exportados/teste-hyperframes.mp4 --quality draft --low-memory-mode --fps 24
```

O Chrome já instalado é usado pelas duas ferramentas. As exportações de teste
apenas comprovam o funcionamento; não são a apresentação final.

Remotion e HyperFrames oferecem caminhos alternativos para compor títulos,
slides e elementos visuais. FFmpeg faz cortes, conversões e processamento de
áudio. Whisper transcreve a fala para orientar cortes e legendas. A transcrição
Python fica separada do comando `hyperframes transcribe`, que usa outro backend
opcional (whisper.cpp), não instalado aqui.

Referências de instalação:
- https://www.remotion.dev/docs/
- https://github.com/heygen-com/hyperframes
- https://github.com/openai/whisper
- https://www.gyan.dev/ffmpeg/builds/
