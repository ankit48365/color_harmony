# Codex + GitHub Workflow

This guide explains a practical start-to-end workflow for using ChatGPT Codex with a GitHub repository.

It is written around the way you described working before:

1. Create an issue on GitHub.
2. Create a branch for that issue.
3. Work locally on that branch.
4. Push the branch to GitHub.
5. Open and merge a pull request.
6. Close the issue automatically or manually.
7. Delete the branch on GitHub and clean up local branches.

This document also makes it clear when a human must step in and when Codex can do the work for you.

## Quick rule of thumb

- Human is always needed for product decisions, reviewing the work, and any GitHub action that depends on your account permissions or preferences.
- Codex is strongest at local repository work: reading code, editing code, running tests, fixing failures, preparing commits, and helping with GitHub workflow steps.
- Codex can often help with GitHub operations too, but only if your machine is already authenticated with tools such as `gh` and you want Codex to use them.

## Roles

### Human responsibilities

- Create or approve the GitHub issue.
- Decide what should be built.
- Review the final code or pull request.
- Approve merge strategy and branch deletion policy.
- Provide GitHub access if you want Codex to push branches, open PRs, or close issues on your behalf.

### Codex responsibilities

- Inspect the repository and understand the codebase.
- Create or switch local branches.
- Implement the requested change.
- Split files, refactor modules, and update docs.
- Run tests, lint, coverage, and other local checks.
- Stage and commit the changes if asked.
- Push, open a PR, and help with cleanup if GitHub access is available and you request it.

## Example workflow

This example uses a fictional issue:

- Issue number: `#42`
- Issue title: `Fix hero heading contrast on light background`
- Repository default branch: `main`
- Working branch: `codex/42-fix-hero-contrast`

### Step 1: Create the issue on GitHub

Human needed:
- Yes.

What happens:
- You create GitHub issue `#42` describing the bug or task.
- You can also assign labels, milestone, priority, and screenshots.

What you can tell Codex next:

```text
Work on issue #42: Fix hero heading contrast on light background.
Create a branch, make the fix, run tests, and prepare the changes.
```

If GitHub CLI is configured and you want Codex to fetch the issue directly, you can say:

```text
Use GitHub CLI to read issue #42 and implement it.
or
Use GitHub CLI to read issue {CreateActionsWorkflows #1} and implement it.
```

## Step 2: Create the working branch

Human needed:
- Sometimes.

Codex can do this locally:
- Create and switch to `codex/42-fix-hero-contrast`

Human is needed if:
- You want to create the branch from the GitHub web UI yourself.
- Your repo has a strict branch naming convention that you want to control manually.

Typical local branch command:

```powershell
git checkout main
git pull
git checkout -b codex/42-fix-hero-contrast
```

You can ask Codex:

```text
Create a branch for issue #42 and do the implementation there.
```

## Step 3: Implement the work locally

Human needed:
- No, unless the requirements are unclear.

What Codex can do here:
- Read the codebase.
- Find the relevant files.
- Edit the implementation.
- Update tests.
- Update docs.
- Explain the changes.

Example request:

```text
Fix the hero heading contrast for issue #42. Update tests and docs too.
```

Typical Codex output at this stage:
- Code changes made locally.
- Tests run locally.
- Short summary of what changed.

## Step 4: Run local quality checks

Human needed:
- Usually no.

What Codex can run:
- `pytest`
- coverage
- `pylint`
- formatting or other repo checks

Example request:

```text
Run pytest, coverage, and pylint. Fix anything that fails.
```

If your repository includes GitHub Actions for these checks, Codex can also update the workflow files locally.

## Step 5: Update badges if you use badge numbers in README

Human needed:
- No, unless you want to review the wording or badge style.

Important note:
- Badge URLs like `https://img.shields.io/badge/coverage-72.22%25-blue` are static.
- The `72.22` and `10.00` values do not update by themselves.
- Something must compute the numbers and rewrite `README.md`.

Codex can help in two ways:

1. Local/manual update flow
- Run coverage and pylint locally.
- Capture the values.
- Rewrite the badge lines in `README.md`.

2. CI-driven update flow
- Create or update GitHub Actions so the workflow computes the metrics and updates the badge values automatically.

Example prompt:

```text
Run coverage and pylint, then update the README badges with the latest values.
```

## Step 6: Commit the changes

Human needed:
- Optional.

Codex can:
- Stage files.
- Write a commit message.
- Create the commit.

