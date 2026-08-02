---
name: pr-description
description: Generate comprehensive PR descriptions by analyzing git diffs and understanding the intent behind changes. Use this whenever the user is about to create a pull request, mentions writing PR descriptions, or has made code changes they want to document. Extracts the diff, identifies what changed and why, and produces a well-structured PR description with summary, testing notes, and context for reviewers.
compatibility: Git (installed), Node.js or Python optional for enhanced analysis
---

# PR Description Generator Skill

This skill helps you create clear, comprehensive pull request descriptions by automatically analyzing your code changes and understanding the reasoning behind them.

## What This Skill Does

When invoked, the skill:
1. **Extracts your git diff** — reads the current uncommitted changes or compares your branch against main
2. **Analyzes what changed** — identifies files modified, new features, bug fixes, refactoring, etc.
3. **Understands why** — uses file names, commit messages, and conversation context to infer the motivation
4. **Generates a PR description** — produces a structured, reviewer-friendly summary

## When to Use This Skill

Trigger this skill when you:
- Are about to create a pull request and want a well-written description
- Have made code changes and need to document them clearly
- Ask "generate a PR description", "write the PR body", "what should I put in the PR?", or similar
- Want to make sure your reviewers understand the context and reasoning behind your changes
- Have changes across multiple files and need a clear summary

## How It Works

### Input

The skill reads:
- **Git diff** — automatically fetches `git diff HEAD` or compares against your base branch
- **Conversation context** — any explanation you've given in this chat about why you made the changes
- **File structure** — uses naming patterns to understand what type of changes were made

### Output

A structured PR description template with:

```markdown
## What
Brief summary of what was changed (1-2 sentences).

## Why
Explanation of the reasoning, problem being solved, or benefit provided.

## Changes
Organized list of specific changes by category or file:
- **Feature/Fix/Refactor:** File or module changed and what was done

## Testing
- How to test the changes
- What should be verified
- Edge cases covered (if applicable)

## Notes for Reviewers
- Any architectural decisions worth noting
- Dependencies or side effects
- Questions or areas needing discussion
```

## Workflow

### Quick PR Description
```
User: "Generate a PR description for my current changes"
→ Skill extracts diff
→ Analyzes changes
→ Generates description
→ User reviews and modifies as needed
```

### PR with Context
```
User: "I refactored the auth middleware to support session tokens. Generate a PR description."
→ Skill reads the explanation
→ Extracts diff to understand scope
→ Combines context with code analysis
→ Generates description emphasizing the why
```

### Large Multi-File Changes
```
User: "Create a PR description for this database migration"
→ Skill groups changes by type (schema, migrations, models)
→ Identifies database changes, ORM updates, test modifications
→ Explains impact and testing approach
→ Generates comprehensive description
```

## Key Principles

- **Be specific** — reference actual file names, functions, and modules from the diff
- **Explain the why** — reviewers care more about motivation than mechanics
- **Anticipate questions** — address edge cases, performance considerations, dependencies
- **Group logically** — organize changes by feature/component, not just by file
- **Keep it concise** — long descriptions are overwhelming; focus on what matters
- **Make testing clear** — describe how to verify the changes work correctly

## Examples

### Example 1: Bug Fix
**Input:** "Fixed the pagination bug where users can't navigate past page 3"

**Output:**
```markdown
## What
Fixed pagination limit that prevented users from viewing results beyond page 3.

## Why
Database query was using LIMIT 50 (hardcoded) instead of dynamic pagination. Users with large datasets couldn't access full results. This was causing customer support tickets.

## Changes
- **lib/pagination.ts:** Removed hardcoded LIMIT, now uses offset/limit from request params
- **tests/pagination.test.ts:** Added tests for pagination beyond page 3

## Testing
1. Create a dataset with 200+ records
2. Navigate pagination and confirm you can reach the last page
3. Verify page numbers update correctly

## Notes
No breaking changes. Database query unchanged, only the application layer.
```

### Example 2: Feature
**Input:** User added TypeScript support to a JavaScript project

**Output:**
```markdown
## What
Added TypeScript configuration and type definitions to the project.

## Why
Enable type safety for better developer experience and catch bugs earlier. This is the first step toward migrating to TypeScript incrementally.

## Changes
- **tsconfig.json:** New TypeScript configuration with strict mode enabled
- **types/index.d.ts:** Global type definitions for existing JavaScript modules
- **.gitignore:** Added TypeScript build output directory
- **package.json:** Added typescript and @types/* dependencies

## Testing
- Run `npm run typecheck` to verify no type errors
- Existing tests should pass without modification
- Visual inspection of generated .d.ts files

## Notes
This is non-breaking. Existing JavaScript code works as-is while we incrementally migrate to TypeScript.
```

## Tips for Best Results

- **Provide context** — explain what problem you're solving or feature you're adding in the chat, and the skill will weave it into the description
- **Use descriptive commit messages** — they help the skill understand intent
- **Review and customize** — the generated description is a starting point; refine it for your project's conventions
- **Include testing approach** — think about how reviewers will verify your changes
- **Call out risks** — if there are potential side effects or performance implications, mention them

## Output Customization

The skill generates descriptions following this project's PR conventions. You can:
- Ask it to reformat in a different style
- Request more/less detail in any section
- Add specific sections your team requires (e.g., Deployment Notes, Breaking Changes)
- Adjust tone or formality

Just let me know what you'd like to change!
