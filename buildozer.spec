[app]
title = Project Mind - Living AI
package.name = projectmind
package.domain = org.projectmind
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3,kivy,pillow
permissions = CAMERA,MICROPHONE,INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 33
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.logcat_filters = *:S python:D
android.entrypoint = org.renpy.android.PythonActivity

[buildozer]
log_level = 2
warn_on_root = 1
