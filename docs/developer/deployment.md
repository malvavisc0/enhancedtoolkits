# GitHub Pages Deployment Guide

## 🚀 Deploy Enhanced Toolkits Documentation to GitHub Pages

This guide shows you how to deploy your MkDocs documentation to GitHub Pages for free hosting.

## Method 1: Manual Deployment (Recommended)

### Prerequisites
```bash
# Install MkDocs and dependencies
pip install -r docs/requirements.txt

# Verify MkDocs works locally
mkdocs serve
```

### Deploy to GitHub Pages
```bash
# From your project root directory
mkdocs gh-deploy
```

This command will:
- Build your documentation
- Create/update the `gh-pages` branch
- Push the built site to GitHub Pages
- Make it available at `https://malvavisc0.github.io/enhancedtoolkits/`

### First-Time Setup
If this is your first deployment:

1. **Enable GitHub Pages** in your repository:
   - Go to repository **Settings**
   - Scroll to **Pages** section
   - Set **Source** to "Deploy from a branch"
   - Select **Branch**: `gh-pages`
   - Click **Save**

2. **Deploy the documentation**:
   ```bash
   mkdocs gh-deploy --force  # Use --force for first deployment
   ```

3. **Access your site**:
   - Visit `https://malvavisc0.github.io/enhancedtoolkits/`
   - May take a few minutes to become available

## Method 2: GitHub Actions (Automated)

### Create GitHub Actions Workflow

Create `.github/workflows/docs.yml`:

```yaml
name: Deploy Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r docs/requirements.txt
    
    - name: Build documentation
      run: mkdocs build
    
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v2
      with:
        path: ./site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v2
```

### Enable GitHub Actions Deployment

1. **Repository Settings**:
   - Go to **Settings** > **Pages**
   - Set **Source** to "GitHub Actions"

2. **Commit the workflow**:
   ```bash
   git add .github/workflows/docs.yml
   git commit -m "Add GitHub Pages deployment workflow"
   git push
   ```

3. **Automatic deployment**:
   - Documentation deploys automatically on every push to `main`
   - Check **Actions** tab for deployment status

## Method 3: Custom Domain (Optional)

### Set Up Custom Domain

1. **Add CNAME file**:
   ```bash
   echo "docs.enhancedtoolkits.com" > docs/CNAME
   ```

2. **Update mkdocs.yml**:
   ```yaml
   site_url: https://docs.enhancedtoolkits.com
   ```

3. **Configure DNS**:
   - Add CNAME record: `docs.enhancedtoolkits.com` → `malvavisc0.github.io`
   - Or A records pointing to GitHub Pages IPs

4. **Enable HTTPS**:
   - GitHub Pages automatically provides SSL certificates
   - Check "Enforce HTTPS" in repository settings

## Deployment Configuration

### Update mkdocs.yml for GitHub Pages

Ensure your `mkdocs.yml` has the correct settings:

```yaml
# Site Information
site_name: Enhanced Toolkits
site_url: https://malvavisc0.github.io/enhancedtoolkits/

# Repository
repo_name: malvavisc0/enhancedtoolkits
repo_url: https://github.com/malvavisc0/enhancedtoolkits
edit_uri: edit/main/docs/

# GitHub Pages specific settings
use_directory_urls: true
```

### Handle MkDocstrings Issues in CI

For GitHub Actions deployment, add this to your workflow:

```yaml
- name: Install package for MkDocstrings
  run: |
    pip install -e .
  continue-on-error: true  # Continue even if package install fails

- name: Build documentation
  run: mkdocs build
```

Or disable problematic auto-generated pages in CI:

```yaml
- name: Build documentation (fallback)
  run: |
    # Remove auto-generated API pages if module import fails
    if ! python -c "import enhancedtoolkits" 2>/dev/null; then
      echo "Module not available, using manual reference only"
      # Remove auto-generated API pages from navigation
      sed -i '/Auto-Generated APIs:/,/Time Value Calculator:/d' mkdocs.yml
    fi
    mkdocs build
```

## Troubleshooting Deployment

