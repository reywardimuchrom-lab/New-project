#!/bin/bash

# APK Decompiler CLI - Quick Setup Script
# Automated setup for rapid deployment

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_header() {
    echo -e "${PURPLE}=== $1 ===${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "Linux";;
        Darwin*)    echo "macOS";;
        CYGWIN*)    echo "Windows";;
        MINGW*)     echo "Windows";;
        MSYS*)      echo "Windows";;
        *)          echo "Unknown";;
    esac
}

# Check Python version
check_python_version() {
    log_info "Checking Python version..."
    
    if ! command_exists python3; then
        log_error "Python 3 is not installed"
        return 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)
    
    if [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -ge 9 ]]; then
        log_success "Python $PYTHON_VERSION (compatible)"
        return 0
    else
        log_error "Python $PYTHON_VERSION found, but 3.9+ is required"
        return 1
    fi
}

# Create virtual environment
create_virtual_env() {
    log_info "Creating virtual environment..."
    
    if [[ -d ".venv" ]]; then
        log_warning "Virtual environment already exists"
        return 0
    fi
    
    python3 -m venv .venv
    source .venv/bin/activate
    
    log_success "Virtual environment created and activated"
    log_info "To activate manually: source .venv/bin/activate"
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    source .venv/bin/activate
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install dependencies
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        log_success "Python dependencies installed"
    else
        log_warning "requirements.txt not found"
        return 1
    fi
    
    # Install development dependencies if dev mode
    if [[ "$DEV_MODE" == "true" ]]; then
        if [[ -f "pyproject.toml" ]]; then
            pip install -e .[dev]
            log_success "Development dependencies installed"
        fi
    fi
}

# Install external tools
install_external_tools() {
    log_info "Installing external tools..."
    
    if [[ -f "scripts/install-tools.sh" ]]; then
        bash scripts/install-tools.sh
        log_success "External tools installation completed"
    else
        log_error "install-tools.sh script not found"
        return 1
    fi
}

# Setup environment file
setup_env_file() {
    log_info "Setting up environment file..."
    
    if [[ -f ".env.example" ]]; then
        if [[ ! -f ".env" ]]; then
            cp .env.example .env
            log_success ".env file created from .env.example"
            log_info "Please review and customize .env file as needed"
        else
            log_warning ".env file already exists"
        fi
    else
        log_warning ".env.example not found"
    fi
}

# Install system dependencies
install_system_deps() {
    log_info "Installing system dependencies..."
    
    OS=$(detect_os)
    
    case $OS in
        Linux)
            if command_exists apt-get; then
                log_info "Installing dependencies via apt..."
                sudo apt-get update
                sudo apt-get install -y \
                    openjdk-11-jdk \
                    wget \
                    curl \
                    unzip \
                    git \
                    build-essential
            elif command_exists yum; then
                log_info "Installing dependencies via yum..."
                sudo yum install -y \
                    java-11-openjdk-devel \
                    wget \
                    curl \
                    unzip \
                    git \
                    gcc
            else
                log_warning "Unknown Linux distribution. Please install Java 11+, wget, curl, unzip, git manually."
            fi
            ;;
        macOS)
            if command_exists brew; then
                log_info "Installing dependencies via Homebrew..."
                brew install openjdk@11 wget curl git
            else
                log_error "Homebrew not found. Please install dependencies manually."
                log_info "Required: Java 11+, wget, curl, git"
                return 1
            fi
            ;;
        Windows)
            log_info "Windows detected. Please install the following manually:"
            log_info "- Java 11 or later (from Oracle or OpenJDK)"
            log_info "- Git for Windows"
            log_info "- Windows Subsystem for Linux (recommended)"
            return 1
            ;;
        *)
            log_error "Unknown operating system"
            return 1
            ;;
    esac
    
    log_success "System dependencies installation completed"
}

# Make scripts executable
make_scripts_executable() {
    log_info "Making scripts executable..."
    
    if [[ -d "scripts" ]]; then
        find scripts/ -name "*.sh" -exec chmod +x {} \;
        log_success "Scripts are now executable"
    else
        log_warning "scripts directory not found"
    fi
}

# Run verification
run_verification() {
    log_info "Running environment verification..."
    
    if [[ -f "scripts/verify-tools.sh" ]]; then
        if bash scripts/verify-tools.sh; then
            log_success "Environment verification passed"
        else
            log_warning "Environment verification found some issues"
            log_info "Please review the output above"
        fi
    else
        log_warning "verify-tools.sh script not found"
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating project directories..."
    
    local directories=(
        "src"
        "tests"
        "tests/unit"
        "tests/integration"
        "decompiled"
        "temp"
        "cache"
        "logs"
    )
    
    for dir in "${directories[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            log_info "Created directory: $dir"
        fi
    done
    
    log_success "Directory structure created"
}

# Display final instructions
show_final_instructions() {
    log_header "Setup Complete!"
    
    echo
    log_success "APK Decompiler CLI setup completed successfully!"
    echo
    
    echo "Next steps:"
    echo "1. Activate the virtual environment: source .venv/bin/activate"
    echo "2. Review the .env file and customize as needed"
    echo "3. Add external tools to your PATH:"
    echo "   export PATH=\"\$PATH:\$HOME/.local/bin\""
    echo "4. Test the installation: apk-decompiler --help"
    echo
    
    echo "Available commands:"
    echo "- make help           Show all available commands"
    echo "- make test           Run tests"
    echo "- make verify-deps    Verify all dependencies"
    echo "- make update-tools   Update external tools"
    echo
    
    if [[ "$DEV_MODE" == "true" ]]; then
        echo "Development mode is enabled."
        echo "Additional commands available:"
        echo "- make lint           Run linting"
        echo "- make format         Format code"
        echo "- make type-check     Run type checking"
        echo
    fi
    
    echo "For troubleshooting, see README.md or run:"
    echo "- make validate-environment   Validate environment setup"
    echo
}

# Parse command line arguments
DEV_MODE=false
SKIP_TOOLS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dev)
            DEV_MODE=true
            shift
            ;;
        --skip-tools)
            SKIP_TOOLS=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --dev          Enable development mode (install dev dependencies)"
            echo "  --skip-tools   Skip external tools installation"
            echo "  --help, -h     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Main setup function
main() {
    log_header "APK Decompiler CLI Quick Setup"
    
    echo "This script will set up a complete development environment for APK decompilation."
    echo "Python 3.9+, Java 11+, and system tools will be installed as needed."
    echo
    
    # Check prerequisites
    log_header "Checking Prerequisites"
    check_python_version || exit 1
    
    # Create directory structure
    create_directories
    
    # Install system dependencies
    install_system_deps || log_warning "Some system dependencies may be missing"
    
    # Create virtual environment
    create_virtual_env
    
    # Install Python dependencies
    install_python_deps
    
    # Setup environment file
    setup_env_file
    
    # Make scripts executable
    make_scripts_executable
    
    # Install external tools (unless skipped)
    if [[ "$SKIP_TOOLS" != true ]]; then
        install_external_tools || log_warning "External tools installation failed"
    else
        log_info "Skipping external tools installation (--skip-tools specified)"
    fi
    
    # Run verification
    run_verification
    
    # Show final instructions
    show_final_instructions
}

# Run main function
main "$@"