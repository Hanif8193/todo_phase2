# AI-Assisted Development Skills

## Overview
This document defines skills for effective collaboration with AI coding assistants like Claude Code. These skills maximize AI productivity through clear prompts, proper task decomposition, iterative refinement workflows, and phase-based architectural planning.

---

## 1. Prompt-Driven Implementation

### Purpose
Communicate development intent clearly and precisely to AI assistants, enabling them to generate correct, maintainable code that aligns with project architecture and coding standards.

### Key Capabilities
- **Contextual Prompts**: Provide sufficient context for accurate implementation
- **Constraint Specification**: Define boundaries and requirements explicitly
- **Example-Driven**: Show desired patterns through examples
- **Incremental Requests**: Break complex tasks into manageable steps
- **Verification Criteria**: Specify how to validate the result

### Anatomy of an Effective Prompt

```text
[Context] + [Task] + [Constraints] + [Examples] + [Success Criteria]
```

#### Poor Prompt Examples

```text
❌ "Add authentication"
   Problem: Too vague, no context, unclear scope

❌ "Make the app better"
   Problem: No specific task, unmeasurable

❌ "Fix the bug"
   Problem: No description of bug, no reproduction steps

❌ "Create a user model with FastAPI and make it secure"
   Problem: Ambiguous requirements, no architectural context
```

#### Good Prompt Examples

```text
✅ "Create a User model for our FastAPI backend using SQLModel.
   The model should:
   - Include fields: id, email (unique), hashed_password, full_name, created_at
   - Use the TimestampMixin from models/base.py
   - Follow the pattern in models/task.py
   - Include Pydantic validation (email format, password min length 8)

   Success criteria:
   - Model follows existing project structure
   - All fields properly typed
   - Database constraints included (unique email)
   - Compatible with Alembic migrations"

✅ "Implement JWT authentication in our FastAPI backend.
   Context:
   - We use python-jose for JWT
   - Secrets in environment variables (JWT_SECRET_KEY)
   - Access tokens expire in 30 minutes
   - We need both /login and /refresh endpoints

   Requirements:
   - Follow the auth pattern from backend-skills.md
   - Return both access_token and refresh_token
   - Include proper error handling (401 for invalid credentials)
   - Add get_current_user dependency for protected routes

   Reference: See backend/config.py for settings structure"

✅ "Add a task creation form to the Next.js dashboard.
   Context:
   - Using App Router (app/dashboard/tasks/new/page.tsx)
   - Form library: react-hook-form with zod validation
   - API client in lib/api/tasks.ts
   - UI components from components/ui (shadcn)

   Requirements:
   - Fields: title (required), description (optional), priority (select)
   - Client-side validation with zod schema
   - Loading state during submission
   - Success toast notification
   - Redirect to /dashboard/tasks on success
   - Error handling with error messages

   Style:
   - Match existing form styling in components/task-form.tsx
   - Responsive design (mobile-first)
   - Proper accessibility (labels, aria attributes)"
```

### Prompt Templates

#### Feature Implementation Template

```text
Implement [FEATURE] in [LOCATION]

Context:
- Current state: [What exists now]
- Related code: [Relevant files/patterns]
- Architecture: [How this fits in the system]

Requirements:
- Functional: [What it should do]
- Non-functional: [Performance, security, UX constraints]
- Dependencies: [What it relies on]

Technical Constraints:
- Technology: [Framework/library versions]
- Patterns: [Design patterns to follow]
- Standards: [Coding standards, best practices]

Success Criteria:
- [Testable condition 1]
- [Testable condition 2]
- [Testable condition 3]

References:
- [Link to spec/documentation]
- [Similar implementation to reference]
```

#### Bug Fix Template

```text
Fix bug: [BUG DESCRIPTION]

Reproduction Steps:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected Behavior:
- [What should happen]

Actual Behavior:
- [What actually happens]
- [Error messages/logs]

Context:
- File(s): [Affected files]
- Recent changes: [Related commits/PRs]
- Environment: [Dev/staging/production]

Investigation:
- [What you've tried]
- [What you've ruled out]

Constraints:
- [Don't break existing functionality]
- [Maintain backwards compatibility]
```

#### Refactoring Template

```text
Refactor [COMPONENT/MODULE] in [LOCATION]

Current Issues:
- [Problem 1]
- [Problem 2]
- [Problem 3]

Goals:
- [Improvement goal 1]
- [Improvement goal 2]

Constraints:
- ⚠️ Don't change external API/interface
- ⚠️ Maintain test coverage
- ⚠️ Keep backwards compatibility

Approach:
- [Suggested strategy, if you have one]

Success Criteria:
- [Same functionality, improved structure]
- [All existing tests pass]
- [Improved metric: performance/readability/maintainability]
```

### Context-Setting Techniques

