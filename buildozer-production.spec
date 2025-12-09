[app]

# =============================================================================
# Application Metadata
# =============================================================================
title = Project Mind - Living AI
package.name = projectmind
package.domain = org.projectmind
version = 1.0.0

# Version code for Play Store (increment for each release)
android.release_artifact = aab

# =============================================================================
# Source and Build Settings
# =============================================================================
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,md

# Exclude unnecessary files from APK
source.exclude_exts = spec,pyc,pyo,pyd,so,exe

# =============================================================================
# Application UI Configuration
# =============================================================================
orientation = portrait
fullscreen = 0
android.presplash_fqn = org.kivy.android.PythonPresplash
android.presplash = 1

# =============================================================================
# Android SDK Configuration (CRITICAL FOR CI/CD)
# =============================================================================

# Target API Level (highest supported)
android.api = 33

# Minimum API Level (lowest supported devices)
android.minapi = 21

# Build Tools Version (must match SDK installation)
android.build_tools_version = 33.0.0

# Android NDK Version
# 25b corresponds to NDK 25.1.8387110 (latest stable for Kivy)
android.ndk = 25b

# Architecture support: both 64-bit and 32-bit
# arm64-v8a: Modern 64-bit devices (required for Play Store)
# armeabi-v7a: Legacy 32-bit devices
android.archs = arm64-v8a,armeabi-v7a

# Accept Android SDK licenses automatically (required for CI/CD)
android.accept_sdk_license = True

# =============================================================================
# Android Gradle Configuration (For CI/CD Build System)
# =============================================================================

# JVM memory allocation (increased for larger builds)
# -Xmx2048m: Maximum heap size (2GB)
# Increase to 3072m if building larger projects
android.gradle_options = org.gradle.jvmargs=-Xmx2048m

# Enable Gradle caching (faster builds)
android.gradle_options = org.gradle.caching=true

# Parallel build threads
android.gradle_options = org.gradle.workers.max=4

# =============================================================================
# Application Permissions
# =============================================================================
permissions = CAMERA,MICROPHONE,INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_PHONE_STATE,ACCESS_NETWORK_STATE

# Features required for app functionality
android.features = android.hardware.camera,android.hardware.microphone

# =============================================================================
# Python Requirements
# =============================================================================

# CRITICAL: Cython version must be exactly 0.29.33
# This is hardcoded in Buildozer compilation process
# Other versions may cause build failures
requirements = python3,kivy,pillow

# Meta packages for faster installation
requirements.source.gradle = None

# Python version (affects compilation)
android.meta_data = com.android.launcher.py_version=python3

# =============================================================================
# Gradle Build Configuration
# =============================================================================

# Gradle plugins automatically managed by Buildozer:
# - com.android.application (v7.0+)
# - google-services (optional, for Firebase)
# - kotlinc (optional, for Kotlin)

# Gradle dependencies automatically added by Buildozer:
# - androidx.appcompat:appcompat:1.x.x
# - androidx.constraintlayout:constraintlayout:2.x.x
# - com.google.android.material:material:1.x.x
# Plus Kivy runtime dependencies

# Custom Gradle options (advanced)
android.gradle_options_custom = true
android.gradle_gradle_options = org.gradle.java.home=${JAVA_HOME}

# =============================================================================
# Android App Entry Point
# =============================================================================

# PythonActivity: Standard Kivy entry point
# Launches app, initializes Python, runs kivy_main.py
android.entrypoint = org.renpy.android.PythonActivity

# =============================================================================
# App Icon and Branding
# =============================================================================

# Icon can be PNG (recommended 512x512)
# Buildozer will automatically scale to ldpi/mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi
# icon.filename = %(source.dir)s/data/icon.png

# Presplash image (shown while app loads)
# presplash.filename = %(source.dir)s/data/presplash.png

# =============================================================================
# Android Manifest Settings
# =============================================================================

# Minimum supported Android version (from API level)
android.minapi_manifest = 21

# Target SDK (affects permission behavior and features available)
android.targetapi = 33

# Version code (for Play Store, must increment each release)
android.version_code = 1

# Version name (user-facing version)
android.version_name = 1.0.0

