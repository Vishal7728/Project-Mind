import subprocess
import sys
import os
import json
from pathlib import Path


def check_android_sdk():
    android_home = os.getenv('ANDROID_HOME')
    if not android_home:
        print("⚠️  ANDROID_HOME not set. Checking default locations...")
        possible_paths = [
            f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Android\\Sdk",
            "C:\\Android\\sdk",
            "C:\\android-sdk"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                android_home = path
                print(f"✓ Found Android SDK at: {android_home}")
                os.environ['ANDROID_HOME'] = android_home
                break
        else:
            print("✗ Android SDK not found!")
            print("\nTo set ANDROID_HOME, run:")
            print('[Environment]::SetEnvironmentVariable("ANDROID_HOME", "C:\\path\\to\\android\\sdk", "User")')
            return False
    else:
        print(f"✓ ANDROID_HOME: {android_home}")
    
    required_paths = [
        os.path.join(android_home, 'platforms'),
        os.path.join(android_home, 'build-tools'),
        os.path.join(android_home, 'platform-tools')
    ]
    
    for path in required_paths:
        if not os.path.exists(path):
            print(f"✗ Missing: {path}")
            return False
    
    print("✓ Android SDK configured correctly")
    return True


def check_java():
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Java JDK installed")
            return True
    except:
        pass
    
    print("✗ Java JDK not found")
    return False


def build_apk():
    print("\n" + "="*60)
    print("PROJECT MIND - APK BUILD PROCESS")
    print("="*60 + "\n")
    
    if not check_java():
        print("Install Java JDK 17+ and try again")
        return False
    
    if not check_android_sdk():
        return False
    
    print("\n✓ All prerequisites verified")
    print("\nStarting APK build...")
    print("Estimated time: 5-15 minutes (first build)\n")
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'buildozer', 'android', 'release'],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            apk_path = Path("bin/projectmind-1.0.0-release.apk")
            if apk_path.exists():
                print(f"\n✓ APK built successfully!")
                print(f"✓ Location: {apk_path.absolute()}")
                print(f"✓ Size: {apk_path.stat().st_size / (1024*1024):.2f} MB")
                return True
        
        print("✗ APK build failed")
        return False
        
    except Exception as e:
        print(f"✗ Build error: {str(e)}")
        return False


def install_apk():
    print("\n" + "="*60)
    print("CHECKING FOR CONNECTED DEVICES")
    print("="*60 + "\n")
    
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = [line.strip() for line in result.stdout.split('\n') 
                  if line.strip() and 'device' in line and not line.startswith('List')]
        
        if not devices:
            print("✗ No Android devices detected")
            print("Ensure device is connected with USB debugging enabled")
            return False
        
        print(f"✓ Found {len(devices)} device(s)")
        for device in devices:
            print(f"  • {device}")
        
        apk_path = Path("bin/projectmind-1.0.0-release.apk")
        if not apk_path.exists():
            print(f"✗ APK not found at {apk_path}")
            return False
        
        print(f"\nInstalling APK...")
        result = subprocess.run(['adb', 'install', '-r', str(apk_path)], 
                              capture_output=True, text=True)
        
        if 'Success' in result.stdout or result.returncode == 0:
            print("✓ APK installed successfully!")
            return True
        else:
            print("✗ Installation failed")
            print(result.stdout)
            return False
            
    except FileNotFoundError:
        print("✗ ADB not found. Ensure Android SDK platform-tools are in PATH")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def launch_app():
    print("\n" + "="*60)
    print("LAUNCHING APPLICATION")
    print("="*60 + "\n")
    
    try:
        subprocess.run(['adb', 'shell', 'am', 'start', '-n', 
                       'org.projectmind.projectmind/.ProjectMindApp'],
                      capture_output=True)
        print("✓ App launched on device!")
        return True
    except Exception as e:
        print(f"✗ Failed to launch: {str(e)}")
        return False


def main():
    steps = [
        ("Android SDK Check", check_android_sdk),
        ("Java Check", check_java),
        ("APK Build", build_apk),
        ("Device Check", lambda: True),
        ("APK Install", install_apk),
        ("App Launch", launch_app)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*60}")
        print(f"STEP: {step_name}")
        print('='*60)
        
        if not step_func():
            print(f"\n✗ {step_name} failed. Stopping.")
            return 1
    
    print("\n" + "="*60)
    print("✓ ALL STEPS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nProject Mind is now installed and running on your Android device!")
    print("\nFeatures available:")
    print("  • Persona customization (9 archetypes)")
    print("  • AI naming system")
    print("  • Voice synthesis")
    print("  • Emotion expressions")
    print("  • Memory persistence")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