#### Reference Existing Code

```text
✅ "Follow the pattern in auth/jwt.py for token generation"
✅ "Use the same error handling as in routers/tasks.py:45-60"
✅ "Match the component structure of components/task-card.tsx"
```

#### Specify Architecture Files

```text
✅ "Refer to specs/auth/plan.md for architectural decisions"
✅ "Follow the API design in specs/tasks/contracts/tasks.openapi.yaml"
✅ "Use the data model from specs/tasks/data-model.md"
```

#### Link to Documentation

```text
✅ "Reference backend-skills.md section on JWT Security Patterns"
✅ "See frontend-skills.md for App Router layout patterns"
✅ "Follow the Neon configuration in devops-config-skills.md"
```

### Incremental Prompt Strategy

Instead of:
```text
❌ "Build a complete authentication system with login, signup,
   password reset, email verification, 2FA, and admin panel"
```

Do this:
```text
✅ Step 1: "Create User model and database schema"
   [Wait for completion, review]

✅ Step 2: "Implement password hashing and validation"
   [Wait for completion, review]

✅ Step 3: "Add JWT token generation and validation"
   [Wait for completion, review]

✅ Step 4: "Create /login and /signup endpoints"
   [Wait for completion, review]

✅ Step 5: "Add authentication middleware for protected routes"
   [Wait for completion, review]
```

### Handling Ambiguity

When requirements are unclear:

```text
Option 1 - Ask for clarification:
"Before implementing user roles, I need clarification:
1. Should roles be: (a) simple string field, or (b) many-to-many relationship?
2. Are roles hierarchical (admin > moderator > user)?
3. Should role changes be audited?"

Option 2 - Propose with assumptions:
"I'll implement user roles with these assumptions:
- Simple role field (enum: 'admin', 'user')
- Non-hierarchical
- No audit logging (can add later if needed)

Proceed with this approach, or would you prefer a different design?"
```

### Success Criteria
- Prompts include sufficient context (related files, architecture)
- Tasks broken into manageable chunks
- Constraints and requirements clearly stated
- Examples or references provided
- Success criteria are testable
- Ambiguities resolved before implementation

---

## 2. Task Decomposition for Claude Code

### Purpose
Break down large features into atomic, independent tasks that AI can execute sequentially without requiring manual intervention between steps.

### Key Capabilities
- **Atomic Tasks**: Each task is self-contained and completable
- **Dependency Ordering**: Tasks sequenced to respect dependencies
- **Clear Boundaries**: Each task has defined inputs and outputs
- **Verification Points**: Each task includes validation criteria
- **Minimal Context Switching**: Related changes grouped together

### Task Granularity Guidelines

```text
Too Large (❌):
- "Build the entire authentication system"
- "Implement all CRUD operations for all entities"
- "Create the complete frontend dashboard"

Too Small (❌):
- "Add a blank line after line 45"
- "Rename variable x to y"
- "Import the datetime module"

Just Right (✅):
- "Create User model with validation"
- "Implement JWT token generation function"
- "Add login endpoint with error handling"
- "Create login form component with validation"
```

### Task Decomposition Framework

#### Level 1: Feature (Epic)
```text
Feature: User Authentication System
  ↓
```

#### Level 2: Components (Stories)
```text
- Backend Authentication
- Frontend Login/Signup UI
- Protected Route Middleware
- Session Management
  ↓
```

#### Level 3: Tasks (Implementable)
```text
Backend Authentication:
  ✓ Task 1: Create User model (SQLModel)
  ✓ Task 2: Add password hashing utilities
  ✓ Task 3: Create JWT token generation
  ✓ Task 4: Create JWT validation middleware
  ✓ Task 5: Implement /login endpoint
  ✓ Task 6: Implement /signup endpoint
  ✓ Task 7: Implement /refresh endpoint
  ✓ Task 8: Add authentication tests

Frontend Login/Signup UI:
  ✓ Task 9: Create auth context provider
  ✓ Task 10: Create login page
  ✓ Task 11: Create signup page
  ✓ Task 12: Add form validation (zod)
  ✓ Task 13: Implement token storage
  ✓ Task 14: Add logout functionality
```

### Dependency Mapping

```text
Task Dependencies:

Task 2 (Password hashing) → Task 5 (Login endpoint)
Task 3 (JWT generation) → Task 5 (Login endpoint)
Task 4 (JWT validation) → Protected routes

Task 1,2,3,5 (Backend auth) → Task 9 (Auth context)
Task 9 (Auth context) → Task 10,11 (Login/Signup pages)
```

### Task Template

