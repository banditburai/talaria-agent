# Phase 1: Foundation & Core Structure - Implementation Plan

> **Epic:** `talaria-agent-wzj`
> **Design:** `docs/designs/2026-03-07-phase-1-foundation.md`
> **For Claude:** Use `skills/collaboration/execute-plan-with-beads` to implement.

## Tasks Overview

| ID | Task | Description | Blocked By |
|----|------|-------------|------------|
| 1 | Namespace Setup | Create root namespace and directory structure | - |
| 2 | Meta-Package | Create talaria-agent pyproject.toml | 1 |
| 3 | Core Package | Create talaria-core pyproject.toml and src structure | 1 |
| 4 | Root Config | Update root pyproject.toml for development | 2, 3 |
| 5 | CI/CD Pipeline | Create GitHub Actions workflow | 4 |
| 6 | Test Scaffold | Set up pytest and initial test | 4 |
| 7 | Type Check Config | Configure mypy | 4 |
| 8 | Lint Config | Configure ruff | 4 |
| 9 | Verify Build | Test that package builds and imports work | 5, 6, 7, 8 |

---

## Task Details

### Task 1: Namespace Setup (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task - surfaces when task closes)
**Blocked by:** None

**Files:**
- Create: `talaria/__init__.py` (empty namespace marker)
- Create: `talaria/talaria-agent/__init__.py` (empty)
- Create: `talaria/talaria-core/__init__.py` (empty)
- Delete: `main.py` (old scaffold)

**Step 1: Create directories**
```bash
mkdir -p talaria/talaria-agent
mkdir -p talaria/talaria-core
touch talaria/__init__.py
touch talaria/talaria-agent/__init__.py
touch talaria/talaria-core/__init__.py
rm -f main.py
```

**Step 2: Verify namespace**
```bash
python -c "import talaria; print('Namespace works!')"
```

**Step 3: Commit**
```bash
git add -A && git commit -m "chore: add namespace package structure"
```

---

### Task 2: Meta-Package (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task)
**Blocked by:** 1

**Files:**
- Create: `talaria/talaria-agent/pyproject.toml`

**Step 1: Write pyproject.toml**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "talaria-agent"
version = "0.1.0"
description = "A modular AI agent system with optional messaging integrations."
readme = "README.md"
requires-python = ">=3.11"

dependencies = [
    "talaria-core>=0.1.0",
]

[project.optional-dependencies]
gateway = ["talaria-gateway>=0.1.0"]
telegram = ["talaria-telegram>=0.1.0"]
discord = ["talaria-discord>=0.1.0"]
skills = ["talaria-skills>=0.1.0"]
rl = ["talaria-rl>=0.1.0"]
full = [
    "talaria-gateway>=0.1.0",
    "talaria-telegram>=0.1.0",
    "talaria-discord>=0.1.0",
    "talaria-skills>=0.1.0",
    "talaria-rl>=0.1.0",
]

[project.scripts]
talaria = "talaria.core.cli:main"
```

**Step 2: Verify meta-package**
```bash
# Should not install (no code), but validate TOML
python -c "import tomllib; tomllib.load(open('talaria/talaria-agent/pyproject.toml', 'rb'))"
```

**Step 3: Commit**
```bash
git add talaria/talaria-agent/pyproject.toml && git commit -m "feat: add talaria-agent meta-package"
```

---

### Task 3: Core Package (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task)
**Blocked by:** 1

**Files:**
- Create: `talaria/talaria-core/pyproject.toml`
- Create: `talaria/talaria-core/src/talaria/__init__.py`

**Step 1: Write pyproject.toml**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "talaria-core"
version = "0.1.0"
description = "Core agent and CLI for Talaria."
readme = "README.md"
requires-python = ">=3.11"

dependencies = [
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0.0",
    "rich>=13.0.0",
    "prompt-toolkit>=3.0.0",
    "httpx>=0.25.0",
    "tenacity>=8.0.0",
    "jinja2>=3.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "hypothesis>=6.0.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/talaria"]

[tool.hatch.build.targets.sdist]
include = ["src/"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --strict-markers --tb=short"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]
```

