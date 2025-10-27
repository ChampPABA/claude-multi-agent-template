#!/usr/bin/env node

import fs from 'fs-extra'
import path from 'path'
import { fileURLToPath } from 'url'
import chalk from 'chalk'
import ora from 'ora'
import prompts from 'prompts'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Template directory path (relative to this script)
const TEMPLATE_DIR = path.join(__dirname, '..', 'template')

async function main() {
  console.log(chalk.cyan.bold('\n🤖 Create Claude Agent Template\n'))

  // Get target directory
  const response = await prompts({
    type: 'text',
    name: 'targetDir',
    message: 'Where would you like to install the template?',
    initial: process.cwd(),
  })

  if (!response.targetDir) {
    console.log(chalk.red('Installation cancelled'))
    process.exit(0)
  }

  const targetDir = path.resolve(response.targetDir)
  const claudeDir = path.join(targetDir, '.claude')

  // Check if .claude directory already exists
  if (fs.existsSync(claudeDir)) {
    const overwrite = await prompts({
      type: 'confirm',
      name: 'value',
      message: `.claude directory already exists in ${targetDir}. Overwrite?`,
      initial: false,
    })

    if (!overwrite.value) {
      console.log(chalk.yellow('Installation cancelled'))
      process.exit(0)
    }
  }

  // Copy template files
  const spinner = ora('Installing Claude Agent template...').start()

  try {
    // Create target directory if it doesn't exist
    fs.ensureDirSync(targetDir)

    // Copy .claude directory
    fs.copySync(TEMPLATE_DIR, claudeDir, { overwrite: true })

    spinner.succeed(chalk.green('Template installed successfully!'))

    // Show next steps
    console.log(chalk.cyan('\n📋 Next steps:\n'))
    console.log(chalk.white('1. Read the documentation:'))
    console.log(chalk.gray(`   cat ${path.join(claudeDir, 'CLAUDE.md')}\n`))
    console.log(chalk.white('2. Create your tasks.md file'))
    console.log(chalk.white('3. Run the orchestrator agent:'))
    console.log(chalk.gray('   /agents orchestrator\n'))
    console.log(chalk.cyan('📖 Full documentation:'))
    console.log(chalk.gray('   https://github.com/yourusername/create-claude-agent\n'))
    console.log(chalk.green('✨ Happy coding with AI agents!\n'))
  } catch (error) {
    spinner.fail(chalk.red('Installation failed'))
    console.error(chalk.red('Error:'), error.message)
    process.exit(1)
  }
}

main().catch((error) => {
  console.error(chalk.red('Unexpected error:'), error)
  process.exit(1)
})
