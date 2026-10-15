# AI-Assisted Code Review Bot

A learning project for reviewing Python changes for potential regressions,
using relevant repository context and an optional local LLM. Secret scanning
will be a secondary feature.

## Current status

Initial data models and Python function extraction are implemented. The parser
finds ordinary, async, and nested functions (including methods), returning names
and line ranges in source order. Six tests cover the current parser behavior.

The entry point still prints a scaffold message. Git change detection, model
calls, target-repository test execution, and GitHub integration are not implemented.
Extracted functions are not yet filtered to those changed by a commit.

## Local setup (PowerShell)

Use Python 3.11 or newer. From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m reviewbot
```

Activation is optional: these commands use the virtual environment directly.
The bot does not require Ollama to run its scaffold. We will configure Ollama
when implementing the model client.

## Files and learning order

1. `src/reviewbot/models.py`: shared records for changed functions and findings.
2. `src/reviewbot/python_context.py`: parse Python with `ast`; locate functions,
   imports, direct calls, and relevant tests. Start with simple direct calls.
3. `src/reviewbot/git_changes.py`: read a base/head diff and changed line ranges.
4. `src/reviewbot/context.py`: assemble a bounded review packet from changes,
   callers, tests, and old/new source.
5. `src/reviewbot/config.py`: explicit local model settings and limits.
6. `src/reviewbot/llm.py`: call local Ollama and validate the response.
7. `src/reviewbot/report.py`: format findings, evidence, and limitations.
8. `src/reviewbot/pipeline.py`: connect these steps.
9. `src/reviewbot/__main__.py`: replace the starter message with CLI arguments.
10. `src/reviewbot/test_runner.py`: compare test results in controlled base/head
    environments; later investigate generated regression tests.
11. `src/reviewbot/secrets.py`: integrate a secret scanner with redacted results.

Write behavioral tests in `tests/` as each component is implemented. Keep
small source examples in `tests/fixtures/`. These are tests of the bot itself;
running a target repository's tests is a separate feature.

Run the bot's tests with:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Planned review flow

Base/head commits -> changed functions -> relevant context -> AI concerns
-> optional test evidence -> report.

Start with a controlled Python demo repository using pytest. Report AI concerns
as unverified unless supported by execution evidence. A test that passes on the
base and fails on the head demonstrates changed behavior, which may be intended.
Never describe a partial or failed review as proof that the changes are safe.

## Later milestones

- GitHub App, webhook validation, background queue, and updated PR comments.
- Duplicate delivery handling and protection against stale review results.
- Evaluation on regressions and harmless changes, compared with diff-only review.
- Another language implementation after the Python workflow is reliable.

Keep Python parsing separate from the pipeline so another language can supply
its own parser and test runner. Avoid building a generic plugin system yet.

## Test execution boundary

Do not execute arbitrary downloaded repository code on the host. The future
test runner needs an isolated environment, explicit dependency setup, limits,
and no access to bot credentials. The scaffold executes no target code.
