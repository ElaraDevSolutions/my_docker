# Build Script - My Docker

This directory contains scripts to generate standalone executables for the My Docker application.

## Installation of Dependencies

```bash
pip install -r requirements.txt
```

## How to Generate the Executable

### Method 1: Interactive Script (Recommended)

```bash
python build.py
```

Choose one of the menu options:
- **Option 1**: Quick build - generates a single executable file
- **Option 2**: Generate .spec file for advanced customization
- **Option 3**: Clean previous build files
- **Option 4**: Build using existing .spec file

### Method 2: Direct PyInstaller

#### macOS
```bash
pyinstaller --name=MyDocker \
    --onefile \
    --windowed \
    --icon=src/icon.png \
    --add-data="src/icon.png:." \
    --target-arch=universal2 \
    --osx-bundle-identifier=com.mydocker.app \
    src/main.py
```

#### Linux
```bash
pyinstaller --name=MyDocker \
    --onefile \
    --windowed \
    --icon=src/icon.png \
    --add-data="src/icon.png:." \
    src/main.py
```

## Result

After the build, the executable will be in:
- **Directory**: `dist/`
- **File**: `MyDocker` (Linux) or `MyDocker.app` (macOS bundle)

## Important Notes

### macOS
- The executable generated with `--target-arch=universal2` works on Intel and Apple Silicon
- For distribution, consider signing the app with an Apple developer certificate
- Users may need to allow execution in "System Preferences > Security"

### Linux
- The executable is specific to the distribution where it was compiled
- Recommended to compile on a common distribution (Ubuntu LTS)
- Users may need to install `libxcb` and other Qt libraries

### Both Platforms
- Docker must be installed on the user's machine
- The application will check and try to start Docker automatically
- The `icon.png` file must be in the `src/` directory

## File Structure

```
my_docker/
├── build.py              # Interactive build script
├── requirements.txt      # Python dependencies
├── src/
│   ├── main.py          # Main code
│   └── icon.png         # Application icon
├── build/               # Temporary files (ignore)
├── dist/                # Final executable
└── MyDocker.spec        # PyInstaller config (optional)
```

## Troubleshooting

### Error: "command not found: pyinstaller"
```bash
pip install pyinstaller
```

### Error: PyQt6 not found in executable
Add to the .spec file:
```python
hiddenimports=['PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets']
```

### Executable too large
Use UPX to compress (already included in build.py):
```bash
pip install upx-ucl  # macOS: brew install upx
```

### Permission error on Linux
```bash
chmod +x dist/MyDocker
```

## Distribution

To distribute your application:

1. **macOS**: Create a DMG or distribute the .app file
2. **Linux**: Create a .deb/.rpm or distribute the binary with a .desktop file
3. **Both**: Consider using GitHub Releases to host the executables

## Cross-Platform Build

To generate executables for both platforms:

1. Compile on macOS to generate the macOS version
2. Compile on Linux to generate the Linux version
3. Use CI/CD (GitHub Actions) to automate cross-platform builds

### GitHub Actions Example

```yaml
name: Build
on: [push]
jobs:
  build:
    strategy:
      matrix:
        os: [macos-latest, ubuntu-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python build.py
      - uses: actions/upload-artifact@v2
        with:
          name: MyDocker-${{ matrix.os }}
          path: dist/
```
