# Feature Best Practices Detection & Validation

> **Version:** 1.0.0
> **Purpose:** Detect features from spec and validate against industry standards
> **Used by:** `/csetup` Step 2.6

---

## Overview

Before querying stack-level best practices (React, Next.js, etc.), we first need to:
1. Detect what features the change involves (Auth, Payment, etc.)
2. Query industry best practices for each feature
3. Compare spec against industry standards
4. Report gaps and get user decision

WHY: Stack best practices tell you "how to use React well", but Feature best practices tell you "what a good auth system needs". The feature layer is higher-level and informs whether your spec is complete.

---

## Feature Detection

### Keyword Mapping

| Keywords in proposal/tasks/design | Feature Type | Security Tier |
|-----------------------------------|--------------|---------------|
| login, auth, register, password, session, jwt, token, oauth | Authentication | Tier 1 (Blocking) |
| payment, stripe, checkout, billing, subscription, invoice | Payment | Tier 1 (Blocking) |
| upload, file, image, s3, storage, attachment | File Upload | Tier 1 (Blocking) |
| admin, role, permission, rbac, acl, access control | Authorization | Tier 1 (Blocking) |
| api, endpoint, rest, graphql, webhook | API Design | Tier 2 (Warning) |
| realtime, websocket, notification, push, sse | Real-time | Tier 2 (Warning) |
| email, smtp, sendgrid, notification, mailer | Email/Notification | Tier 2 (Warning) |
| search, elasticsearch, algolia, filter, query | Search | Tier 2 (Warning) |
| cache, redis, memcached, cdn | Caching | Tier 2 (Warning) |
| crud, list, table, form, dashboard | CRUD/UI | Tier 3 (Info) |
| landing, hero, marketing, seo | Marketing Page | Tier 3 (Info) |

### Security Tiers

**Tier 1 (Blocking):** Security-critical features
- Validation against industry standard is required
- User must explicitly approve if skipping requirements
- Gaps are documented in design.md

**Tier 2 (Warning):** Important but not security-critical
- Show warning if gaps found
- Allow continue without blocking
- Log decision

**Tier 3 (Info):** Nice-to-have
- Suggest best practices
- No blocking or warning
- Optional to follow

---

## Industry Standard Queries

### Authentication

**Query Topics:**
```
- "JWT authentication best practices 2024"
- "refresh token rotation security"
- "session management security best practices"
- "OAuth 2.0 implementation best practices"
```

**Expected Standards:**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Short-lived access token | JWT 15-60 minutes max | Required |
| Refresh token rotation | New refresh token on each use | Required |
| Secure token storage | httpOnly cookies, not localStorage | Required |
| Token revocation | Ability to invalidate tokens immediately | Required |
| Rate limiting | 5-10 attempts per minute on auth endpoints | Required |
| Account lockout | Lock after N failed attempts | Recommended |
| Password requirements | Min length, complexity | Required |
| Secure password storage | bcrypt/argon2, never plain text | Required |
| HTTPS only | All auth endpoints over TLS | Required |
| CSRF protection | For cookie-based auth | Required |

---

### Payment

**Query Topics:**
```
- "payment integration security best practices"
- "PCI DSS compliance requirements"
- "Stripe integration best practices"
```

**Expected Standards:**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| No card data on server | Use Stripe Elements/Checkout | Required |
| Webhook signature verification | Validate Stripe webhook signatures | Required |
| Idempotency keys | Prevent duplicate charges | Required |
| Amount validation | Server-side price validation | Required |
| Audit logging | Log all payment events | Required |
| Error handling | Graceful failure, no sensitive data in errors | Required |
| Test mode separation | Clear separation of test/live keys | Required |

---

### File Upload

**Query Topics:**
```
- "file upload security best practices"
- "image upload validation security"
- "S3 presigned URL best practices"
```

**Expected Standards:**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| File type validation | Server-side MIME type check | Required |
| File size limits | Configurable max size | Required |
| Filename sanitization | Remove path traversal, special chars | Required |
| Virus scanning | For user-uploaded files | Recommended |
| Presigned URLs | For direct-to-S3 uploads | Recommended |
| Access control | Private by default, signed URLs for access | Required |
| Content-Disposition | Force download, prevent XSS | Required |

---

### Authorization (RBAC)

**Query Topics:**
```
- "role based access control best practices"
- "RBAC implementation patterns"
- "authorization security best practices"
```

**Expected Standards:**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Deny by default | No access unless explicitly granted | Required |
| Server-side checks | Never trust client-side only | Required |
| Principle of least privilege | Minimal permissions needed | Required |
| Role hierarchy | Clear inheritance if needed | Recommended |
| Audit logging | Log access decisions | Required |
| Separation of duties | Critical actions need multiple roles | Recommended |

---

### API Design

**Query Topics:**
```
- "REST API design best practices 2024"
- "API security best practices"
- "API rate limiting best practices"
```

**Expected Standards:**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| Consistent naming | Resource-based URLs, proper HTTP methods | Required |
| Versioning | URL or header-based versioning | Recommended |
| Rate limiting | Per-user/IP rate limits | Required |
| Input validation | Validate all inputs server-side | Required |
| Error format | Consistent error response structure | Required |
| Pagination | For list endpoints | Required |
| CORS configuration | Proper origin restrictions | Required |

