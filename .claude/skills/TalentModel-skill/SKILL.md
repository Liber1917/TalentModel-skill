```markdown
# TalentModel-skill Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill introduces the core development patterns and workflows used in the `TalentModel-skill` TypeScript repository. It covers code conventions, file organization, commit practices, and documentation update workflows, providing practical guidance for contributing to or extending the project.

## Coding Conventions

**File Naming**
- Use PascalCase for all file names.
  - Example: `TalentModel.ts`, `SkillManager.ts`

**Import Style**
- Use relative imports for all modules.
  - Example:
    ```typescript
    import { SkillManager } from './SkillManager';
    ```

**Export Style**
- Use named exports exclusively.
  - Example:
    ```typescript
    export function evaluateTalent() { /* ... */ }
    export const TALENT_LEVELS = ['Junior', 'Mid', 'Senior'];
    ```

**Commit Patterns**
- Follow [Conventional Commits](https://www.conventionalcommits.org/) with these prefixes:
  - `feat`: New features
  - `fix`: Bug fixes
  - `docs`: Documentation changes
- Example commit message:
  ```
  feat: add skill evaluation logic for advanced candidates
  ```

## Workflows

### Documentation Update
**Trigger:** When someone adds major features, refactors architecture, or introduces new methodologies that require documentation updates.  
**Command:** `/update-docs`

1. Edit or add documentation files such as `README.md`, `README_en.md`, or files in `references/`.
2. Update feature tables, project structure sections, and changelogs to reflect the latest changes.
3. Add or update pull request templates and development guidelines if necessary.
4. Commit changes with a `docs:` prefix, e.g., `docs: update README with new skill workflow`.
5. Open a pull request for review.

**Files Involved:**
- `README.md`
- `README_en.md`
- `references/*.md`
- `.github/pull_request_template/*.md`
- `AGENT.md`
- `SKILL.md`

**Example:**
```bash
# After adding a new feature
/update-docs
# Then edit README.md and commit:
git add README.md
git commit -m "docs: update README with new feature"
git push
```

## Testing Patterns

- Test files follow the pattern `*.test.*` (e.g., `TalentModel.test.ts`).
- Testing framework is not explicitly defined; check test files for usage patterns.
- To add a test:
  1. Create a new file named `FeatureName.test.ts`.
  2. Use named exports for test utilities.
  3. Place the test file alongside the module it tests.

**Example:**
```typescript
// TalentModel.test.ts
import { evaluateTalent } from './TalentModel';

describe('evaluateTalent', () => {
  it('should return Senior for high scores', () => {
    expect(evaluateTalent(95)).toBe('Senior');
  });
});
```

## Commands

| Command       | Purpose                                               |
|---------------|-------------------------------------------------------|
| /update-docs  | Initiate the documentation update workflow            |

```