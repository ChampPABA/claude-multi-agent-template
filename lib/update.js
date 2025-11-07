/**
 * Update Command - Update Claude Agent Kit template to latest version
 *
 * This function:
 * 1. Checks for new version in npm registry
 * 2. Optionally updates the global package
 * 3. Merges latest template files into .claude/
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const pkg = require('../package.json');
const {
  promptUser,
  mergeTemplateFiles,
  getLatestVersion,
  getCurrentVersion,
  installGlobalPackage
} = require('./helpers');

module.exports = async function update(options = {}) {
  const packageName = pkg.name;

  // Paths
  const templatePath = path.join(__dirname, '../.claude');
  const targetPath = path.join(process.cwd(), '.claude');

  console.log(chalk.cyan('\n🤖 Claude Agent Kit - Updating...\n'));

  // Check if .claude/ exists
  if (!fs.existsSync(targetPath)) {
    console.log(chalk.yellow('⚠️  .claude/ not found in this project.'));
    console.log(chalk.gray('   Run init first:\n'));
    console.log(chalk.cyan('   cak init\n'));
    return;
  }

  // STEP 1: Check version
  console.log(chalk.gray('🔍 Checking for updates...\n'));

  const currentVersion = getCurrentVersion(packageName) || pkg.version;
  const latestVersion = await getLatestVersion(packageName);

  if (!latestVersion) {
    console.log(chalk.yellow('⚠️  Unable to check npm registry. Continuing with local version.\n'));
  } else if (currentVersion === latestVersion) {
    console.log(chalk.green(`✅ Already on latest version (${latestVersion})\n`));
  } else {
    console.log(chalk.cyan(`📦 New version available: ${chalk.bold(latestVersion)} (current: ${currentVersion})\n`));

    const shouldUpdatePackage = await promptUser(
      chalk.cyan('❓ Update package globally first? (y/N): ')
    );

    // STEP 2: Update package globally
    if (shouldUpdatePackage) {
      const success = await installGlobalPackage(packageName, latestVersion);

      if (!success) {
        console.log(chalk.yellow('⚠️  Package update failed. Continuing with current version.\n'));
      }
    } else {
      console.log(chalk.gray('\n⏭️  Skipping package update. Using current version.\n'));
    }
  }

  // Check if template exists
  if (!fs.existsSync(templatePath)) {
    throw new Error('Template folder not found. Please reinstall the package.');
  }

  // STEP 3: Update files (merge mode)
  console.log(chalk.gray('📦 Merging template files...\n'));

  try {
    await mergeTemplateFiles(templatePath, targetPath);

    console.log(chalk.green('✅ Successfully updated Claude Agent Kit!\n'));
    console.log(chalk.white('📁 Updated files in: ') + chalk.cyan(targetPath));
    console.log(chalk.gray('   (Existing files preserved, template files merged)\n'));

    console.log(chalk.white('📚 What\'s new:\n'));
    console.log(chalk.gray('   Check CHANGELOG.md for latest changes'));
    console.log(chalk.gray('   Or visit: ') + chalk.cyan('https://github.com/ChampPABA/claude-multi-agent-template\n'));

  } catch (error) {
    throw new Error(`Failed to update template: ${error.message}`);
  }
};
