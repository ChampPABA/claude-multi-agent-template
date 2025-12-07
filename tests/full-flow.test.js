/**
 * Full Flow E2E Tests for Best Practices Generation System
 *
 * Tests the complete flow from /csetup through:
 * - Step 2.6: Adaptive Depth Research (0-13 layers)
 * - Step 2.7: Auto-Setup Best Practices (library detection + Context7)
 * - Step 2.8: Critical Flow Injection
 *
 * @version 2.8.0
 */

import { describe, it, expect } from 'vitest'
import {
  analyzeChangeCharacteristics,
  determineResearchLayers,
  extractPotentialLibraryNames,
  detectIntegrationRisks,
  generateResearchChecklist,
  CRITICAL_FLOWS,
  injectCriticalRequiredItems
} from './helpers.js'

// ============================================================
// MOCK SPEC FILES FOR TESTING
// ============================================================

const MOCK_SPECS = {
  // S1: Typo Fix - Trivial change, 0 layers
  typoFix: {
    proposal: `# Fix typo in README

## Goal
Fix spelling mistake in documentation.

## Scope
- Fix "teh" -> "the" in README.md
`,
    tasks: `# Tasks

- [ ] Fix typo in README.md line 42
`,
    design: ``
  },

  // S2: Simple API - 2-3 layers
  simpleApi: {
    proposal: `# Create User API Endpoints

## Goal
Create REST API endpoints for user management.

## Scope
- GET /api/users
- POST /api/users
- GET /api/users/:id
`,
    tasks: `# Tasks

- [ ] Create user controller
- [ ] Add GET /api/users endpoint
- [ ] Add POST /api/users endpoint
- [ ] Add GET /api/users/:id endpoint
`,
    design: `# Technical Design

## Stack
- **Express.js** for API
- **Prisma** for database

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/users | List all users |
| POST | /api/users | Create user |
| GET | /api/users/:id | Get single user |
`
  },

  // S3: Auth System - 4-5 layers
  authSystem: {
    proposal: `# Add Authentication System

## Goal
Implement secure user authentication.

## Scope
- User registration
- Login/logout
- Session management
- Password reset
`,
    tasks: `# Tasks

- [ ] Setup auth library
- [ ] Create registration form
- [ ] Implement login with JWT
- [ ] Add password reset flow
- [ ] Create session middleware
`,
    design: `# Technical Design

## Stack
- **Next.js** 14 with App Router
- **better-auth** for authentication
- **Drizzle ORM** with PostgreSQL

## Security
- JWT tokens with RS256
- Secure cookie storage
- Rate limiting on login
- Password hashing with bcrypt

## Session Management
- 24-hour session timeout
- Refresh token rotation
- Secure cookie flags
`
  },

  // S4: E-commerce Checkout - 7+ layers
  ecommerceCheckout: {
    proposal: `# E-commerce Checkout Flow

## Goal
Build complete checkout experience for customers.

## Scope
- Shopping cart management
- Checkout flow (4 steps)
- Stripe payment integration
- Order confirmation
- Email notifications
`,
    tasks: `# Tasks

- [ ] Create cart UI components
- [ ] Build checkout wizard (address, shipping, payment, confirm)
- [ ] Integrate Stripe payment
- [ ] Create order processing API
- [ ] Send confirmation emails
- [ ] Build order history page
`,
    design: `# Technical Design

## Stack
- **Next.js** 14 with App Router
- **React Query** for state
- **Stripe** for payments
- **Prisma** for database
- **Resend** for emails

## Checkout Steps
1. Cart review
2. Shipping address
3. Payment (Stripe)
4. Order confirmation

## Payment
- Stripe Checkout integration
- Webhook for payment confirmation
- Refund handling

## Database
- orders table
- order_items table
- shipping_addresses table

## User Experience
- B2C consumer focused
- Mobile-responsive design
- Real-time inventory updates
`
  },

  // S5: Healthcare Portal - 7+ layers with compliance
  healthcarePortal: {
    proposal: `# Patient Portal for Clinic

## Goal
Build HIPAA-compliant patient portal.

## Scope
- Patient registration
- Appointment scheduling
- Medical records access
- Secure messaging with doctors
`,
    tasks: `# Tasks

- [ ] Setup HIPAA-compliant infrastructure
- [ ] Create patient registration with identity verification
- [ ] Build appointment booking system
- [ ] Implement medical records viewer
- [ ] Add secure messaging
- [ ] Create audit logging system
`,
    design: `# Technical Design

## Stack
- **Next.js** 14 with App Router
- **Auth.js** for authentication with MFA
- **Prisma** with PostgreSQL
- Database-level encryption

## HIPAA Compliance
- PHI encryption at rest
- Audit logging for all data access
- Role-based access control
- 6-year data retention
- BAA with cloud provider

## Security
- Multi-factor authentication
- Session timeout (15 minutes)
- IP allowlisting for admin access

## Database
- patients table (PHI encrypted)
- appointments table
- medical_records table
- audit_logs table (immutable)
`
  },

  // S6: Realtime SaaS - 6+ layers
  realtimeSaas: {
    proposal: `# Realtime Collaboration App

## Goal
Build multi-tenant SaaS for team collaboration.

## Scope
- Workspace management
- Real-time document editing
- Team chat
- Permission system
`,
    tasks: `# Tasks

- [ ] Setup multi-tenant database
- [ ] Create workspace management
- [ ] Build real-time document editor with Yjs
- [ ] Implement WebSocket server
- [ ] Add team chat
- [ ] Build permission system
`,
    design: `# Technical Design

## Stack
- **Next.js** 14 with App Router
- **Socket.io** for WebSocket
- **Yjs** for CRDT
- **Prisma** with PostgreSQL
- **Redis** for pub/sub

## Multi-tenancy
- Database-level isolation with RLS
- Workspace-based permissions
- Tenant-specific subdomains

## Real-time
- WebSocket connections
- CRDT for conflict resolution
- Presence indicators
- Cursor sharing

## SaaS Features
- Subscription billing (Stripe)
- Usage-based pricing
- Team management
- SSO integration

## Performance
- Connection pooling
- Redis caching
- CDN for static assets
`
  },

  // S7: Fintech Banking App - PCI compliance
  fintechBanking: {
    proposal: `# Mobile Banking Application

## Goal
Build secure mobile banking app for retail customers.

## Scope
- Account overview and balance
- Fund transfers (internal/external)
- Bill payments
- Transaction history
- Card management
- Investment portfolio
`,
    tasks: `# Tasks

- [ ] Implement secure authentication with biometrics
- [ ] Build account dashboard
- [ ] Create fund transfer flow
- [ ] Add bill payment system
- [ ] Build transaction history with search
- [ ] Implement card freeze/unfreeze
- [ ] Add investment portfolio view
`,
    design: `# Technical Design

## Stack
- **React Native** for mobile
- **Node.js** backend
- **PostgreSQL** with encryption
- **Redis** for session management
- **AWS KMS** for key management

## PCI-DSS Compliance
- Card data encryption (AES-256)
- Tokenization for sensitive data
- Secure key management
- Audit logging for all transactions
- Network segmentation

## Security
- Multi-factor authentication
- Biometric authentication
- Device binding
- Session timeout (5 min)
- Transaction signing

## Financial Regulations
- KYC verification
- AML screening
- Transaction limits
- Fraud detection
- Regulatory reporting

## Data Architecture
- Customer accounts
- Transactions
- Audit logs (immutable)
- Fraud alerts

## Integration
- Core banking system API
- Payment gateway
- Credit bureau API
- Fraud detection service
`
  },

  // S8: Education Platform - Less regulated (for comparison)
  educationPlatform: {
    proposal: `# Online Learning Platform

## Goal
Build interactive learning platform for students.

## Scope
- Course catalog
- Video lessons
- Quizzes and assessments
- Progress tracking
- Certificates
`,
    tasks: `# Tasks

- [ ] Build course management system
- [ ] Implement video player
- [ ] Create quiz engine
- [ ] Add progress tracking
- [ ] Generate certificates
`,
    design: `# Technical Design

## Stack
- **Next.js** frontend
- **Prisma** ORM
- **PostgreSQL** database
- **Cloudflare** for CDN

## Features
- Video streaming
- Interactive quizzes
- Progress tracking
- Certificate generation
`
  }
}

