[app]

# =============================================================================
# Application Metadata
# =============================================================================
title = Project Mind - Living AI
package.name = projectmind
package.domain = org.projectmind
version = 1.0.0

# Source and Build Settings
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,md,env
source.exclude_exts = spec,pyc,pyo,pyd,so,exe,git,github,vscode,deploy_apk.py

# =============================================================================
# Application UI Configuration
# =============================================================================
orientation = portrait
fullscreen = 0
android.presplash_fqn = org.kivy.android.PythonPresplash
android.presplash = 1

# =============================================================================
# Android Configuration (CRITICAL FOR CI/CD)
# =============================================================================
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

# Optimization for CI/CD Speed and Memory
android.gradle_options = org.gradle.jvmargs=-Xmx2048m
android.gradle_options = org.gradle.caching=true
android.gradle_options = org.gradle.workers.max=4

# =============================================================================
# Python Requirements
# =============================================================================
# CRITICAL: Cython must be pinned to 0.29.33 for Kivy compatibility
requirements = python3,kivy,pillow,Cython==0.29.33

# =============================================================================
# Permissions & Features
# =============================================================================
permissions = CAMERA,MICROPHONE,INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_PHONE_STATE,ACCESS_NETWORK_STATE
android.features = android.hardware.camera,android.hardware.microphone

# =============================================================================
# Entry Point
# =============================================================================
android.entrypoint = org.renpy.android.PythonActivity
android.enable_proguard = 1

[buildozer]
log_level = 2
warn_on_root = 1
android_skip_update = False