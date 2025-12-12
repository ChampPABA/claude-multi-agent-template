/**
 * Development Principles Integration Tests
 *
 * Tests to verify that:
 * 1. development-principles.md is properly integrated into context-loading-protocol
 * 2. All agents can access the principles
 * 3. Principles cover maintainability and scalability concerns
 * 4. Edge cases are handled
 *
 * @version 3.0.1
 */

import { describe, it, expect, beforeAll } from 'vitest'
import fs from 'fs'
import path from 'path'

// ============================================================
// TEST CONSTANTS
// ============================================================

const CLAUDE_DIR = path.join(process.cwd(), '.claude')
const AGENTS_DIR = path.join(CLAUDE_DIR, 'agents')
const PATTERNS_DIR = path.join(CLAUDE_DIR, 'contexts', 'patterns')
const LIB_DIR = path.join(CLAUDE_DIR, 'lib')

const CONTEXT_LOADING_PROTOCOL = path.join(LIB_DIR, 'context-loading-protocol.md')
const DEVELOPMENT_PRINCIPLES = path.join(PATTERNS_DIR, 'development-principles.md')

const AGENT_FILES = [
  '01-integration.md',
  '02-uxui-frontend.md',
  '03-test-debug.md',
  '04-frontend.md',
  '05-backend.md',
  '06-database.md',
  '07-ux-tester.md'
]

// Agents that write code and need development principles
// ux-tester excluded: only tests UI, doesn't write code
const CODE_WRITING_AGENTS = [
  '01-integration.md',
  '02-uxui-frontend.md',
  '03-test-debug.md',
  '04-frontend.md',
  '05-backend.md',
  '06-database.md'
]

// Required principles for maintainability and scalability
const REQUIRED_PRINCIPLES = [
  'KISS',
  'YAGNI',
  'SOLID',
  'Single Responsibility',
  'Open/Closed',
  'Liskov Substitution',
  'Interface Segregation',
  'Dependency Inversion',
  'DRY',
  'Separation of Concerns',
  'Fail Fast'
]

// Required code examples (❌ bad vs ✅ good)
const REQUIRED_EXAMPLES = [
  { principle: 'SRP', mustHave: ['class UserService', 'class EmailService'] },
  { principle: 'DIP', mustHave: ['interface Database', 'constructor(private db: Database)'] },
  { principle: 'Separation of Concerns', mustHave: ['API Layer', 'Validation Layer', 'Business Layer'] },
  { principle: 'DRY', mustHave: ['lib/constants.ts', 'Single source of truth'] }
]

// ============================================================
// HELPER FUNCTIONS
// ============================================================

function readFile(filePath) {
  return fs.readFileSync(filePath, 'utf-8')
}

function fileExists(filePath) {
  return fs.existsSync(filePath)
}

// ============================================================
// TEST SUITE 1: FILE EXISTENCE & STRUCTURE
// ============================================================

describe('File Existence & Structure', () => {
  it('development-principles.md exists', () => {
    expect(fileExists(DEVELOPMENT_PRINCIPLES)).toBe(true)
  })

  it('context-loading-protocol.md exists', () => {
    expect(fileExists(CONTEXT_LOADING_PROTOCOL)).toBe(true)
  })

  it('all agent files exist', () => {
    for (const agentFile of AGENT_FILES) {
      const agentPath = path.join(AGENTS_DIR, agentFile)
      expect(fileExists(agentPath), `Agent file missing: ${agentFile}`).toBe(true)
    }
  })
})

// ============================================================
// TEST SUITE 2: CONTEXT LOADING INTEGRATION
// ============================================================

describe('Context Loading Integration', () => {
  let contextLoadingContent

  beforeAll(() => {
    contextLoadingContent = readFile(CONTEXT_LOADING_PROTOCOL)
  })

  it('context-loading-protocol.md includes development-principles.md in Level 1', () => {
    expect(contextLoadingContent).toContain('development-principles.md')
  })

  it('development-principles.md is in Core Patterns (ALWAYS load) section', () => {
    // Find the Core Patterns section
    const corePatternsSectionMatch = contextLoadingContent.match(
      /\*\*Core Patterns \(ALWAYS load\):\*\*([\s\S]*?)(?=\*\*Why load these:|---)/
    )

    expect(corePatternsSectionMatch).not.toBeNull()

    const corePatterns = corePatternsSectionMatch[1]
    expect(corePatterns).toContain('development-principles.md')
  })

  it('development-principles.md has description mentioning key principles', () => {
    // Should mention SOLID, DRY, KISS, or Separation of Concerns
    const hasKeyPrinciples =
      contextLoadingContent.includes('SOLID') ||
      contextLoadingContent.includes('DRY') ||
      contextLoadingContent.includes('KISS') ||
      contextLoadingContent.includes('Separation of Concerns')

    expect(hasKeyPrinciples).toBe(true)
  })
})

