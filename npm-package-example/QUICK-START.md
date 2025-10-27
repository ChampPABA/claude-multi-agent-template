# Quick Start Guide

## 🎯 Goal
Transform your template into an npm package that users can install via:
```bash
npx create-claude-agent
```

---

## ⚡ TL;DR (5 Minutes Setup)

```bash
# 1. Create package directory
mkdir create-claude-agent
cd create-claude-agent

# 2. Initialize npm package
npm init -y

# 3. Create structure
mkdir -p bin template
cp -r /path/to/.claude/* template/

# 4. Create CLI script
touch bin/cli.js
chmod +x bin/cli.js

# 5. Install dependencies
npm install chalk ora prompts fs-extra

# 6. Test locally
npm link
cd ~/test-project
npx create-claude-agent

# 7. Publish to npm
npm login
npm publish --access public

# Done! 🎉
```

---

## 📁 Final Structure

```
create-claude-agent/               # Your npm package
├── package.json                   # See example below
├── README.md                      # Documentation
├── LICENSE                        # MIT license
├── bin/
│   └── cli.js                     # CLI installer (see example below)
└── template/                      # Your .claude directory
    ├── CLAUDE.md
    ├── agents/
    │   ├── 01-orchestrator.md
    │   ├── 02-uxui-frontend.md
    │   ├── 03-test-debug.md
    │   ├── 04-frontend.md
    │   ├── 05-backend.md
    │   └── 06-database.md
    ├── contexts/
    │   ├── patterns/
    │   │   └── *.md
    │   └── design/
    │       └── *.md
    └── settings.local.json
```

---

## 📋 Step-by-Step

### Step 1: Create Package Directory

```bash
# Create a NEW repository (separate from your template)
mkdir create-claude-agent
cd create-claude-agent
git init
```

### Step 2: Initialize npm Package

```bash
npm init -y
```

Edit `package.json` (see npm-package-example/package.json for full example):
```json
{
  "name": "create-claude-agent",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "create-claude-agent": "./bin/cli.js"
  },
  "files": ["bin", "template", "README.md"],
  "dependencies": {
    "chalk": "^5.3.0",
    "ora": "^8.0.1",
    "prompts": "^2.4.2",
    "fs-extra": "^11.2.0"
  }
}
```

### Step 3: Create Template Directory

```bash
mkdir template
cp -r /path/to/your/.claude/* template/
```

### Step 4: Create CLI Script

Create `bin/cli.js` (see npm-package-example/bin/cli.js for full code):
```javascript
#!/usr/bin/env node
import fs from 'fs-extra'
import path from 'path'
import chalk from 'chalk'
// ... (copy from example)
```

Make it executable:
```bash
chmod +x bin/cli.js
```

### Step 5: Install Dependencies

```bash
npm install
```

### Step 6: Test Locally

```bash
# Link package globally
npm link

# Test in another directory
cd ~/test-project
npx create-claude-agent

# Check installation
ls -la .claude/
cat .claude/CLAUDE.md
```

### Step 7: Publish to npm

```bash
# Login to npm (first time only)
npm login

# Publish
npm publish --access public
```

### Step 8: Verify Published Package

```bash
# Test installation
cd ~/another-test-project
npx create-claude-agent

# Check npm page
open https://www.npmjs.com/package/create-claude-agent
```

---

## 🎨 Customization Options

### Option 1: Add Interactive Prompts

```javascript
// In bin/cli.js
const options = await prompts([
  {
    type: 'select',
    name: 'framework',
    message: 'Which framework are you using?',
    choices: [
      { title: 'Next.js', value: 'nextjs' },
      { title: 'React', value: 'react' },
      { title: 'Vue', value: 'vue' }
    ]
  },
  {
    type: 'multiselect',
    name: 'agents',
    message: 'Which agents do you want?',
    choices: [
      { title: 'UX-UI Frontend', value: 'uxui', selected: true },
      { title: 'Test-Debug', value: 'test', selected: true },
      { title: 'Frontend', value: 'frontend', selected: true },
      { title: 'Backend', value: 'backend', selected: true },
      { title: 'Database', value: 'database', selected: true }
    ]
  }
])

// Copy only selected agents
options.agents.forEach(agent => {
  // Copy specific agent files
})
```

### Option 2: Add Post-Install Setup

```javascript
// In bin/cli.js after copying files

console.log(chalk.cyan('\n🔧 Running setup...\n'))

// Create tasks.md template
fs.writeFileSync(
  path.join(targetDir, 'tasks.md'),
  `# Feature: [Feature Name]

## Tech Stack
- Frontend: ${options.framework}
- Backend: [Your backend]
- Database: [Your database]

## Tasks
### Phase 1: UX-UI
- Task 1.1: [Description]
`
)

console.log(chalk.green('✅ Created tasks.md template'))
```

### Option 3: Add Version Checking

```javascript
// In bin/cli.js

import { createRequire } from 'module'
const require = createRequire(import.meta.url)
const packageJson = require('../package.json')

console.log(chalk.gray(`v${packageJson.version}`))

// Check for updates
const latest = await fetch('https://registry.npmjs.org/create-claude-agent/latest')
  .then(r => r.json())

if (latest.version !== packageJson.version) {
  console.log(chalk.yellow(`⚠️  New version available: ${latest.version}`))
  console.log(chalk.gray(`   Run: npm install -g create-claude-agent@latest`))
}
```

---

## 🚀 Alternative: Scoped Package

If `create-claude-agent` is taken:

```json
{
  "name": "@yourname/create-claude-agent"
}
```

**Usage:**
```bash
npx @yourname/create-claude-agent
```

---

## 📊 Expected Timeline

- **Setup**: 10 minutes
- **Testing**: 5 minutes
- **Publishing**: 2 minutes
- **Total**: ~20 minutes

---

## 🎉 Success Criteria

After publishing, users should be able to:

```bash
# Install template
npx create-claude-agent

# See .claude directory
ls .claude/
├── CLAUDE.md
├── agents/
├── contexts/
└── settings.local.json

# Read documentation
cat .claude/CLAUDE.md

# Use orchestrator
# (in Claude Code)
/agents orchestrator
```

---

## 🆘 Common Issues

### Issue: "command not found: npx"
**Solution:** Update Node.js to v18+
```bash
node --version  # Should be >= 18.0.0
```

### Issue: "Package name already taken"
**Solution:** Use scoped package
```bash
npm init --scope=yourname
```

### Issue: "Permission denied: bin/cli.js"
**Solution:** Make executable
```bash
chmod +x bin/cli.js
```

### Issue: "Cannot find module 'chalk'"
**Solution:** Add as dependency (not devDependency)
```json
{
  "dependencies": {
    "chalk": "^5.3.0"
  }
}
```

---

## 📚 Next Steps

1. ✅ Create npm package (this guide)
2. 📝 Write good README.md
3. 🏷️ Add LICENSE (MIT recommended)
4. 📦 Publish to npm
5. 📢 Share on:
   - GitHub
   - Reddit (r/ClaudeAI, r/node)
   - Twitter/X
   - Dev.to
6. 📊 Monitor downloads: `npm info create-claude-agent`

---

## 🌟 Pro Tips

1. **Use semantic versioning**: Start at 1.0.0
2. **Keep dependencies minimal**: Only production deps
3. **Test before publishing**: Always `npm link` first
4. **Document breaking changes**: In CHANGELOG.md
5. **Add badges to README**: Version, downloads, license
6. **Setup GitHub Actions**: Auto-publish on release

---

**Ready to publish?** Follow PUBLISH-GUIDE.md for detailed steps! 🚀