---

## Spec Comparison Logic

### Extracting Spec Requirements

From `design.md`, look for:
1. **Decision sections** (### D1, ### D2, etc.)
2. **Technical specs** (tables, bullet points)
3. **Architecture descriptions**

### Comparison Algorithm

```typescript
interface SpecComparison {
  feature: string
  industryRequirements: Requirement[]
  specRequirements: string[]
  gaps: Gap[]
  matches: Match[]
}

interface Gap {
  requirement: string
  priority: 'required' | 'recommended'
  securityImpact: 'high' | 'medium' | 'low'
  suggestion: string
}

function compareSpecToIndustry(
  featureType: string,
  specContent: string,
  industryStandards: Requirement[]
): SpecComparison {
  const gaps = []
  const matches = []

  for (const standard of industryStandards) {
    // Check if spec mentions this requirement
    const mentioned = checkIfMentioned(specContent, standard.keywords)

    if (mentioned) {
      matches.push({ requirement: standard.name, specText: mentioned })
    } else if (standard.priority === 'required') {
      gaps.push({
        requirement: standard.name,
        priority: standard.priority,
        securityImpact: standard.securityImpact,
        suggestion: standard.suggestion
      })
    }
  }

  return { feature: featureType, industryRequirements, specRequirements, gaps, matches }
}
```

---

## Gap Report Format

### For Tier 1 (Blocking) Features

```markdown
## Feature Best Practice Validation

### Feature: Authentication
**Security Tier:** 1 (Blocking)

### Spec vs Industry Standard

| Requirement | Industry Standard | Your Spec | Status |
|-------------|------------------|-----------|--------|
| Access token expiry | 15-60 min | 15 min | ✅ Match |
| Refresh token rotation | Required | Not specified | ❌ Gap |
| Token revocation | Required | Redis-based | ✅ Match |
| Rate limiting | 5-10/min | Not specified | ❌ Gap |
| Account lockout | Recommended | Not specified | ⚠️ Missing |

### Gaps Found: 2 Required, 1 Recommended

**Security Impact:** HIGH

⚠️ Your spec is missing security-critical requirements.

### Options:

**A) Update spec (Recommended)**
   Add missing requirements to design.md:
   - Refresh token rotation on each use
   - Rate limiting: 5 attempts per minute

**B) Document conscious skip**
   Record why these aren't needed for your use case.
   (Requires justification for security review)

**C) Continue anyway**
   Proceed without these requirements.
   ⚠️ Security risk - not recommended for production

Which option? [A/B/C]
```

### For Tier 2 (Warning) Features

```markdown
## Feature Best Practice Validation

### Feature: API Design
**Security Tier:** 2 (Warning)

### Recommendations

Your spec could be improved with:
- [ ] API versioning strategy
- [ ] Pagination for list endpoints
- [ ] Consistent error format

These are recommended but not blocking.
Continuing with implementation...
```

---

## Suggested Spec Updates

When user chooses Option A (Update spec), generate:

```markdown
### D{n}: Security Requirements (Industry Standard Alignment)

**Added based on industry best practices:**

#### Authentication Security
- Refresh token rotation: Generate new refresh token on each use
- Rate limiting: Max 5 login attempts per minute per IP
- Account lockout: Lock account for 15 minutes after 5 failed attempts

#### Rationale
These requirements align with OWASP Authentication Guidelines and
industry standard security practices for production applications.

**Source:** Feature Best Practice Validation in /csetup
**Added:** {date}
```

---

## Conscious Skip Documentation

When user chooses Option B (Document skip):

```markdown
### D{n}: Conscious Security Trade-offs

**Skipped requirements (with justification):**

| Requirement | Why Skipped | Risk Level | Mitigation |
|-------------|-------------|------------|------------|
| Refresh token rotation | Internal tool, 3 users only | Low | Short session timeout (1 hour) |
| Rate limiting | Behind VPN, no public access | Low | VPN already rate-limits |

**Acknowledged by:** User decision in /csetup
**Date:** {date}
**Review reminder:** Re-evaluate if app becomes public-facing
```

---

## Integration with /csetup

This file is used in Step 2.6 of `/csetup`:

```typescript
// In csetup.md Step 2.6

// 1. Detect features
const features = detectFeatures(proposalContent, tasksContent, designContent)

// 2. For each Tier 1/2 feature, validate
for (const feature of features) {
  const industryStandards = loadIndustryStandards(feature.type)
  const comparison = compareSpecToIndustry(feature.type, designContent, industryStandards)

  if (comparison.gaps.length > 0 && feature.tier <= 2) {
    // Show gap report and get user decision
    const decision = await showGapReport(comparison)

    if (decision === 'A') {
      // Generate spec update suggestions
      await updateSpec(changeId, comparison.gaps)
    } else if (decision === 'B') {
      // Document conscious skip
      await documentSkip(changeId, comparison.gaps)
    }
  }
}
```

---

## Best Practice Sources

When querying, use these sources in order:
1. **Context7** - For library-specific best practices
2. **OWASP** - For security best practices
3. **Industry standards** - PCI DSS, OAuth 2.0 RFC, etc.

---

This feature-first validation ensures specs are complete before we check if libraries support them.
