$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\devolutiva_orientador_20261101'
$taskSources = @(
    @{doc='C:\Users\User\Documents\PROJETOS SOFTWARE\ESNAUTO\reports\monografia\versoes\v008\MayconGarciaSilva_monografia_v008.docx'; pdf='base_v008.pdf'},
    @{doc='C:\Users\User\Downloads\MayconGarciaSilva_monografia_correcao final antes da banca.docx'; pdf='recebido_orientador.pdf'}
)
$taskWord = New-Object -ComObject Word.Application
$taskWord.Visible = $false
$taskWord.DisplayAlerts = 0
try {
    foreach ($taskSource in $taskSources) {
        $taskDoc = $taskWord.Documents.Open($taskSource.doc, $false, $true)
        $taskDoc.ExportAsFixedFormat((Join-Path $taskRoot $taskSource.pdf), 17)
        $taskDoc.Close(0)
        Write-Output ('Conferência exportada ' + $taskSource.pdf)
    }
} finally {
    $taskWord.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord) | Out-Null
}