```markdown
## Task: [Task Name]

### Description
[1-2 sentences describing what this task accomplishes]

### Dependencies
- [Task/Feature this depends on]
- [Existing code this builds upon]

### Files to Create/Modify
- `path/to/file1.py` - [What changes]
- `path/to/file2.tsx` - [What changes]

### Requirements
1. [Specific requirement 1]
2. [Specific requirement 2]
3. [Specific requirement 3]

### Technical Details
- Technology: [Framework/library]
- Pattern: [Reference to existing pattern]
- Integration: [How it connects to other parts]

### Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

### Testing
- [ ] Unit tests for [component]
- [ ] Integration test for [flow]

### References
- [Link to spec/documentation]
- [Similar implementation]
```

### Example: Decomposed Feature

```markdown
# Feature: Task Priority Management

## Task 1: Add priority field to Task model

### Description
Add a priority field (enum: low, medium, high, urgent) to the Task SQLModel.

### Dependencies
- Existing Task model in `backend/models/task.py`

### Files to Modify
- `backend/models/task.py` - Add priority field
- `alembic/versions/` - Generate migration

### Requirements
1. Add priority field as Enum (low, medium, high, urgent)
2. Default value: medium
3. Include in database migration

### Acceptance Criteria
- [ ] Priority field added to Task model
- [ ] Migration generated and tested
- [ ] Default value is 'medium'

---

## Task 2: Update API to accept priority

### Description
Modify task creation and update endpoints to accept priority field.

### Dependencies
- Task 1 (priority field exists in model)

### Files to Modify
- `backend/routers/tasks.py` - Update endpoints
- `backend/schemas/task.py` - Update Pydantic schemas

### Requirements
1. TaskCreate schema includes priority (optional)
2. TaskUpdate schema includes priority (optional)
3. Priority validated against enum values

### Acceptance Criteria
- [ ] POST /tasks accepts priority
- [ ] PATCH /tasks/{id} accepts priority
- [ ] Invalid priority values rejected with 400

---

## Task 3: Add priority filter to list endpoint

### Description
Allow filtering tasks by priority in GET /tasks endpoint.

### Dependencies
- Task 1 (priority field exists)

### Files to Modify
- `backend/routers/tasks.py` - Add priority query param
- `backend/services/task_service.py` - Add filter logic

### Requirements
1. Accept ?priority=high query parameter
2. Support multiple priorities: ?priority=high,urgent
3. Maintain existing filters (status, etc.)

### Acceptance Criteria
- [ ] GET /tasks?priority=high returns only high priority tasks
- [ ] Multiple priorities work correctly
- [ ] Combines with other filters

---

## Task 4: Add priority UI to task form

### Description
Add priority dropdown to task creation/edit form in frontend.

### Dependencies
- Task 2 (API accepts priority)

### Files to Modify
- `frontend/components/task-form.tsx` - Add priority field
- `frontend/lib/api/tasks.ts` - Update types

### Requirements
1. Dropdown with options: Low, Medium, High, Urgent
2. Default to Medium
3. Form validation includes priority

### Acceptance Criteria
- [ ] Priority dropdown appears in form
- [ ] Default value is Medium
- [ ] Selected priority sent to API

---

## Task 5: Display priority badge on task cards

### Description
Show priority as colored badge on task list/card views.

### Dependencies
- Task 4 (priority in frontend)

### Files to Modify
- `frontend/components/task-card.tsx` - Add badge
- `frontend/components/ui/badge.tsx` - Priority variants

### Requirements
1. Badge colors: Low (gray), Medium (blue), High (orange), Urgent (red)
2. Display on task card
3. Responsive design

### Acceptance Criteria
- [ ] Priority badge visible on each task
- [ ] Correct colors for each priority
- [ ] Mobile-friendly
```

### Decomposition Anti-Patterns

```text
❌ Tasks with vague descriptions
   "Improve the user experience"
   → ✅ "Add loading spinner to task list during data fetch"

❌ Tasks spanning multiple unrelated areas
   "Update backend and frontend for priority feature"
   → ✅ Split into backend task and frontend task

❌ Tasks with unclear dependencies
   "This should work after the auth stuff is done"
   → ✅ "Depends on Task 7: JWT middleware implementation"

❌ Tasks without acceptance criteria
   "Add priority field"
   → ✅ "Add priority field (acceptance: migration runs, API accepts values)"

❌ Tasks requiring manual steps between
   "Create model, then I'll add the migration manually"
   → ✅ "Create model and generate Alembic migration"
```

### Task Sequencing Strategies

#### Strategy 1: Bottom-Up (Data First)
```text
1. Database schema/models
2. Database migrations
3. Backend services/business logic
4. API endpoints
5. Frontend API client
6. Frontend UI components
7. Integration
```

#### Strategy 2: Top-Down (UI First)
```text
1. Frontend UI mockups/components
2. Frontend API client (with mock data)
3. API endpoint definitions
4. Backend services
5. Database models
6. Database migrations
7. Integration
```

