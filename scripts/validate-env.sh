#!/bin/bash

# APK Decompiler CLI - Environment Validation Script
# Comprehensive validation of the development environment

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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
    echo -e "${CYAN}=== $1 ===${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get Python path
get_python_path() {
    python3 -c "import sys; print(sys.executable)" 2>/dev/null || echo "python3"
}

# Validate Python installation
validate_python() {
    log_header "Python Installation"
    
    if ! command_exists python3; then
        log_error "Python 3 is not installed"
        return 1
    fi
    
    PYTHON_PATH=$(get_python_path)
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)
    
    log_info "Python path: $PYTHON_PATH"
    log_info "Python version: $PYTHON_VERSION"
    
    if [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -ge 9 ]]; then
        log_success "Python version is compatible (3.9+ required)"
        return 0
    else
        log_error "Python version $PYTHON_VERSION is not supported (3.9+ required)"
        return 1
    fi
}

# Validate Java installation
validate_java() {
    log_header "Java Installation"
    
    if ! command_exists java; then
        log_error "Java is not installed"
        return 1
    fi
    
    JAVA_VERSION=$(java -version 2>&1 | head -n1)
    JAVA_HOME_SET=false
    
    if [[ -n "$JAVA_HOME" ]]; then
        log_info "JAVA_HOME is set to: $JAVA_HOME"
        JAVA_HOME_SET=true
    else
        log_warning "JAVA_HOME is not set"
    fi
    
    log_info "$JAVA_VERSION"
    
    # Test Java functionality
    if java -version >/dev/null 2>&1; then
        log_success "Java is working properly"
        
        # Check Java version requirement
        JAVA_VERSION_NUMBER=$(java -version 2>&1 | head -n1 | cut -d'"' -f2 | cut -d'.' -f1)
        if [[ "$JAVA_VERSION_NUMBER" -ge 11 ]]; then
            log_success "Java version meets requirements (11+)"
        else
            log_warning "Java version might be too old (11+ recommended)"
        fi
        return 0
    else
        log_error "Java is not working properly"
        return 1
    fi
}

