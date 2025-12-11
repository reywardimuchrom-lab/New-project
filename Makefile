# APK Decompiler CLI - Makefile

.PHONY: help install install-dev install-tools setup setup-dev test test-unit test-integration lint format type-check clean clean-all verify-deps setup-os-deps validate-environment

# Default target
help:
	@echo "APK Decompiler CLI - Available targets:"
	@echo ""
	@echo "Setup and Installation:"
	@echo "  install          - Install Python dependencies only"
	@echo "  install-dev      - Install with development dependencies"
	@echo "  install-tools    - Install external tools (apktool, jadx, aapt, adb)"
	@echo "  setup            - Complete setup (dependencies + tools)"
	@echo "  setup-dev        - Complete development setup"
	@echo "  setup-os-deps    - Install OS-specific dependencies"
	@echo ""
	@echo "Tool verification:"
	@echo "  verify-deps      - Verify all dependencies are installed"
	@echo "  validate-environment - Validate environment setup"
	@echo ""
	@echo "Development:"
	@echo "  test             - Run all tests"
	@echo "  test-unit        - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  lint             - Run linting checks"
	@echo "  format           - Format code with black and isort"
	@echo "  type-check       - Run type checking with mypy"
	@echo "  check            - Run all checks (lint, type-check, tests)"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean            - Clean temporary files"
	@echo "  clean-all        - Clean all generated files and dependencies"
	@echo "  update-tools     - Update external tools to latest versions"
	@echo ""

# Installation targets
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

install-dev:
	@echo "Installing development dependencies..."
	pip install -e .[dev]

install-tools:
	@echo "Installing external tools..."
	@bash scripts/install-tools.sh

setup: install install-tools
	@echo "Setup completed successfully!"

setup-dev: install-dev install-tools
	@echo "Development setup completed successfully!"

# OS-specific setup
setup-os-deps:
	@echo "Setting up OS-specific dependencies..."
	@if command -v apt-get >/dev/null 2>&1; then \
		echo "Detected Debian/Ubuntu - installing system dependencies..."; \
		sudo apt-get update && sudo apt-get install -y \
			openjdk-11-jdk \
			wget \
			curl \
			unzip \
			build-essential; \
	elif command -v brew >/dev/null 2>&1; then \
		echo "Detected macOS - installing system dependencies..."; \
		brew install openjdk@11 wget curl; \
	elif command -v yum >/dev/null 2>&1; then \
		echo "Detected RHEL/CentOS - installing system dependencies..."; \
		sudo yum install -y java-11-openjdk-devel wget curl unzip gcc; \
	else \
		echo "Unknown package manager. Please install Java 11+, wget, curl, and build tools manually."; \
	fi

# Verification targets
verify-deps:
	@echo "Verifying Python dependencies..."
	@python -c "import click, colorama, tqdm, yaml" && echo "✓ Python dependencies OK" || echo "✗ Python dependencies missing"
	@echo "Verifying external tools..."
	@bash scripts/verify-tools.sh

validate-environment:
	@echo "Validating environment..."
	@bash scripts/validate-env.sh

# Development targets
test: test-unit test-integration

test-unit:
	@echo "Running unit tests..."
	pytest tests/unit/ -v

test-integration:
	@echo "Running integration tests..."
	pytest tests/integration/ -v --slow

lint:
	@echo "Running linting checks..."
	flake8 src/ tests/
	@echo "Linting completed!"

format:
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/
	@echo "Code formatting completed!"

type-check:
	@echo "Running type checks..."
	mypy src/
	@echo "Type checking completed!"

check: lint type-check test
	@echo "All checks passed!"

# Maintenance targets
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/
	@echo "Clean completed!"

clean-all: clean
	@echo "Removing virtual environment..."
	@if [ -d "venv" ]; then rm -rf venv; fi
	@if [ -d ".venv" ]; then rm -rf .venv; fi
	@echo "Clean all completed!"

update-tools:
	@echo "Updating external tools..."
	@bash scripts/update-tools.sh

# Convenience target for quick setup
quick-setup:
	@echo "Performing quick setup..."
	@bash scripts/quick-setup.sh