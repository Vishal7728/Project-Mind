import subprocess
import sys
import os


def build_apk():
    print("="*70)
    print("PROJECT MIND - APK BUILD")
    print("="*70)
    print()
    
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        print("Building APK with Buildozer...")
        print("Estimated time: 5-15 minutes (first build may be slower)")
        print()
        
        cmd = [sys.executable, '-m', 'buildozer', 'android', 'release']
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
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
            return 0
        else:
            print()
            print("="*70)
            print("✗ APK BUILD FAILED")
            print("="*70)
            print()
            print("Check the output above for errors.")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(build_apk())
