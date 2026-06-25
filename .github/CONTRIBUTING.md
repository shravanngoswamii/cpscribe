# Contributing

Open an issue before starting non-trivial work so we can discuss the approach.

## Setup

```sh
git clone https://github.com/shravanngoswamii/cpscribe
cd cpscribe
pip install -e ".[dev]"
git config core.hooksPath .githooks
```

## Workflow

- One commit per logical change, concise message in casual tone
- Run `ruff check src/ tests/` and `ruff format src/ tests/` before committing
- Add or update tests for any changed behavior
- Update `CHANGELOG.md` under `[Unreleased]`
