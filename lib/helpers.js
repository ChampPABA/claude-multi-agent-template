/**
 * Helpers - Shared utility functions for CLI commands
 */

const fs = require('fs-extra');
const path = require('path');
const readline = require('readline');
const { execSync } = require('child_process');
const chalk = require('chalk');

/**
 * Prompt user for yes/no question
 * @param {string} question - Question to ask
 * @returns {Promise<boolean>} - True if user answered yes
 */
async function promptUser(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

/**
 * Merge template files into target directory
 * - Overwrites files with same name
 * - Keeps existing files that don't exist in template
 * @param {string} templatePath - Source template directory
 * @param {string} targetPath - Target directory
 */
async function mergeTemplateFiles(templatePath, targetPath) {
  await fs.copy(templatePath, targetPath, {
    overwrite: true,
    errorOnExist: false
  });
}

/**
 * Get latest version from npm registry
 * @param {string} packageName - Package name
 * @returns {Promise<string|null>} - Latest version or null if failed
 */
async function getLatestVersion(packageName) {
  try {
    const result = execSync(`npm view ${packageName} version`, {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    return result.trim();
  } catch (error) {
    return null;
  }
}

/**
 * Get currently installed global package version
 * @param {string} packageName - Package name
 * @returns {string|null} - Current version or null if not installed
 */
function getCurrentVersion(packageName) {
  try {
    const result = execSync(`npm list -g ${packageName} --depth=0`, {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    const match = result.match(new RegExp(`${packageName}@([\\d.]+)`));
    return match ? match[1] : null;
  } catch (error) {
    return null;
  }
}

/**
 * Install package globally
 * @param {string} packageName - Package name
 * @param {string} version - Version to install (default: latest)
 * @returns {Promise<boolean>} - True if successful
 */
async function installGlobalPackage(packageName, version = 'latest') {
  try {
    console.log(chalk.gray(`\n📦 Installing ${packageName}@${version} globally...\n`));

    execSync(`npm install -g ${packageName}@${version}`, {
      encoding: 'utf-8',
      stdio: 'inherit'
    });

    console.log(chalk.green(`\n✅ Package installed successfully!\n`));
    return true;
  } catch (error) {
    console.error(chalk.red(`\n❌ Failed to install package: ${error.message}\n`));
    return false;
  }
}

module.exports = {
  promptUser,
  mergeTemplateFiles,
  getLatestVersion,
  getCurrentVersion,
  installGlobalPackage
};
