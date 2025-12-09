[app]

# Application Metadata
title = Project Mind - Living AI
package.name = projectmind
package.domain = org.projectmind
version = 1.0.0

# Source and Build Settings
source.dir = app/src
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,md
source.exclude_exts = spec,pyc,pyo,pyd,so,exe

# Application UI Configuration
orientation = portrait
fullscreen = 0

# Android SDK Configuration (CRITICAL FOR CI/CD)
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

# Android Gradle Configuration
android.gradle_options = org.gradle.jvmargs=-Xmx2048m,org.gradle.caching=true,org.gradle.workers.max=4

# Python Requirements (CRITICAL: Cython must be 0.29.33)
requirements = python3,kivy==2.1.0,cython==0.29.33,pillow,numpy,flask,requests,setuptools,wheel

# Android App Entry Point
android.entrypoint = org.kivy.android.PythonActivity

# Permissions
permissions = CAMERA,MICROPHONE,INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_PHONE_STATE,ACCESS_NETWORK_STATE

# Features
android.features = android.hardware.camera,android.hardware.microphone

# Build optimization
android.enable_proguard = 1
android.presplash = 1

[buildozer]
log_level = 2
warn_on_root = 1
android_skip_update = False
android_skip_download = False