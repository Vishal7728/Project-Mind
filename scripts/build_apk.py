#!/usr/bin/env python3
"""
Project Mind - APK Build Script
Automates Android APK generation and deployment
"""

import subprocess
import sys
import os
from pathlib import Path


def check_buildozer():
    """Check if buildozer is installed"""
    try:
        subprocess.run(['buildozer', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_java():
    """Check if Java is installed"""
    try:
        subprocess.run(['java', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_android_sdk():
    """Check if Android SDK is installed"""
    android_home = os.environ.get('ANDROID_HOME')
    return android_home is not None and os.path.exists(android_home)


def install_requirements():
    """Install required build tools"""
    print("[*] Installing build requirements...")
    
    tools = ['buildozer', 'Cython', 'pillow']
    
    for tool in tools:
        try:
            __import__(tool)
            print(f"[+] {tool} already installed")
        except ImportError:
            print(f"[*] Installing {tool}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', tool], 
                         check=True, capture_output=True)
            print(f"[+] {tool} installed")


def build_apk(release=True):
    """Build APK using buildozer"""
    print("[*] Building APK...")
    
    cmd = ['buildozer', 'android']
    
    if release:
        cmd.append('release')
    else:
        cmd.append('debug')
    
    try:
        subprocess.run(cmd, check=True)
        print("[+] APK build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] APK build failed: {e}")
        return False


def install_apk(apk_path):
    """Install APK on connected Android device"""
    print(f"[*] Installing APK: {apk_path}")
    
    try:
        subprocess.run(['adb', 'install', '-r', apk_path], check=True)
        print("[+] APK installed successfully!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[-] APK installation failed (adb not found or device not connected)")
        return False


def launch_app():
    """Launch the app on connected device"""
    print("[*] Launching Project Mind...")
    
    package_name = "org.projectmind.projectmind"
    activity_name = "org.renpy.android.PythonActivity"
    
    try:
        subprocess.run([
            'adb', 'shell', 'am', 'start',
            '-n', f'{package_name}/{activity_name}'
        ], check=True)
        print("[+] App launched!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[-] Failed to launch app")
        return False


def main():
    """Main build orchestration"""
    print("""
    ╔════════════════════════════════════════╗
    ║   Project Mind - APK Build System      ║
    ║   Android 15+ Deployment               ║
    ╚════════════════════════════════════════╝
    """)
    
    print("\n[*] Checking environment...")
    
    print("[*] Skipping buildozer check...")
    # if not check_buildozer():
    #     print("[*] Buildozer not found, installing...")
    #     install_requirements()
    
    if not check_java():
        print("[-] Java not found. Please install Java Development Kit (JDK)")
        sys.exit(1)
    
    if not check_android_sdk():
        print("[!] Android SDK not found. Set ANDROID_HOME environment variable")
        print("[*] You can still generate the APK structure for manual building")
    
    print("[+] Environment check completed")
    
    build_apk(release=True)
    
    apk_path = Path('bin/projectmind-1.0.0-release.apk')
    if apk_path.exists():
        print(f"\n[+] APK generated at: {apk_path}")
        
        if len(sys.argv) > 1 and sys.argv[1] == '--install':
            install_apk(str(apk_path))
            if len(sys.argv) > 2 and sys.argv[2] == '--launch':
                launch_app()
    else:
        print("[-] APK not found after build")


if __name__ == '__main__':
    main()
