$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\apresentacao_banca_v010_fala_clara'
$taskDeck = Join-Path $taskRoot 'entrega\Apresentacao_ESNAUTO_v010_notas_fala_clara.pptx'
$taskPreview = Join-Path $taskRoot 'build\powerpoint_render'
New-Item -ItemType Directory -Path $taskPreview -Force | Out-Null
$taskPpt = New-Object -ComObject PowerPoint.Application
$taskCountBefore = $taskPpt.Presentations.Count
$taskLinks = @()
$taskEffects = @()
try {
    $taskPresentation = $taskPpt.Presentations.Open($taskDeck, -1, 0, 0)
    $taskPresentation.Export($taskPreview, 'PNG', 1280, 720)
    foreach ($taskSlide in $taskPresentation.Slides) {
        $taskEffects += @{slide=$taskSlide.SlideIndex;effect=$taskSlide.SlideShowTransition.EntryEffect;onClick=$taskSlide.SlideShowTransition.AdvanceOnClick;onTime=$taskSlide.SlideShowTransition.AdvanceOnTime}
        foreach ($taskShape in $taskSlide.Shapes) {
            if ($taskShape.Name.StartsWith('nav-')) {
                $taskAction = $taskShape.ActionSettings.Item(1)
                $taskLinks += @{slide=$taskSlide.SlideIndex;shape=$taskShape.Name;action=$taskAction.Action;subAddress=$taskAction.Hyperlink.SubAddress}
            }
        }
    }
    @{effects=$taskEffects;links=$taskLinks;slideCount=$taskPresentation.Slides.Count} | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $taskRoot 'build\verificacao_nativa.json') -Encoding utf8
    Write-Output ('Slides exportados ' + $taskPresentation.Slides.Count + ', atalhos reconhecidos ' + $taskLinks.Count)
    $taskPresentation.Close()
} finally {
    if ($taskCountBefore -eq 0) { $taskPpt.Quit() }
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskPpt) | Out-Null
}

