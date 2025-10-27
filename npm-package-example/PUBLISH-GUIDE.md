# Publishing Guide

## 📦 How to Publish to npm

### Prerequisites

1. **npm account**: Create at https://www.npmjs.com/signup
2. **npm CLI login**:
   ```bash
   npm login
   ```

### Step-by-Step Publishing

#### 1. Prepare Package

```bash
# Clone or navigate to your package directory
cd create-claude-agent

# Install dependencies
npm install

# Copy template files from your main project
cp -r ../.claude/* template/
```

#### 2. Test Locally

```bash
# Link package globally
npm link

# Test in another directory
cd ~/test-project
npx create-claude-agent

# Verify installation
ls -la .claude/
```

#### 3. Update Version

```bash
# First release
npm version 1.0.0

# Or for updates:
npm version patch   # 1.0.0 -> 1.0.1
npm version minor   # 1.0.0 -> 1.1.0
npm version major   # 1.0.0 -> 2.0.0
```

#### 4. Publish to npm

```bash
# First time publish
npm publish --access public

# For scoped packages (e.g., @yourname/create-claude-agent)
npm publish --access public
```

#### 5. Verify Published Package

```bash
# Check on npm
npm info create-claude-agent

# Test installation
npx create-claude-agent
```

---

## 🏷️ Package Naming Options

### Option 1: Simple Name
```json
{
  "name": "create-claude-agent"
}
```
**Usage:** `npx create-claude-agent`

### Option 2: Scoped Package
```json
{
  "name": "@yourname/create-claude-agent"
}
```
**Usage:** `npx @yourname/create-claude-agent`

### Option 3: Organization Package
```json
{
  "name": "@claude-templates/multi-agent"
}
```
**Usage:** `npx @claude-templates/multi-agent`

---

## 📊 Versioning Strategy

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
  - Changed agent structure
  - Removed features

- **MINOR** (1.0.0 → 1.1.0): New features (backward compatible)
  - Added new agent
  - New context patterns

- **PATCH** (1.0.0 → 1.0.1): Bug fixes
  - Fixed typos in docs
  - Updated dependencies

---

## 🔒 Publishing Checklist

Before `npm publish`:

- [ ] All files in `template/` are up-to-date
- [ ] `package.json` version updated
- [ ] `README.md` reviewed and accurate
- [ ] Test with `npm link` locally
- [ ] `bin/cli.js` has correct permissions (`chmod +x`)
- [ ] All dependencies in `package.json` are necessary
- [ ] `.npmignore` or `files` field configured correctly
- [ ] LICENSE file exists
- [ ] Repository URL in `package.json` is correct

---

## 🚀 Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to npm

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          registry-url: 'https://registry.npmjs.org'

      - run: npm ci

      - run: npm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**Setup:**
1. Go to https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. Create "Automation" token
3. Add to GitHub: Settings → Secrets → New repository secret
   - Name: `NPM_TOKEN`
   - Value: (your token)

---

## 📈 Post-Publish

### Update README badges

```markdown
[![npm version](https://badge.fury.io/js/create-claude-agent.svg)](https://www.npmjs.com/package/create-claude-agent)
[![npm downloads](https://img.shields.io/npm/dm/create-claude-agent.svg)](https://www.npmjs.com/package/create-claude-agent)
```

### Monitor Usage

```bash
# Check download stats
npm info create-claude-agent

# View on npm
open https://www.npmjs.com/package/create-claude-agent
```

---

## 🔄 Updating the Package

```bash
# 1. Make changes to template files
cp -r ../.claude/* template/

# 2. Commit changes
git add .
git commit -m "feat: add new agent pattern"

# 3. Bump version
npm version minor

# 4. Push to GitHub
git push --follow-tags

# 5. Publish to npm
npm publish
```

---

## 🛡️ Best Practices

1. **Test before publishing**: Always `npm link` and test locally
2. **Keep dependencies minimal**: Only include what's necessary
3. **Document breaking changes**: In CHANGELOG.md
4. **Use .npmignore**: Exclude unnecessary files
5. **Add LICENSE**: MIT is common for templates
6. **Tag releases on GitHub**: Use semantic versioning tags

---

## 🆘 Troubleshooting

### Error: "Package name already exists"
```bash
# Use scoped package instead
npm init --scope=yourname
```

### Error: "You need to authorize this machine"
```bash
npm login
```

### Error: "403 Forbidden"
```bash
# Check if package name is taken
npm search create-claude-agent

# Or use different name
```

---

## 📝 Example: Complete Flow

```bash
# 1. Setup
cd create-claude-agent
npm install

# 2. Copy latest template
cp -r ../.claude/* template/

# 3. Test locally
npm link
cd ~/test && npx create-claude-agent

# 4. Publish
cd ~/create-claude-agent
npm version 1.0.0
npm publish --access public

# 5. Verify
npx create-claude-agent@latest
```

**Done!** 🎉 Your package is now available via `npx create-claude-agent`
