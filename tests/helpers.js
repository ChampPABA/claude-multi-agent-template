/**
 * Shared Test Helpers
 *
 * Common helper functions used across test files.
 * Extracted from csetup.md for testing purposes.
 *
 * @version 2.8.0
 */

// ============================================================
// CHANGE ANALYSIS
// ============================================================

/**
 * Analyze change characteristics using semantic understanding
 * This determines complexity, risk, and what research layers are needed
 */
export function analyzeChangeCharacteristics(combined, proposal, tasks) {
  const analysis = {
    primaryType: 'general',
    complexity: 1,
    riskLevel: 'LOW',
    audience: 'internal',
    domains: [],
    features: [],
    hasUI: false,
    hasAPI: false,
    hasDatabase: false,
    hasPayment: false,
    hasAuth: false,
    hasCompliance: false,
    hasSensitiveData: false,
    isExternalFacing: false,
    industryContext: null
  }

  // Detect primary type
  if (/marketing|landing|hero|cta|conversion|sales/i.test(combined)) {
    analysis.primaryType = 'marketing'
    analysis.isExternalFacing = true
  } else if (/dashboard|admin|management|analytics/i.test(combined)) {
    analysis.primaryType = 'dashboard'
  } else if (/api|endpoint|rest|graphql/i.test(combined)) {
    analysis.primaryType = 'api'
  } else if (/auth|login|register|password/i.test(combined)) {
    analysis.primaryType = 'auth'
  } else if (/database|schema|migration|model/i.test(combined)) {
    analysis.primaryType = 'database'
    analysis.hasDatabase = true
  }

  // Detect auth separately (can be combined with other types)
  if (/auth|login|register|password|jwt|session|token/i.test(combined)) {
    analysis.hasAuth = true
  }

  // Detect features and domains
  if (/payment|stripe|billing|checkout|subscription/i.test(combined)) {
    analysis.hasPayment = true
    analysis.features.push('payment')
    analysis.riskLevel = 'HIGH'
  }
  if (/health|medical|patient|hipaa|phi/i.test(combined)) {
    analysis.hasCompliance = true
    analysis.hasSensitiveData = true
    analysis.domains.push('healthcare')
    analysis.industryContext = 'healthcare'
    analysis.riskLevel = 'HIGH'
  }
  if (/fintech|banking|finance|pci|financial/i.test(combined)) {
    analysis.hasCompliance = true
    analysis.domains.push('fintech')
    analysis.industryContext = 'fintech'
    analysis.riskLevel = 'HIGH'
  }
  if (/saas|multi-tenant|tenant/i.test(combined)) {
    analysis.domains.push('saas')
    analysis.features.push('multi-tenancy')
  }
  if (/ecommerce|e-commerce|cart|product|shop/i.test(combined)) {
    analysis.domains.push('ecommerce')
    analysis.isExternalFacing = true
  }
  if (/realtime|real-time|websocket|collaboration/i.test(combined)) {
    analysis.features.push('realtime')
  }

  // Detect UI/API/Database
  analysis.hasUI = /ui|page|component|form|button|modal/i.test(combined)
  analysis.hasAPI = /api|endpoint|route|controller/i.test(combined)
  analysis.hasDatabase = analysis.hasDatabase || /table|column|relation|index|database|data architecture|prisma|postgresql|mysql|mongodb/i.test(combined)

  // Detect audience
  if (/b2c|consumer|user|customer/i.test(combined)) {
    analysis.audience = 'consumer'
    analysis.isExternalFacing = true
  } else if (/b2b|enterprise|business/i.test(combined)) {
    analysis.audience = 'business'
    analysis.isExternalFacing = true
  }

  // Calculate complexity (1-10)
  let complexity = 1
  if (analysis.features.length > 0) complexity += analysis.features.length
  if (analysis.domains.length > 0) complexity += analysis.domains.length
  if (analysis.hasCompliance) complexity += 2
  if (analysis.hasPayment) complexity += 2
  if (analysis.hasAuth) complexity += 1
  if (analysis.isExternalFacing) complexity += 1
  if (/integration|external api|third-party/i.test(combined)) complexity += 2

  analysis.complexity = Math.min(complexity, 10)

  // Adjust risk level
  if (analysis.complexity >= 7 || analysis.hasCompliance || analysis.hasPayment) {
    analysis.riskLevel = 'HIGH'
  } else if (analysis.complexity >= 4 || analysis.hasAuth) {
    analysis.riskLevel = 'MEDIUM'
  }

  return analysis
}

