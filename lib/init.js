/**
 * Init Command - Initialize Claude Agent Kit template
 *
 * This function merges the .claude/ template folder into the current project.
 * - Overwrites files with same name
 * - Keeps existing files that don't exist in template
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const { promptUser, mergeTemplateFiles } = require('./helpers');

module.exports = async function init(options = {}) {
  // Paths
  const templatePath = path.join(__dirname, '../.claude');
  const targetPath = path.join(process.cwd(), '.claude');

  console.log(chalk.cyan('\n🤖 Claude Agent Kit - Initializing...\n'));

  // Check if template exists
  if (!fs.existsSync(templatePath)) {
    throw new Error('Template folder not found. Please reinstall the package.');
  }

  // Check if .claude/ already exists
  if (fs.existsSync(targetPath)) {
    console.log(chalk.yellow('⚠️  .claude/ already exists in this project.'));
    console.log(chalk.gray('   Existing files will be preserved, template files will be merged.\n'));

    const shouldContinue = await promptUser(
      chalk.cyan('❓ Merge with template files? (y/N): ')
    );

    if (!shouldContinue) {
      console.log(chalk.gray('\n❌ Initialization cancelled.\n'));
      return;
    }

    console.log(chalk.gray('\n📦 Merging template files...\n'));
  }

  // Merge template files
  try {
    await mergeTemplateFiles(templatePath, targetPath);

    console.log(chalk.green('✅ Successfully initialized Claude Agent Kit!\n'));
    console.log(chalk.white('📁 Files merged to: ') + chalk.cyan(targetPath));
    console.log(chalk.white('\n📚 Next steps:\n'));
    console.log(chalk.gray('   1. Review the .claude/ folder'));
    console.log(chalk.gray('   2. Run: ') + chalk.cyan('/psetup') + chalk.gray(' (one-time project setup)'));
    console.log(chalk.gray('   3. Start using agents with Claude Code\n'));

  } catch (error) {
    throw new Error(`Failed to merge template: ${error.message}`);
  }
};
