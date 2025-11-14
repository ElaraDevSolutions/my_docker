# My Docker

System tray application to manage Docker containers in a simple and visual way, compatible with macOS and Linux.

## ✨ Features

- 🐳 Docker container management via tray icon
- ▶️ Start/Stop containers with one click
- 🟢 Real-time container status visualization
- 🔄 Automatic container list updates
- 🚀 Automatically starts Docker if not running
- ⚠️ Intelligent Docker installation verification

## 📋 Requirements

### For Development
- Python 3.8+
- Docker installed and configured
- PyQt6
- docker-py

### For Usage (Executable)
- Docker installed
- macOS 10.13+ or Linux (Ubuntu 20.04+)

## 🚀 Installation for Development

1. Clone the repository:
```bash
git clone <your-repo>
cd my_docker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## 📦 Download (Ready-to-Use Executable)

**No need to compile!** Download the ready-to-use executable for your system:

👉 **[Releases](https://github.com/your-username/my_docker/releases/latest)**

- **macOS** (Intel & Apple Silicon): `MyDocker-macos.zip`
- **Linux**: `MyDocker-linux.tar.gz`

### Quick Installation

**macOS:**
```bash
# Download and unzip
unzip MyDocker-macos.zip

# First run
xattr -cr MyDocker.app  # Remove quarantine
open MyDocker.app
```

**Linux:**
```bash
# Download and extract
tar -xzf MyDocker-linux.tar.gz

# Give permission and run
chmod +x MyDocker
./MyDocker
```

## 🛠️ Local Compilation (Optional)

If you want to compile the code yourself:

### Quick Local Build
```bash
pip install -r requirements.txt
python build.py
```

The executable will be generated in `dist/MyDocker`.

### Build and Release Documentation

- **[BUILD.md](BUILD.md)** - Detailed compilation instructions
- **[RELEASE.md](RELEASE.md)** - How to create releases and tags

## 💡 How to Use

1. **Run the application**: 
   - Development: `python src/main.py`
   - Executable: Double-click `MyDocker`

2. **Tray icon**: An icon will appear in the system tray

3. **Manage containers**:
   - Click the icon to see the container list
   - 🟢 = Container running
   - ⚪ = Container stopped
   - Click a container to start/stop

4. **Automatic Docker**:
   - If Docker is not running, the app starts it automatically
   - Waits for Docker to be ready before opening
   - Shows error if Docker is not installed

## 🏗️ Project Structure

```
my_docker/
├── src/
│   ├── main.py          # Main application code
│   └── icon.png         # Application icon
├── build.py             # Script to generate executables
├── requirements.txt     # Python dependencies
├── BUILD.md            # Detailed build documentation
└── README.md           # This file
```

## 🌍 Compatibility

| System | Status | Notes |
|---------|--------|-------|
| macOS Intel | ✅ Supported | Tested on macOS 11+ |
| macOS Apple Silicon | ✅ Supported | Universal binary |
| Linux (systemd) | ✅ Supported | Ubuntu, Fedora, Arch |
| Linux (sysvinit) | ✅ Supported | Debian, CentOS |
| Windows | ⚠️ Not tested | May work with adaptations |

## 🔧 Troubleshooting

### Docker doesn't start automatically on Linux
The application tries to start Docker but may need sudo permissions. Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```
Then log out and log in again.

### Error "Docker is not installed"
Install Docker:
- **macOS**: [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- **Linux**: `sudo apt install docker.io` (Ubuntu/Debian)

### Executable won't open on macOS
```bash
xattr -cr dist/MyDocker.app  # Remove quarantine
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or pull requests.

### How to Contribute
1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/MyFeature`)
3. Commit your changes (`git commit -m 'feat: Add new feature'`)
4. Push to the branch (`git push origin feature/MyFeature`)
5. Open a Pull Request

### Creating a Release
See [RELEASE.md](RELEASE.md) for instructions on how to create a new version.

## 📄 License

[Add your license here]

## 💖 Support

If this project was useful to you, consider supporting via [Patreon](https://patreon.com/ElaraDevSolutions).
