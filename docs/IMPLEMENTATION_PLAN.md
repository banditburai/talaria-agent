# Talaria Agent - Implementation Plan

**Version**: 0.1.0  
**Date**: March 2026  
**Status**: Planning

---

## Project Overview

**Name**: Talaria  
**PyPI Name**: `talaria-agent` (meta-package)  
**Python Namespace**: `talaria`  
**Approach**: Namespace packages with TDD throughout

---

## Architecture

### Package Structure

```
talaria/                          # Root namespace (empty dir with __init__.py)
│
├── talaria-agent/               # Meta-package (PyPI: talaria-agent)
│   └── pyproject.toml          # Routes to sub-packages
│
├── talaria-core/               # Core agent (PyPI: talaria-core)
│   ├── pyproject.toml
│   └── src/talaria/
│       ├── __init__.py        # Exports: Agent, run, tools
│       ├── run_agent.py       # Main entry point
│       ├── agent/             # Agent internals
│       │   ├── __init__.py
│       │   ├── loop.py       # Agent loop logic
│       │   ├── executor.py    # Tool execution
│       │   ├── prompts.py    # Prompt building
│       │   └── state.py      # Session state
│       ├── tools/            # Core tools
│       │   ├── __init__.py
│       │   ├── registry.py   # Tool registry
│       │   ├── terminal.py   # Terminal tool
│       │   ├── file.py       # File tools
│       │   ├── todo.py       # Todo tool
│       │   └── memory.py     # Memory tool
│       └── cli/             # CLI
│           ├── __init__.py
│           ├── main.py
│           ├── config.py
│           └── setup.py
│
├── talaria-gateway/            # Messaging gateway (PyPI: talaria-gateway)
│   ├── pyproject.toml
│   └── src/talaria/
│       └── gateway/
│           ├── __init__.py
│           ├── run.py
│           ├── session.py
│           ├── hooks.py
│           └── platforms/
│
├── talaria-telegram/           # Telegram (PyPI: talaria-telegram)
│   ├── pyproject.toml
│   └── src/talaria/
│       └── gateway/
│           └── telegram/
│
├── talaria-discord/           # Discord (PyPI: talaria-discord)
│   └── ...
│
├── talaria-skills/            # Skills system (PyPI: talaria-skills)
│   └── ...
│
└── talaria-rl/               # RL/training (PyPI: talaria-rl)
    └── ...
```

### Namespace & PyPI Mapping

| PyPI Name | Python Import | Purpose |
|-----------|--------------|---------|
| talaria-agent | - | Meta-package (routes to others) |
| talaria-core | talaria.core | Agent + CLI |
| talaria-gateway | talaria.gateway | Messaging gateway |
| talaria-telegram | talaria.gateway.telegram | Telegram adapter |
| talaria-discord | talaria.gateway.discord | Discord adapter |
| talaria-skills | talaria.skills | Skills system |
| talaria-rl | talaria.rl | RL/training |

### Installation Variants

```bash
# Minimal - agent + CLI only
pip install talaria-agent

# With messaging gateway
pip install talaria-agent[gateway]

# Full Telegram bot
pip install talaria-agent[telegram]

# Full Discord bot
pip install talaria-agent[discord]

# Everything
pip install talaria-agent[full]
```

---

## Phase Breakdown

### Phase 1: Foundation & Core Structure

**Duration**: Weeks 1-2  
**Goal**: Establish namespace, CI/CD, and core package structure

| Task | Description | Test Focus |
|------|-------------|------------|
| 1.1 | Create namespace root `talaria/` | Verify namespace works |
| 1.2 | Create talaria-agent meta-package | Test meta-package routing |
| 1.3 | Create talaria-core scaffold | Test package builds |
| 1.4 | Set up pytest + CI | Test discovery works |
| 1.5 | Configure mypy/pyright | Type checking setup |
| 1.6 | Add pre-commit hooks | Lint/format enforcement |