### Common Issues

#### 1. Build Fails Due to MkDocstrings
**Solution**: Use manual reference only for deployment
```bash
# Temporarily disable auto-generated APIs
# Edit mkdocs.yml to comment out problematic pages
mkdocs gh-deploy
```

#### 2. Site Not Updating
**Solutions**:
```bash
# Force rebuild and deploy
mkdocs gh-deploy --force

# Clear browser cache
# Check GitHub Pages settings
```

#### 3. 404 Errors
**Solutions**:
- Verify `site_url` in `mkdocs.yml`
- Check GitHub Pages source branch
- Ensure `gh-pages` branch exists

#### 4. CSS/JS Not Loading
**Solution**: Use relative paths in `mkdocs.yml`:
```yaml
extra_css:
  - assets/css/custom.css
extra_javascript:
  - assets/js/custom.js
```

### Deployment Checklist

Before deploying:

- [ ] Test locally: `mkdocs serve`
- [ ] Check all links work
- [ ] Verify images and assets load
- [ ] Test manual reference works
- [ ] Commit all changes to git
- [ ] Push to main branch

## Deployment Commands

### Quick Deployment
```bash
# One-command deployment
mkdocs gh-deploy --clean --message "Deploy documentation"
```

### Development Workflow
```bash
# 1. Make documentation changes
# 2. Test locally
mkdocs serve

# 3. Commit changes
git add docs/
git commit -m "Update documentation"
git push

# 4. Deploy to GitHub Pages
mkdocs gh-deploy
```

### Advanced Options
```bash
# Deploy with custom commit message
mkdocs gh-deploy --message "Update docs with new API reference"

# Deploy specific branch
mkdocs gh-deploy --remote-branch gh-pages

# Deploy with verbose output
mkdocs gh-deploy --verbose

# Clean build before deploy
mkdocs gh-deploy --clean
```

## Monitoring Deployment

### Check Deployment Status
1. **GitHub Actions**: Check the **Actions** tab for build status
2. **GitHub Pages**: Check **Settings** > **Pages** for deployment status
3. **Site Health**: Visit your site URL to verify it's working

### Deployment Logs
```bash
# View recent deployments
git log --oneline gh-pages

# Check GitHub Pages build logs in repository settings
```

## Best Practices

### 1. Automated Deployment
- Use GitHub Actions for automatic deployment
- Deploy on every push to main branch
- Include build status badges in README

### 2. Content Strategy
- Use manual reference as primary API documentation
- Enable auto-generated APIs only when module is available
- Include comprehensive examples and guides

### 3. Performance
- Optimize images and assets
- Use CDN for external resources
- Enable GitHub Pages caching

### 4. Maintenance
- Regular dependency updates
- Monitor for broken links
- Keep documentation in sync with code changes

## Example Deployment Script

Create `scripts/deploy-docs.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 Deploying Enhanced Toolkits Documentation"

# Test locally first
echo "📋 Testing documentation locally..."
mkdocs serve --dev-addr=127.0.0.1:8001 &
SERVER_PID=$!
sleep 5
kill $SERVER_PID

# Build and deploy
echo "🔨 Building and deploying to GitHub Pages..."
mkdocs gh-deploy --clean --message "Deploy docs: $(date)"

echo "✅ Documentation deployed successfully!"
echo "🌐 Visit: https://malvavisc0.github.io/enhancedtoolkits/"
```

Make it executable:
```bash
chmod +x scripts/deploy-docs.sh
./scripts/deploy-docs.sh
```

## Result

After deployment, your Enhanced Toolkits documentation will be available at:
- **Primary URL**: `https://malvavisc0.github.io/enhancedtoolkits/`
- **Custom domain** (if configured): `https://docs.enhancedtoolkits.com/`

The site will feature:
- Professional documentation with search
- Complete API reference (manual + auto-generated)
- Responsive design for all devices
- Fast loading with GitHub Pages CDN
- Automatic HTTPS encryption

Your documentation is now publicly accessible and will update automatically with your chosen deployment method! 🚀