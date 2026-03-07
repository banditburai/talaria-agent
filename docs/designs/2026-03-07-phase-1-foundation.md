# Phase 1: Foundation & Core Structure - Design

**Created:** 2026-03-07
**Status:** Approved
**Epic:** talaria-agent-1a2b3c (to be created)

## Problem Statement

We need to establish the foundational structure for Talaria - a modular, namespace-based Python project with proper testing, CI/CD, and type checking. This phase creates the scaffold that all future phases depend on.

## Solution Overview

Create the namespace package structure, CI/CD pipeline, and testing infrastructure. Establish the multi-package layout with talaria-agent as meta-package routing to talaria-core and future packages.

## Architecture

### Namespace Structure

```
talaria/                          # Root namespace (PEP 420)
│
├── talaria-agent/               # Meta-package (PyPI: talaria-agent)
│   └── pyproject.toml          # Routes to talaria-core
│
├── talaria-core/               # Core package
│   ├── pyproject.toml
│   └── src/talaria/
│       └── __init__.py        # Empty marker for namespace
│
└── (future packages)          # gateway, skills, rl, etc.
```

### Key Components

1. **Namespace Package**: PEP 420 implicit namespace - empty directories with `__init__.py`
2. **Meta-Package**: `talaria-agent` depends on `talaria-core` with optional extras
3. **Core Package**: `talaria-core` contains actual code under `src/talaria/`
4. **Entry Points**: CLI command via `talaria` console script

### Dependency Graph

```
talaria/ (namespace root)
    ↑
talaria-agent/ (meta-package)
    ↑
talaria-core/ (actual code)
```

## Data Flow

- User runs: `pip install talaria-agent`
- pip downloads talaria-agent (meta-package)
- meta-package declares dependency on talaria-core
- pip downloads talaria-core
- Python can import: `from talaria.core import Agent`

## Key Decisions

### 1. Namespace Package vs Regular Package

**Decision:** Use PEP 420 implicit namespace packages

**Rationale:**
- Allows multiple PyPI packages to share `talaria` namespace
- Users install `talaria-core` but import `from talaria import ...`
- Professional standard (used by Flask, Google Cloud, etc.)

### 2. Build System

**Decision:** Use hatchling (from Astral)

**Rationale:**
- Modern, fast
- Well-maintained
- Works well with uv

### 3. Test Framework

**Decision:** pytest with pytest-asyncio

**Rationale:**
- Industry standard
- Good async support needed for agent
- Rich ecosystem

### 4. Type Checking

**Decision:** mypy with strict mode

**Rationale:**
- Catches bugs early
- Required for production code
- Strict mode ensures quality

### 5. Code Quality

**Decision:** ruff

**Rationale:**
- Fast (written in Rust)
- Modern linter
- Replaces flake8, isort, etc.

## Technical Implementation

### talaria-agent/pyproject.toml

```toml
[project]
name = "talaria-agent"
version = "0.1.0"
description = "A modular AI agent system with optional messaging integrations."
requires-python = ">=3.11"
dependencies = [
    "talaria-core>=0.1.0",
]

[project.optional-dependencies]
gateway = ["talaria-gateway>=0.1.0"]
# ... more extras

[project.scripts]
talaria = "talaria.core.cli:main"
```

### talaria-core/pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "talaria-core"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
    "rich>=13.0.0",
    "prompt-toolkit>=3.0.0",
    # ... core deps
]

[project.optional-dependencies]
test = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
]
lint = ["ruff>=0.1.0"]
typecheck = ["mypy>=1.0.0"]

[tool.hatch.build.targets.wheel]
packages = ["src/talaria"]

[tool.hatch.build.targets.sdist]
include = ["src/"]
```

### Directory Layout

```
talaria/
├── talaria-agent/
│   └── pyproject.toml
├── talaria-core/
│   ├── pyproject.toml
│   ├── src/
│   │   └── talaria/
│   │       └── __init__.py  # Empty namespace marker
│   └── tests/
│       └── test_core.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml              # Root (for development)
├── uv.lock
└── README.md
```

### CI/CD Pipeline

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --all-extras
      - run: uv run pytest
      - run: uv run ruff check src/
      - run: uv run mypy src/
```

## Open Questions

1. **Python Version**: Using 3.11+ - should we require 3.12 for better type safety?
2. **Pre-commit**: Should we add pre-commit hooks for linting?
3. **Coverage**: What minimum coverage % should we require?

## Next Steps

→ Create implementation plan with write-plan-with-beads
→ Tasks: Scaffold packages, configure pyproject.toml, set up CI/CD, add tests