**Step 2: Create src structure**
```bash
mkdir -p talaria/talaria-core/src/talaria
touch talaria/talaria-core/src/talaria/__init__.py
```

**Step 3: Add minimal exports**
```python
# talaria/talaria-core/src/talaria/__init__.py
"""Talaria - A modular AI agent system."""

__version__ = "0.1.0"
```

**Step 4: Commit**
```bash
git add -A && git commit -m "feat: add talaria-core package"
```

---

### Task 4: Root Config (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task)
**Blocked by:** 2, 3

**Files:**
- Modify: `pyproject.toml`

**Step 1: Update root pyproject.toml**
```toml
[project]
name = "talaria"
version = "0.1.0"
description = "Talaria - A modular AI agent system"
requires-python = ">=3.11"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
```

**Step 2: Sync with uv**
```bash
uv sync --all-extras
```

**Step 3: Commit**
```bash
git add pyproject.toml && git commit -m "chore: configure root pyproject.toml"
```

---

### Task 5: CI/CD Pipeline (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task)
**Blocked by:** 4

**Files:**
- Create: `.github/workflows/ci.yml`

**Step 1: Create workflow**
```bash
mkdir -p .github/workflows
```

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
          
      - name: Install dependencies
        run: uv sync --all-extras
        
      - name: Lint
        run: uv run ruff check src/
        
      - name: Type check
        run: uv run mypy src/
        
      - name: Test
        run: uv run pytest --cov=src --cov-report=term-missing
```

**Step 2: Commit**
```bash
git add .github/ && git commit -m "ci: add GitHub Actions workflow"
```

---

### Task 6: Test Scaffold (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task)
**Blocked by:** 4

**Files:**
- Create: `talaria/talaria-core/tests/test_core.py`

**Step 1: Create tests directory and file**
```bash
mkdir -p talaria/talaria-core/tests
touch talaria/talaria-core/tests/__init__.py
touch talaria/talaria-core/tests/test_core.py
```

**Step 2: Write test**
```python
"""Tests for talaria-core."""

def test_version():
    """Test version is defined."""
    from talaria import __version__
    assert __version__ == "0.1.0"


def test_namespace_import():
    """Test namespace package works."""
    import talaria
    assert hasattr(talaria, "__version__")
```

**Step 3: Run test**
```bash
uv run pytest talaria/talaria-core/tests/ -v
```

**Step 4: Commit**
```bash
git add talaria/talaria-core/tests/ && git commit -m "test: add test scaffold"
```

---

### Task 7: Type Check Config (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task)
**Blocked by:** 4

**Files:**
- Create: `mypy.ini` or add to pyproject.toml

**Step 1: Verify mypy works**
```bash
uv run mypy talaria/talaria-core/src/
```

**Step 2: Fix any issues (should be clean with empty init)**

**Step 3: Commit**
```bash
git commit -m "chore: verify type checking works"
```

---

### Task 8: Lint Config (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task)
**Blocked by:** 4

**Step 1: Run ruff**
```bash
uv run ruff check talaria/
```

**Step 2: Fix any issues**

**Step 3: Commit**
```bash
git commit -m "chore: verify linting works"
```

---

### Task 9: Verify Build (`bd-xxx`)

**Review:** `bd-xxx` (P1, blocked by this task)
**Blocked by:** 5, 6, 7, 8

**Step 1: Verify imports work**
```bash
python -c "from talaria import Agent; print('Import works!')"
```

**Step 2: Verify CLI script defined**
```bash
uv run talaria --help
```

**Step 3: Final commit**
```bash
git commit -m "feat: Phase 1 complete - namespace structure ready"
```

---

## Dependencies Summary

```
Task 1 (Namespace) → Task 2, 3
Task 2 (Meta-pkg) → Task 4
Task 3 (Core pkg) → Task 4
Task 4 (Root) → Tasks 5, 6, 7, 8
Tasks 5,6,7,8 → Task 9 (Final verification)
```
