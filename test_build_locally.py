#!/usr/bin/env python3
"""
Script to test Project Mind APK build locally
"""

import subprocess
import sys
import os
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print("Checking prerequisites...")
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✓ Python: {result.stdout.strip()}")
    except Exception as e:
        print(f"✗ Python not found: {e}")
        return False
    
    # Check Java
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        print(f"✓ Java: {result.stderr.split()[0]} {result.stderr.split()[1]} {result.stderr.split()[2]}")
    except Exception as e:
        print(f"✗ Java not found: {e}")
        return False
    
    # Check Android SDK
    android_home = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
    if android_home and Path(android_home).exists():
        print(f"✓ Android SDK: {android_home}")
    else:
        print("⚠ Android SDK not found (can be installed during build)")
    
    # Check buildozer
    try:
        result = subprocess.run([sys.executable, "-m", "buildozer", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Buildozer: Installed")
        else:
            print("✗ Buildozer: Not installed")
            print("  Install with: pip install buildozer")
            return False
    except Exception as e:
        print(f"✗ Buildozer not found: {e}")
        print("  Install with: pip install buildozer")
        return False
    
    return True

def validate_project():
    """Run project validation"""
    print("\nValidating project...")
    try:
        result = subprocess.run([sys.executable, "validate_build.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Project validation passed")
            return True
        else:
            print("✗ Project validation failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Error running validation: {e}")
        return False

def clean_build():
    """Clean previous builds"""
    print("\nCleaning previous builds...")
    try:
        result = subprocess.run([sys.executable, "-m", "buildozer", "android", "clean"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Build cleaned successfully")
            return True
        else:
            print("⚠ Warning during clean (may not be critical):")
            print(result.stdout[-200:])  # Show last 200 chars
            return True  # Continue anyway
    except Exception as e:
        print(f"⚠ Error during clean: {e}")
        return True  # Continue anyway

def build_debug_apk():
    """Build debug APK"""
    print("\nBuilding debug APK...")
    try:
        # Run buildozer with output to stdout
        process = subprocess.Popen([
            sys.executable, "-m", "buildozer", "android", "debug"
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Print output in real-time
        for line in process.stdout:
            print(line.rstrip())
        
        process.wait()
        
        if process.returncode == 0:
            print("✓ Debug APK built successfully")
            return True
        else:
            print("✗ Debug APK build failed")
            return False
    except Exception as e:
        print(f"✗ Error during build: {e}")
        return False

def check_apk():
    """Check if APK was created"""
    print("\nChecking for generated APK...")
    
    # Check common locations
    apk_locations = [
        "bin/projectmind-1.0.0-debug.apk",
        "bin/projectmind-1.0.0-release.apk",
    ]
    
    for location in apk_locations:
        if Path(location).exists():
            size = Path(location).stat().st_size
            print(f"✓ APK found: {location} ({size//1024} KB)")
            return True
    
    # Check buildozer output directory
    build_outputs = list(Path(".buildozer").rglob("*.apk"))
    if build_outputs:
        for apk in build_outputs:
            size = apk.stat().st_size
            print(f"✓ APK found: {apk} ({size//1024} KB)")
        return True
    
    print("✗ APK not found")
    return False

def main():
    """Main function"""
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    Project Mind - Local Build Test                             ║
║              Test your APK build before pushing to GitHub                       ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install required tools.")
        return 1
    
    # Validate project
    if not validate_project():
        print("\n❌ Project validation failed. Please fix issues before building.")
        return 1
    
    # Ask user if they want to proceed with build
    response = input("\nDo you want to proceed with building the APK? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Build cancelled.")
        return 0
    
    # Clean previous builds
    if not clean_build():
        print("\n❌ Failed to clean previous builds.")
        return 1
    
    # Build APK
    if not build_debug_apk():
        print("\n❌ APK build failed.")
        return 1
    
    # Check if APK was created
    if not check_apk():
        print("\n❌ APK was not created successfully.")
        return 1
    
    print("\n🎉 Success! Your APK build is working correctly.")
    print("You can now push to GitHub and the workflow should succeed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())