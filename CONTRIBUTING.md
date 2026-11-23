# Contributing

Thank you for helping make this course better! 🎉

## Ways to contribute
- Fix typos, unclear explanations or broken links.
- Report or fix an example whose output differs from the lesson.
- Suggest better practice tasks, interview questions or DevOps/MLOps connections.
- Translate lessons (open an issue first to coordinate).

## Ground rules
1. **Beginner first.** Explain new terms, prefer simple code over clever code.
2. **Every example must run** with Python 3.10+ and match its *Expected Output* section.
3. **No secrets.** Never commit credentials, tokens, `.env` files or real account IDs.
4. **Keep the lesson template.** Every day keeps all 12 sections, ≥ 3 tasks, and separate solutions.
5. **PEP 8**, meaningful names, comments where they help a beginner.

## Workflow
```bash
git checkout -b fix/day-042-kwargs-typo
# make your change
python scripts/validate_repo.py          # structure & section checks
python scripts/run_examples.py --days 42 # run the examples you touched
git commit -m "Day 042: clarify **kwargs unpacking"
git push origin fix/day-042-kwargs-typo
```
Then open a pull request describing **what** changed and **why**.

## Commit message style
`Day NNN: <short summary>` for lessons, `Project N: ...` for projects, `docs: ...` / `ci: ...` otherwise.

## Code of conduct
Be kind and constructive. Everyone here is learning.
