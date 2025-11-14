# Versioning and Release Guide

This document describes how to create and distribute new versions of My Docker.

## 📋 Versioning Strategy

We use **Semantic Versioning** (SemVer): `MAJOR.MINOR.PATCH`

- **MAJOR** (1.0.0): Incompatible API changes
- **MINOR** (0.1.0): New functionality compatible with previous versions
- **PATCH** (0.0.1): Bug fixes

### Examples
- `1.0.0` - First stable version
- `1.1.0` - New functionality (e.g., compose files support)
- `1.1.1` - Bug fix
- `2.0.0` - Significant change (e.g., complete rewrite)

## 🚀 How to Create a Release

### Automatic Method (Recommended)

1. **Commit all changes:**
```bash
git add .
git commit -m "feat: your description"
git push origin main
```

2. **Run the release script:**
```bash
./release.sh 1.0.0 "First stable release"
```

The script will:
- ✅ Create the tag locally
- ✅ Push the tag to GitHub
- ✅ Trigger GitHub Actions
- ✅ Compile executables for macOS and Linux
- ✅ Create the release automatically

### Manual Method

1. **Create the tag:**
```bash
git tag -a v1.0.0 -m "Release 1.0.0"
```

2. **Push the tag:**
```bash
git push origin v1.0.0
```

3. **Wait for the build:**
   - Access: `https://github.com/your-username/my_docker/actions`
   - Wait for the workflow to complete

4. **Check the release:**
   - Access: `https://github.com/your-username/my_docker/releases`

## 📦 What Happens During the Build

GitHub Actions will automatically:

1. **Checkout** the code at the specified tag
2. **Setup** Python 3.11
3. **Install** dependencies
4. **Build** in parallel:
   - macOS (Universal Binary - Intel + Apple Silicon)
   - Linux (Ubuntu 22.04)
5. **Package**:
   - macOS: `MyDocker-macos.zip`
   - Linux: `MyDocker-linux.tar.gz`
6. **Upload** files to the release
7. **Publish** the release on GitHub

## 📝 Checklist Before Creating a Release

- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated (README.md)
- [ ] Changelog prepared
- [ ] Version updated in relevant files
- [ ] Main branch updated

## 🔄 Development Workflow

```
main (protected)
  ↓
  ├─ feature/new-feature
  ├─ fix/fix-bug
  └─ release/v1.0.0
       ↓
     merge → main
       ↓
   tag v1.0.0
       ↓
   GitHub Actions
       ↓
   Published Release
```

## 🏷️ Managing Tags

### List all tags:
```bash
git tag
```

### See tag details:
```bash
git show v1.0.0
```

### Delete local tag:
```bash
git tag -d v1.0.0
```

### Delete remote tag:
```bash
git push origin --delete v1.0.0
```

### Redo a release (use with caution):
```bash
# Delete locally and remotely
git tag -d v1.0.0
git push origin --delete v1.0.0

# Delete the release on GitHub
# (use the web interface: Settings > Releases)

# Create again
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

## 🐛 Troubleshooting

### Build failed on GitHub Actions

1. Go to `Actions` on GitHub
2. Click on the failed workflow
3. View logs to identify the error
4. Fix the problem
5. Delete the tag and release
6. Create again

### Release created but no files

- Check if the workflow completed successfully
- Check token permissions: `Settings > Actions > General > Workflow permissions`
- Must be checked: "Read and write permissions"

### Executable doesn't work

- **macOS**: Users need to right-click > Open on first run
- **Linux**: Check execution permission: `chmod +x MyDocker`

## 📊 Changelog Example

Keep a `CHANGELOG.md` file updated:

```markdown
# Changelog

## [1.0.0] - 2025-11-14
### Added
- Container management via system tray
- Automatic Docker startup
- Support for macOS and Linux

### Changed
- Improved interface

### Fixed
- Bug fix in Docker detection

## [0.1.0] - 2025-11-01
### Added
- Initial version
```

## 🎯 Best Practices

1. **Never commit executables** in the repository
2. **Use annotated tags** (with `-a`), not lightweight tags
3. **Follow SemVer** rigorously
4. **Test locally** before creating the tag
5. **Write good release messages**
6. **Keep a CHANGELOG** updated
7. **Protect the main branch** to avoid direct pushes

## 🌐 Distribution

After the release is created, share with:

```markdown
🎉 My Docker v1.0.0 is available!

📦 Download:
- macOS: https://github.com/your-user/my_docker/releases/download/v1.0.0/MyDocker-macos.zip
- Linux: https://github.com/your-user/my_docker/releases/download/v1.0.0/MyDocker-linux.tar.gz

📝 Changelog: https://github.com/your-user/my_docker/releases/tag/v1.0.0
```

## 📚 Additional Resources

- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Git Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
