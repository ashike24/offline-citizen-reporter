param([Parameter(Mandatory = $true)][string]$Repo)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    $env:Path += ";C:\Program Files\GitHub CLI"
}

Write-Host "Installing requirements..."
python -m pip install -r requirements.txt

if (-not (Test-Path .git)) { git init -b main }

git check-ignore -q .env
if ($LASTEXITCODE -ne 0) { Write-Host "STOP: .env is not git-ignored." -ForegroundColor Red; exit 1 }
if (git ls-files .env) { Write-Host "STOP: .env is tracked by git." -ForegroundColor Red; exit 1 }

git add .
git commit -m "Offline-first citizen reporter"
gh repo create $Repo --public --source . --remote origin --push