Set-Location $PSScriptRoot
$env:TENANT_ID = "テナント ID"
$env:CLIENT_ID = "クライアント ID"
$env:TEAM_ID = "チームの ID"
$env:FOLDERS = "規程,手順,過去の問い合わせ"
$env:DIFY_URL = "http://localhost"
$env:DIFY_DATASET_ID = "ナレッジの ID"
$env:DIFY_API_KEY = "dataset-で始まるキー"
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
"=== " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") | Out-File -Append -Encoding utf8 sync.log
& .\.venv\Scripts\python.exe sp_sync.py 2>&1 | Out-File -Append -Encoding utf8 sync.log
