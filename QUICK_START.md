# 🚀 Quick Start Guide

Quick guide to get started with My Docker.

## 📥 For End Users

### Download and Installation

1. **Access the releases page:**
   ```
   https://github.com/your-username/my_docker/releases/latest
   ```

2. **Download the file for your system:**
   - macOS: `MyDocker-macos.zip`
   - Linux: `MyDocker-linux.tar.gz`

3. **Install:**
   
   **macOS:**
   ```bash
   unzip MyDocker-macos.zip
   xattr -cr MyDocker.app  # First time only
   open MyDocker.app
   ```
   
   **Linux:**
   ```bash
   tar -xzf MyDocker-linux.tar.gz
   chmod +x MyDocker
   ./MyDocker
   ```

4. **Use:**
   - An icon will appear in the system tray
   - Click to see your Docker containers
   - Click on a container to start/stop

## 💻 For Developers

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/my_docker.git
cd my_docker

# Install dependencies
pip install -r requirements.txt

# Run in dev mode
python src/main.py
```

### Making Changes

```bash
# Create a branch
git checkout -b feature/my-feature

# Make your changes
# ... edit files ...

# Test locally
python src/main.py

# Commit
git add .
git commit -m "feat: change description"

# Push
git push origin feature/my-feature

# Open a Pull Request on GitHub
```

### Creating a Release

```bash
# Update CHANGELOG.md with changes

# Commit all changes
git add .
git commit -m "chore: prepare release 1.0.0"
git push origin main

# Create and push the tag
./release.sh 1.0.0 "Release description"

# GitHub Actions will:
# - Compile for macOS and Linux
# - Create the release automatically
# - Attach the executables
```

## 📚 Complete Documentation

- **[README.md](README.md)** - Overview and features
- **[BUILD.md](BUILD.md)** - How to compile executables
- **[RELEASE.md](RELEASE.md)** - Versioning and releases process
- **[CHANGELOG.md](CHANGELOG.md)** - Change history

## ❓ Common Problems

### Docker doesn't start automatically
```bash
# Linux: add your user to docker group
sudo usermod -aG docker $USER
# Log out and log in again
```

### macOS blocks execution
```bash
# Remove quarantine
xattr -cr MyDocker.app
```

### Error "Docker not installed"
- macOS: Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux: `sudo apt install docker.io`

## 🆘 Need Help?

- 🐛 **Bug?** Open an [issue](https://github.com/your-username/my_docker/issues)
- 💡 **Suggestion?** Open a [discussion](https://github.com/your-username/my_docker/discussions)
- 📧 **Contact:** [your-email@example.com]
