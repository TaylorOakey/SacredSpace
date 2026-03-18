# SacredSpace Starter Pack

A git-ready foundation for SacredSpace repositories.

## Includes
- Repo structure
- Issue templates
- Pull request template
- Canon and governance docs
- Agent role files
- Task and decision record templates
- Starter PowerShell and Bash scaffold scripts
- GitHub Actions workflow stubs
- Initial label set

## Recommended branch model
- `main` → canon / stable trunk
- `dev` → active integration branch
- `feature/*` → scoped implementation branches
- `experiment/*` → non-canon prototypes
- `docs/*` → documentation work

## Suggested first steps
1. Create a new GitHub repository.
2. Unzip this pack into the repo root.
3. Commit the baseline.
4. Create labels from `config/labels/github-labels.csv`.
5. Enable Actions.
6. Protect `main`.
7. Start with `docs/canon/canon-vs-experimental.md` and `docs/governance/working-agreement.md`.