// ============================================================
// RESEARCH LAYERS
// ============================================================

/**
 * Determine research layers dynamically based on change characteristics
 * Returns 0-13 layers depending on what the change needs
 */
export function determineResearchLayers(analysis) {
  const layers = []
  let order = 1

  // Check for trivial changes (0 layers)
  if (analysis.complexity <= 1 &&
      !analysis.hasUI && !analysis.hasAPI && !analysis.hasDatabase &&
      analysis.riskLevel === 'LOW') {
    return [] // No research needed
  }

  // L1: Best Practice (ALWAYS for non-trivial changes)
  layers.push({
    order: order++,
    name: 'Best Practice / Industry Standard',
    focus: `How do others implement ${analysis.primaryType}?`,
    questions: [
      `What is the industry standard for ${analysis.primaryType}?`,
      'What are common patterns and anti-patterns?',
      'What are the key success factors?',
      'What are common failure modes?'
    ],
    searchTopics: [`${analysis.primaryType} best practices`, `${analysis.primaryType} patterns`]
  })

  // L2: Security layer (for auth, payment, sensitive data)
  if (analysis.hasAuth || analysis.hasPayment || analysis.hasSensitiveData) {
    layers.push({
      order: order++,
      name: 'Security Requirements',
      focus: 'What security measures are required?',
      questions: [
        'What authentication/authorization is needed?',
        'What data protection is required?',
        'What are common security vulnerabilities?',
        'What compliance requirements apply?'
      ],
      searchTopics: ['security best practices', `${analysis.primaryType} security`]
    })
  }

  // L3: Compliance layer (for regulated industries)
  if (analysis.hasCompliance || analysis.industryContext) {
    layers.push({
      order: order++,
      name: `${analysis.industryContext || 'Industry'} Compliance`,
      focus: `What ${analysis.industryContext || 'industry'} regulations apply?`,
      questions: [
        'What regulatory requirements must be met?',
        'What audit trails are needed?',
        'What data handling rules apply?',
        'What documentation is required?'
      ],
      searchTopics: [`${analysis.industryContext} compliance`, `${analysis.industryContext} regulations`]
    })
  }

  // L4: UX layer (for external-facing UI)
  if (analysis.isExternalFacing && analysis.hasUI) {
    layers.push({
      order: order++,
      name: 'User Experience Patterns',
      focus: 'What UX patterns work for this audience?',
      questions: [
        'What user journey is expected?',
        'What conversion patterns work?',
        'What accessibility requirements apply?',
        'What are user expectations?'
      ],
      searchTopics: [`${analysis.primaryType} UX`, `${analysis.audience} UX patterns`]
    })
  }

  // L5: Psychology layer (for marketing/sales)
  if (analysis.primaryType === 'marketing' || /conversion|sales|cta/i.test(analysis.primaryType)) {
    layers.push({
      order: order++,
      name: 'Conversion Psychology',
      focus: 'What psychological triggers work?',
      questions: [
        'What is the buyer awareness level?',
        'What pain points to address?',
        'What objections to overcome?',
        'What social proof is needed?'
      ],
      searchTopics: ['conversion psychology', 'landing page psychology']
    })
  }

  // L6: Content Strategy layer (for content-heavy pages)
  if (analysis.primaryType === 'marketing' || /content|blog|documentation/i.test(analysis.primaryType)) {
    layers.push({
      order: order++,
      name: 'Content Strategy',
      focus: 'What content structure works?',
      questions: [
        'What content hierarchy is effective?',
        'What tone and voice to use?',
        'What call-to-actions work?',
        'What content gaps exist?'
      ],
      searchTopics: ['content strategy', 'copywriting best practices']
    })
  }

  // L7: Data Architecture layer (for database/data-intensive)
  if (analysis.hasDatabase || /data|analytics|reporting/i.test(analysis.primaryType)) {
    layers.push({
      order: order++,
      name: 'Data Architecture',
      focus: 'What data patterns are appropriate?',
      questions: [
        'What normalization level is appropriate?',
        'What indexing strategy is needed?',
        'What scaling considerations apply?',
        'What data integrity rules?'
      ],
      searchTopics: ['database design patterns', 'data architecture']
    })
  }

  // L8: API Design layer (for API-focused changes)
  if (analysis.hasAPI || analysis.primaryType === 'api') {
    layers.push({
      order: order++,
      name: 'API Design',
      focus: 'What API patterns are appropriate?',
      questions: [
        'What API style is appropriate (REST/GraphQL)?',
        'What versioning strategy?',
        'What error handling patterns?',
        'What rate limiting/throttling?'
      ],
      searchTopics: ['API design best practices', 'REST API patterns']
    })
  }

  // L9: Multi-tenancy layer (for SaaS)
  if (analysis.features.includes('multi-tenancy')) {
    layers.push({
      order: order++,
      name: 'Multi-tenancy Patterns',
      focus: 'What isolation and scaling patterns?',
      questions: [
        'What data isolation model?',
        'What authentication per tenant?',
        'What resource limits?',
        'What billing model integration?'
      ],
      searchTopics: ['multi-tenant architecture', 'SaaS patterns']
    })
  }

  // L10: Real-time layer (for collaboration/live features)
  if (analysis.features.includes('realtime')) {
    layers.push({
      order: order++,
      name: 'Real-time Architecture',
      focus: 'What real-time patterns are needed?',
      questions: [
        'WebSocket vs SSE vs polling?',
        'What conflict resolution?',
        'What offline support?',
        'What scaling for connections?'
      ],
      searchTopics: ['real-time architecture', 'WebSocket patterns']
    })
  }

  // L11: Performance layer (for high-traffic or data-intensive)
  if (analysis.isExternalFacing || analysis.complexity >= 6 ||
      /performance|speed|optimization|cache/i.test(analysis.primaryType)) {
    layers.push({
      order: order++,
      name: 'Performance Optimization',
      focus: 'What performance patterns are needed?',
      questions: [
        'What caching strategy?',
        'What lazy loading patterns?',
        'What CDN/edge considerations?',
        'What database optimization?'
      ],
      searchTopics: ['performance optimization', 'caching strategies']
    })
  }

  // L12: Integration layer (for external APIs/services)
  if (/integration|external api|third-party|webhook/i.test(analysis.primaryType) ||
      analysis.features.some(f => /payment|email|sms|notification/i.test(f))) {
    layers.push({
      order: order++,
      name: 'Integration Patterns',
      focus: 'What integration patterns are robust?',
      questions: [
        'What retry/circuit breaker patterns?',
        'What error handling for external failures?',
        'What monitoring/alerting?',
        'What idempotency requirements?'
      ],
      searchTopics: ['integration patterns', 'API integration best practices']
    })
  }

  // L13: Testing Strategy layer (for complex/high-risk)
  if (analysis.riskLevel === 'HIGH' || analysis.complexity >= 7) {
    layers.push({
      order: order++,
      name: 'Testing Strategy',
      focus: 'What testing coverage is needed?',
      questions: [
        'What unit vs integration vs e2e balance?',
        'What edge cases to cover?',
        'What load/stress testing?',
        'What security testing?'
      ],
      searchTopics: ['testing strategy', `${analysis.primaryType} testing`]
    })
  }

  return layers
}

