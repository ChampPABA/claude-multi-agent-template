#!/usr/bin/env node

/**
 * Claude Agent Kit - CLI Entry Point
 *
 * This is the main CLI file that handles all commands:
 * - cak init        → Initialize template in current project
 * - cak update      → Update template to latest version
 * - cak --version   → Show version
 * - cak --help      → Show help
 */

const { program } = require('commander');
const chalk = require('chalk');
const pkg = require('../package.json');

// Import command handlers
const initCommand = require('../lib/init');
const updateCommand = require('../lib/update');

// Configure CLI
program
  .name('cak')
  .description(chalk.cyan('🤖 Claude Agent Kit - Universal Multi-Agent Template'))
  .version(pkg.version, '-v, --version', 'Show version number');

// Command: cak init
program
  .command('init')
  .description('Initialize Claude Agent Kit template in current project')
  .action(async (options) => {
    try {
      await initCommand(options);
    } catch (error) {
      console.error(chalk.red('❌ Error:'), error.message);
      process.exit(1);
    }
  });

// Command: cak update
program
  .command('update')
  .description('Update template files to latest version')
  .action(async (options) => {
    try {
      await updateCommand(options);
    } catch (error) {
      console.error(chalk.red('❌ Error:'), error.message);
      process.exit(1);
    }
  });

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}

// Parse command line arguments
program.parse(process.argv);