**Deliverables**:
- `talaria/` namespace root
- `talaria-agent` meta-package with pyproject.toml
- `talaria-core` scaffold with tests
- CI pipeline (GitHub Actions)

---

### Phase 2: Tool Registry & Core Tools

**Duration**: Weeks 2-4  
**Goal**: Implement tool system with TDD

| Task | Description | Test Focus |
|------|-------------|------------|
| 2.1 | Implement `tools/registry.py` | Test tool registration |
| 2.2 | Implement `tools/registry.py` - dispatch | Test tool dispatch |
| 2.3 | Implement terminal tool | Test command execution |
| 2.4 | Implement file tools | Test read/write/patch |
| 2.5 | Implement todo tool | Test task management |
| 2.6 | Implement memory tool | Test session memory |
| 2.7 | Tool availability checks | Test conditional loading |

**Test Files to Create**:
```
tests/
├── unit/
│   ├── tools/
│   │   ├── test_registry.py
│   │   ├── test_terminal.py
│   │   ├── test_file.py
│   │   ├── test_todo.py
│   │   └── test_memory.py
│   └── conftest.py
├── fixtures/
│   └── sample_files/
└── pyproject.toml
```

---

### Phase 3: Agent Loop

**Duration**: Weeks 4-6  
**Goal**: Implement core agent with TDD

| Task | Description | Test Focus |
|------|-------------|------------|
| 3.1 | Extract agent/ package structure | Module tests |
| 3.2 | Implement agent loop (loop.py) | Test conversation flow |
| 3.3 | Implement tool executor (executor.py) | Test tool execution |
| 3.4 | Implement prompt builder (prompts.py) | Test prompt assembly |
| 3.5 | Implement session state (state.py) | Test state management |
| 3.6 | Integrate with tools | Integration tests |
| 3.7 | Context compression | Test compression |

**Test Files**:
```
tests/
├── unit/
│   └── agent/
│       ├── test_loop.py
│       ├── test_executor.py
│       ├── test_prompts.py
│       └── test_state.py
├── integration/
│   └── agent/
│       ├── test_conversation.py
│       └── test_tool_calling.py
└── fixtures/
    └── conversations/
```

---

### Phase 4: CLI

**Duration**: Weeks 6-7  
**Goal**: Interactive CLI with TDD

| Task | Description | Test Focus |
|------|-------------|------------|
| 4.1 | CLI entry point | Test CLI invocation |
| 4.2 | Config loading | Test config parsing |
| 4.3 | Setup wizard | Test interactive prompts |
| 4.4 | Slash commands | Test command parsing |
| 4.5 | Rich output | Test formatting |
| 4.6 | prompt_toolkit integration | Test input handling |

---

### Phase 5: Plugin System

**Duration**: Weeks 7-8  
**Goal**: Dynamic plugin discovery via entry points

| Task | Description | Test Focus |
|------|-------------|------------|
| 5.1 | Define entry points spec | - |
| 5.2 | Plugin registry | Test discovery |
| 5.3 | Tool plugin base | Test tool plugins |
| 5.4 | CLI command plugins | Test command plugins |
| 5.5 | Platform adapter plugins | Test platform plugins |

---

### Phase 6: Gateway Package

**Duration**: Weeks 8-10  
**Goal**: Extract gateway to separate package

| Task | Description | Test Focus |
|------|-------------|------------|
| 6.1 | Create talaria-gateway package | Package tests |
| 6.2 | Implement session management | Test sessions |
| 6.3 | Implement event hooks | Test hook system |
| 6.4 | Implement delivery | Test message delivery |
| 6.5 | Integration with core | Test gateway-core |

---

### Phase 7: Platform Adapters

**Duration**: Weeks 10-12  
**Goal**: Individual platform packages

| Task | Description |
|------|-------------|
| 7.1 | talaria-telegram package |
| 7.2 | talaria-discord package |
| 7.3 | talaria-slack package |
| 7.4 | talaria-whatsapp package |

---

### Phase 8: Skills Package

