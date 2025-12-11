# Contributing to APK Decompiler CLI

Thank you for your interest in contributing to the APK Decompiler CLI project! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Code Style](#code-style)
7. [Commit Messages](#commit-messages)
8. [Pull Request Process](#pull-request-process)
9. [Reporting Issues](#reporting-issues)

## Code of Conduct

Please be respectful and professional when interacting with other contributors. We are committed to providing a welcoming and inclusive environment.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or fix
4. Make your changes
5. Submit a pull request

## Development Setup

### Prerequisites

Ensure you have all system requirements installed:
- Python 3.9+
- Java JDK 8+
- Git
- External tools (APKTool, JADX, ADB, AAPT)

See [SETUP.md](SETUP.md) for detailed installation instructions.

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/apk-decompiler-cli.git
cd apk-decompiler-cli

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make install-dev
# Or: pip install -e ".[dev]"

# Verify setup
make check-tools
```

## Making Changes

### Branch Naming Convention

Use descriptive branch names:
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions

Examples:
- `feature/add-batch-processing`
- `fix/resolve-jadx-timeout`
- `docs/update-api-reference`

### Code Organization

The project structure:

```
apk_decompiler/
├── cli.py              # CLI commands and entry point
├── core/               # Core functionality
│   ├── decompiler.py
│   ├── analyzer.py
│   └── extractor.py
├── tools/              # External tool wrappers
│   ├── apktool.py
│   ├── jadx.py
│   └── adb.py
├── models/             # Data models and types
├── utils/              # Utility functions
└── __init__.py
```

### Creating New Features

1. Create a new branch from `main`
2. Add your code following the project structure
3. Add corresponding tests in `tests/`
4. Update documentation as needed
5. Ensure all tests pass
6. Submit a pull request

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_decompiler.py

# Run with coverage
pytest --cov=apk_decompiler --cov-report=html

# Run specific test
pytest tests/test_decompiler.py::TestDecompiler::test_decompile
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test names: `test_feature_does_something`
- Use fixtures for common setup

Example:

```python
import pytest
from apk_decompiler.core import Decompiler

@pytest.fixture
def decompiler():
    return Decompiler()

def test_decompile_valid_apk(decompiler, tmp_path):
    """Test decompiling a valid APK file."""
    # Test implementation
    assert decompiler.decompile("test.apk", tmp_path)

def test_decompile_invalid_file(decompiler):
    """Test handling of invalid APK files."""
    with pytest.raises(ValueError):
        decompiler.decompile("invalid.txt")
```

### Test Coverage

- Aim for at least 80% code coverage
- All public APIs should have tests
- Test both success and failure cases

## Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some additional conventions:

- Line length: 100 characters (set in `pyproject.toml`)
- Use type hints for all function arguments and returns
- Use meaningful variable names

### Tools

```bash
# Format code with black and isort
make format

# Check formatting without changes
make format-check

# Run linters
make lint
```

### Code Style Examples

```python
# ✅ Good
def decompile_apk(
    apk_path: str,
    output_dir: str,
    timeout: int = 600
) -> Dict[str, Any]:
    """
    Decompile an APK file.
    
    Args:
        apk_path: Path to the APK file
        output_dir: Directory for output files
        timeout: Decompilation timeout in seconds
    
    Returns:
        Dictionary with decompilation results
    
    Raises:
        FileNotFoundError: If APK file not found
        ValueError: If APK is invalid
    """
    # Implementation
    pass

# ❌ Avoid
def decompile(ap, out):
    #do decompile
    pass
```

### Import Organization

```python
# Standard library
import json
import subprocess
from pathlib import Path
from typing import Dict, Any

# Third-party
import click
from pydantic import BaseModel

# Local
from apk_decompiler.core import Decompiler
from apk_decompiler.utils import logger
```

### Docstring Format

Use Google-style docstrings:

```python
def analyze_manifest(apk_path: str) -> Dict[str, Any]:
    """
    Analyze Android manifest file from APK.
    
    Args:
        apk_path: Path to the APK file to analyze
    
    Returns:
        Dictionary containing manifest information with keys:
            - package: Package name
            - permissions: List of required permissions
            - activities: List of activities
            - services: List of services
    
    Raises:
        FileNotFoundError: If APK file does not exist
        ValueError: If manifest cannot be parsed
    
    Example:
        >>> manifest = analyze_manifest('app.apk')
        >>> print(manifest['package'])
        'com.example.app'
    """
    pass
```

## Commit Messages

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `test`: Adding or updating tests
- `chore`: Build, dependencies, tooling

### Examples

```
feat(decompiler): add batch processing support

Implement parallel decompilation for multiple APKs.
Supports concurrent processing with configurable worker count.

Fixes #123
```

```
fix(jadx): handle timeout errors gracefully

Previously, timeout errors would crash the entire decompilation.
Now catches timeout and logs a warning message.

Fixes #456
```

```
docs(setup): add troubleshooting guide for Windows
```

### Rules

- Use imperative mood ("add feature" not "added feature")
- Don't capitalize subject line
- Limit subject to 50 characters
- Reference issues in footer: `Fixes #123`, `Closes #456`
- Keep commits atomic and focused

## Pull Request Process

### Before Submitting

1. Update your fork with latest changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Ensure all tests pass:
   ```bash
   make test
   ```

3. Check code quality:
   ```bash
   make lint
   make format-check
   ```

4. Update documentation if needed

### Submitting a Pull Request

1. Push your branch to your fork
2. Open a pull request on GitHub
3. Fill in the PR template completely:
   - Clear description of changes
   - Reference related issues
   - List any breaking changes
   - Add testing notes

### Pull Request Guidelines

- Keep PRs focused and reasonably sized (aim for <400 lines)
- Link to related issues: `Fixes #123`
- Add tests for new features
- Update documentation
- Ensure CI passes
- Be responsive to review feedback

### Review Process

- At least one approval required before merging
- All CI checks must pass
- Address all review comments
- Squash commits if requested

## Reporting Issues

### Before Opening an Issue

- Check existing issues to avoid duplicates
- Review [SETUP.md](SETUP.md) troubleshooting section
- Gather relevant information

### Issue Template

```markdown
### Description
Brief description of the issue

### Steps to Reproduce
1. Step one
2. Step two
3. Step three

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Environment
- OS: (e.g., Ubuntu 20.04)
- Python: (output of `python3 --version`)
- APKTool version: (output of `apktool --version`)
- JADX version: (output of `jadx --version`)

### Error Messages
```
Paste any error messages or logs here
```

### Additional Context
Any other relevant information
```

### Issue Labels

- `bug` - Report bugs
- `enhancement` - Suggest improvements
- `documentation` - Documentation issues
- `help wanted` - Help needed
- `good first issue` - For new contributors

## Development Commands

```bash
# Install dependencies
make install            # Python only
make install-dev        # With development tools
make install-tools      # External tools only

# Verification
make check-tools        # Verify all dependencies
make check-python       # Check Python version

# Testing
make test               # Run tests with coverage

# Code Quality
make lint               # Run linters
make format             # Format code
make format-check       # Check formatting

# Cleanup
make clean              # Clean build artifacts
make clean-all          # Full cleanup including venv
```

## Documentation

### Updating Docs

- Keep documentation up-to-date with code changes
- Use clear, concise language
- Include examples where helpful
- Link to relevant sections

### Documentation Files

- `README.md` - Project overview and quick start
- `SETUP.md` - Installation and setup guide
- `CONTRIBUTING.md` - This file
- Inline code comments for complex logic
- Type hints for function signatures

## Getting Help

- Join our discussions on GitHub
- Ask questions in issue comments
- Check existing documentation
- Review similar code in the project

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- CONTRIBUTORS.md file (coming soon)
- Release notes for significant contributions

## Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

## Questions?

Feel free to:
- Open a GitHub Discussion
- Ask in issue comments
- Email the project maintainers

---

Thank you for contributing to APK Decompiler CLI! 🎉