#### Strategy 3: Vertical Slice (Feature-Complete)
```text
1. End-to-end happy path (simple version)
2. Error handling
3. Validation
4. Edge cases
5. Optimization
6. Polish
```

### Success Criteria
- Each task is completable in one session
- Tasks have clear dependencies
- Acceptance criteria are testable
- No manual steps required between tasks
- Each task adds working, testable increment

---

## 3. Iterative Refinement Without Manual Edits

### Purpose
Use AI feedback loops to refine implementations through natural language instead of manual code editing, maintaining full code generation traceability and avoiding context loss.

### Key Capabilities
- **Feedback-Driven Refinement**: Provide structured feedback instead of editing
- **Incremental Improvement**: Request targeted changes
- **Test-Driven Validation**: Use tests to validate each iteration
- **Context Preservation**: Keep AI aware of all changes
- **Revert Capability**: Easy rollback through conversation history

### Iterative Refinement Workflow

```text
┌─────────────────────────────────────┐
│ 1. Initial Implementation Request   │
│    "Create task model with..."      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. AI Generates Code                │
│    [Code generated]                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Review & Test                    │
│    Run tests, manual verification   │
└──────────────┬──────────────────────┘
               │
          ┌────┴────┐
          │         │
     ✅ Good    ❌ Issues Found
          │         │
          │         ▼
          │    ┌─────────────────────────────┐
          │    │ 4. Provide Specific Feedback│
          │    │    "Change X to Y because..." │
          │    └──────────┬──────────────────┘
          │               │
          │               ▼
          │    ┌─────────────────────────────┐
          │    │ 5. AI Refines Code          │
          │    │    [Updated code]            │
          │    └──────────┬──────────────────┘
          │               │
          └───────────────┴─────► Continue until ✅
```

### Effective Feedback Patterns

#### ❌ Poor Feedback (Manual Edit)
```text
User: [Opens file and edits code manually]
Problem: AI loses context, can't learn from changes
```

#### ✅ Good Feedback (Descriptive)
```text
User: "The task model looks good, but I need two changes:
1. Change 'due_date' to Optional[datetime] (can be None)
2. Add a 'completed_at' field (Optional[datetime])

Reason: Tasks don't always have due dates, and we need to track completion time."

AI: [Regenerates code with changes]
```

#### ❌ Poor Feedback (Vague)
```text
User: "This doesn't work"
User: "Make it better"
User: "Fix the bug"
```

#### ✅ Good Feedback (Specific)
```text
User: "The login endpoint returns 500 when email is invalid.
Expected: Return 401 with message 'Invalid credentials'
Actual: Returns 500 Internal Server Error

Please update the error handling to catch invalid email and return 401."
```

### Feedback Templates

#### Code Quality Feedback

```text
The [COMPONENT] works but needs refinement:

Code Quality Issues:
1. [Issue 1] - [Why it's problematic]
2. [Issue 2] - [Why it's problematic]

Suggested Changes:
1. [Change 1] - [Expected improvement]
2. [Change 2] - [Expected improvement]

Example:
"The password validation works but needs refinement:

Code Quality Issues:
1. Password validation is in the router - should be in the model
2. Error messages are not specific enough

Suggested Changes:
1. Move validation to User model as a Pydantic validator
2. Return specific errors: 'Password must be at least 8 characters'
   instead of 'Invalid password'"
```

#### Functional Issue Feedback

```text
The [FEATURE] has a functional issue:

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected Behavior:
[What should happen]

Actual Behavior:
[What actually happens]

Error Message (if any):
[Exact error text]

Requested Fix:
[Specific change needed]

Example:
"The task creation endpoint has a functional issue:

Steps to Reproduce:
1. POST /tasks with title: 'Test Task'
2. Check response

Expected Behavior:
Should return 201 with created task including id, created_at, updated_at

Actual Behavior:
Returns 200 (wrong status code) and missing created_at field

Requested Fix:
1. Change status code to 201
2. Ensure created_at is included in response (check TaskResponse schema)"
```

#### Performance Feedback

```text
The [FEATURE] has performance issues:

Observation:
[What you noticed]

Measurement:
[Metrics/timing if available]

Root Cause (if known):
[What's causing the slowness]

Optimization Request:
[Specific optimization to apply]

Example:
"The task list endpoint has performance issues:

Observation:
Loading 100 tasks takes 3+ seconds

Root Cause:
N+1 query problem - fetching user for each task separately

Optimization Request:
Add eager loading for user relationship using selectinload()
Reference: backend-skills.md section 4 on async database handling"
```

#### Style/Convention Feedback