**Duration**: Weeks 12-13  
**Goal**: Skills system as optional package

| Task | Description |
|------|-------------|
| 8.1 | Create talaria-skills package |
| 8.2 | Progressive disclosure |
| 8.3 | Skills hub |
| 8.4 | Security scanning |

---

### Phase 9: RL Package

**Duration**: Weeks 13-14  
**Goal**: RL/training as optional package

| Task | Description |
|------|-------------|
| 9.1 | Create talaria-rl package |
| 9.2 | Environment registry |
| 9.3 | Training tools |
| 9.4 | Batch runner |

---

### Phase 10: Integration & Polish

**Duration**: Weeks 14-16  
**Goal**: Full integration tests and polish

| Task | Description |
|------|-------------|
| 10.1 | End-to-end tests |
| 10.2 | Performance testing |
| 10.3 | Documentation |
| 10.4 | Release prep |

---

## Technical Stack

### Test Framework

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=src",
    "--cov-report=term-missing",
]
```

**Testing Stack**:
- pytest (framework)
- pytest-asyncio (async tests)
- pytest-cov (coverage)
- pytest-mock (mocking)
- hypothesis (property-based testing)

### Type Checking

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Code Quality

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]
```

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --test
      - run: uv run pytest
      - run: uv run mypy src
      - run: uv run ruff check src
```

---

## Core Tools (Minimal Install)

| Tool | Purpose | Status |
|------|---------|--------|
| terminal | Shell commands | Core |
| file | Read/write/patch | Core |
| todo | Task management | Core |
| memory | Session memory | Core |

**All other tools become optional plugins**.

---

## Meta-Package Configuration

```toml
# talaria-agent/pyproject.toml
[project]
name = "talaria-agent"
version = "0.1.0"
description = "A modular AI agent system with optional messaging integrations."
requires-python = ">=3.11"

dependencies = [
    "talaria-core>=0.1.0"
]

[project.optional-dependencies]
gateway = ["talaria-gateway>=0.1.0"]
telegram = ["talaria-telegram>=0.1.0"]
discord = ["talaria-discord>=0.1.0"]
slack = ["talaria-slack>=0.1.0"]
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
talaria = "talaria.cli:main"
```

---

## Entry Points Configuration

```toml
# talaria-core/pyproject.toml
[project.entry-points.talaria]
core = "talaria:register_core"

[project.entry-points.talaria.tools]
terminal = "talaria.tools.terminal:register"
file = "talaria.tools.file:register"
todo = "talaria.tools.todo:register"
memory = "talaria.tools.memory:register"

# talaria-gateway/pyproject.toml
[project.entry-points.talaria]
gateway = "talaria.gateway:register"

[project.entry-points.talaria.platforms]
telegram = "talaria.gateway.telegram:register"
discord = "talaria.gateway.discord:register"
```

---

## Package Publishing

```toml
# talaria-core/pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "talaria-core"
version = "0.1.0"
readme = "README.md"
requires-python = ">=3.11"

[tool.hatch.build.targets.wheel]
packages = ["src/talaria"]

[tool.hatch.build.targets.sdist]
include = ["src/"]
```

---

## Implementation Order

1. **Phase 1**: Foundation - Set up namespace, CI/CD, testing
2. **Phase 2**: Tools - Registry + 4 core tools
3. **Phase 3**: Agent - Loop, executor, prompts, state
4. **Phase 4**: CLI - Interactive interface
5. **Phase 5**: Plugins - Dynamic discovery
6. **Phase 6**: Gateway - Messaging core
7. **Phase 7**: Platforms - Telegram, Discord, etc.
8. **Phase 8**: Skills - Knowledge system
9. **Phase 9**: RL - Training features
10. **Phase 10**: Polish - Integration tests, release

---

## Notes

- All phases should follow TDD (Test-Driven Development)
- Each package should have >90% test coverage
- Type hints required for all code (strict mypy)
- Pre-commit hooks must pass before merge
- Documentation should be updated with each phase
