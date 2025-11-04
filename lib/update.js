/**
 * Update Command - Update Claude Agent Kit template to latest version
 *
 * This function updates the .claude/ folder with the latest template files.
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');

module.exports = async function update(options = {}) {
  const { backup } = options;

  // Paths
  const templatePath = path.join(__dirname, '../.claude');
  const targetPath = path.join(process.cwd(), '.claude');
  const backupPath = path.join(process.cwd(), '.claude.backup');

  console.log(chalk.cyan('\n🤖 Claude Agent Kit - Updating...\n'));

  // Check if .claude/ exists
  if (!fs.existsSync(targetPath)) {
    console.log(chalk.yellow('⚠️  .claude/ not found in this project.'));
    console.log(chalk.gray('   Run init first:\n'));
    console.log(chalk.cyan('   cak init\n'));
    return;
  }

  // Check if template exists
  if (!fs.existsSync(templatePath)) {
    throw new Error('Template folder not found. Please reinstall the package.');
  }

  // Create backup if requested
  if (backup) {
    console.log(chalk.gray('📦 Creating backup...\n'));

    // Remove old backup if exists
    if (fs.existsSync(backupPath)) {
      await fs.remove(backupPath);
    }

    // Copy current .claude/ to backup
    await fs.copy(targetPath, backupPath);
    console.log(chalk.green('✅ Backup created: ') + chalk.cyan('.claude.backup\n'));
  }

  // Update template
  try {
    // Strategy: Overwrite all files from template
    // User customizations in domain/ should be preserved if they don't conflict
    await fs.copy(templatePath, targetPath, {
      overwrite: true,
      errorOnExist: false
    });

    console.log(chalk.green('✅ Successfully updated Claude Agent Kit!\n'));
    console.log(chalk.white('📁 Updated files in: ') + chalk.cyan(targetPath));

    if (backup) {
      console.log(chalk.white('\n💾 Backup available at: ') + chalk.cyan(backupPath));
      console.log(chalk.gray('   You can restore it if needed:\n'));
      console.log(chalk.cyan('   rm -rf .claude && mv .claude.backup .claude\n'));
    }

    console.log(chalk.white('\n📚 What\'s new:\n'));
    console.log(chalk.gray('   Check CHANGELOG.md for latest changes'));
    console.log(chalk.gray('   Or visit: ') + chalk.cyan('https://github.com/your-username/claude-agent-kit\n'));

  } catch (error) {
    throw new Error(`Failed to update template: ${error.message}`);
  }
};