```text
The [CODE] works but doesn't match our conventions:

Current Style:
[What was generated]

Project Convention:
[What we use in this project]

Examples:
[Reference to existing code]

Requested Changes:
[Specific style adjustments]

Example:
"The component works but doesn't match our conventions:

Current Style:
- Uses 'function' keyword for components
- Inline styles

Project Convention:
- Arrow function components (const ComponentName = () => {})
- Tailwind CSS classes only

Example: See components/task-card.tsx

Requested Changes:
Convert to arrow function and replace inline styles with Tailwind classes"
```

### Test-Driven Refinement

```text
Step 1: Generate Initial Implementation
User: "Create a function to calculate task completion percentage"

Step 2: Generate Test First (Optional)
User: "Before implementing, create a test that verifies:
- Returns 0 when no tasks
- Returns 50 when half completed
- Returns 100 when all completed"

Step 3: Implement to Pass Tests
AI: [Generates implementation]

Step 4: Refine Based on Test Results
User: "Tests are failing on edge case: when tasks array is empty,
function returns NaN instead of 0. Fix this."

AI: [Updates implementation]
```

### Incremental Enhancement Pattern

```text
Version 1 - Minimal:
"Create a basic task card component showing just title and status"

Version 2 - Add Details:
"Enhance the task card to also show description and due date"

Version 3 - Add Interactivity:
"Add edit and delete buttons to the task card"

Version 4 - Add Loading States:
"Show loading spinner when delete is in progress"

Version 5 - Add Confirmation:
"Add confirmation dialog before delete"
```

### Comparison-Based Refinement

```text
"The current implementation in components/task-card.tsx is:
[Describe current state]

But I want it to match the pattern in components/user-card.tsx:
- Use Card component from ui/card
- Layout: image left, content right
- Actions in footer

Please refactor task-card to follow the same structure as user-card"
```

### A/B Option Refinement

```text
"I'm not sure about the error handling approach. Can you show me two options:

Option A: Throw exceptions and let error boundary catch them
Option B: Return error state and display inline error messages

Show me both implementations and explain trade-offs"

[After reviewing]

"I'll go with Option B - please implement that approach"
```

### Refinement Anti-Patterns

```text
❌ Making manual edits, then asking AI to continue
   (AI loses context of changes)

❌ Describing problems without specifics
   "Something is wrong with the auth"

❌ Requesting complete rewrites for small issues
   "Rewrite the entire component" (when only one function needs change)

❌ Providing contradictory feedback in same message
   "Make it more secure but simpler" (without clarifying priority)

❌ Skipping validation between iterations
   "Change X, then Y, then Z" (without testing X first)
```

### Success Criteria
- Refinement requests are specific and actionable
- Each iteration improves code measurably
- Tests validate each change
- AI maintains full context throughout
- No manual code editing required
- Clear rollback path via conversation

---

## 4. Phase-Based Architectural Scaling

### Purpose
Design systems that evolve incrementally across defined phases (Phase I: Foundation, Phase II: Enhancement, Phase III: AI Integration) without requiring architectural rewrites.

### Key Capabilities
- **Foundation-First**: Build extensible core in Phase I
- **Loose Coupling**: Design for future enhancement
- **Interface Stability**: Maintain backwards compatibility
- **Feature Flags**: Control rollout of new capabilities
- **Migration Paths**: Plan transitions between phases

### Phase-Based Architecture Framework

```text
Phase I: Foundation (MVP)
├── Core data models
├── Essential CRUD operations
├── Basic authentication
├── Simple UI
└── Database setup

Phase II: Enhancement
├── Advanced features
├── Improved UX
├── Performance optimization
├── Enhanced security
└── Integration with services

Phase III: AI Integration
├── AI-powered insights
├── Intelligent recommendations
├── Automated workflows
├── Predictive features
└── Natural language interfaces
```

### Phase I: Foundation Principles

#### Design for Extension

```python
# ❌ Tightly coupled - hard to extend
class TaskService:
    def create_task(self, title: str, user_id: int):
        task = Task(title=title, user_id=user_id)
        db.add(task)
        db.commit()
        return task

# ✅ Extensible - easy to add features in Phase II/III
class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.validators: List[TaskValidator] = []
        self.post_processors: List[TaskPostProcessor] = []

    async def create_task(self, task_data: TaskCreate, user_id: int):
        # Phase I: Basic validation
        task = Task(**task_data.dict(), user_id=user_id)

        # Phase II: Can add advanced validators
        for validator in self.validators:
            await validator.validate(task)

        self.db.add(task)
        await self.db.commit()

        # Phase III: Can add AI-powered post-processing
        for processor in self.post_processors:
            await processor.process(task)

        return task
```

#### Abstraction Layers

```typescript
// Phase I: Direct API calls
// ❌ Hard to modify later
export async function getTasks() {
  const response = await fetch('/api/tasks')
  return response.json()
}

// ✅ Abstracted - easy to enhance
export class TaskService {
  constructor(private apiClient: ApiClient) {}

  async getTasks(): Promise<Task[]> {
    // Phase I: Simple fetch
    const tasks = await this.apiClient.get<Task[]>('/tasks')

    // Phase II: Can add caching
    // Phase III: Can add AI-powered sorting/filtering
    return tasks
  }
}
```

