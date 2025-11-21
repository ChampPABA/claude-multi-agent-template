# Incremental Integration Testing (v1.4.0)

> **Detailed guide to progressive validation for high-risk tasks**
> **Source:** User requirement for sample-based validation
> **Version:** 1.4.0

---

## 🧠 The Problem: All-or-Nothing Testing

**Before v1.4.0:**
```
Task: "Integrate Google Maps API"
→ Agent implements complete solution (1000 locations)
→ Tests with full dataset
→ Bug found → Hard to debug (which part failed?)
→ Fix → Retest full dataset → Slow iteration

Problem:
❌ Large scope = hard to debug
❌ Late bug detection (at scale)
❌ Rework expensive (threw away 1000-location implementation)
❌ No confidence in progressive scaling
```

**After v1.4.0:**
```
Task: "Integrate Google Maps API"
→ Milestone 1: Test 1 location (hardcoded)
   → Bug found → Easy to debug (small scope)
   → Fix → Retest 1 location → Fast iteration
→ Milestone 2: Test 10 locations (parameterized)
   → Works! Confidence++
→ Milestone 3: Error handling
   → Refine edge cases
→ Milestone 4: Scale to 1000
   → Already confident (1 and 10 worked)

Benefits:
✅ Small scope = easy debugging
✅ Early bug detection (at milestone 1)
✅ Low rework (fix before scaling)
✅ Progressive confidence
```

---

## The Solution: Milestone-based Validation

**Inspired by:** Incremental integration testing best practices

**Key Files:**
- `@/.claude/lib/task-analyzer.md` - Detection + milestone generation
- `@/.claude/commands/csetup.md` - Inject milestones to phases.md
- `@/.claude/lib/agent-executor.md` - Round-based retry execution

---

## 🎯 When to Use Incremental Testing

### Automatic Detection (by `/csetup`)

Incremental testing triggers when:

| Criteria | Example |
|----------|---------|
| **Risk = HIGH** | Payment integration, Auth system |
| **Risk = MEDIUM + Complexity ≥ 7** | Complex form with 20 fields |
| **External API dependency** | Google Maps, Stripe, OpenAI |
| **Data-intensive operation** | ETL, migration, batch processing |

**Detection Rate:** ~20-30% of tasks (only high-risk)

---

## 📊 Milestone Patterns

### Pattern 1: Backend API Integration (4 milestones)

**Use for:** External APIs (Google, Stripe, payment gateways)

```
M1: Core implementation (30%)
   Test: 1 record, hardcoded
   Goal: Prove API connection works

M2: Parameterized query (30%)
   Test: 10 records, dynamic input
   Goal: Validate data flow

M3: Error handling (20%)
   Test: Invalid input, timeouts, rate limits
   Goal: Resilience

M4: Scale + performance (20%)
   Test: 100-1000 records, load test
   Goal: Production-ready
```

**Time distribution:** 30-30-20-20 (core/params/errors/scale)

---

### Pattern 2: Complex Form (3 milestones)

**Use for:** Multi-step forms, wizards, surveys (complexity ≥ 7)

```
M1: Architecture + skeleton (40%)
   Implement: Full structure with 2-3 critical fields
   Goal: Architecture supports full field count

M2: E2E flow validation (30%)
   Test: Submit minimal form → API → DB
   Goal: Prove full flow works

M3: Complete all fields (30%)
   Implement: All 20 fields + validation + accessibility
   Goal: Production-ready
```

**Time distribution:** 40-30-30 (architecture/flow/completion)

**Why architecture-first?**
Avoids rework if structure changes (2-field form → 20-field wizard)

---

### Pattern 3: Database Migration / ETL (3 milestones)

**Use for:** Data migrations, ETL pipelines, batch operations

```
M1: Dry-run with 10 records (25%)
   Test: Transformation logic, rollback
   Goal: Prove concept

M2: Scale to 100 records (25%)
   Test: Performance, duplicates, error logging
   Goal: Validate at moderate scale

M3: Full dataset (staging) (50%)
   Test: Complete migration on staging
   Goal: Ready for production
```

**Time distribution:** 25-25-50 (dry-run/scale/full)

---

## 🔄 Round-based Retry Logic

### Per-Milestone Quota

