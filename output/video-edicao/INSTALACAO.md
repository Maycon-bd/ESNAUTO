# Instalação e conferência — 02/11/2026

- Node.js existente: 22.16.0.
- Python existente: 3.13.2; dependências isoladas em `.venv`.
- Remotion e CLI: 4.0.540; React e React DOM: 19.3.1.
- HyperFrames CLI: 0.9.4.
- FFmpeg e FFprobe: 9.0.2, build essentials Gyan para Windows.
- OpenAI Whisper: 20250625; PyTorch: 2.15.0+cpu.
- Modelo Whisper: `base`, multilíngue, já baixado em `modelos/base.pt`.

Conferências realizadas:

1. FFmpeg e FFprobe executaram com sucesso. SHA256 do ZIP conferido com o
   distribuidor: `60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`.
   O ZIP foi removido após extração e conferência; os executáveis foram mantidos.
2. Remotion exportou `exportados/teste-remotion.mp4`: H.264, 1280×720, 1 segundo.
3. HyperFrames exportou o modelo inicial oficial para
   `exportados/teste-hyperframes.mp4`: H.264, 1920×1080, 10 segundos.
   `hyperframes check` retornou `ok: true`, com navegador ativo.
4. Duração e codec dos dois vídeos conferidos com FFprobe; quadros decodificados
   com FFmpeg e inspecionados visualmente.
5. `pip check`: sem dependências quebradas. Whisper importado, modelo `base`
   carregado em CPU e inferência sobre um WAV de silêncio concluída em português.
   Esse é um teste de funcionamento, não de qualidade de reconhecimento de fala.

Dependências npm fixadas em `package-lock.json`; inventário Python em
`requirements-installed.txt`. O Chrome existente foi utilizado nas exportações.
FFmpeg e comandos Python/Node ficam disponíveis ao carregar `ativar.ps1`.
Docker e whisper.cpp são opcionais e não foram instalados. A transcrição funciona
com o Whisper Python pelo script `transcrever.ps1`.
