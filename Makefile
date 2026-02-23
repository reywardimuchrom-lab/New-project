.PHONY: help install install-dev install-tools check-tools test lint format clean build docs

help:
	@echo "APK Decompiler CLI - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install              Install Python dependencies"
	@echo "  make install-dev          Install Python dependencies with dev tools"
	@echo "  make install-tools        Install external tools (apktool, jadx, aapt, adb)"
	@echo "  make setup                Complete setup (Python + external tools)"
	@echo ""
	@echo "Verification:"
	@echo "  make check-tools          Verify all external tools are installed"
	@echo "  make check-python         Verify Python version"
	@echo ""
	@echo "Development:"
	@echo "  make test                 Run unit tests"
	@echo "  make lint                 Run linters (flake8, pylint, mypy)"
	@echo "  make format               Format code with black and isort"
	@echo "  make format-check         Check code formatting without changes"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean                Remove build artifacts and cache"
	@echo "  make clean-all            Remove all generated files and venv"
	@echo ""

check-python:
	@python3 --version
	@python3 -c "import sys; assert sys.version_info >= (3, 9), 'Python 3.9+ required'; print('✓ Python version is 3.9 or higher')"

install: check-python
	@echo "Installing Python dependencies..."
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

install-dev: install
	@echo "Installing development dependencies..."
	pip install -e ".[dev]"

install-tools:
	@echo "Installing external tools..."
	@./scripts/install_tools.sh

setup: check-python install install-dev install-tools check-tools

check-tools:
	@echo "Checking external tools..."
	@./scripts/check_tools.sh

test:
	pytest -v --cov=apk_decompiler --cov-report=term-plus

lint:
	flake8 apk_decompiler tests
	pylint apk_decompiler
	mypy apk_decompiler

format:
	black apk_decompiler tests
	isort apk_decompiler tests

format-check:
	black --check apk_decompiler tests
	isort --check-only apk_decompiler tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/

clean-all: clean
	rm -rf venv/
	rm -rf env/
	rm -f .env
