# Core Skills for Spec-Driven Development

## Overview
This document defines the fundamental skills required for effective Spec-Driven Development (SDD) implementation. These skills ensure systematic, incremental, and validated software delivery.

---

## 1. Spec Interpretation & Clarification

### Purpose
Transform ambiguous requirements into precise, actionable specifications through systematic analysis and targeted questioning.

### Key Capabilities
- **Requirement Decomposition**: Break down user stories into granular, testable requirements
- **Ambiguity Detection**: Identify underspecified areas, implicit assumptions, and missing edge cases
- **Targeted Clarification**: Ask 2-3 precise questions that resolve maximum uncertainty
- **Context Preservation**: Maintain business intent while translating to technical specifications

### Application Pattern
```text
1. Read the requirement/spec
2. Identify unclear boundaries, missing error cases, or implicit assumptions
3. Formulate targeted clarifying questions
4. Document answers directly in spec.md
5. Validate completeness against acceptance criteria
```

### Success Criteria
- No TBD or NEEDS CLARIFICATION markers in final spec
- All error paths explicitly documented
- Edge cases enumerated with expected behavior
- Business rules stated as testable conditions

---

## 2. Cross-Layer System Thinking

### Purpose
Understand and design systems holistically across all architectural layers, ensuring coherent integration from UI to data persistence.

### Key Capabilities
- **Vertical Tracing**: Track data flow from user action → API → business logic → database
- **Dependency Mapping**: Identify cross-layer dependencies and contracts
- **Interface Design**: Define clean boundaries between layers
- **Impact Analysis**: Assess ripple effects of changes across the stack

### Architectural Layers
```text
┌─────────────────────────────┐
│  Presentation Layer (UI)    │
├─────────────────────────────┤
│  API Layer (Endpoints)      │
├─────────────────────────────┤
│  Business Logic Layer       │
├─────────────────────────────┤
│  Data Access Layer (ORM)    │
├─────────────────────────────┤
│  Persistence Layer (DB)     │
└─────────────────────────────┘
```

### Application Pattern
```text
For each feature:
1. Map user interaction to UI components
2. Define API contracts (inputs/outputs/errors)
3. Design business logic and validation rules
4. Model data schema and relationships
5. Validate vertical integration and error propagation
```

### Success Criteria
- Clear contracts between all layers
- Error handling at appropriate boundaries
- No tight coupling between layers
- Testable integration points

---

## 3. Incremental Evolution from Phase-I

### Purpose
Systematically build upon existing Phase-I infrastructure without breaking contracts or introducing regressions.

### Key Capabilities
- **Contract Preservation**: Extend APIs without breaking existing consumers
- **Schema Evolution**: Add fields/tables while maintaining backward compatibility
- **Feature Flags**: Gate new functionality for safe rollout
- **Migration Planning**: Define safe paths from current to target state

### Phase-I Foundation
Phase-I typically includes:
- Core data models
- Authentication/authorization
- Basic CRUD operations
- Foundational UI components

### Application Pattern
```text
1. Read existing Phase-I artifacts (data-model.md, contracts/, code)
2. Identify extension points vs. modification points
3. Design additive changes (new fields, endpoints, components)
4. Plan migration for breaking changes
5. Validate backward compatibility
```

### Success Criteria
- Zero breaking changes to existing APIs
- Existing tests continue to pass
- Clear migration path for schema changes
- Feature flags for new functionality

---

## 4. Dependency-Aware Planning

### Purpose
Sequence work to respect technical dependencies, minimize blocking, and enable parallel development where possible.

### Key Capabilities
- **Dependency Identification**: Recognize which tasks must precede others
- **Critical Path Analysis**: Identify longest dependency chains
- **Parallel Work Detection**: Find independent tasks for concurrent execution
- **Blocking Risk Mitigation**: Surface dependencies early to avoid late discoveries

### Dependency Types
```text
1. Technical: Task B requires Task A's output
2. Integration: Multiple tasks must align on shared contract
3. Data: Schema must exist before queries can be written
4. Testing: Implementation must complete before tests can run
```

### Application Pattern
```text
1. List all tasks from plan.md
2. For each task, identify prerequisites
3. Build dependency graph
4. Order tasks by:
   - Zero dependencies first
   - Critical path prioritized
   - Independent tasks flagged for parallel work
5. Document in tasks.md with clear prerequisites
```

### Success Criteria
- No task depends on incomplete prerequisites
- Critical path clearly identified
- Independent tasks marked for parallel execution
- Blocking risks surfaced in plan.md

---

## 5. Validation via Acceptance Criteria

### Purpose
Ensure every deliverable is testable, measurable, and verifiable against explicit success conditions.

### Key Capabilities
- **Criteria Definition**: Translate requirements into testable conditions
- **Test Case Generation**: Derive concrete test scenarios from criteria
- **Verification Planning**: Define how to validate each criterion
- **Regression Prevention**: Ensure existing criteria remain satisfied

### Acceptance Criteria Format
```text
Given: [initial state/context]
When: [action/trigger]
Then: [expected outcome]
And: [additional expectations]

Example:
Given: A logged-in user with admin role
When: User clicks "Delete" on a task
Then: Confirmation dialog appears
And: Task is removed only after confirmation
And: Audit log records the deletion
```

### Application Pattern
```text
1. For each requirement in spec.md:
   - Define 2-5 acceptance criteria
   - Include happy path + error cases
   - Specify observable outcomes
2. In tasks.md, link each task to criteria
3. In implementation, write tests that verify criteria
4. In validation, check all criteria pass
```

### Success Criteria
- Every requirement has explicit acceptance criteria
- All criteria are testable (manual or automated)
- Error paths have failure criteria
- Edge cases enumerated with expected behavior

---

## Integration Workflow

These five skills work together in the SDD lifecycle:

```text
┌─────────────────────────────────────────────────────────┐
│ 1. Spec Interpretation & Clarification                 │
│    → Produce: spec.md with clear requirements          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│ 2. Cross-Layer System Thinking                         │
│    → Produce: plan.md with architecture decisions      │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│ 3. Incremental Evolution from Phase-I                  │
│    → Produce: migration strategy, backward compat plan │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│ 4. Dependency-Aware Planning                           │
│    → Produce: tasks.md with ordered, testable tasks    │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│ 5. Validation via Acceptance Criteria                  │
│    → Produce: test cases, verification results         │
└─────────────────────────────────────────────────────────┘
```

---

## Skill Mastery Checklist

For each skill, practitioners should demonstrate:

- [x] **Understand**: Can explain the skill's purpose and value
- [x] **Apply**: Can use the skill in routine development tasks
- [x] **Adapt**: Can modify approach based on project context
- [x] **Teach**: Can guide others in applying the skill
- [x] **Innovate**: Can identify skill improvements and refinements

---

## References

- `.specify/memory/constitution.md` - Project-specific coding standards
- `specs/<feature>/spec.md` - Feature specifications
- `specs/<feature>/plan.md` - Architectural plans
- `specs/<feature>/tasks.md` - Testable task breakdown
- `history/prompts/` - Prompt History Records (PHRs)
- `history/adr/` - Architectural Decision Records (ADRs)