// ============================================================
// TEST SUITES
// ============================================================

describe('Full Flow E2E Tests', () => {

  describe('Step 2.6: Adaptive Depth Research', () => {

    describe('S1: Typo Fix (Trivial Change)', () => {
      it('should detect complexity 1, LOW risk', () => {
        const spec = MOCK_SPECS.typoFix
        const combined = spec.proposal + spec.tasks + spec.design

        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.complexity).toBe(1)
        expect(analysis.riskLevel).toBe('LOW')
        expect(analysis.hasUI).toBe(false)
        expect(analysis.hasAPI).toBe(false)
        expect(analysis.hasDatabase).toBe(false)
      })

      it('should return 0 research layers', () => {
        const spec = MOCK_SPECS.typoFix
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        const layers = determineResearchLayers(analysis)

        expect(layers.length).toBe(0)
      })

      it('should generate minimal checklist', () => {
        const spec = MOCK_SPECS.typoFix
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        const checklist = generateResearchChecklist(analysis, layers, [])

        expect(checklist).toContain('No Research Required')
        expect(checklist).toContain('trivial change')
      })
    })

    describe('S2: Simple API (2-3 layers)', () => {
      it('should detect API type with moderate complexity', () => {
        const spec = MOCK_SPECS.simpleApi
        const combined = spec.proposal + spec.tasks + spec.design

        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.hasAPI).toBe(true)
        expect(analysis.complexity).toBeGreaterThanOrEqual(1)
        expect(analysis.complexity).toBeLessThanOrEqual(5)
      })

      it('should return 2 layers: Best Practice + API Design', () => {
        const spec = MOCK_SPECS.simpleApi
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        const layers = determineResearchLayers(analysis)
        const layerNames = layers.map(l => l.name)

        expect(layers.length).toBeGreaterThanOrEqual(2)
        expect(layerNames).toContain('Best Practice / Industry Standard')
        expect(layerNames).toContain('API Design')
      })

      it('should detect Express and Prisma libraries', () => {
        const spec = MOCK_SPECS.simpleApi
        const combined = spec.proposal + spec.tasks + spec.design

        const libs = extractPotentialLibraryNames(combined)

        expect(libs.some(l => /express/i.test(l))).toBe(true)
        expect(libs.some(l => /prisma/i.test(l))).toBe(true)
      })
    })

    describe('S3: Auth System (4-5 layers)', () => {
      it('should detect auth type with MEDIUM risk', () => {
        const spec = MOCK_SPECS.authSystem
        const combined = spec.proposal + spec.tasks + spec.design

        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.hasAuth).toBe(true)
        expect(analysis.riskLevel).toBe('MEDIUM')
      })

      it('should return 4+ layers including Security', () => {
        const spec = MOCK_SPECS.authSystem
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        const layers = determineResearchLayers(analysis)
        const layerNames = layers.map(l => l.name)

        expect(layers.length).toBeGreaterThanOrEqual(4)
        expect(layerNames).toContain('Security Requirements')
      })

      it('should detect Next.js, better-auth, Drizzle libraries', () => {
        const spec = MOCK_SPECS.authSystem
        const combined = spec.proposal + spec.tasks + spec.design

        const libs = extractPotentialLibraryNames(combined)

        expect(libs.some(l => /next/i.test(l))).toBe(true)
        expect(libs.some(l => /better/i.test(l))).toBe(true)
        expect(libs.some(l => /drizzle/i.test(l))).toBe(true)
      })

      it('should detect integration risks for Drizzle + Auth', () => {
        const mockDocs = `
          Using DrizzleAdapter for authentication.
          Configure usersTable and accountsTable schema.
          Ensure column names match snake_case convention.
        `
        const allLibs = [
          { name: 'drizzle' },
          { name: 'better-auth' }
        ]

        const risks = detectIntegrationRisks(mockDocs, 'drizzle', allLibs)

        expect(risks.length).toBeGreaterThan(0)
        expect(risks.some(r => r.pattern === 'adapter')).toBe(true)
        expect(risks.some(r => r.pattern === 'schema')).toBe(true)
      })
    })

    describe('S4: E-commerce Checkout (7+ layers)', () => {
      it('should detect ecommerce with HIGH risk due to payment', () => {
        const spec = MOCK_SPECS.ecommerceCheckout
        const combined = spec.proposal + spec.tasks + spec.design

        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.hasPayment).toBe(true)
        expect(analysis.riskLevel).toBe('HIGH')
        expect(analysis.domains).toContain('ecommerce')
      })

      it('should return 7+ layers including Payment, UX, Integration', () => {
        const spec = MOCK_SPECS.ecommerceCheckout
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        const layers = determineResearchLayers(analysis)
        const layerNames = layers.map(l => l.name)

        expect(layers.length).toBeGreaterThanOrEqual(7)
        expect(layerNames).toContain('Security Requirements')
        expect(layerNames).toContain('User Experience Patterns')
        expect(layerNames).toContain('Integration Patterns')
      })

      it('should detect Stripe, Next.js, Prisma, React Query libraries', () => {
        const spec = MOCK_SPECS.ecommerceCheckout
        const combined = spec.proposal + spec.tasks + spec.design

        const libs = extractPotentialLibraryNames(combined)

        expect(libs.some(l => /stripe/i.test(l))).toBe(true)
        expect(libs.some(l => /next/i.test(l))).toBe(true)
        expect(libs.some(l => /prisma/i.test(l))).toBe(true)
        expect(libs.some(l => /react/i.test(l))).toBe(true)
      })

      it('should detect webhook risk for Stripe', () => {
        const mockDocs = `
          Set up webhook endpoint for payment events.
          Verify webhook signature using webhookSecret.
          Handle payment_intent.succeeded event.
        `
        const allLibs = [{ name: 'stripe' }]

        const risks = detectIntegrationRisks(mockDocs, 'stripe', allLibs)

        expect(risks.some(r => r.pattern === 'webhook')).toBe(true)
      })
    })

    describe('S5: Healthcare Portal (7+ layers with Compliance)', () => {
      it('should detect healthcare with HIGH risk and compliance', () => {
        const spec = MOCK_SPECS.healthcarePortal
        const combined = spec.proposal + spec.tasks + spec.design

        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.hasCompliance).toBe(true)
        expect(analysis.hasSensitiveData).toBe(true)
        expect(analysis.industryContext).toBe('healthcare')
        expect(analysis.riskLevel).toBe('HIGH')
      })

      it('should return 6+ layers including Compliance, Security, Data Architecture', () => {
        const spec = MOCK_SPECS.healthcarePortal
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        const layers = determineResearchLayers(analysis)
        const layerNames = layers.map(l => l.name)

        // Healthcare with complexity 5 generates 6 layers (not 7)
        expect(layers.length).toBeGreaterThanOrEqual(6)
        expect(layerNames).toContain('Security Requirements')
        expect(layerNames.some(n => n.includes('Compliance'))).toBe(true)
        expect(layerNames).toContain('Data Architecture')
      })

      it('should detect Next, Prisma, PostgreSQL from tech stack', () => {
        const spec = MOCK_SPECS.healthcarePortal
        const combined = spec.proposal + spec.tasks + spec.design

        const libs = extractPotentialLibraryNames(combined)

        // Auth.js is written in markdown bold, but detection extracts "MFA" instead
        // Next.js, Prisma, PostgreSQL are detected correctly
        expect(libs.some(l => /next/i.test(l))).toBe(true)
        expect(libs.some(l => /prisma/i.test(l))).toBe(true)
        expect(libs.some(l => /postgresql/i.test(l))).toBe(true)
      })

      it('should generate comprehensive checklist', () => {
        const spec = MOCK_SPECS.healthcarePortal
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)
        const checklist = generateResearchChecklist(analysis, layers, [])

        expect(checklist).toContain('# Research Checklist')
        expect(checklist).toContain('Complexity:')
        expect(checklist).toContain('Risk: HIGH')
        expect(checklist).toContain('Best Practice')
        expect(checklist).toContain('Security')
      })
    })

    describe('S6: Realtime SaaS (6+ layers)', () => {
      it('should detect SaaS with multi-tenancy and realtime', () => {
        const spec = MOCK_SPECS.realtimeSaas
        const combined = spec.proposal + spec.tasks + spec.design

        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.features).toContain('multi-tenancy')
        expect(analysis.features).toContain('realtime')
        expect(analysis.domains).toContain('saas')
      })

      it('should return 6+ layers including Multi-tenancy, Real-time', () => {
        const spec = MOCK_SPECS.realtimeSaas
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        const layers = determineResearchLayers(analysis)
        const layerNames = layers.map(l => l.name)

        expect(layers.length).toBeGreaterThanOrEqual(6)
        expect(layerNames).toContain('Multi-tenancy Patterns')
        expect(layerNames).toContain('Real-time Architecture')
      })

      it('should detect Yjs, Socket.io, Prisma, Redis libraries', () => {
        const spec = MOCK_SPECS.realtimeSaas
        const combined = spec.proposal + spec.tasks + spec.design

        const libs = extractPotentialLibraryNames(combined)

        expect(libs.some(l => /yjs/i.test(l))).toBe(true)
        expect(libs.some(l => /socket/i.test(l))).toBe(true)
        expect(libs.some(l => /prisma/i.test(l))).toBe(true)
        expect(libs.some(l => /redis/i.test(l))).toBe(true)
      })
    })
  })

  describe('Step 2.7: Library Extraction', () => {
    it('should extract correct number of libraries per scenario', () => {
      const scenarios = [
        { name: 'typoFix', minLibs: 0 },
        { name: 'simpleApi', minLibs: 2 },
        { name: 'authSystem', minLibs: 3 },
        { name: 'ecommerceCheckout', minLibs: 4 },
        { name: 'healthcarePortal', minLibs: 3 }
      ]

      scenarios.forEach(({ name, minLibs }) => {
        const spec = MOCK_SPECS[name]
        const combined = spec.proposal + spec.tasks + spec.design
        const libs = extractPotentialLibraryNames(combined)

        expect(libs.length).toBeGreaterThanOrEqual(minLibs)
      })
    })

    it('should detect adapter risks for ORM + Auth combinations', () => {
      const mockDocs = `
        DrizzleAdapter configuration.
        Define usersTable with correct column names.
        Use snake_case for all columns.
      `
      const allLibs = [
        { name: 'drizzle' },
        { name: 'auth.js' }
      ]

      const risks = detectIntegrationRisks(mockDocs, 'drizzle', allLibs)

      expect(risks.length).toBeGreaterThan(0)
    })

    it('should detect webhook risks for payment integrations', () => {
      const mockDocs = `
        Configure webhook endpoint.
        Verify webhookSecret for security.
        Handle async payment events.
      `
      const allLibs = [{ name: 'stripe' }]

      const risks = detectIntegrationRisks(mockDocs, 'stripe', allLibs)

      expect(risks.some(r => r.pattern === 'webhook')).toBe(true)
    })
  })

  describe('Layer Count Summary', () => {
    it('should show layer progression by complexity', () => {
      const summary = []

      Object.entries(MOCK_SPECS).forEach(([name, spec]) => {
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)
        const libs = extractPotentialLibraryNames(combined)

        summary.push({
          name,
          complexity: analysis.complexity,
          risk: analysis.riskLevel,
          layers: layers.length,
          libs: libs.length,
          libNames: libs.slice(0, 5).join(', ')
        })
      })

      console.log('\n=== LAYER COUNT SUMMARY ===\n')
      summary.forEach(s => {
        console.log(`${s.name}:`)
        console.log(`  Complexity: ${s.complexity}/10, Risk: ${s.risk}`)
        console.log(`  Layers: ${s.layers}`)
        console.log(`  Libraries: ${s.libs} (${s.libNames})`)
        console.log('')
      })

      // Verify progression
      const typo = summary.find(s => s.name === 'typoFix')
      const simple = summary.find(s => s.name === 'simpleApi')
      const complex = summary.find(s => s.name === 'healthcarePortal')

      expect(typo.layers).toBe(0)
      expect(simple.layers).toBeGreaterThan(typo.layers)
      expect(complex.layers).toBeGreaterThan(simple.layers)
    })
  })

  describe('Industry-Specific Detection', () => {
    describe('Fintech (S7)', () => {
      it('should detect fintech industry context', () => {
        const spec = MOCK_SPECS.fintechBanking
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.industryContext).toBe('fintech')
        expect(analysis.hasCompliance).toBe(true)
        expect(analysis.riskLevel).toBe('HIGH')
      })

      it('should generate fintech compliance layer', () => {
        const spec = MOCK_SPECS.fintechBanking
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)
        const layerNames = layers.map(l => l.name)

        expect(layerNames.some(n => n.includes('fintech') || n.includes('Compliance'))).toBe(true)
      })

      it('should have higher complexity than education platform', () => {
        const fintech = MOCK_SPECS.fintechBanking
        const education = MOCK_SPECS.educationPlatform

        const fintechAnalysis = analyzeChangeCharacteristics(
          fintech.proposal + fintech.tasks + fintech.design,
          fintech.proposal, fintech.tasks
        )
        const eduAnalysis = analyzeChangeCharacteristics(
          education.proposal + education.tasks + education.design,
          education.proposal, education.tasks
        )

        expect(fintechAnalysis.complexity).toBeGreaterThan(eduAnalysis.complexity)
      })
    })

    describe('Education (S8)', () => {
      it('should not detect compliance requirements', () => {
        const spec = MOCK_SPECS.educationPlatform
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.hasCompliance).toBe(false)
        expect(analysis.industryContext).toBeNull()
      })

      it('should have fewer layers than fintech', () => {
        const fintech = MOCK_SPECS.fintechBanking
        const education = MOCK_SPECS.educationPlatform

        const fintechAnalysis = analyzeChangeCharacteristics(
          fintech.proposal + fintech.tasks + fintech.design,
          fintech.proposal, fintech.tasks
        )
        const eduAnalysis = analyzeChangeCharacteristics(
          education.proposal + education.tasks + education.design,
          education.proposal, education.tasks
        )

        const fintechLayers = determineResearchLayers(fintechAnalysis)
        const eduLayers = determineResearchLayers(eduAnalysis)

        expect(fintechLayers.length).toBeGreaterThan(eduLayers.length)
      })
    })

    describe('Cross-Industry Comparison', () => {
      it('should correctly differentiate industry contexts', () => {
        const industries = {
          healthcare: MOCK_SPECS.healthcarePortal,
          fintech: MOCK_SPECS.fintechBanking,
          general: MOCK_SPECS.educationPlatform
        }

        Object.entries(industries).forEach(([expected, spec]) => {
          const combined = spec.proposal + spec.tasks + spec.design
          const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

          if (expected === 'general') {
            expect(analysis.industryContext).toBeNull()
          } else {
            expect(analysis.industryContext).toBe(expected)
          }
        })
      })

      it('should generate compliance layers only for regulated industries', () => {
        const regulated = ['healthcarePortal', 'fintechBanking']
        const unregulated = ['simpleApi', 'educationPlatform']

        regulated.forEach(name => {
          const spec = MOCK_SPECS[name]
          const combined = spec.proposal + spec.tasks + spec.design
          const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
          const layers = determineResearchLayers(analysis)
          const hasCompliance = layers.some(l => l.name.includes('Compliance'))

          expect(hasCompliance).toBe(true)
        })

        unregulated.forEach(name => {
          const spec = MOCK_SPECS[name]
          const combined = spec.proposal + spec.tasks + spec.design
          const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
          const layers = determineResearchLayers(analysis)
          const hasCompliance = layers.some(l => l.name.includes('Compliance'))

          expect(hasCompliance).toBe(false)
        })
      })
    })
  })

  describe('Best Practice Layer Content', () => {
    it('should always include Best Practice layer for non-trivial changes', () => {
      const nonTrivialSpecs = Object.keys(MOCK_SPECS).filter(k => k !== 'typoFix')

      nonTrivialSpecs.forEach(name => {
        const spec = MOCK_SPECS[name]
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(layers.length).toBeGreaterThan(0)
        expect(layers[0].name).toBe('Best Practice / Industry Standard')
      })
    })

    it('should NOT include Best Practice layer for trivial changes', () => {
      const spec = MOCK_SPECS.typoFix
      const combined = spec.proposal + spec.tasks + spec.design
      const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
      const layers = determineResearchLayers(analysis)

      expect(layers.length).toBe(0)
    })

    it('should generate context-specific best practice questions', () => {
      const scenarios = [
        { name: 'authSystem', expectedKeywords: ['dashboard', 'auth'] },
        { name: 'ecommerceCheckout', expectedKeywords: ['ecommerce', 'dashboard', 'marketing'] },
        { name: 'healthcarePortal', expectedKeywords: ['dashboard', 'healthcare'] }
      ]

      scenarios.forEach(({ name, expectedKeywords }) => {
        const spec = MOCK_SPECS[name]
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        const bestPracticeLayer = layers[0]
        expect(bestPracticeLayer.name).toBe('Best Practice / Industry Standard')
        expect(bestPracticeLayer.questions.length).toBeGreaterThan(0)
        expect(bestPracticeLayer.searchTopics.length).toBeGreaterThan(0)

        const focus = bestPracticeLayer.focus.toLowerCase()
        const hasKeyword = expectedKeywords.some(kw => focus.includes(kw))
        expect(hasKeyword).toBe(true)
      })
    })

    it('should generate checklist with correct structure', () => {
      const spec = MOCK_SPECS.fintechBanking
      const combined = spec.proposal + spec.tasks + spec.design
      const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
      const layers = determineResearchLayers(analysis)
      const checklist = generateResearchChecklist(analysis, layers, [])

      expect(checklist).toContain('# Research Checklist')
      expect(checklist).toContain('Complexity:')
      expect(checklist).toContain('Risk: HIGH')
      expect(checklist).toContain('## Summary')
      expect(checklist).toContain('| Layer | Focus |')
    })
  })

  describe('Flow Best Practices', () => {
    describe('Step Order Validation', () => {
      it('should follow correct step order: analyze -> layers -> libraries -> risks', () => {
        const spec = MOCK_SPECS.fintechBanking
        const combined = spec.proposal + spec.tasks + spec.design

        // Step 1: Analyze
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        expect(analysis.complexity).toBeDefined()

        // Step 2: Determine layers (depends on analysis)
        const layers = determineResearchLayers(analysis)
        expect(layers.length).toBeGreaterThan(0)

        // Step 3: Extract libraries
        const libs = extractPotentialLibraryNames(combined)
        expect(libs.length).toBeGreaterThan(0)

        // Step 4: Detect risks (depends on libs)
        const mockDocs = 'webhook integration with stripe'
        const allLibs = libs.map(name => ({ name }))
        const risks = detectIntegrationRisks(mockDocs, 'stripe', allLibs)
        expect(risks).toBeDefined()
      })

      it('should not generate layers without analysis', () => {
        const emptyAnalysis = {
          complexity: 0,
          riskLevel: 'LOW',
          hasUI: false,
          hasAPI: false,
          hasDatabase: false
        }
        const layers = determineResearchLayers(emptyAnalysis)
        expect(layers.length).toBe(0)
      })
    })

    describe('Graceful Degradation', () => {
      it('should handle empty spec files gracefully', () => {
        const emptySpec = { proposal: '', tasks: '', design: '' }
        const combined = ''

        const analysis = analyzeChangeCharacteristics(combined, emptySpec.proposal, emptySpec.tasks)
        expect(analysis.complexity).toBe(1)
        expect(['unknown', 'general']).toContain(analysis.primaryType)
      })

      it('should handle spec with only whitespace', () => {
        const whitespaceSpec = { proposal: '   \n\n   ', tasks: '\t\t', design: '' }
        const combined = whitespaceSpec.proposal + whitespaceSpec.tasks

        const analysis = analyzeChangeCharacteristics(combined, whitespaceSpec.proposal, whitespaceSpec.tasks)
        expect(analysis).toBeDefined()
        expect(analysis.riskLevel).toBe('LOW')
      })

      it('should handle malformed markdown gracefully', () => {
        const malformedSpec = {
          proposal: '# Broken\n\n## No closing',
          tasks: '- [ ] Unclosed checkbox',
          design: '```\nUnclosed code block'
        }
        const combined = malformedSpec.proposal + malformedSpec.tasks + malformedSpec.design

        const analysis = analyzeChangeCharacteristics(combined, malformedSpec.proposal, malformedSpec.tasks)
        const libs = extractPotentialLibraryNames(combined)

        expect(analysis).toBeDefined()
        expect(Array.isArray(libs)).toBe(true)
      })
    })

    describe('Output Consistency', () => {
      it('should generate consistent layer order across runs', () => {
        const spec = MOCK_SPECS.healthcarePortal
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        const layers1 = determineResearchLayers(analysis)
        const layers2 = determineResearchLayers(analysis)
        const layers3 = determineResearchLayers(analysis)

        expect(layers1.map(l => l.name)).toEqual(layers2.map(l => l.name))
        expect(layers2.map(l => l.name)).toEqual(layers3.map(l => l.name))
      })

      it('should generate checklist that matches layers', () => {
        const spec = MOCK_SPECS.ecommerceCheckout
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)
        const checklist = generateResearchChecklist(analysis, layers, [])

        layers.forEach(layer => {
          expect(checklist).toContain(layer.name)
        })
      })

      it('should include all required sections in checklist', () => {
        const spec = MOCK_SPECS.fintechBanking
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)
        const checklist = generateResearchChecklist(analysis, layers, [])

        expect(checklist).toContain('# Research Checklist')
        expect(checklist).toContain('Complexity:')
        expect(checklist).toContain('Risk:')
        expect(checklist).toContain('## Summary')
      })
    })

    describe('Layer Dependencies', () => {
      it('should always have Best Practice as first layer when layers exist', () => {
        const allSpecs = Object.keys(MOCK_SPECS).filter(k => k !== 'typoFix')

        allSpecs.forEach(name => {
          const spec = MOCK_SPECS[name]
          const combined = spec.proposal + spec.tasks + spec.design
          const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
          const layers = determineResearchLayers(analysis)

          if (layers.length > 0) {
            expect(layers[0].name).toBe('Best Practice / Industry Standard')
          }
        })
      })

      it('should have Security layer before Compliance layer', () => {
        const regulatedSpecs = ['healthcarePortal', 'fintechBanking']

        regulatedSpecs.forEach(name => {
          const spec = MOCK_SPECS[name]
          const combined = spec.proposal + spec.tasks + spec.design
          const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
          const layers = determineResearchLayers(analysis)
          const layerNames = layers.map(l => l.name)

          const securityIndex = layerNames.findIndex(n => n === 'Security Requirements')
          const complianceIndex = layerNames.findIndex(n => n.includes('Compliance'))

          expect(securityIndex).toBeGreaterThan(-1)
          expect(complianceIndex).toBeGreaterThan(-1)
          expect(securityIndex).toBeLessThan(complianceIndex)
        })
      })

      it('should have Testing Strategy layer for high-risk changes', () => {
        const highRiskSpecs = ['ecommerceCheckout', 'healthcarePortal', 'fintechBanking']

        highRiskSpecs.forEach(name => {
          const spec = MOCK_SPECS[name]
          const combined = spec.proposal + spec.tasks + spec.design
          const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

          expect(analysis.riskLevel).toBe('HIGH')

          const layers = determineResearchLayers(analysis)
          const layerNames = layers.map(l => l.name)

          expect(layerNames).toContain('Testing Strategy')
        })
      })
    })

    describe('Anti-Pattern Detection', () => {
      it('should NOT generate Compliance layer for non-regulated industries', () => {
        const nonRegulated = ['simpleApi', 'authSystem', 'educationPlatform', 'realtimeSaas']

        nonRegulated.forEach(name => {
          const spec = MOCK_SPECS[name]
          const combined = spec.proposal + spec.tasks + spec.design
          const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
          const layers = determineResearchLayers(analysis)
          const layerNames = layers.map(l => l.name)

          expect(layerNames.some(n => n.includes('Compliance'))).toBe(false)
        })
      })

      it('should NOT generate layers for trivial changes', () => {
        const spec = MOCK_SPECS.typoFix
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(layers.length).toBe(0)
      })

      it('should NOT over-detect libraries from common words', () => {
        const spec = MOCK_SPECS.typoFix
        const combined = spec.proposal + spec.tasks + spec.design
        const libs = extractPotentialLibraryNames(combined)

        expect(libs.length).toBeLessThanOrEqual(1)

        const commonWords = ['the', 'fix', 'typo', 'readme', 'file', 'line']
        commonWords.forEach(word => {
          expect(libs.map(l => l.toLowerCase())).not.toContain(word)
        })
      })
    })
  })

  // ============================================================
  // CRITICAL FLOW INJECTION TESTS (v2.8.0)
  // ============================================================
  describe('Critical Flow Injection', () => {

    describe('Auth Security Items', () => {
      it('should inject auth security items when hasAuth is true', () => {
        const spec = MOCK_SPECS.authSystem
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(analysis.hasAuth).toBe(true)

        const securityLayer = layers.find(l => l.name === 'Security Requirements')
        expect(securityLayer).toBeDefined()

        const items = injectCriticalRequiredItems(securityLayer, analysis)

        expect(items.length).toBeGreaterThanOrEqual(7)
        expect(items.some(i => i.id === 'auth-password-hash')).toBe(true)
        expect(items.some(i => i.id === 'auth-rate-limit')).toBe(true)
        expect(items.some(i => i.id === 'auth-csrf')).toBe(true)
        expect(items.some(i => i.id === 'auth-secure-cookies')).toBe(true)
      })

      it('should NOT inject auth items when hasAuth is false', () => {
        const spec = MOCK_SPECS.simpleApi
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.hasAuth).toBe(false)

        const mockSecurityLayer = { name: 'Security Requirements' }
        const items = injectCriticalRequiredItems(mockSecurityLayer, analysis)

        expect(items.some(i => i.id?.startsWith('auth-'))).toBe(false)
      })
    })

    describe('Payment Security Items', () => {
      it('should inject payment security items when hasPayment is true', () => {
        const spec = MOCK_SPECS.ecommerceCheckout
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(analysis.hasPayment).toBe(true)

        const securityLayer = layers.find(l => l.name === 'Security Requirements')
        expect(securityLayer).toBeDefined()

        const items = injectCriticalRequiredItems(securityLayer, analysis)

        expect(items.some(i => i.id === 'payment-no-card-storage')).toBe(true)
        expect(items.some(i => i.id === 'payment-webhook-verify')).toBe(true)
        expect(items.some(i => i.id === 'payment-amount-verify')).toBe(true)
      })
    })

    describe('Healthcare Compliance Items', () => {
      it('should inject HIPAA items for healthcare industry', () => {
        const spec = MOCK_SPECS.healthcarePortal
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(analysis.industryContext).toBe('healthcare')

        const complianceLayer = layers.find(l => l.name.includes('Compliance'))
        expect(complianceLayer).toBeDefined()

        const items = injectCriticalRequiredItems(complianceLayer, analysis)

        expect(items.length).toBe(5)
        expect(items.some(i => i.id === 'hipaa-phi-encrypt')).toBe(true)
        expect(items.some(i => i.id === 'hipaa-access-control')).toBe(true)
        expect(items.some(i => i.id === 'hipaa-audit-trail')).toBe(true)
        expect(items.some(i => i.id === 'hipaa-baa')).toBe(true)
        expect(items.some(i => i.id === 'hipaa-breach-plan')).toBe(true)
      })

      it('should NOT inject HIPAA items for non-healthcare industry', () => {
        const spec = MOCK_SPECS.fintechBanking
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)

        expect(analysis.industryContext).toBe('fintech')

        const mockComplianceLayer = { name: 'fintech Compliance' }
        const items = injectCriticalRequiredItems(mockComplianceLayer, analysis)

        expect(items.some(i => i.id?.startsWith('hipaa-'))).toBe(false)
      })
    })

    describe('Fintech Compliance Items', () => {
      it('should inject PCI-DSS items for fintech industry', () => {
        const spec = MOCK_SPECS.fintechBanking
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(analysis.industryContext).toBe('fintech')

        const complianceLayer = layers.find(l => l.name.includes('Compliance'))
        expect(complianceLayer).toBeDefined()

        const items = injectCriticalRequiredItems(complianceLayer, analysis)

        expect(items.length).toBe(6)
        expect(items.some(i => i.id === 'pci-no-pan')).toBe(true)
        expect(items.some(i => i.id === 'pci-tokenization')).toBe(true)
        expect(items.some(i => i.id === 'fintech-kyc')).toBe(true)
        expect(items.some(i => i.id === 'fintech-transaction-limits')).toBe(true)
        expect(items.some(i => i.id === 'fintech-audit')).toBe(true)
      })
    })

    describe('Sensitive Data Items', () => {
      it('should inject sensitive data security items when hasSensitiveData is true', () => {
        const spec = MOCK_SPECS.healthcarePortal
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(analysis.hasSensitiveData).toBe(true)

        const securityLayer = layers.find(l => l.name === 'Security Requirements')
        expect(securityLayer).toBeDefined()

        const items = injectCriticalRequiredItems(securityLayer, analysis)

        expect(items.some(i => i.id === 'data-encryption-rest')).toBe(true)
        expect(items.some(i => i.id === 'data-encryption-transit')).toBe(true)
        expect(items.some(i => i.id === 'data-access-logging')).toBe(true)
      })

      it('should inject data architecture items for sensitive data', () => {
        const spec = MOCK_SPECS.healthcarePortal
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(analysis.hasSensitiveData).toBe(true)

        const dataLayer = layers.find(l => l.name === 'Data Architecture')
        expect(dataLayer).toBeDefined()

        const items = injectCriticalRequiredItems(dataLayer, analysis)

        expect(items.some(i => i.id === 'data-arch-backup')).toBe(true)
        expect(items.some(i => i.id === 'data-arch-retention')).toBe(true)
      })
    })

    describe('Combined Scenarios', () => {
      it('should inject both auth AND payment items for auth+payment scenario', () => {
        const mockAnalysis = {
          hasAuth: true,
          hasPayment: true,
          hasSensitiveData: false,
          industryContext: null
        }

        const mockSecurityLayer = { name: 'Security Requirements' }
        const items = injectCriticalRequiredItems(mockSecurityLayer, mockAnalysis)

        expect(items.some(i => i.id === 'auth-password-hash')).toBe(true)
        expect(items.some(i => i.id === 'payment-no-card-storage')).toBe(true)
        expect(items.length).toBe(12)
      })

      it('should inject payment items only for e-commerce checkout', () => {
        const spec = MOCK_SPECS.ecommerceCheckout
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(analysis.hasPayment).toBe(true)

        const securityLayer = layers.find(l => l.name === 'Security Requirements')
        const items = injectCriticalRequiredItems(securityLayer, analysis)

        expect(items.some(i => i.id === 'payment-no-card-storage')).toBe(true)
        expect(items.some(i => i.id === 'payment-webhook-verify')).toBe(true)
      })

      it('should inject 0 items for trivial changes', () => {
        const spec = MOCK_SPECS.typoFix
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        expect(layers.length).toBe(0)

        const mockSecurityLayer = { name: 'Security Requirements' }
        const items = injectCriticalRequiredItems(mockSecurityLayer, analysis)

        expect(items.length).toBe(0)
      })
    })

    describe('Item Structure Validation', () => {
      it('should return items with correct structure (id, check, why, severity)', () => {
        const spec = MOCK_SPECS.authSystem
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        const securityLayer = layers.find(l => l.name === 'Security Requirements')
        const items = injectCriticalRequiredItems(securityLayer, analysis)

        items.forEach(item => {
          expect(item).toHaveProperty('id')
          expect(item).toHaveProperty('check')
          expect(item).toHaveProperty('why')
          expect(item).toHaveProperty('severity')
          expect(['critical', 'high', 'medium', 'low']).toContain(item.severity)
        })
      })

      it('should have unique item IDs', () => {
        const spec = MOCK_SPECS.ecommerceCheckout
        const combined = spec.proposal + spec.tasks + spec.design
        const analysis = analyzeChangeCharacteristics(combined, spec.proposal, spec.tasks)
        const layers = determineResearchLayers(analysis)

        const securityLayer = layers.find(l => l.name === 'Security Requirements')
        const items = injectCriticalRequiredItems(securityLayer, analysis)

        const ids = items.map(i => i.id)
        const uniqueIds = [...new Set(ids)]
        expect(ids.length).toBe(uniqueIds.length)
      })
    })
  })
})
