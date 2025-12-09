## Project Mind - APK Build Guide

### Build Status
- **Status**: Ready for APK Build
- **Platform**: Android 13+ (API 33)
- **Architecture**: arm64-v8a, armeabi-v7a
- **Build System**: GitHub Actions CI/CD

### Quick Start

#### Option 1: GitHub Actions (Recommended - Cloud Build)
1. Push code to GitHub
2. Go to Actions tab
3. Monitor build progress
4. Download APK from artifacts when complete

```bash
git push origin master
# Build starts automatically
```

#### Option 2: Local Build
```bash
# Install buildozer
pip install buildozer Cython==0.29.33

# Build APK
buildozer android release

# APK will be in bin/
```

### Build Validation

Before building, validate your environment:

```bash
python validate_build.py
```

This checks:
- ✓ All Python files compile
- ✓ buildozer.spec configuration
- ✓ Data files integrity
- ✓ Critical imports available
- ✓ Android configuration

### Common Issues & Solutions

#### Issue: NDK not found
**Solution**: Buildozer will download it automatically. Ensure you have ~2GB free space.

#### Issue: Java/SDK errors
**Solution**: GitHub Actions includes Java 11. For local builds, install:
```bash
# macOS
brew install openjdk@11

# Ubuntu/Debian
sudo apt-get install openjdk-11-jdk

# Windows
choco install openjdk11
```

#### Issue: Build timeout
**Solution**: GitHub Actions has 45-minute timeout. Local builds may take longer.

#### Issue: Memory errors
**Solution**: buildozer.spec includes: `android.gradle_options = org.gradle.jvmargs=-Xmx1024m`

### Build Configuration

Key settings in `buildozer.spec`:

```ini
# App Configuration
title = Project Mind - Living AI
package.name = projectmind
package.domain = org.projectmind
version = 1.0.0

# Requirements
requirements = python3,kivy,pillow

# Android Target
android.api = 33          # Target API
android.minapi = 33       # Minimum API
android.ndk = 25b         # NDK version
android.archs = arm64-v8a,armeabi-v7a

# Build Optimization
android.gradle_options = org.gradle.jvmargs=-Xmx1024m
```

### GitHub Actions Workflow

The `.github/workflows/build-apk.yml` workflow:

1. **Checkout Code**: Downloads your repository
2. **Setup Python 3.11**: Configures Python environment
3. **Setup Java 11**: Configures Android build tools
4. **Install Dependencies**: Installs buildozer and Kivy
5. **Verify Environment**: Logs configuration for debugging
6. **Build APK**: Runs buildozer for 45 minutes maximum
7. **Upload Artifacts**: Makes APK available for download

### Installing APK on Device

Once APK is built:

```bash
# Enable USB Debugging on your Android device
# Settings → Developer Options → USB Debugging

# Connect device via USB
adb devices

# Install APK
adb install -r projectmind-1.0.0-release.apk

# Launch app
adb shell am start -n org.projectmind.projectmind/.PythonActivity
```

### Troubleshooting

#### Check Build Logs
1. Go to GitHub Actions
2. Click on failed workflow run
3. Expand failed step to see error logs

#### Common Error Patterns
- **"build-tools not found"**: Buildozer downloads on first run
- **"gradle build failed"**: Check memory settings
- **"Python not found"**: buildozer includes Python 3 by default
- **"Missing .so files"**: Native compilation issue - rebuild with verbose

#### Enable Verbose Output
Add to buildozer.spec:
```ini
log_level = 3
android.gradle_options = -d
```

### Performance Tips

1. **First Build**: Takes 15-20 minutes (downloads NDK, Java, gradle)
2. **Subsequent Builds**: Take 5-10 minutes (uses cached files)
3. **Memory**: Need ~2GB available RAM
4. **Disk Space**: Need ~5GB for NDK and build tools

### File Structure Required

```
Project Mind/
├── buildozer.spec          # Build configuration
├── kivy_main.py            # Kivy UI entry point
├── validate_build.py       # Build validator
├── src/                    # Source code
│   ├── main.py
│   ├── types.py
│   └── ... (other modules)
├── data/
│   └── mind_heart.json     # Data file
└── .github/
    └── workflows/
        └── build-apk.yml   # GitHub Actions workflow
```

### Next Steps

1. ✓ Code is validated
2. ✓ Configuration is optimized
3. ✓ GitHub Actions is ready
4. → Push to GitHub to start build
5. → Monitor build progress
6. → Download APK when ready
7. → Install on Android device

### Support

For issues:
1. Check build logs in GitHub Actions
2. Run `python validate_build.py` locally
3. Ensure all files are present and valid
4. Check Python and Java versions match requirements

---

**Project Mind** - A living, learning AI with emotions and personality
Built with Python, Kivy, and Buildozer for Android
