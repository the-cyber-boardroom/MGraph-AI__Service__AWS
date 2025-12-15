# Creating Services from MGraph-AI__Service__AWS

This guide describes how to create new MGraph-AI services from this template using a clean, automated approach that enables future template updates.

## 🚀 Quick Start

### Step 1: Create Empty Repository on GitHub

1. Go to GitHub and create a new repository
2. Name it following the pattern: `MGraph-AI__Service__YourName`
   - Example: `MGraph-AI__Service__Auth`
   - Example: `MGraph-AI__Service__Analytics`
3. **Important**: Create it as a **bare repository**:
   - ❌ Do NOT add README
   - ❌ Do NOT add .gitignore
   - ❌ Do NOT add license

### Step 2: Clone Your Empty Repository

```bash
git clone git@github.com:the-cyber-boardroom/MGraph-AI__Service__YourName.git
cd MGraph-AI__Service__YourName
```

### Step 3: Run the Setup Script

```bash
# Download and run the setup script
curl -O https://raw.githubusercontent.com/the-cyber-boardroom/MGraph-AI__Service__AWS/main/setup-from-template.sh
chmod +x setup-from-template.sh
./setup-from-template.sh
```

The script will:
1. Pull the template from `MGraph-AI__Service__AWS`
2. Extract service name from your repo name (e.g., `MGraph-AI__Service__Auth` → `mgraph_ai_service_auth`)
3. Rename all files and folders
4. Replace all placeholders
5. Commit the changes
6. Set up template remote for future updates

## 🔧 Manual Process (if needed)

If you prefer to run the steps manually:

```bash
# 1. Add template as remote and pull
git remote add template https://github.com/the-cyber-boardroom/MGraph-AI__Service__AWS.git
git fetch template
git merge template/main --allow-unrelated-histories

# 2. Extract service name from repo
REPO_NAME=$(basename -s .git `git config --get remote.origin.url`)
SERVICE_NAME=$(echo $REPO_NAME | sed 's/MGraph-AI__Service__/mgraph_ai_service_/g' | tr '[:upper:]' '[:lower:]')

# 3. Run the rename script
./scripts/rename-service.sh $SERVICE_NAME

# 4. Commit changes
git add .
git commit -m "Initialize from MGraph-AI__Service__AWS"

# 5. Push to GitHub
git push -u origin main
```

## 📜 The Setup Script

Here's what `setup-from-template.sh` does:

```bash
#!/bin/bash
set -e

echo "🚀 Setting up MGraph-AI Service from template..."

# 1. Get repo name and derive service name
REPO_URL=$(git config --get remote.origin.url)
REPO_NAME=$(basename -s .git "$REPO_URL")

# Extract service name (MGraph-AI__Service__Auth -> mgraph_ai_service_auth)
SERVICE_NAME=$(echo "$REPO_NAME" | sed 's/MGraph-AI__Service__/mgraph_ai_service_/' | tr '[:upper:]' '[:lower:]' | tr '-' '_')
SERVICE_NAME_HYPHEN=$(echo "$SERVICE_NAME" | tr '_' '-')
SERVICE_DISPLAY_NAME=$(echo "$REPO_NAME" | sed 's/__/ /g' | sed 's/-/ /g')

echo "📦 Repository: $REPO_NAME"
echo "🔧 Service name: $SERVICE_NAME"
echo "📋 Display name: $SERVICE_DISPLAY_NAME"

# 2. Add template remote and pull
echo "📥 Pulling from template..."
git remote add template https://github.com/the-cyber-boardroom/MGraph-AI__Service__AWS.git
git fetch template
git merge template/main --allow-unrelated-histories -m "Initial template import"

# 3. Rename template service to actual service
echo "🔄 Renaming service..."

# Rename directories
find . -type d -name "*mgraph_ai_service_aws*" | while read dir; do
    newdir=$(echo "$dir" | sed "s/mgraph_ai_service_aws/$SERVICE_NAME/g")
    mv "$dir" "$newdir"
done

# Replace in all files
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.sh" -o -name "*.txt" \) | while read file; do
    # Skip .git directory
    if [[ "$file" == *".git"* ]]; then
        continue
    fi
    
    # Replace service names
    sed -i.bak "s/mgraph_ai_service_aws/$SERVICE_NAME/g" "$file"        
    sed -i.bak "s/MGraph-AI__Service__AWS/$REPO_NAME/g" "$file"
    
    # Clean up backup files
    rm -f "$file.bak"
done

# 4. Update version to v0.1.0
echo "v0.1.0" > "$SERVICE_NAME/version"

# 5. Create .template directory for tracking
mkdir -p .template
echo "TEMPLATE_VERSION=1.0.0" > .template/VERSION
echo "TEMPLATE_COMMIT=$(git rev-parse template/main)" >> .template/VERSION
echo "CREATED_DATE=$(date -u +%Y-%m-%d)" >> .template/VERSION
echo "SERVICE_NAME=$SERVICE_NAME" >> .template/VERSION

# 6. Commit changes
echo "💾 Committing changes..."
git add .
git commit -m "Initialize $SERVICE_DISPLAY_NAME from template

- Based on MGraph-AI__Service__AWS v1.0.0
- Service name: $SERVICE_NAME
- Repository: $REPO_NAME"

# 7. Push to origin
echo "⬆️ Pushing to GitHub..."
git push -u origin main

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Review the generated files"
echo "2. Update the README.md with your service details"
echo "3. Configure GitHub secrets for deployment"
echo "4. Run: pip install -r requirements-test.txt"
echo "5. Run: ./scripts/run-locally.sh"
```