// ============================================================
// TEST SUITE 3: AGENT REFERENCES
// ============================================================

describe('Agent References to Context Loading Protocol', () => {
  it('code-writing agents reference context-loading-protocol.md', () => {
    // Only agents that write code need development principles
    // ux-tester excluded: only tests UI from user perspective
    for (const agentFile of CODE_WRITING_AGENTS) {
      const agentPath = path.join(AGENTS_DIR, agentFile)
      const content = readFile(agentPath)

      expect(
        content.includes('context-loading-protocol.md'),
        `Agent ${agentFile} does not reference context-loading-protocol.md`
      ).toBe(true)
    }
  })

  it('code-writing agents have Context Loading section', () => {
    for (const agentFile of CODE_WRITING_AGENTS) {
      const agentPath = path.join(AGENTS_DIR, agentFile)
      const content = readFile(agentPath)

      // Should have "Context Loading" header or reference
      const hasContextLoading =
        content.includes('## Context Loading') ||
        content.includes('Context Loading') ||
        content.includes('context-loading-protocol')

      expect(
        hasContextLoading,
        `Agent ${agentFile} missing Context Loading section`
      ).toBe(true)
    }
  })

  it('ux-tester agent does NOT need context-loading (tests UI only)', () => {
    const uxTesterPath = path.join(AGENTS_DIR, '07-ux-tester.md')
    const content = readFile(uxTesterPath)

    // ux-tester should focus on user perspective, not code architecture
    expect(content).toContain('Core Mission')
    expect(content).toContain('Persona')
  })
})

// ============================================================
// TEST SUITE 4: PRINCIPLES CONTENT COVERAGE
// ============================================================

describe('Development Principles Content Coverage', () => {
  let principlesContent

  beforeAll(() => {
    principlesContent = readFile(DEVELOPMENT_PRINCIPLES)
  })

  it('contains all required principles', () => {
    for (const principle of REQUIRED_PRINCIPLES) {
      expect(
        principlesContent.includes(principle),
        `Missing principle: ${principle}`
      ).toBe(true)
    }
  })

  it('has both bad (❌) and good (✅) examples', () => {
    const hasBadExamples = principlesContent.includes('❌')
    const hasGoodExamples = principlesContent.includes('✅')

    expect(hasBadExamples, 'Missing bad examples (❌)').toBe(true)
    expect(hasGoodExamples, 'Missing good examples (✅)').toBe(true)
  })

  it('has code examples for each major principle', () => {
    for (const example of REQUIRED_EXAMPLES) {
      for (const mustHave of example.mustHave) {
        expect(
          principlesContent.includes(mustHave),
          `Missing example for ${example.principle}: "${mustHave}"`
        ).toBe(true)
      }
    }
  })

  it('has Quick Reference table', () => {
    expect(principlesContent).toContain('Quick Reference')
    expect(principlesContent).toContain('| Principle | Summary |')
  })
})

// ============================================================
// TEST SUITE 5: MAINTAINABILITY COVERAGE
// ============================================================

describe('Maintainability Coverage', () => {
  let principlesContent

  beforeAll(() => {
    principlesContent = readFile(DEVELOPMENT_PRINCIPLES)
  })

  it('covers Single Responsibility Principle with file organization example', () => {
    expect(principlesContent).toContain('lib/services/')
    expect(principlesContent).toContain('user-service')
    expect(principlesContent).toContain('email-service')
  })

  it('covers Separation of Concerns with layer architecture', () => {
    expect(principlesContent).toContain('API Layer')
    expect(principlesContent).toContain('Validation Layer')
    expect(principlesContent).toContain('Business Layer')
  })

  it('covers DRY with constants example', () => {
    expect(principlesContent).toContain('lib/constants')
    expect(principlesContent).toContain('Single source of truth')
  })

  it('explains WHY for each principle', () => {
    // Count "WHY" or explanatory patterns
    const whyCount = (principlesContent.match(/ONE reason to change|should be|prevents|ensures/gi) || []).length
    expect(whyCount).toBeGreaterThan(5)
  })
})

