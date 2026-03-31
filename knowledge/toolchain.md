# Toolchain

Development tooling and dependency management for pyramid-rollers.

## Overview

The project uses **uv** for dependency management and virtual environments, **nox** (with the uv backend) for running the test matrix, and **ruff** for linting/formatting.

## Design Decisions

- **uv over pip/virtualenv**: uv manages the lockfile (`uv.lock`), virtual environment (`.venv`), and dependency resolution in one tool.
- **`[dependency-groups]` over `[project.optional-dependencies]`**: Dev dependencies live in `[dependency-groups] dev` (PEP 735) so `uv sync --dev` installs them directly. The old `[project.optional-dependencies] dev` extra required `--extra dev` with uv.
- **nox over tox**: nox uses plain Python for session definitions, and its `uv` venv backend delegates environment creation to uv. This avoids maintaining a separate `tox.ini` with its own dependency specs.
- **setuptools as build backend**: The build backend remains `setuptools` — uv only manages deps and envs, not the build itself.

## Key Commands

| Command | Purpose |
|---|---|
| `uv sync --dev` | Install all deps (including dev group) and create `.venv` |
| `uv run nox` | Run the full test matrix (marshmallow 3 + marshmallow 4) |
| `uv run ruff check .` | Run the linter |

## Test Matrix

Defined in `noxfile.py`. Two parametrized sessions:

- `tests(marshmallow='marshmallow3')` — installs `marshmallow>=3.13,<4`
- `tests(marshmallow='marshmallow4')` — installs `marshmallow>=4`

Both sessions install the package from source plus shared test dependencies (`pytest`, `pytest-cache`, `pytest-cov`, `WebTest`).

## Key Learnings / Gotchas

- `uv sync --dev` installs `[dependency-groups] dev`, **not** `[project.optional-dependencies] dev`. These are different PEP standards.
- `uv.lock` must be committed — it pins the full resolution graph for reproducible installs.