// ============================================================
// LIBRARY EXTRACTION
// ============================================================

/**
 * Extract potential library names from text using pattern matching.
 * Comprehensive extraction for package files, imports, and prose mentions.
 */
export function extractPotentialLibraryNames(text) {
  const candidates = new Set()

  // NPM dependencies: "react": "^18.0.0"
  const npmDeps = text.match(/"([a-z@][a-z0-9._/-]*)"\s*:\s*"[\^~]?\d/gi) || []
  npmDeps.forEach(m => {
    const match = m.match(/"([^"]+)"/)
    if (match) candidates.add(match[1].replace(/^@[^/]+\//, ''))
  })

  // Python requirements: sqlalchemy==2.0.0
  const pyDeps = text.match(/^\s*([a-zA-Z][a-zA-Z0-9_-]*)\s*[=<>~!]/gm) || []
  pyDeps.forEach(m => {
    const match = m.match(/([a-zA-Z][a-zA-Z0-9_-]*)\s*[=<>~!]/)
    if (match) candidates.add(match[1])
  })

  // Rust Cargo: tokio = "1.0"
  const rustDeps = text.match(/^\s*([a-z][a-z0-9_-]*)\s*=/gm) || []
  rustDeps.forEach(m => {
    const match = m.match(/([a-z][a-z0-9_-]*)\s*=/)
    if (match) candidates.add(match[1])
  })

  // Go mod: github.com/gin-gonic/gin
  const goDeps = text.match(/(?:require\s+)?github\.com\/[^/\s]+\/([a-z][a-z0-9_-]*)/gi) || []
  goDeps.forEach(m => {
    const match = m.match(/\/([a-z][a-z0-9_-]*)$/i)
    if (match) candidates.add(match[1])
  })

  // Python imports: from sqlalchemy import, import pydantic
  const pyImports = text.match(/(?:from|import)\s+([a-zA-Z][a-zA-Z0-9_]*)/g) || []
  pyImports.forEach(m => {
    const match = m.match(/(?:from|import)\s+([a-zA-Z][a-zA-Z0-9_]*)/)
    if (match) candidates.add(match[1])
  })

  // JS imports: import X from 'Y', require('Y')
  const jsImports = text.match(/(?:from|require\s*\(\s*)['"]([a-zA-Z@][a-zA-Z0-9._/-]*)['"]/g) || []
  jsImports.forEach(m => {
    const match = m.match(/['"]([^'"]+)['"]/)
    if (match) {
      const pkg = match[1].replace(/^@[^/]+\//, '').split('/')[0]
      candidates.add(pkg)
    }
  })

  // Rust imports: use tokio::, extern crate serde
  const rustImports = text.match(/(?:use|extern\s+crate)\s+([a-z][a-z0-9_]*)/g) || []
  rustImports.forEach(m => {
    const match = m.match(/(?:use|extern\s+crate)\s+([a-z][a-z0-9_]*)/)
    if (match) candidates.add(match[1])
  })

  // Prose mentions: "using FastAPI", "with Prisma"
  const techMentions = text.match(/(?:using|with|via|built with|powered by)\s+([A-Z][a-zA-Z0-9.]*)/gi) || []
  techMentions.forEach(m => {
    const match = m.match(/\s([A-Z][a-zA-Z0-9.]*)$/i)
    if (match) candidates.add(match[1])
  })

  // CamelCase: FastAPI, NextAuth
  const camelCase = text.match(/\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b/g) || []
  camelCase.forEach(w => candidates.add(w))

  // Mixed case: SQLAlchemy, PostgreSQL
  const mixedCase = text.match(/\b([A-Z]{2,}[a-z]+[A-Za-z]*)\b/g) || []
  mixedCase.forEach(w => candidates.add(w))

  // PascalCase after tech keywords
  const techKeywordPatterns = [
    /(?:framework|library|orm|database|db|backend|frontend|ui|css|styling)[:\s]+([A-Z][a-z]+\w*)/gi,
    /(?:built\s+with|powered\s+by|using|via|with)\s+([A-Z][a-z]+\w*)/gi
  ]
  techKeywordPatterns.forEach(pattern => {
    const matches = text.matchAll(pattern)
    for (const match of matches) {
      if (match[1]) candidates.add(match[1])
    }
  })

  // Markdown bold: **Express.js**, **Prisma**, **Drizzle ORM**
  const boldWords = text.match(/\*\*([a-zA-Z][a-zA-Z0-9._\- ]+)\*\*/g) || []
  boldWords.forEach(m => {
    const match = m.match(/\*\*([a-zA-Z][a-zA-Z0-9._\- ]+)\*\*/)
    if (match) {
      const lib = match[1].replace(/\.(js|ts|py|rb|go|rs)$/i, '').trim()
      const firstWord = lib.split(/\s+/)[0]
      candidates.add(firstWord)
    }
  })

  // Code backticks: `prisma`, `express`
  const codeWords = text.match(/`([a-zA-Z][a-zA-Z0-9_-]+)`/g) || []
  codeWords.forEach(m => {
    const match = m.match(/`([a-zA-Z][a-zA-Z0-9_-]+)`/)
    if (match && match[1].length > 2) candidates.add(match[1])
  })

  // Known framework patterns: Next.js, Vue.js
  const dotJs = text.match(/\b([A-Z][a-z]+)\.js\b/gi) || []
  dotJs.forEach(m => {
    const match = m.match(/([A-Z][a-z]+)/i)
    if (match) candidates.add(match[1])
  })

  // Stop words filter
  const stopWords = new Set([
    'the', 'this', 'that', 'with', 'from', 'using', 'for', 'and', 'but', 'not',
    'all', 'any', 'can', 'could', 'should', 'would', 'will', 'may', 'might',
    'each', 'every', 'some', 'many', 'most', 'other', 'such', 'only', 'just',
    'also', 'well', 'back', 'even', 'still', 'already', 'always', 'never',
    'api', 'rest', 'http', 'https', 'json', 'xml', 'html', 'css', 'sql',
    'get', 'post', 'put', 'delete', 'patch', 'url', 'uri', 'uuid', 'id',
    'true', 'false', 'none', 'null', 'undefined', 'error', 'exception',
    'class', 'function', 'method', 'object', 'array', 'string', 'number',
    'boolean', 'int', 'float', 'double', 'char', 'byte', 'long', 'short',
    'public', 'private', 'protected', 'static', 'final', 'const', 'let', 'var',
    'import', 'export', 'module', 'package', 'interface', 'type', 'enum',
    'test', 'tests', 'spec', 'specs', 'mock', 'stub', 'fake', 'spy',
    'config', 'configuration', 'settings', 'options', 'params', 'args',
    'user', 'users', 'admin', 'auth', 'login', 'logout', 'session', 'token',
    'data', 'database', 'table', 'column', 'row', 'index', 'key', 'value',
    'file', 'files', 'path', 'dir', 'directory', 'folder', 'name', 'size',
    'create', 'read', 'update', 'delete', 'list', 'get', 'set', 'add', 'remove',
    'start', 'stop', 'run', 'build', 'deploy', 'install', 'setup', 'init',
    'version', 'release', 'beta', 'alpha', 'stable', 'latest', 'current'
  ])

  return [...candidates]
    .filter(w => w.length > 2 && w.length < 30)
    .filter(w => !stopWords.has(w.toLowerCase()))
    .filter(w => !/^\d+$/.test(w))
    .filter(w => !/^v?\d+\.\d+/.test(w))
    .slice(0, 50)
}

// ============================================================
// CONTEXT7 PARSING
// ============================================================

/**
 * Parse Context7 response and select the best matching library.
 */
export function parseContext7Response(response, searchTerm) {
  const libraries = []
  const blocks = response.split('----------').filter(b => b.trim())

  for (const block of blocks) {
    const titleMatch = block.match(/Title:\s*(.+)/i)
    const idMatch = block.match(/Context7-compatible library ID:\s*(\S+)/i)
    const snippetsMatch = block.match(/Code Snippets:\s*(\d+)/i)
    const scoreMatch = block.match(/Benchmark Score:\s*([\d.]+)/i)

    if (titleMatch && idMatch) {
      libraries.push({
        title: titleMatch[1].trim(),
        id: idMatch[1].trim(),
        snippets: snippetsMatch ? parseInt(snippetsMatch[1]) : 0,
        score: scoreMatch ? parseFloat(scoreMatch[1]) : 50
      })
    }
  }

  if (libraries.length === 0) return null

  const searchLower = searchTerm.toLowerCase()

  // First: exact match
  const exactMatch = libraries.find(l =>
    l.title.toLowerCase() === searchLower ||
    l.id.toLowerCase().includes(searchLower)
  )
  if (exactMatch) return exactMatch

  // Second: partial match with good score
  const partialMatches = libraries.filter(l =>
    l.title.toLowerCase().includes(searchLower) ||
    searchLower.includes(l.title.toLowerCase())
  )
  if (partialMatches.length > 0) {
    return partialMatches.sort((a, b) => b.score - a.score)[0]
  }

  // Third: best overall score (only if snippets > 100 for quality)
  const qualityLibs = libraries.filter(l => l.snippets > 100)
  if (qualityLibs.length > 0) {
    return qualityLibs.sort((a, b) => b.score - a.score)[0]
  }

  // Fallback: first result
  return libraries[0]
}

// ============================================================
// INTEGRATION RISKS
// ============================================================

/**
 * Detect integration risks from library documentation.
 */
export function detectIntegrationRisks(docs, currentLib, allLibs) {
  const risks = []
  const docsLower = docs.toLowerCase()

  const riskPatterns = [
    {
      keywords: ['adapter', 'drizzleadapter', 'prismaadapter'],
      risk: 'Database adapter configuration required',
      pattern: 'adapter',
      recommendation: 'Verify adapter schema matches expected column names'
    },
    {
      keywords: ['column', 'columnname', 'snake_case', 'camelcase', 'mapping'],
      risk: 'Column naming convention mismatch possible',
      pattern: 'schema',
      recommendation: 'Check column naming between ORM schema and library expectations'
    },
    {
      keywords: ['userstable', 'accountstable', 'sessionstable', 'schema'],
      risk: 'Custom table schema required',
      pattern: 'schema',
      recommendation: 'Ensure table schemas match library documentation exactly'
    },
    {
      keywords: ['sync', 'migrate', 'migration', 'syncurl', 'embedded replica'],
      risk: 'Data synchronization setup required',
      pattern: 'sync',
      recommendation: 'Configure sync intervals and handle offline scenarios'
    },
    {
      keywords: ['webhook', 'webhookendpoint', 'webhooksecret'],
      risk: 'Webhook endpoint configuration required',
      pattern: 'webhook',
      recommendation: 'Set up webhook endpoints and verify signatures'
    },
    {
      keywords: ['apikey', 'secretkey', 'authtoken', 'bearer'],
      risk: 'API credentials setup required',
      pattern: 'credentials',
      recommendation: 'Store credentials securely in environment variables'
    },
    {
      keywords: ['beforeall', 'afterall', 'beforeeach', 'aftereach', 'setup', 'teardown'],
      risk: 'Test lifecycle hooks required',
      pattern: 'lifecycle',
      recommendation: 'Implement proper setup/teardown in test configuration'
    }
  ]

  for (const rp of riskPatterns) {
    const found = rp.keywords.some(kw => docsLower.includes(kw.toLowerCase()))
    if (found) {
      const involvedLibs = allLibs
        .filter(l => l.name !== currentLib)
        .filter(l => docsLower.includes(l.name.toLowerCase()))
        .map(l => l.name)

      risks.push({
        library: currentLib,
        risk: rp.risk,
        pattern: rp.pattern,
        recommendation: rp.recommendation,
        involvedLibraries: involvedLibs
      })
    }
  }

  return risks
}

// ============================================================
// RESEARCH CHECKLIST
// ============================================================

/**
 * Generate research checklist markdown content
 */
export function generateResearchChecklist(analysis, layers, libraryResults) {
  if (layers.length === 0) {
    return `# Research Checklist

> No Research Required

This is a trivial change that doesn't require research layers.
`
  }

  let content = `# Research Checklist

> Generated by Adaptive Depth Research
> Complexity: ${analysis.complexity}/10 | Risk: ${analysis.riskLevel}

## Summary

| Layer | Focus | Status |
|-------|-------|--------|
`

  layers.forEach(layer => {
    content += `| ${layer.name} | ${layer.focus} | ⏳ Pending |\n`
  })

  content += '\n'

  layers.forEach(layer => {
    content += `## ${layer.name}\n\n`
    content += `**Focus:** ${layer.focus}\n\n`
    content += '### Key Questions\n'
    layer.questions.forEach(q => {
      content += `- [ ] ${q}\n`
    })
    content += '\n'
  })

  return content
}

// ============================================================
// CRITICAL FLOWS
// ============================================================

/**
 * Critical Flow Definitions for security and compliance
 */
export const CRITICAL_FLOWS = {
  auth: {
    security: [
      { id: 'auth-password-hash', check: '☐ Password hashing with bcrypt/argon2 (cost factor ≥ 10)', why: 'Plain text or weak hashing = immediate breach if DB leaked', severity: 'critical' },
      { id: 'auth-rate-limit', check: '☐ Rate limiting on login (max 5 attempts per 15 min)', why: 'Prevents brute force attacks', severity: 'critical' },
      { id: 'auth-session-timeout', check: '☐ Session timeout configured (≤ 24h, ≤ 15min for sensitive)', why: 'Abandoned sessions are attack vectors', severity: 'high' },
      { id: 'auth-csrf', check: '☐ CSRF protection on all state-changing endpoints', why: 'OWASP Top 10 vulnerability', severity: 'critical' },
      { id: 'auth-secure-cookies', check: '☐ Cookies: httpOnly, secure, sameSite=strict', why: 'Prevents XSS token theft and CSRF', severity: 'critical' },
      { id: 'auth-password-policy', check: '☐ Password policy enforced (min 8 chars, complexity optional)', why: 'Weak passwords are #1 breach cause', severity: 'high' },
      { id: 'auth-account-lockout', check: '☐ Account lockout after repeated failures (with unlock mechanism)', why: 'Prevents brute force, but needs recovery path', severity: 'medium' }
    ],
    flow: [
      { id: 'auth-flow-login', check: '☐ Login flow: input → validate → session → redirect', why: 'Standard secure login pattern', severity: 'high' },
      { id: 'auth-flow-logout', check: '☐ Logout: invalidate session server-side (not just cookie)', why: 'Client-side only logout leaves session valid', severity: 'high' },
      { id: 'auth-flow-forgot', check: '☐ Forgot password: email → time-limited token → reset', why: 'Token must expire (≤ 1 hour)', severity: 'high' }
    ]
  },
  payment: {
    security: [
      { id: 'payment-no-card-storage', check: '☐ NO raw card numbers stored (use Stripe/payment provider tokens)', why: 'PCI-DSS requirement, storing cards = massive liability', severity: 'critical' },
      { id: 'payment-https', check: '☐ HTTPS enforced on all payment pages', why: 'Payment data in transit must be encrypted', severity: 'critical' },
      { id: 'payment-webhook-verify', check: '☐ Webhook signature verification (never trust unverified webhooks)', why: 'Attackers can fake payment success webhooks', severity: 'critical' },
      { id: 'payment-idempotency', check: '☐ Idempotency keys for payment creation', why: 'Prevents double charges on retry', severity: 'high' },
      { id: 'payment-amount-verify', check: '☐ Server-side price verification (never trust client price)', why: 'Attackers modify client-side prices', severity: 'critical' }
    ],
    flow: [
      { id: 'payment-flow-checkout', check: '☐ Checkout flow: cart → address → payment → confirm → receipt', why: 'Standard e-commerce pattern users expect', severity: 'medium' },
      { id: 'payment-flow-error', check: '☐ Payment error handling with clear user message', why: 'Failed payments need recovery path', severity: 'high' },
      { id: 'payment-flow-refund', check: '☐ Refund flow documented (even if manual)', why: 'Legal requirement in most jurisdictions', severity: 'high' }
    ]
  },
  sensitiveData: {
    security: [
      { id: 'data-encryption-rest', check: '☐ Encryption at rest for PII/PHI (AES-256 or DB-level)', why: 'Breached DB without encryption = full exposure', severity: 'critical' },
      { id: 'data-encryption-transit', check: '☐ Encryption in transit (TLS 1.2+)', why: 'Data interception prevention', severity: 'critical' },
      { id: 'data-access-logging', check: '☐ Audit logging for sensitive data access', why: 'Required for breach investigation and compliance', severity: 'high' },
      { id: 'data-minimization', check: '☐ Data minimization (only collect what is needed)', why: 'GDPR principle, reduces breach impact', severity: 'medium' }
    ],
    dataArchitecture: [
      { id: 'data-arch-backup', check: '☐ Backup strategy with encryption', why: 'Backups are often unencrypted breach vector', severity: 'high' },
      { id: 'data-arch-retention', check: '☐ Data retention policy defined', why: 'Legal requirement (GDPR right to deletion)', severity: 'medium' }
    ]
  },
  healthcare: {
    compliance: [
      { id: 'hipaa-phi-encrypt', check: '☐ All PHI encrypted at rest and in transit', why: 'HIPAA Security Rule requirement', severity: 'critical' },
      { id: 'hipaa-access-control', check: '☐ Role-based access control for PHI', why: 'Minimum necessary standard', severity: 'critical' },
      { id: 'hipaa-audit-trail', check: '☐ Audit trail for all PHI access (who, what, when)', why: 'HIPAA requires 6-year audit log retention', severity: 'critical' },
      { id: 'hipaa-baa', check: '☐ BAA signed with all vendors handling PHI', why: 'Business Associate Agreement legally required', severity: 'critical' },
      { id: 'hipaa-breach-plan', check: '☐ Breach notification plan documented', why: '60-day notification requirement', severity: 'high' }
    ]
  },
  fintech: {
    compliance: [
      { id: 'pci-no-pan', check: '☐ No PAN (card numbers) stored unless PCI certified', why: 'PCI-DSS Level 1 requirement', severity: 'critical' },
      { id: 'pci-tokenization', check: '☐ Tokenization for card data (Stripe, Braintree)', why: 'Removes PCI scope from your systems', severity: 'critical' },
      { id: 'pci-network-segment', check: '☐ Network segmentation for payment systems', why: 'Limits breach blast radius', severity: 'high' },
      { id: 'fintech-kyc', check: '☐ KYC verification flow for financial accounts', why: 'AML/KYC regulations', severity: 'high' },
      { id: 'fintech-transaction-limits', check: '☐ Transaction limits and velocity checks', why: 'Fraud prevention, regulatory requirement', severity: 'high' },
      { id: 'fintech-audit', check: '☐ Transaction audit trail (immutable)', why: 'Regulatory reporting requirement', severity: 'critical' }
    ]
  }
}

/**
 * Inject critical required items based on layer type and change analysis
 */
export function injectCriticalRequiredItems(layer, changeAnalysis) {
  const items = []

  // Security Requirements Layer
  if (layer.name === 'Security Requirements') {
    if (changeAnalysis.hasAuth) {
      items.push(...CRITICAL_FLOWS.auth.security)
    }
    if (changeAnalysis.hasPayment) {
      items.push(...CRITICAL_FLOWS.payment.security)
    }
    if (changeAnalysis.hasSensitiveData) {
      items.push(...CRITICAL_FLOWS.sensitiveData.security)
    }
  }

  // Compliance Layer
  if (layer.name.includes('Compliance')) {
    if (changeAnalysis.industryContext === 'healthcare') {
      items.push(...CRITICAL_FLOWS.healthcare.compliance)
    }
    if (changeAnalysis.industryContext === 'fintech') {
      items.push(...CRITICAL_FLOWS.fintech.compliance)
    }
  }

  // Data Architecture Layer
  if (layer.name === 'Data Architecture') {
    if (changeAnalysis.hasSensitiveData) {
      items.push(...CRITICAL_FLOWS.sensitiveData.dataArchitecture)
    }
  }

  return items
}