## 🔄 Syncing Template Updates

After initial setup, you can pull template updates:

```bash
# Fetch latest template changes
git fetch template

# Option 1: Merge all updates
git merge template/main

# Option 2: Cherry-pick specific updates
git log template/main --oneline
git cherry-pick <commit-hash>
```

## 🏗️ Repository Naming Convention

Your repository name determines the service configuration:

| Repository Name | Service Name (code) | Display Name |
|----------------|-------------------|--------------|
| `MGraph-AI__Service__Auth` | `mgraph_ai_service_auth` | MGraph-AI Service Auth |
| `MGraph-AI__Service__AWS` | `mgraph_ai_service_aws` | MGraph AI Service AWS |
| `MGraph-AI__Service__Data-Pipeline` | `mgraph_ai_service_data_pipeline` | MGraph-AI Service Data Pipeline |

## 📁 Template Structure

The template uses `mgraph_ai_service_aws` as the placeholder service name:

```
MGraph-AI__Service__AWS/
├── mgraph_ai_service_aws/     # Will be renamed to your service
├── tests/
├── docs/
├── scripts/
│   └── rename-service.sh           # Handles renaming
├── setup-from-template.sh          # Main setup script
└── README.md
```

## ⚡ Advantages of This Approach

1. **Clean Start**: Each service begins with its own repo
2. **Name-Driven**: Service name automatically derived from repo name
3. **Template Updates**: Can still pull updates from template
4. **Single Script**: One command sets everything up
5. **No Manual Renaming**: Script handles all replacements

## 🎯 Best Practices

### For Template Maintainers:
- Always use `mgraph_ai_service_aws` as the placeholder
- Document any new placeholders in the template
- Tag template versions for easy reference
- Keep setup script updated

### for Service creators:
- Follow the naming convention strictly
- Review all renamed files after setup
- Document any service-specific changes
- Keep template remote for future updates

## 🔍 Troubleshooting

### If the script fails:
```bash
# Check what changed
git status

# Reset if needed
git reset --hard
git clean -fd

# Try manual process
```

### Common issues:
- **Permission denied**: Make sure you have write access to the repo
- **Merge conflicts**: Resolve manually, usually happens if repo wasn't empty
- **Rename failures**: Check for special characters in repo name

## 📊 Summary

This approach provides:
- ✅ One-command service creation
- ✅ Automatic naming from repository
- ✅ Clean Git history
- ✅ Template update capability
- ✅ No external dependencies

Perfect for quickly spinning up new MGraph-AI services while maintaining consistency and updatability!