# =============================================================================
# Signing Configuration (For Release Builds)
# =============================================================================

# Keystore location (set via environment variable in CI/CD)
# android.keystore = 1
# android.keystore_alias = projectmind_key
# android.keystore_path = %(source.dir)s/projectmind.jks
# android.keystore_password = yourpassword
# android.key_password = yourpassword

# For CI/CD environments: Signing credentials passed via environment variables
# RELEASE_KEYSTORE_BASE64 -> projectmind.jks
# RELEASE_KEYSTORE_PASSWORD -> keystore password
# RELEASE_KEY_ALIAS -> key alias
# RELEASE_KEY_PASSWORD -> key password

# =============================================================================
# ProGuard / R8 Configuration (For Optimization)
# =============================================================================

# Obfuscate APK for release builds
android.enable_proguard = 1

# ProGuard rules file
# android.proguard_rules = proguard-rules.pro

# Default Kivy ProGuard rules (auto-applied by Buildozer):
# - Keep Kivy classes
# - Keep Python runtime
# - Keep native methods
# - Keep getters/setters

# =============================================================================
# Buildozer Meta Configuration
# =============================================================================

[buildozer]

# Log level (0-3, 3 is most verbose)
# 0 = errors only
# 1 = info
# 2 = debug
# 3 = verbose (use for CI/CD debugging)
log_level = 2

# Warn if running as root (disable in Docker/CI environments)
warn_on_root = 1

# Gradle auto-download and cache
android_skip_update = False

# Do not download newer versions if compatible version exists
android_skip_download = False

# =============================================================================
# =============================================================================
# NOTES FOR CI/CD DEPLOYMENT
# =============================================================================
# =============================================================================

# 1. Environment Variables Required in GitHub Actions:
#    ANDROID_SDK_ROOT=/usr/local/lib/android/sdk
#    ANDROID_NDK_HOME=/usr/local/lib/android/sdk/ndk/25.1.8387110
#    GRADLE_USER_HOME=~/.gradle
#    GRADLE_OPTS=-Xmx2048m -XX:MaxPermSize=512m

# 2. Java Version:
#    Must be Java 11+ (recommend Java 17 for modern builds)
#    GitHub Actions: setup-java@v3 with java-version: '17'

# 3. Python Version:
#    Must be Python 3.7+ (recommend 3.11 for Kivy)
#    GitHub Actions: setup-python@v4 with python-version: '3.11'

# 4. Cython Version:
#    CRITICAL: Must be exactly 0.29.33
#    Other versions will cause compilation failures

# 5. Build Time:
#    First build (cold): 15-20 minutes (downloads NDK, SDK, Gradle)
#    Subsequent builds (warm): 5-10 minutes (uses cache)

# 6. Gradle Caching:
#    Cache ~/.gradle/caches for faster builds
#    Cache .buildozer for faster subsequent builds
#    Cache /usr/local/lib/android/sdk for Android tools

# 7. APK Location:
#    bin/projectmind-1.0.0-release.apk (symlinked by Buildozer)
#    .buildozer/android/app/build/outputs/apk/release/app-release.apk (original)

# 8. Signing:
#    Create keystore locally: keytool -genkey -v -keystore projectmind.jks ...
#    Encode to base64: base64 projectmind.jks > projectmind.jks.b64
#    Store in GitHub Secrets: RELEASE_KEYSTORE_BASE64
#    GitHub Actions will decode and use for signing

# 9. Common Errors and Fixes:
#    - "NDK not found": Set ANDROID_NDK_HOME correctly
#    - "SDK not found": Install with sdkmanager before build
#    - "Gradle build failed": Increase memory (-Xmx2048m)
#    - "Cython error": Use Cython==0.29.33 exactly
#    - "Java version mismatch": Use Java 17 or 11
#    - "Permission denied": Make gradlew executable
#    - "Manifest merger failed": Check for duplicate permissions

# 10. Testing Locally:
#     buildozer android clean  (removes old build)
#     buildozer android debug  (test build)
#     buildozer android release  (final build)
#     adb install -r bin/projectmind-1.0.0-release.apk

# =============================================================================
