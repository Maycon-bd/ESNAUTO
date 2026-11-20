$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\devolutiva_orientador_20261101'
$taskFile = 'C:\Users\User\Downloads\MayconGarciaSilva_monografia_correcao final antes da banca.docx'
$taskWord = New-Object -ComObject Word.Application
$taskWord.Visible = $false
$taskWord.DisplayAlerts = 0
$taskTitles = @()
try {
    $taskDoc = $taskWord.Documents.Open($taskFile, $false, $true)
    foreach ($taskParagraph in $taskDoc.Paragraphs) {
        $taskStyle = $taskParagraph.Style.NameLocal
        if ($taskStyle -in @('TITULO TCC','SEÇÃO TCC','SUBÇÃO 2')) {
            $taskRange = $taskParagraph.Range
            $taskTitles += @{
                title=$taskRange.Text.Trim();
                style=$taskStyle;
                number=$taskRange.ListFormat.ListString;
                page=$taskRange.Information(1);
                physicalPage=$taskRange.Information(3)
            }
        }
    }
    $taskTitles | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $taskRoot 'numeracao_word_recebido.json') -Encoding utf8
    $taskDoc.Close(0)
    Write-Output ('Títulos conferidos no Word: ' + $taskTitles.Count)
} finally {
    $taskWord.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord) | Out-Null
}
