/**
 * Init Command - Initialize Claude Agent Kit template
 *
 * This function merges the .claude/ template folder into the current project.
 * - Overwrites files with same name
 * - Keeps existing files that don't exist in template
 * - Optionally creates PROJECT_STATUS.yml for cross-session context
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const { promptUser, mergeTemplateFiles } = require('./helpers');

module.exports = async function init(options = {}) {
  // Paths
  const templatePath = path.join(__dirname, '../.claude');
  const targetPath = path.join(process.cwd(), '.claude');
  const projectStatusTemplatePath = path.join(__dirname, '../PROJECT_STATUS.template.yml');
  const projectStatusTargetPath = path.join(process.cwd(), 'PROJECT_STATUS.yml');

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

    // Prompt for PROJECT_STATUS.yml (optional)
    if (!fs.existsSync(projectStatusTargetPath)) {
      console.log(chalk.white('\n📊 Optional: Cross-Session Context\n'));
      console.log(chalk.gray('   PROJECT_STATUS.yml helps Claude remember:'));
      console.log(chalk.gray('   - Infrastructure state (DB, API, tunnels)'));
      console.log(chalk.gray('   - Blockers (waiting for domain, API keys)'));
      console.log(chalk.gray('   - Completed work & next priorities\n'));

      const addProjectStatus = await promptUser(
        chalk.cyan('❓ Add PROJECT_STATUS.yml? Recommended for multi-session projects (y/N): ')
      );

      if (addProjectStatus) {
        await fs.copy(projectStatusTemplatePath, projectStatusTargetPath);
        console.log(chalk.green('\n✅ PROJECT_STATUS.yml created!'));
        console.log(chalk.gray('   Edit this file to add your project context.'));
        console.log(chalk.gray('   Use /pstatus in Claude Code to update it.\n'));
      } else {
        console.log(chalk.gray('\n   Skipped. Run `cak init` again to add later.\n'));
      }
    } else {
      console.log(chalk.gray('\n📊 PROJECT_STATUS.yml already exists (preserved)\n'));
    }

    console.log(chalk.white('📚 Next steps:\n'));
    console.log(chalk.gray('   1. Review the .claude/ folder'));
    console.log(chalk.gray('   2. Run: ') + chalk.cyan('/csetup {change-id}') + chalk.gray(' to setup a change'));
    console.log(chalk.gray('   3. Start using agents with Claude Code\n'));

  } catch (error) {
    throw new Error(`Failed to merge template: ${error.message}`);
  }
};
