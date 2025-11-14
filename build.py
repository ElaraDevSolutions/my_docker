#!/usr/bin/env python3
"""
Script to generate My Docker executables
for macOS and Linux using PyInstaller.
"""

import sys
import os
import platform
import subprocess
import shutil


def get_platform_name():
    """Returns the current platform name."""
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    elif system == 'linux':
        return 'linux'
    else:
        return system


def clean_build_dirs():
    """Remove previous build directories."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for d in dirs_to_clean:
        if os.path.exists(d):
            print(f"Removing {d}/")
            shutil.rmtree(d)
    
    # Remove .spec files
    for f in os.listdir('.'):
        if f.endswith('.spec'):
            print(f"Removing {f}")
            os.remove(f)


def build_executable():
    """Generate the executable using PyInstaller."""
    platform_name = get_platform_name()
    print(f"\n🔨 Building executable for {platform_name}...\n")
    
    # Base PyInstaller arguments
    args = [
        'pyinstaller',
        '--name=MyDocker',
        '--onefile',  # Generate a single executable file
        '--windowed',  # Don't show console (important for GUI apps)
        '--icon=src/icon.png',  # Application icon
        '--add-data=src/icon.png:.',  # Include icon in resources
        '--clean',  # Clean cache before building
        '--noconfirm',  # Don't ask for confirmation to overwrite
    ]
    
    # Platform-specific configurations
    if platform_name == 'macos':
        args.extend([
            '--osx-bundle-identifier=com.mydocker.app',
            '--target-arch=universal2',  # Support for Intel and Apple Silicon
        ])
    
    # Main file
    args.append('src/main.py')
    
    # Execute PyInstaller
    try:
        result = subprocess.run(args, check=True)
        print(f"\n✅ Build completed successfully!")
        print(f"📦 Executable generated at: dist/MyDocker")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error generating executable: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False


def create_spec_file():
    """Create a custom .spec file for greater control."""
    platform_name = get_platform_name()
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/icon.png', '.')],
    hiddenimports=[
        'docker',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyDocker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console for GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='{"universal2" if platform_name == "macos" else None}',
    codesign_identity=None,
    entitlements_file=None,
    icon='src/icon.png',
)

{"'''app = BUNDLE(exe, name='MyDocker.app', icon='src/icon.png', bundle_identifier='com.mydocker.app')'''" if platform_name == "macos" else ""}
"""
    
    with open('MyDocker.spec', 'w') as f:
        f.write(spec_content)
    
    print("📄 .spec file created: MyDocker.spec")
    print("   You can edit this file to customize the build")
    print("   and then run: pyinstaller MyDocker.spec\n")


def main():
    """Main function."""
    print("=" * 60)
    print("🐳 My Docker - Build Script")
    print("=" * 60)
    
    # Check if icon.png exists
    if not os.path.exists('src/icon.png'):
        print("\n⚠️  Warning: src/icon.png not found!")
        print("   Build will continue but without an icon.\n")
    
    # Options menu
    print("\nOptions:")
    print("1. Quick build (one-file)")
    print("2. Generate .spec file for custom build")
    print("3. Clean build files")
    print("4. Build using existing .spec")
    print("0. Exit")
    
    choice = input("\nChoose an option: ").strip()
    
    if choice == '1':
        clean_build_dirs()
        build_executable()
    elif choice == '2':
        create_spec_file()
    elif choice == '3':
        clean_build_dirs()
        print("✅ Build files removed")
    elif choice == '4':
        if os.path.exists('MyDocker.spec'):
            subprocess.run(['pyinstaller', 'MyDocker.spec'])
        else:
            print("❌ MyDocker.spec file not found. Use option 2 first.")
    elif choice == '0':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid option")


if __name__ == '__main__':
    main()
