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

## CI / CD

Two GitHub Actions workflows in `.github/workflows/`:

### `ci.yml` — Continuous Integration

- **Triggers:** push to `main`, pull requests to `main`.
- **Lint job:** installs uv, runs `uv run ruff check .`.
- **Test job:** matrix over Python 3.10, 3.11, 3.12, 3.13. Each runs `uv run nox` (which exercises both marshmallow 3 and marshmallow 4 sessions).

### `publish.yml` — Publish to PyPI

- **Trigger:** GitHub release published.
- Uses **PyPI Trusted Publishing** (OIDC) via `pypa/gh-action-pypi-publish`. No API token secrets needed.
- Requires a GitHub environment named `pypi` and a matching trusted publisher configured on PyPI (owner: `tomascorrea`, repo: `pyramid-rollers`, workflow: `publish.yml`, environment: `pypi`).
- Builds sdist + wheel with `python -m build`, then publishes.

## Key Learnings / Gotchas

- `uv sync --dev` installs `[dependency-groups] dev`, **not** `[project.optional-dependencies] dev`. These are different PEP standards.
- `uv.lock` must be committed — it pins the full resolution graph for reproducible installs.
- The publish workflow uses `actions/setup-python` (not `astral-sh/setup-uv`) because it only needs `pip install build` and `python -m build` — no uv-specific features required.
- Trusted publishing requires both the GitHub environment (`pypi`) and the PyPI publisher config to be set up before the first release.