Human may want to step in if:
- You prefer to review the diff before commit.
- You have a commit message convention to enforce manually.

Example commit message:

```text
Fix hero heading contrast on light theme
```

## Step 7: Push the branch to GitHub

Human needed:
- Maybe.

Codex can do this if:
- Git is configured locally.
- Authentication to GitHub is already working.
- You explicitly ask Codex to push.

Human is needed if:
- Authentication is not configured.
- Your organization requires browser approval, SSO, or manual credential entry.

Example prompt:

```text
Push this branch to origin.
```

Typical command:

```powershell
git push -u origin codex/42-fix-hero-contrast
```

## Step 8: Open the pull request

Human needed:
- Maybe.

Codex can do this if:
- `gh` is installed and authenticated.
- You want Codex to use it.

Human is needed if:
- You prefer to write the PR description yourself.
- Your team requires selecting reviewers, labels, or templates manually in the GitHub web UI.

Very important for issue closing:
- The PR description should include a closing keyword such as `Closes #42`.

Example PR body:

```text
Fixes the hero heading contrast on the light background.

Closes #42
```

Why this matters:
- A linked PR merged into the default branch usually auto-closes the issue.
- Deleting the branch alone does not close the issue.

## Step 9: Review and merge the pull request

Human needed:
- Usually yes.

Why:
- Most teams want a human to review the PR.
- Merge rights may be limited.
- You may need to choose merge, squash, or rebase strategy.

What Codex can still help with:
- Explain the diff.
- Address review comments.
- Make follow-up commits.
- Re-run tests.

Important issue-closing behavior:
- If the PR contains `Closes #42` and it is merged into `main`, the issue should auto-close, assuming the repository has not disabled auto-closing for linked PRs.

## Step 10: Delete the branch on GitHub

Human needed:
- Optional.

Codex can help if GitHub access is available.

Human may still choose to do this manually because:
- Some teams prefer reviewing the merged PR page before deleting the branch.
- Some repositories automatically delete merged branches.

Important:
- This is cleanup only.
- Branch deletion is not what closes the issue.

## Step 11: Clean up local branches

Human needed:
- Recommended for approval, because deleting branches is destructive.

Codex can do this when asked explicitly.

Your old Linux-style cleanup command was:

```bash
git fetch --all --prune
git branch | grep -v "main" | xargs git branch -D
```

Because this repository is being used from PowerShell on Windows, a safer PowerShell version is:

```powershell
git fetch --all --prune
git branch --format="%(refname:short)" | Where-Object { $_ -ne "main" } | ForEach-Object { git branch -D $_ }
```

Use caution:
- This deletes all local branches except `main`.
- Only run it when you are sure no local work needs to be kept.

## Human intervention checklist

Human definitely needed:
- Creating the issue if Codex does not have GitHub issue access.
- Clarifying requirements when the task is ambiguous.
- Reviewing the final code or PR.
- Approving merge decisions.
- Approving destructive cleanup commands.

Human maybe needed:
- Creating the branch in GitHub UI.
- Pushing to GitHub if authentication is not set up.
- Opening the PR if `gh` is unavailable.
- Deleting the remote branch if automation is not enabled.

Human usually not needed:
- Reading the codebase.
- Implementing the fix.
- Refactoring files.
- Updating tests.
- Updating docs.
- Running local checks.
- Preparing commits.

## Best-practice prompt pattern

For a typical issue-driven task, you can use a prompt like this:

```text
Work on GitHub issue #42.
Create or switch to a branch named codex/42-fix-hero-contrast.
Implement the fix locally, update tests and docs, run pytest, coverage, and pylint,
then prepare the commit. If GitHub CLI is available, push the branch and open a PR
with "Closes #42" in the description.
```

## Recommended real-world flow

1. Human creates the issue on GitHub.
2. Human asks Codex to work on that issue.
3. Codex creates the local branch.
4. Codex implements the change.
5. Codex runs tests, lint, and coverage.
6. Codex updates docs and badges if needed.
7. Codex stages and commits the change.
8. Codex pushes and opens the PR if GitHub access is available.
9. Human reviews and merges the PR.
10. GitHub auto-closes the issue if the PR was linked with a closing keyword and merged into the default branch.
11. Human or Codex deletes the branch.
12. Human approves local branch cleanup; Codex can run it.

## Final takeaway

The most important distinction is this:

- Merging a linked PR into the default branch is what usually closes the issue.
- Deleting the branch is only cleanup.

Codex fits best as your local implementation and automation partner inside that process.