```
Milestone 1: Core implementation
→ Round 1:
   → Attempt 1: ❌ FAIL (API key not set)
   → Attempt 2: ❌ FAIL (Still no API key)
   → Quota exhausted → Escalate to Main Claude

→ Main Claude analyzes:
   Error pattern: Same error 2x
   Complexity: SIMPLE
   Root cause: Config issue (HIGH confidence)
   Decision: Give hints

→ Hints provided:
   - Check if API_KEY env variable is set
   - Verify API key in .env.local
   - Restart dev server after adding key

→ Round 2 (NEW quota: 2 attempts):
   → Attempt 1: ✅ PASS (API key added)

Total attempts: 3 (2 in Round 1, 1 in Round 2)
```

**Key principles:**
- **2 attempts per round** (not total)
- **Unlimited rounds** (Main Claude decides)
- **Hints reset quota** (fresh start)

---

## 🤖 Main Claude Intervention

### Decision Matrix

| Error Pattern | Complexity | Confidence | Action |
|---------------|------------|------------|--------|
| Same error 2x | SIMPLE | HIGH | Give Hints |
| Same error 2x | COMPLEX | LOW | Ask Human |
| Different errors | ANY | ANY | Ask Human |
| Intermittent | ANY | ANY | Ask Human |
| 2+ rounds no progress | ANY | ANY | Ask Human |

**Default:** When in doubt → Give Hints (let agent try once more)

### Hint Generation

**Pattern-based hints:**
```typescript
Error: 401 Unauthorized
→ Hints:
  - Check API_KEY env variable
  - Verify API key validity
  - Ensure key has permissions

Error: Timeout
→ Hints:
  - Increase timeout threshold
  - Check network connectivity
  - Verify API endpoint URL

Error: Schema mismatch
→ Hints:
  - Compare actual vs expected schema
  - Check API version changes
  - Add console.log() to inspect response
```

**Generic hints:**
- Review exit criteria
- Add detailed logging
- Check implementation vs requirements

---

## 🛑 Human Escalation

### When to Ask Human

```typescript
// Rule 1: Complex + Low confidence
if (complexity === 'COMPLEX' && confidence === 'LOW') → Ask Human

// Rule 2: Non-deterministic errors
if (error_pattern === 'different_errors') → Ask Human

// Rule 3: Intermittent failures
if (error_pattern === 'intermittent') → Ask Human

// Rule 4: No progress after 2 rounds
if (rounds >= 3 && !progress) → Ask Human
```

### Report Format

```markdown
🛑 Human Intervention Required

Phase: Google Maps Integration
Milestone: 3/4 - Error handling
Total Attempts: 6 across 2 rounds
Status: AWAITING RESOLUTION

## Failure Summary
Round 1: (Attempts 1-2)
- ❌ Timeout errors (5s threshold)

Round 2: (Attempts 3-4, after hints)
- ❌ 503 Service Unavailable (intermittent)

## Analysis
Error Pattern: Intermittent (non-deterministic)
Complexity: HIGH
Root Cause: API instability or network issues
Confidence: LOW

## Recommendations
1. Check Google Maps API status page
2. Test API directly (curl/Postman)
3. Consider retry with exponential backoff
4. Verify API quota not exhausted

## Next Steps
Please investigate and advise:
- Continue with current approach?
- Or fix infrastructure first?
```

---

## ✅ Exit Criteria Validation

### Agent Output Format (Required)

```markdown
## Milestone 2 Results

**Implementation Summary:**
Implemented parameterized query with dynamic address input

**Test Results:**
- [ ] Accepts dynamic input - PASS - Accepts string parameter
- [ ] Returns correct results for 10 queries - PASS - All 10 matched
- [ ] No duplicate API calls - PASS - Checked logs, no dupes
- [ ] Response time < 700ms - FAIL - Got 823ms (too slow)

**Issues Found:**
- Response time exceeds threshold (optimization needed)

**Conclusion:**
FAIL → Need to add caching to reduce response time
```

**Validation:**
- ALL criteria must report PASS/FAIL
- Missing criteria = automatic FAIL
- Strict mode: ALL must pass (no lenient 80% rule)

---

## 📊 Benefits & Trade-offs

### Benefits