// ============================================================
// TEST SUITE 6: SCALABILITY COVERAGE
// ============================================================

describe('Scalability Coverage', () => {
  let principlesContent

  beforeAll(() => {
    principlesContent = readFile(DEVELOPMENT_PRINCIPLES)
  })

  it('covers Open/Closed Principle for extensibility', () => {
    expect(principlesContent).toContain('Open/Closed')
    expect(principlesContent).toContain('open for extension')
    expect(principlesContent).toContain('closed for modification')
  })

  it('covers Dependency Inversion for swappable components', () => {
    expect(principlesContent).toContain('Dependency Inversion')
    expect(principlesContent).toContain('interface')
    expect(principlesContent).toContain('Easy to swap')
  })

  it('covers Interface Segregation for modular interfaces', () => {
    expect(principlesContent).toContain('Interface Segregation')
    expect(principlesContent).toContain('Clients should not depend on interfaces they don\'t use')
  })

  it('has strategy pattern example for OCP', () => {
    expect(principlesContent).toContain('DiscountStrategy')
    expect(principlesContent).toContain('implements')
  })
})

// ============================================================
// TEST SUITE 7: EDGE CASES
// ============================================================

describe('Edge Cases', () => {
  it('development-principles.md is not empty', () => {
    const content = readFile(DEVELOPMENT_PRINCIPLES)
    expect(content.length).toBeGreaterThan(1000)
  })

  it('development-principles.md has proper markdown structure', () => {
    const content = readFile(DEVELOPMENT_PRINCIPLES)

    // Should have headers
    expect(content).toContain('# Development Principles')
    expect(content).toContain('## ')
    expect(content).toContain('### ')
  })

  it('no broken internal links in context-loading-protocol.md', () => {
    const content = readFile(CONTEXT_LOADING_PROTOCOL)

    // Find all referenced .md files
    const mdReferences = content.match(/`@?\.claude\/[^`]+\.md`/g) || []

    for (const ref of mdReferences) {
      // Extract path from reference
      const relativePath = ref.replace(/`|@/g, '').trim()
      const fullPath = path.join(process.cwd(), relativePath)

      expect(
        fileExists(fullPath),
        `Broken reference: ${ref} -> ${fullPath}`
      ).toBe(true)
    }
  })

  it('development-principles.md path in context-loading matches actual file', () => {
    const contextContent = readFile(CONTEXT_LOADING_PROTOCOL)

    // Should reference the correct path
    expect(contextContent).toContain('patterns/development-principles.md')
  })
})

// ============================================================
// TEST SUITE 8: ANTI-PATTERNS DETECTION
// ============================================================

describe('Anti-Patterns Detection', () => {
  let principlesContent

  beforeAll(() => {
    principlesContent = readFile(DEVELOPMENT_PRINCIPLES)
  })

  it('shows anti-patterns for God Class (violates SRP)', () => {
    // The bad example shows a class with multiple responsibilities
    expect(principlesContent).toContain('createUser')
    expect(principlesContent).toContain('sendWelcomeEmail')
    expect(principlesContent).toContain('logActivity')
  })

  it('shows anti-patterns for hardcoded dependencies (violates DIP)', () => {
    expect(principlesContent).toContain('new MySQLDatabase()')
    expect(principlesContent).toContain('Direct dependency')
  })

  it('shows anti-patterns for code duplication (violates DRY)', () => {
    expect(principlesContent).toContain('duplicate')
    expect(principlesContent).toContain('Hardcoded')
  })

  it('shows anti-patterns for mixed concerns', () => {
    expect(principlesContent).toContain('Mixed Concerns')
    expect(principlesContent).toContain('Validation mixed with business logic')
  })
})

// ============================================================
// TEST SUITE 9: PRACTICAL APPLICABILITY
// ============================================================

describe('Practical Applicability', () => {
  let principlesContent

  beforeAll(() => {
    principlesContent = readFile(DEVELOPMENT_PRINCIPLES)
  })

  it('uses TypeScript/JavaScript examples (primary stack)', () => {
    expect(principlesContent).toContain('typescript')
    expect(principlesContent).toContain('export')
    expect(principlesContent).toContain('async')
  })

  it('references common frameworks/tools', () => {
    const hasCommonTools =
      principlesContent.includes('prisma') ||
      principlesContent.includes('zod') ||
      principlesContent.includes('Next')

    expect(hasCommonTools).toBe(true)
  })

  it('has actionable file path examples', () => {
    expect(principlesContent).toContain('lib/')
    expect(principlesContent).toContain('.ts')
  })
})

