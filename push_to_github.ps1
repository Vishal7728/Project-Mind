$env:Path += ";C:\Program Files\Git\cmd"
cd "d:\Project Mind"

$token = "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"
$username = "Vishal7728"

Write-Host "Configuring git with token..." -ForegroundColor Cyan
& "C:\Program Files\Git\cmd\git.exe" config user.email "dev@projectmind.local"
& "C:\Program Files\Git\cmd\git.exe" config user.name "ProjectMind Developer"

Write-Host "Setting remote URL with token..." -ForegroundColor Cyan
& "C:\Program Files\Git\cmd\git.exe" remote set-url origin "https://${username}:${token}@github.com/${username}/Project-Mind.git"

Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
& "C:\Program Files\Git\cmd\git.exe" push -u origin master -v

Write-Host "Push complete!" -ForegroundColor Green