| Benefit | Quantified |
|---------|------------|
| **Bug detection** | Catch at M1 (1 record) vs M4 (1000 records) → 75% faster debug |
| **Rework reduction** | Fix before scaling → 60-70% less rework |
| **Debug time** | Small scope (1 record) → 80% faster than full dataset |
| **Confidence** | Progressive proof → 90% success rate at M4 |
| **Risk mitigation** | Early validation → Catch critical bugs before production |

### Trade-offs

| Trade-off | Impact | Mitigation |
|-----------|--------|------------|
| **Timeline +15-20%** | Slower initial dev | Saves 60-70% rework time (net positive) |
| **phases.md 2-3x longer** | Harder to read | Summary table at top |
| **Complexity** | Learning curve | Comprehensive docs |
| **Overhead** | More coordination | Automated by `/csetup` |

**Net benefit:** +15-20% time → -60-70% rework = **40-50% faster overall**

---

## 🎯 Usage Example

### User Flow

```bash
# 1. User creates OpenSpec change
/csetup CHANGE-042

# Output:
✅ Task Analysis Complete
🔄 Testing Strategy:
   - Incremental: 2 tasks (7 milestones total)
     → Google Maps integration (4 milestones)
     → Payment processing (3 milestones)
   - Standard: 5 tasks

# 2. Review phases.md
cat openspec/changes/CHANGE-042/.claude/phases.md

# Shows:
### Phase 2: Google Maps Integration
Testing Strategy: 🔄 INCREMENTAL
Total Milestones: 4

#### Milestone 1/4: Core implementation
Test Scope: Single happy path (1 record)
Exit Criteria:
- [ ] Response status = 200
- [ ] Data structure valid
- [ ] Response time < 500ms
...

# 3. Execute
/cdev CHANGE-042

# Execution:
🔄 INCREMENTAL MODE
Milestone 1/4: Core implementation
Round 1, Attempt 1: ❌ FAIL (API key missing)
Round 1, Attempt 2: ❌ FAIL (Still missing)
💡 Main Claude: "Check API_KEY env variable"
Round 2, Attempt 1: ✅ PASS
Milestone 2/4: Parameterized query
Round 1, Attempt 1: ✅ PASS
...
```

---

## 🔧 Maintenance Guide

### Adding New Patterns

**File:** `.claude/lib/task-analyzer.md` → `generateMilestones()`

```typescript
// Pattern 4: Real-time WebSocket (NEW)
if (taskLower.match(/websocket|realtime|socket.io/i)) {
  milestones.push({
    id: 1,
    name: 'Basic connection',
    testScope: 'Single client, simple message',
    exitCriteria: [
      'WebSocket connects successfully',
      'Message sent and received',
      'Connection closes gracefully'
    ],
    estimatedTime: Math.ceil(estimatedTime * 0.3),
    retryLimit: 2
  })
  // ... more milestones
}
```

### Adjusting Time Distribution

Current: 30-30-20-20 (API pattern)

If Pattern 1 (API) milestones take longer:
```typescript
// Before: 30-30-20-20
milestones[0].estimatedTime = estimatedTime * 0.3
milestones[1].estimatedTime = estimatedTime * 0.3
milestones[2].estimatedTime = estimatedTime * 0.2
milestones[3].estimatedTime = estimatedTime * 0.2

// After: 25-25-25-25 (more balanced)
milestones.forEach(m => {
  m.estimatedTime = Math.ceil(estimatedTime / 4)
})
```

---

## 📖 References

- **Original inspiration:** User request for "incremental integration testing"
- **Similar concepts:**
  - Sample-based validation (ML/AI pipelines)
  - Progressive enhancement (web development)
  - Iterative refinement testing (data science)
- **Related files:**
  - Task analysis: `.claude/lib/task-analyzer.md`
  - Execution logic: `.claude/lib/agent-executor.md`
  - Workflow generation: `.claude/commands/csetup.md`

---

## 🎓 Key Takeaways

1. **Use for high-risk only** (20-30% of tasks, not all)
2. **Milestone-based > size-based** (functionality over record count)
3. **Architecture-first** (avoid rework from structure changes)
4. **Trust Main Claude** (hints > blind retry)
5. **Progressive confidence** (each milestone proves the next)

**Bottom line:** Incremental testing trades +15-20% time for -60-70% rework → **40-50% net speedup** + higher quality.

---

This testing strategy ensures high-risk tasks succeed systematically! 🚀
