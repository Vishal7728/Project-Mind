import sys
import os

os.chdir(r'd:\Project Mind')

from buildozer import Buildozer

print("="*70)
print("PROJECT MIND - APK BUILD")
print("="*70)
print()

buildozer = Buildozer(filename='buildozer.spec')
buildozer.set_target('android')

print("Building APK with Buildozer...")
print("Estimated time: 5-15 minutes")
print()

try:
    buildozer.build_application()
    print()
    print("="*70)
    print("✓ APK BUILD SUCCESSFUL!")
    print("="*70)
    print()
    print("APK Location: bin/projectmind-1.0.0-release.apk")
    print()
    print("Next Steps:")
    print("1. Connect Android device via USB")
    print("2. Enable USB Debugging on device")
    print("3. Run: adb install -r bin/projectmind-1.0.0-release.apk")
except Exception as e:
    print()
    print("="*70)
    print("✗ APK BUILD FAILED")
    print("="*70)
    print(f"Error: {e}")
