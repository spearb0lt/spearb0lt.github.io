#Requires -Version 5.1
<#
  serve.ps1 - Run spearb0lt.github.io locally with Docker.

  USAGE
    1. Start Docker Desktop (wait until its icon says "running").
    2. In PowerShell, from the repo folder, run:   .\serve.ps1
       The site opens automatically at http://127.0.0.1:8080/

  OTHER COMMANDS
    .\serve.ps1 -Restart   # rebuild after editing _config.yml or _data/*
    .\serve.ps1 -Stop      # stop the local server

  If PowerShell blocks the script, run this once in the same window:
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#>
param(
  [switch]$Stop,
  [switch]$Restart
)

$ErrorActionPreference = 'Continue'
$Url   = 'http://127.0.0.1:8080/'
$Image = 'amirpourmand/al-folio:latest'

$RepoDir = $PSScriptRoot
if (-not $RepoDir) { $RepoDir = (Get-Location).Path }
Set-Location $RepoDir

function Say($msg, $color = 'Cyan') { Write-Host $msg -ForegroundColor $color }

# --- Docker CLI present? ---------------------------------------------------
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Say 'Docker is not installed or not on PATH. Install Docker Desktop first.' 'Yellow'
  return
}

# --- Stop mode -------------------------------------------------------------
if ($Stop) {
  Say 'Stopping the local server...'
  docker compose down
  Say 'Stopped.' 'Green'
  return
}

# --- Wait for the Docker engine (launch Docker Desktop if needed) ----------
docker info *> $null
if ($LASTEXITCODE -ne 0) {
  Say 'Docker engine not ready. Trying to start Docker Desktop...' 'Yellow'
  $dd = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
  if (Test-Path $dd) { Start-Process $dd }
  $ready = $false
  for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Seconds 5
    docker info *> $null
    if ($LASTEXITCODE -eq 0) { $ready = $true; break }
    Write-Host ("  ...waiting for Docker ({0}s)" -f ($i * 5))
  }
  if (-not $ready) {
    Say 'Docker still not ready. Start Docker Desktop manually, then re-run .\serve.ps1' 'Yellow'
    return
  }
}
Say 'Docker engine is running.' 'Green'

# --- Make sure the image is present (pull once if missing) -----------------
docker image inspect $Image *> $null
if ($LASTEXITCODE -ne 0) {
  Say "Pulling $Image (first time only; this can take a few minutes)..."
  docker pull $Image
}

# --- Start (or restart) the site ------------------------------------------
if ($Restart) {
  Say 'Restarting to pick up _config.yml / _data changes...'
  docker compose restart
} else {
  Say 'Starting the site...'
  docker compose up -d --no-build
}

# --- Wait for the site to respond -----------------------------------------
Say 'Waiting for the site to build (first run can take ~30-60s)...'
$up = $false
for ($i = 0; $i -lt 60; $i++) {
  try {
    if ((Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 5 -ErrorAction Stop).StatusCode -eq 200) {
      $up = $true; break
    }
  } catch {}
  Start-Sleep -Seconds 3
}

if ($up) {
  Say ("Site is up:  {0}" -f $Url) 'Green'
  Start-Process $Url
  Write-Host ''
  Say 'Tips:' 'Magenta'
  Write-Host '  Edit pages / content    ->  just refresh the browser (auto-rebuilds)'
  Write-Host '  Changed _config or _data->  .\serve.ps1 -Restart'
  Write-Host '  Stop the server         ->  .\serve.ps1 -Stop'
  Write-Host '  Watch build logs        ->  docker compose logs -f'
} else {
  Say 'The site did not respond yet. Check the logs with:  docker compose logs --tail 50' 'Yellow'
}