#### Configuration Points

```python
# Phase I: Simple config
class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str

    # Phase II/III: Feature flags for gradual rollout
    enable_ai_insights: bool = False
    enable_smart_recommendations: bool = False
    enable_auto_categorization: bool = False
```

### Phase II: Enhancement Patterns

#### Backward-Compatible Extensions

```python
# Phase I Model
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    status: str
    user_id: int

# Phase II: Add fields without breaking Phase I
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    status: str
    user_id: int

    # New fields (optional, don't break existing code)
    priority: Optional[str] = Field(default="medium")
    tags: Optional[str] = Field(default=None)
    estimated_duration: Optional[int] = Field(default=None)

    # Relationship (doesn't affect existing queries)
    subtasks: List["Task"] = Relationship(back_populates="parent")
```

#### Decorator Pattern for Features

```python
# Phase I: Basic service
class TaskService:
    async def create_task(self, task_data: TaskCreate):
        return await self.db.add(Task(**task_data.dict()))

# Phase II: Add features via decorators
class CachingTaskService(TaskService):
    """Adds caching layer without modifying base service"""
    def __init__(self, base_service: TaskService, cache: Cache):
        self.base = base_service
        self.cache = cache

    async def get_task(self, task_id: int):
        cached = await self.cache.get(f"task:{task_id}")
        if cached:
            return cached

        task = await self.base.get_task(task_id)
        await self.cache.set(f"task:{task_id}", task)
        return task

# Phase III: Add AI features
class AIEnhancedTaskService(TaskService):
    """Adds AI capabilities without modifying base"""
    def __init__(self, base_service: TaskService, ai_service: AIService):
        self.base = base_service
        self.ai = ai_service

    async def create_task(self, task_data: TaskCreate):
        # AI auto-categorization
        if settings.enable_auto_categorization:
            task_data.category = await self.ai.categorize(task_data.title)

        # AI estimated duration
        if settings.enable_duration_prediction:
            task_data.estimated_duration = await self.ai.estimate_duration(task_data)

        return await self.base.create_task(task_data)
```

#### Feature Flags for Gradual Rollout

```python
# backend/routers/tasks.py
from config import settings

@router.get("/tasks/{task_id}/insights")
async def get_task_insights(task_id: int):
    """Phase III: AI-powered insights"""
    if not settings.enable_ai_insights:
        raise HTTPException(status_code=404, detail="Feature not available")

    # AI analysis
    insights = await ai_service.analyze_task(task_id)
    return insights
```

```typescript
// frontend/components/task-detail.tsx
import { env } from '@/lib/env'

export function TaskDetail({ task }: { task: Task }) {
  return (
    <div>
      <TaskHeader task={task} />
      <TaskContent task={task} />

      {/* Phase III: Conditionally render AI features */}
      {env.NEXT_PUBLIC_ENABLE_AI_INSIGHTS && (
        <AIInsightsPanel taskId={task.id} />
      )}
    </div>
  )
}
```

### Phase III: AI Integration Patterns

#### AI Service Layer

```python
# Phase III: Separate AI service (doesn't modify core)
class AITaskService:
    """AI-powered task intelligence"""

    async def suggest_priority(self, task: Task) -> str:
        """Analyze task and suggest priority based on:
        - Title keywords
        - Due date proximity
        - User's task history
        - Current workload
        """
        context = {
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "user_history": await self.get_user_history(task.user_id),
        }

        priority = await self.ai_client.predict_priority(context)
        return priority

    async def generate_subtasks(self, task: Task) -> List[TaskCreate]:
        """AI-powered task decomposition"""
        prompt = f"Break down this task into subtasks: {task.title}"
        subtasks = await self.ai_client.generate_subtasks(prompt)
        return subtasks

    async def smart_search(self, query: str, user_id: int) -> List[Task]:
        """Semantic search across tasks"""
        embedding = await self.ai_client.embed(query)
        similar_tasks = await self.vector_db.search(embedding, user_id)
        return similar_tasks
```

#### Gradual AI Adoption

```python
# Phase I: Manual task creation
@router.post("/tasks")
async def create_task(task_data: TaskCreate):
    return await task_service.create(task_data)

# Phase II: Optional AI suggestions
@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    use_ai_suggestions: bool = False
):
    if use_ai_suggestions and settings.enable_ai_insights:
        # AI-enhanced task data
        task_data = await ai_service.enhance_task_data(task_data)

    return await task_service.create(task_data)

# Phase III: AI by default with opt-out
@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    disable_ai: bool = False
):
    if not disable_ai and settings.enable_ai_insights:
        task_data = await ai_service.enhance_task_data(task_data)

    return await task_service.create(task_data)
```