# Validate system tools
validate_system_tools() {
    log_header "System Tools"
    
    local tools=("wget" "curl" "unzip" "git")
    local missing=()
    
    for tool in "${tools[@]}"; do
        if command_exists "$tool"; then
            log_success "$tool is installed"
        else
            log_error "$tool is missing"
            missing+=("$tool")
        fi
    done
    
    if [[ ${#missing[@]} -eq 0 ]]; then
        return 0
    else
        log_error "Missing system tools: ${missing[*]}"
        return 1
    fi
}

# Validate Python package management
validate_pip() {
    log_header "Python Package Management"
    
    if ! command_exists pip3; then
        log_error "pip3 is not installed"
        return 1
    fi
    
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    log_info "pip version: $PIP_VERSION"
    
    # Check if pip can install packages
    if pip3 install --dry-run click >/dev/null 2>&1; then
        log_success "pip can install packages"
        return 0
    else
        log_error "pip cannot install packages (permission issue?)"
        return 1
    fi
}

# Validate environment configuration
validate_environment_config() {
    log_header "Environment Configuration"
    
    # Check if .env.example exists
    if [[ -f ".env.example" ]]; then
        log_success ".env.example exists"
    else
        log_warning ".env.example is missing"
    fi
    
    # Check if .env exists
    if [[ -f ".env" ]]; then
        log_success ".env file exists"
        
        # Check for common issues in .env
        if grep -q "DEBUG.*true" .env 2>/dev/null; then
            log_warning "Debug mode is enabled in .env"
        fi
        
        if grep -q "PATH.*=.*" .env 2>/dev/null; then
            log_info "Custom PATH configuration found"
        fi
    else
        log_info ".env file does not exist (will be created from .env.example)"
    fi
    
    # Check file permissions
    local scripts_dir="scripts"
    if [[ -d "$scripts_dir" ]]; then
        local executable_scripts=$(find "$scripts_dir" -name "*.sh" -executable | wc -l)
        local total_scripts=$(find "$scripts_dir" -name "*.sh" | wc -l)
        
        if [[ $executable_scripts -eq $total_scripts ]] && [[ $total_scripts -gt 0 ]]; then
            log_success "All scripts in $scripts_dir are executable"
        else
            log_warning "Some scripts in $scripts_dir are not executable"
        fi
    fi
    
    return 0
}

# Validate project structure
validate_project_structure() {
    log_header "Project Structure"
    
    local required_files=(
        "requirements.txt"
        "pyproject.toml"
        ".gitignore"
        "Makefile"
        ".env.example"
    )
    
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [[ -f "$file" ]]; then
            log_success "$file exists"
        else
            log_error "$file is missing"
            missing_files+=("$file")
        fi
    done
    
    # Check directory structure
    local required_dirs=("src" "tests" "scripts")
    
    for dir in "${required_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            log_success "$dir/ directory exists"
        else
            log_warning "$dir/ directory does not exist"
        fi
    done
    
    if [[ ${#missing_files[@]} -eq 0 ]]; then
        return 0
    else
        log_error "Missing required files: ${missing_files[*]}"
        return 1
    fi
}

# Validate virtual environment
validate_virtual_env() {
    log_header "Virtual Environment"
    
    if [[ -n "$VIRTUAL_ENV" ]]; then
        log_success "Virtual environment is active: $VIRTUAL_ENV"
        
        # Check if we're in the project directory
        if [[ "$VIRTUAL_ENV" == *"/.venv" ]] || [[ "$VIRTUAL_ENV" == *"/venv" ]]; then
            log_info "Using project virtual environment"
        else
            log_warning "Using system-wide or non-project virtual environment"
        fi
    else
        log_info "No virtual environment active (this is OK for global installations)"
    fi
    
    return 0
}

# Generate environment report
generate_report() {
    log_header "Environment Report"
    
    local report_file="environment-report.txt"
    
    {
        echo "APK Decompiler CLI - Environment Report"
        echo "Generated on: $(date)"
        echo "========================================"
        echo
        
        echo "System Information:"
        echo "OS: $(uname -s)"
        echo "Architecture: $(uname -m)"
        echo "Kernel: $(uname -r)"
        echo
        
        echo "Python Information:"
        python3 --version 2>/dev/null || echo "Python 3: Not found"
        which python3 2>/dev/null || echo "Python 3 path: Not found"
        echo "pip version: $(pip3 --version 2>/dev/null || echo 'Not found')"
        echo
        
        echo "Java Information:"
        java -version 2>&1 | head -n1 || echo "Java: Not found"
        echo "JAVA_HOME: ${JAVA_HOME:-Not set}"
        echo
        
        echo "Environment Variables:"
        echo "PATH: $PATH"
        echo "ANDROID_HOME: ${ANDROID_HOME:-Not set}"
        echo "VIRTUAL_ENV: ${VIRTUAL_ENV:-Not set}"
        echo
        
        echo "Installed Tools:"
        echo "apktool: $(command -v apktool 2>/dev/null || echo 'Not found')"
        echo "jadx: $(command -v jadx 2>/dev/null || echo 'Not found')"
        echo "aapt: $(command -v aapt 2>/dev/null || echo 'Not found')"
        echo "adb: $(command -v adb 2>/dev/null || echo 'Not found')"
        echo
        
        echo "Project Configuration Files:"
        for file in requirements.txt pyproject.toml .gitignore .env.example Makefile; do
            if [[ -f "$file" ]]; then
                echo "$file: Present"
            else
                echo "$file: Missing"
            fi
        done
        
    } > "$report_file"
    
    log_success "Environment report saved to: $report_file"
}

# Main validation function
main() {
    log_info "Starting comprehensive environment validation..."
    echo
    
    local exit_code=0
    
    # Run all validations
    validate_python || exit_code=1
    echo
    
    validate_java || exit_code=1
    echo
    
    validate_system_tools || exit_code=1
    echo
    
    validate_pip || exit_code=1
    echo
    
    validate_environment_config
    echo
    
    validate_project_structure || exit_code=1
    echo
    
    validate_virtual_env
    echo
    
    # Generate report
    generate_report
    echo
    
    # Summary
    log_header "Summary"
    if [[ $exit_code -eq 0 ]]; then
        log_success "Environment validation completed successfully!"
        log_info "Your environment is properly configured for APK decompilation."
    else
        log_error "Environment validation found issues!"
        log_info "Please address the errors above before proceeding."
    fi
    
    return $exit_code
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --report-only)
            generate_report
            exit 0
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --report-only    Generate environment report only"
            echo "  --help, -h       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
    shift
done

# Run main function
main "$@"