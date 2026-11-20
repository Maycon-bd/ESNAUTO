$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\apresentacao_banca_v008'
$taskDeck = Join-Path $taskRoot 'entrega\Apresentacao_ESNAUTO_banca_v008.pptx'
$taskPreview = Join-Path $taskRoot 'build\powerpoint_render'
New-Item -ItemType Directory -Path $taskPreview -Force | Out-Null
$taskPpt = New-Object -ComObject PowerPoint.Application
$taskCountBefore = $taskPpt.Presentations.Count
try {
    $taskPresentation = $taskPpt.Presentations.Open($taskDeck, -1, 0, 0)
    $taskPresentation.Export($taskPreview, 'PNG', 1280, 720)
    Write-Output ('Slides abertos e exportados pelo PowerPoint: ' + $taskPresentation.Slides.Count)
    $taskPresentation.Close()
} finally {
    if ($taskCountBefore -eq 0) { $taskPpt.Quit() }
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskPpt) | Out-Null
}