### Migration Strategies Between Phases

#### Database Migrations

```python
# Phase I → Phase II Migration
"""Add priority and tags to tasks

Revision ID: 002_add_priority_tags
"""
def upgrade():
    # Add new columns with defaults (backward compatible)
    op.add_column('tasks', sa.Column('priority', sa.String(50), server_default='medium'))
    op.add_column('tasks', sa.Column('tags', sa.Text(), nullable=True))

    # Add indexes for Phase II features
    op.create_index('ix_tasks_priority', 'tasks', ['priority'])

def downgrade():
    op.drop_index('ix_tasks_priority', table_name='tasks')
    op.drop_column('tasks', 'tags')
    op.drop_column('tasks', 'priority')
```

#### API Versioning

```python
# Phase I: v1 API
@router.get("/v1/tasks")
async def get_tasks_v1():
    """Original API - always maintained"""
    return await task_service.get_all()

# Phase II: v2 API with enhancements
@router.get("/v2/tasks")
async def get_tasks_v2(
    priority: Optional[str] = None,
    tags: Optional[str] = None
):
    """Enhanced API with filtering"""
    return await task_service.get_all(priority=priority, tags=tags)

# Phase III: v3 API with AI
@router.get("/v3/tasks")
async def get_tasks_v3(
    priority: Optional[str] = None,
    ai_sort: bool = False
):
    """AI-powered API"""
    tasks = await task_service.get_all(priority=priority)

    if ai_sort:
        tasks = await ai_service.smart_sort(tasks)

    return tasks
```

#### Frontend Feature Evolution

```typescript
// Phase I: Basic component
export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <div>
      {tasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}

// Phase II: Enhanced with filtering
export function TaskList({ tasks }: { tasks: Task[] }) {
  const [filter, setFilter] = useState<TaskFilter>({})

  const filteredTasks = useMemo(() => {
    return filterTasks(tasks, filter)
  }, [tasks, filter])

  return (
    <div>
      <TaskFilters value={filter} onChange={setFilter} />
      {filteredTasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}

// Phase III: AI-powered
export function TaskList({ tasks }: { tasks: Task[] }) {
  const [filter, setFilter] = useState<TaskFilter>({})
  const [aiSortEnabled, setAiSortEnabled] = useState(false)

  const { data: sortedTasks, isLoading } = useAISort(tasks, aiSortEnabled)

  const displayTasks = aiSortEnabled ? sortedTasks : tasks
  const filteredTasks = useMemo(() => {
    return filterTasks(displayTasks, filter)
  }, [displayTasks, filter])

  return (
    <div>
      <TaskFilters value={filter} onChange={setFilter} />

      {/* Phase III: AI toggle */}
      {env.NEXT_PUBLIC_ENABLE_AI_INSIGHTS && (
        <AIToggle value={aiSortEnabled} onChange={setAiSortEnabled} />
      )}

      {isLoading ? (
        <LoadingState />
      ) : (
        filteredTasks.map(task => (
          <TaskCard key={task.id} task={task} />
        ))
      )}
    </div>
  )
}
```

### Architectural Decision Checklist

```text
When designing Phase I (Foundation):
✅ Is this extensible? Can Phase II add features without rewrites?
✅ Are interfaces stable? Will they support future enhancements?
✅ Is coupling loose? Can AI services be added as separate layers?
✅ Are feature flags prepared? Can we toggle Phase III features?
✅ Is the data model flexible? Can we add fields without migrations breaking?

When designing Phase II (Enhancement):
✅ Does this maintain Phase I compatibility?
✅ Are new features opt-in via flags?
✅ Can Phase I code still work without Phase II features?
✅ Are APIs versioned for gradual migration?

When designing Phase III (AI Integration):
✅ Are AI features isolated in separate service layer?
✅ Can the system work without AI (graceful degradation)?
✅ Are AI costs/latency acceptable?
✅ Is user privacy preserved?
✅ Can AI features be disabled per-user?
```

### Success Criteria
- Phase I provides solid foundation for all future phases
- Phase II enhancements don't require Phase I rewrites
- Phase III AI features integrate via separate service layer
- Feature flags control phase rollout
- Backward compatibility maintained across all phases
- Clear migration paths between phases

---

## Integration Example: End-to-End AI-Assisted Workflow

### Scenario: Adding Task Priority Feature (All 4 Skills)

#### Skill 1: Prompt-Driven Implementation

