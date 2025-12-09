# GitHub Actions Setup for Project Mind APK

This document provides instructions for setting up and troubleshooting GitHub Actions to build your Project Mind Android APK.

## File/Folder Structure Expected by GitHub Actions

```
your-repo/
├── .github/
│   └── workflows/
│       └── build-project-mind-apk.yml
├── src/
│   ├── main.py
│   ├── types.py
│   └── [other source files]
├── kivy_main.py
├── buildozer.spec
├── data/
│   └── mind_heart.json
└── [other project files]
```

## Required Files

1. **`.github/workflows/build-project-mind-apk.yml`** - The main workflow file
2. **`buildozer.spec`** - Build configuration file
3. **`kivy_main.py`** - Kivy entry point
4. **`src/`** - Source code directory
5. **`data/mind_heart.json`** - Initial data file

## Environment Variables

The workflow sets these environment variables automatically:
- `ANDROID_SDK_ROOT=/usr/local/lib/android/sdk`
- `ANDROID_NDK_HOME=/usr/local/lib/android/sdk/ndk/25.1.8387110`
- `GRADLE_USER_HOME=~/.gradle`
- `GRADLE_OPTS=-Xmx2048m -XX:MaxMetaspaceSize=512m`

## Common CI Errors and Solutions

### 1. "No matching variant found"
**Cause:** Gradle dependency resolution issue
**Solution:** 
- Ensure `buildozer.spec` has correct `requirements`
- Use specific versions: `kivy==2.1.0` instead of just `kivy`

### 2. "Manifest merger failed"
**Cause:** Duplicate permissions or conflicting manifest entries
**Solution:**
- Check `buildozer.spec` for duplicate permissions
- Remove redundant permission declarations

### 3. "Duplicate class"
**Cause:** Multiple versions of the same library
**Solution:**
- Pin specific versions in `requirements`
- Use `--no-cache-dir` when installing dependencies

### 4. "Resource linking failed"
**Cause:** Missing resources or incorrect resource references
**Solution:**
- Ensure all referenced assets exist
- Check for proper file extensions in `source.include_exts`

### 5. "Minimum supported Gradle is X"
**Cause:** Outdated Gradle version
**Solution:**
- Update `android.build_tools_version` in `buildozer.spec`
- Let buildozer download the latest compatible version

### 6. "AGP X requires Java X"
**Cause:** Java version mismatch
**Solution:**
- Use Java 17 as specified in the workflow
- Ensure `actions/setup-java@v4` with `java-version: '17'`

### 7. "Keystore not found"
**Cause:** Missing signing configuration for release builds
**Solution:**
- For debug builds, no keystore needed
- For release builds, configure signing in `buildozer.spec`

### 8. "Permission denied for Gradle wrapper"
**Cause:** File permission issues
**Solution:**
- Workflow automatically handles permissions
- Ensure no read-only files in repo

## Testing Locally

Before pushing to GitHub, test locally:

```bash
# Validate project structure
python validate_build.py

# Clean previous builds
buildozer android clean

# Build debug APK (faster)
buildozer android debug

# Build release APK (final)
buildozer android release

# Install on connected device
adb install -r bin/projectmind-1.0.0-debug.apk
```

## APK Output Locations

The workflow looks for APKs in these locations:
1. `bin/projectmind-1.0.0-release.apk` (primary)
2. `bin/projectmind-1.0.0-debug.apk` (fallback)
3. `.buildozer/android/app/build/outputs/**/*.apk` (build outputs)

## Troubleshooting Tips

1. **Build takes too long:** Enable caching in workflow
2. **Memory issues:** Increase `Xmx` in `GRADLE_OPTS`
3. **NDK issues:** Verify `ANDROID_NDK_HOME` path
4. **Python issues:** Use Python 3.11 as specified
5. **Kivy issues:** Use `kivy==2.1.0` in requirements

## GitHub Secrets (For Signed Releases)

To create signed releases, add these secrets to your repository:
- `RELEASE_KEYSTORE_BASE64` - Base64 encoded keystore
- `RELEASE_KEYSTORE_PASSWORD` - Keystore password
- `RELEASE_KEY_ALIAS` - Key alias
- `RELEASE_KEY_PASSWORD` - Key password

Create keystore locally:
```bash
keytool -genkey -v -keystore projectmind.jks -keyalg RSA -keysize 2048 -storepass yourpassword -keypass yourpassword -validity 10000 -alias projectmind_key
```

Encode for GitHub:
```bash
base64 projectmind.jks > projectmind.jks.b64
```

## Workflow Triggers

The workflow runs on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to these branches
- Manual trigger via GitHub Actions UI

## Artifact Retention

Generated APKs are uploaded as artifacts and retained for 30 days.