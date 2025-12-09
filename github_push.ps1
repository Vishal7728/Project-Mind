#!/usr/bin/env powershell
param(
    [string]$Token = "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",
    [string]$Username = "Vishal7728"
)

$ErrorActionPreference = "Stop"
$gitExe = "C:\Program Files\Git\cmd\git.exe"
$projectPath = "d:\Project Mind"

try {
    Set-Location $projectPath
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Cyan
    
    Write-Host "Checking git status..." -ForegroundColor Yellow
    & $gitExe status
    
    Write-Host "`nSetting up authentication..." -ForegroundColor Yellow
    $repoUrl = "https://$Username`:$Token@github.com/$Username/Project-Mind.git"
    & $gitExe remote set-url origin $repoUrl
    
    Write-Host "Remote URL configured`n" -ForegroundColor Green
    
    Write-Host "Pushing to GitHub (this may take a moment)..." -ForegroundColor Yellow
    & $gitExe push -u origin master --verbose
    
    Write-Host "`nSuccess! Code pushed to GitHub" -ForegroundColor Green
    Write-Host "Visit: https://github.com/$Username/Project-Mind" -ForegroundColor Cyan
    Write-Host "`nGitHub Actions will now automatically build your APK..." -ForegroundColor Cyan
    Write-Host "Check Actions tab in 1-2 minutes for build status" -ForegroundColor Cyan
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