```text
User: "I want to add a priority feature to tasks. Users should be able to
mark tasks as Low, Medium, High, or Urgent.

Context:
- Backend: FastAPI with SQLModel
- Frontend: Next.js App Router with React
- Current task model: backend/models/task.py
- Current task API: backend/routers/tasks.py
- Frontend task components: frontend/components/task-*.tsx

Requirements:
- Priority is optional, defaults to Medium
- Stored as enum in database
- Filterable in API (GET /tasks?priority=high)
- Displayed as colored badge in UI
- Editable in task form

Phase:
- This is Phase II enhancement
- Must maintain Phase I compatibility (existing tasks without priority)

References:
- Follow pattern in backend-skills.md for SQLModel enums
- Match UI pattern in frontend-skills.md for badges

Please break this down into tasks."
```

#### Skill 2: Task Decomposition

```text
AI: "I'll break this into 5 sequential tasks:

Task 1: Add priority field to Task model
  - Add TaskPriority enum
  - Add priority field (default: medium)
  - Generate Alembic migration
  - Acceptance: Migration runs, existing tasks get default

Task 2: Update API schemas and endpoints
  - Update TaskCreate/TaskUpdate schemas
  - Add priority filter to GET /tasks
  - Acceptance: API accepts priority, filtering works

Task 3: Update frontend types and API client
  - Add priority to Task type
  - Update API client
  - Acceptance: TypeScript types updated, no errors

Task 4: Add priority to task form
  - Add priority dropdown
  - Update form validation
  - Acceptance: Form submits with priority

Task 5: Display priority badge
  - Create PriorityBadge component
  - Add to TaskCard
  - Acceptance: Badge appears with correct colors

Shall I start with Task 1?"
```

#### Skill 3: Iterative Refinement

```text
[After Task 1 completion]

User: "The migration looks good, but I noticed two issues:
1. The default value should be stored as enum value, not string
2. We should add an index on priority for better query performance

Please update the migration to fix these."

AI: [Regenerates migration with fixes]

[After testing]

User: "Perfect! The migration now uses enum values and includes the index.
Let's move to Task 2."

[After Task 4 completion]

User: "The form works, but the priority dropdown should show icons:
- Low: ⬇️
- Medium: ➡️
- High: ⬆️
- Urgent: 🔥

Please update the dropdown to include these icons before each label."

AI: [Updates component with icons]
```

#### Skill 4: Phase-Based Architecture

```text
AI: "I've designed this feature to be Phase II compatible:

Phase I Compatibility:
✅ Existing tasks without priority automatically get 'medium' default
✅ API continues to work without priority filter (optional param)
✅ Frontend gracefully handles tasks with null priority (shows 'Medium')

Phase II Enhancement:
✅ New priority field with filtering
✅ UI enhancements (badges, icons)
✅ Performance optimization (indexed queries)

Phase III Readiness:
🔮 Priority field can be used for AI-powered task sorting
🔮 Priority data feeds into workload prediction AI
🔮 System can suggest priority based on title/due date

Feature Flag:
I've added ENABLE_PRIORITY_FILTER to settings.py for gradual rollout.

The implementation maintains backward compatibility while preparing for
future AI enhancements."
```

---

## AI-Assisted Development Best Practices

### Do's ✅

```text
✅ Provide architectural context in every prompt
✅ Reference existing code patterns
✅ Break large tasks into atomic chunks
✅ Specify acceptance criteria
✅ Give structured feedback, not manual edits
✅ Test each iteration before refining
✅ Design for future phases from Phase I
✅ Use feature flags for gradual rollout
✅ Maintain conversation context across related tasks
✅ Document AI-generated decisions in ADRs
```

### Don'ts ❌

```text
❌ Make manual edits without telling AI
❌ Request large features in single prompt
❌ Provide vague feedback ("make it better")
❌ Skip testing between iterations
❌ Design Phase I with no Phase II/III consideration
❌ Ignore backward compatibility
❌ Mix unrelated tasks in single prompt
❌ Assume AI remembers context from days ago
❌ Request rewrites when refinement would work
❌ Skip documentation for complex implementations
```

---

## Success Metrics

### Prompt Quality
- AI understands requirements on first attempt (>80%)
- Generated code matches project conventions (>90%)
- Minimal clarification questions needed

### Task Decomposition
- Each task completable in <30 minutes
- Dependencies clearly ordered
- No blocking on manual steps

### Refinement Efficiency
- <3 iterations to reach acceptable solution
- No manual edits required
- Test pass rate improves each iteration

### Architectural Scalability
- Phase II features don't require Phase I rewrites
- Feature flags enable safe rollout
- Clear migration paths exist

---

## References

- Spec-Driven Development: `core-skills.md`
- Backend Patterns: `backend-skills.md`
- Frontend Patterns: `frontend-skills.md`
- DevOps Configuration: `devops-config-skills.md`
- Project Constitution: `.specify/memory/constitution.md`
- Task Templates: `specs/<feature>/tasks.md`
- Prompt History Records: `history/prompts/`
- Architecture Decisions: `history/adr/`
