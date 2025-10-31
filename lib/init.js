/**
 * Init Command - Initialize Claude Agent Kit template
 *
 * This function copies the .claude/ template folder to the current project.
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');

module.exports = async function init(options = {}) {
  const { force } = options;

  // Paths
  const templatePath = path.join(__dirname, '../template/.claude');
  const targetPath = path.join(process.cwd(), '.claude');

  console.log(chalk.cyan('\n🤖 Claude Agent Kit - Initializing...\n'));

  // Check if template exists
  if (!fs.existsSync(templatePath)) {
    throw new Error('Template folder not found. Please reinstall the package.');
  }

  // Check if .claude/ already exists
  if (fs.existsSync(targetPath)) {
    if (!force) {
      console.log(chalk.yellow('⚠️  .claude/ already exists in this project.'));
      console.log(chalk.gray('   Use --force to overwrite:\n'));
      console.log(chalk.cyan('   cak init --force\n'));
      return;
    }

    console.log(chalk.yellow('⚠️  Overwriting existing .claude/ folder...\n'));
    await fs.remove(targetPath);
  }

  // Copy template
  try {
    await fs.copy(templatePath, targetPath);

    console.log(chalk.green('✅ Successfully initialized Claude Agent Kit!\n'));
    console.log(chalk.white('📁 Files copied to: ') + chalk.cyan(targetPath));
    console.log(chalk.white('\n📚 Next steps:\n'));
    console.log(chalk.gray('   1. Review the .claude/ folder'));
    console.log(chalk.gray('   2. Run: ') + chalk.cyan('/psetup') + chalk.gray(' (one-time project setup)'));
    console.log(chalk.gray('   3. Start using agents with Claude Code\n'));

  } catch (error) {
    throw new Error(`Failed to copy template: ${error.message}`);
  }
};
