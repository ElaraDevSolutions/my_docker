#!/bin/bash

# Script to create and push a new release
# Usage: ./release.sh 1.0.0 "Change description"

set -e

VERSION=$1
DESCRIPTION=$2

if [ -z "$VERSION" ]; then
    echo "❌ Error: Version not specified"
    echo "Usage: ./release.sh <version> [description]"
    echo "Example: ./release.sh 1.0.0 'First release'"
    exit 1
fi

# Remove 'v' prefix if it exists
VERSION=${VERSION#v}

# Add 'v' prefix for the tag
TAG="v$VERSION"

echo "🏷️  Creating release $TAG"
echo ""

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "⚠️  There are uncommitted changes. Continue? (y/n)"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo "❌ Release cancelled"
        exit 1
    fi
fi

# Update main branch
echo "📥 Updating main branch..."
git pull origin main || git pull origin master

# Create the tag
echo "🏷️  Creating tag $TAG..."
if [ -z "$DESCRIPTION" ]; then
    git tag -a "$TAG" -m "Release $TAG"
else
    git tag -a "$TAG" -m "$DESCRIPTION"
fi

# Push the tag to remote repository
echo "📤 Pushing tag to GitHub..."
git push origin "$TAG"

echo ""
echo "✅ Tag $TAG created and pushed successfully!"
echo ""
echo "🔄 GitHub Actions will now:"
echo "   1. Build executable for macOS"
echo "   2. Build executable for Linux"
echo "   3. Create a release with the files"
echo ""
echo "🌐 Track progress at: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions"
echo ""
echo "📦 After the build, the release will be at:"
echo "   https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/releases/tag/$TAG"