// ============================================================
// TEST SUITE 10: FLOW SIMULATION
// ============================================================

describe('Flow Simulation: Agent Loading Principles', () => {
  it('simulates backend agent loading flow', () => {
    // Step 1: Agent reads its file
    const backendAgent = readFile(path.join(AGENTS_DIR, '05-backend.md'))
    expect(backendAgent).toContain('context-loading-protocol.md')

    // Step 2: Agent follows reference to context-loading-protocol
    const contextLoading = readFile(CONTEXT_LOADING_PROTOCOL)
    expect(contextLoading).toContain('Level 1: Universal Patterns')

    // Step 3: Context loading lists development-principles.md
    expect(contextLoading).toContain('development-principles.md')

    // Step 4: Agent loads development-principles.md
    const principles = readFile(DEVELOPMENT_PRINCIPLES)
    expect(principles).toContain('SOLID')
    expect(principles).toContain('Separation of Concerns')

    // Flow complete!
  })

  it('simulates uxui-frontend agent loading flow', () => {
    const uxuiAgent = readFile(path.join(AGENTS_DIR, '02-uxui-frontend.md'))
    expect(uxuiAgent).toContain('context-loading-protocol.md')

    const contextLoading = readFile(CONTEXT_LOADING_PROTOCOL)
    expect(contextLoading).toContain('development-principles.md')

    const principles = readFile(DEVELOPMENT_PRINCIPLES)
    expect(principles).toContain('DRY')
  })

  it('simulates database agent loading flow', () => {
    const dbAgent = readFile(path.join(AGENTS_DIR, '06-database.md'))
    expect(dbAgent).toContain('context-loading-protocol.md')

    const contextLoading = readFile(CONTEXT_LOADING_PROTOCOL)
    expect(contextLoading).toContain('development-principles.md')

    const principles = readFile(DEVELOPMENT_PRINCIPLES)
    expect(principles).toContain('Single Responsibility')
  })
})

// ============================================================
// TEST SUITE 11: COMPLETENESS CHECK
// ============================================================

describe('Completeness Check', () => {
  let principlesContent

  beforeAll(() => {
    principlesContent = readFile(DEVELOPMENT_PRINCIPLES)
  })

  it('covers all SOLID principles (5 total)', () => {
    const solidPrinciples = [
      'Single Responsibility',
      'Open/Closed',
      'Liskov Substitution',
      'Interface Segregation',
      'Dependency Inversion'
    ]

    for (const principle of solidPrinciples) {
      expect(
        principlesContent.includes(principle),
        `Missing SOLID principle: ${principle}`
      ).toBe(true)
    }
  })

  it('has at least 10 code examples', () => {
    const codeBlockCount = (principlesContent.match(/```typescript/g) || []).length
    expect(codeBlockCount).toBeGreaterThanOrEqual(10)
  })

  it('has Core Philosophy statement', () => {
    expect(principlesContent).toContain('Core Philosophy')
    expect(principlesContent).toContain('maintainable')
  })

  it('file size is reasonable (not too short, not bloated)', () => {
    const content = readFile(DEVELOPMENT_PRINCIPLES)
    const lineCount = content.split('\n').length

    // Should be comprehensive but not excessive
    expect(lineCount).toBeGreaterThan(300) // Not too short
    expect(lineCount).toBeLessThan(1000) // Not bloated
  })
})

// ============================================================
// TEST SUITE 12: REGRESSION PREVENTION
// ============================================================

describe('Regression Prevention', () => {
  it('context-loading-protocol still has all original patterns', () => {
    const content = readFile(CONTEXT_LOADING_PROTOCOL)

    const originalPatterns = [
      'error-handling.md',
      'logging.md',
      'testing.md',
      'code-standards.md'
    ]

    for (const pattern of originalPatterns) {
      expect(
        content.includes(pattern),
        `Original pattern missing: ${pattern}`
      ).toBe(true)
    }
  })

  it('development-principles.md is ADDED not REPLACING other patterns', () => {
    const content = readFile(CONTEXT_LOADING_PROTOCOL)

    // Count patterns in Core Patterns section
    const patterns = [
      'error-handling.md',
      'logging.md',
      'testing.md',
      'code-standards.md',
      'development-principles.md'
    ]

    let foundCount = 0
    for (const pattern of patterns) {
      if (content.includes(pattern)) foundCount++
    }

    expect(foundCount).toBe(5) // All 5 should be present
  })
})
