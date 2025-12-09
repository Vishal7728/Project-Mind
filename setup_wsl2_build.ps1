# Project Mind APK Build - WSL2 Setup Script
# Run with: powershell -ExecutionPolicy Bypass -File setup_wsl2_build.ps1

Write-Host "========================================"
Write-Host "PROJECT MIND - WSL2 BUILD SETUP"
Write-Host "========================================"
Write-Host ""

# Check if WSL2 is installed
Write-Host "Checking WSL2 installation..."
$wslInfo = wsl --list --verbose 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ WSL2 not installed"
    Write-Host ""
    Write-Host "To install WSL2:"
    Write-Host "1. Right-click PowerShell → Run as Administrator"
    Write-Host "2. Run: wsl --install Ubuntu"
    Write-Host "3. Restart your computer"
    Write-Host "4. Re-run this script"
    exit 1
}

Write-Host "✓ WSL2 found"
Write-Host ""

# Check if Ubuntu is available
if ($wslInfo -notlike "*Ubuntu*") {
    Write-Host "Installing Ubuntu distribution..."
    wsl --install -d Ubuntu
    Write-Host "Please restart your computer and run this script again"
    exit 0
}

Write-Host "✓ Ubuntu available"
Write-Host ""

# Get project path
$projectPath = "d:\Project Mind"
$wslPath = "/mnt/d/Project\ Mind"

Write-Host "Setting up build environment in WSL2..."
Write-Host "Project: $projectPath"
Write-Host ""

# Build commands for WSL2
$buildCommands = @'
sudo apt-get update
sudo apt-get install -y python3 python3-pip openjdk-11-jdk-headless
sudo apt-get install -y build-essential git libssl-dev libffi-dev
sudo apt-get install -y libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev
pip install buildozer Cython==0.29.33 virtualenv
pip install kivy Pillow
cd /mnt/d/Project\ Mind
buildozer android release
'@

Write-Host "Build commands to run in WSL2:"
Write-Host "========================================"
Write-Host $buildCommands
Write-Host "========================================"
Write-Host ""

Write-Host "Opening WSL2 Ubuntu terminal..."
Write-Host "Copy-paste the above commands to build the APK"
Write-Host ""

# Launch WSL2
wsl.exe

Write-Host ""
Write-Host "After build completes:"
Write-Host "APK location: $projectPath\bin\projectmind-1.0.0-release.apk"
Write-Host ""
Write-Host "To install on device:"
Write-Host "adb install -r bin\projectmind-1.0.0-release.apk"
