#!/bin/bash

# APK Decompiler CLI - Tool Verification Script
# Verifies that all required tools are properly installed

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verify Python version
verify_python() {
    log_info "Verifying Python installation..."
    
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

# Verify Java
verify_java() {
    log_info "Verifying Java installation..."
    
    if ! command_exists java; then
        log_error "Java is not installed"
        return 1
    fi
    
    JAVA_VERSION=$(java -version 2>&1 | head -n1 | cut -d'"' -f2 | cut -d'.' -f1)
    
    if [[ "$JAVA_VERSION" -ge 11 ]]; then
        log_success "Java $(java -version 2>&1 | head -n1 | cut -d'"' -f2) (compatible)"
        return 0
    else
        log_error "Java version too old (found: $(java -version 2>&1 | head -n1))"
        return 1
    fi
}

# Verify Python dependencies
verify_python_deps() {
    log_info "Verifying Python dependencies..."
    
    local missing_deps=()
    
    # List of required dependencies
    local deps=("click" "colorama" "tqdm" "yaml" "requests")
    
    for dep in "${deps[@]}"; do
        if python3 -c "import $dep" 2>/dev/null; then
            log_success "$dep is installed"
        else
            log_error "$dep is missing"
            missing_deps+=("$dep")
        fi
    done
    
    if [[ ${#missing_deps[@]} -eq 0 ]]; then
        return 0
    else
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Run 'make install' to install dependencies"
        return 1
    fi
}

# Verify apktool
verify_apktool() {
    log_info "Verifying apktool..."
    
    if ! command_exists apktool; then
        log_error "apktool is not in PATH"
        
        # Check common installation locations
        local possible_paths=(
            "$HOME/.local/bin/apktool"
            "/usr/local/bin/apktool"
            "/usr/bin/apktool"
        )
        
        for path in "${possible_paths[@]}"; do
            if [[ -f "$path" ]]; then
                log_info "Found apktool at: $path"
                log_info "Add $(dirname "$path") to your PATH"
                break
            fi
        done
        return 1
    fi
    
    # Test apktool
    if apktool --version >/dev/null 2>&1; then
        APKTOOL_VERSION=$(apktool --version 2>/dev/null | head -n1 || echo "unknown")
        log_success "apktool is working ($APKTOOL_VERSION)"
        return 0
    else
        log_error "apktool is installed but not working properly"
        return 1
    fi
}

# Verify jadx
verify_jadx() {
    log_info "Verifying jadx..."
    
    if ! command_exists jadx; then
        log_error "jadx is not in PATH"
        
        # Check common installation locations
        local possible_paths=(
            "$HOME/.local/bin/jadx"
            "/usr/local/bin/jadx"
            "/usr/bin/jadx"
        )
        
        for path in "${possible_paths[@]}"; do
            if [[ -f "$path" ]]; then
                log_info "Found jadx at: $path"
                log_info "Add $(dirname "$path") to your PATH"
                break
            fi
        done
        return 1
    fi
    
    # Test jadx
    if jadx --help >/dev/null 2>&1; then
        log_success "jadx is working"
        return 0
    else
        log_error "jadx is installed but not working properly"
        return 1
    fi
}

# Verify Android tools (aapt, adb)
verify_android_tools() {
    log_info "Verifying Android tools..."
    
    local all_good=true
    
    # Check aapt
    if command_exists aapt; then
        log_success "aapt is in PATH"
    else
        log_warning "aapt is not in PATH"
        
        # Check Android SDK locations
        if [[ -n "$ANDROID_HOME" ]]; then
            local aapt_paths=(
                "$ANDROID_HOME/build-tools"/*/aapt
                "$ANDROID_HOME/build-tools"/*/aapt2
            )
            
            for path in "${aapt_paths[@]}"; do
                if [[ -f "$path" ]]; then
                    log_info "Found aapt at: $path"
                    log_info "Add $(dirname "$path") to your PATH"
                    break
                fi
            done
        fi
        all_good=false
    fi
    
    # Check adb
    if command_exists adb; then
        log_success "adb is in PATH"
    else
        log_warning "adb is not in PATH"
        
        # Check Android SDK locations
        if [[ -n "$ANDROID_HOME" ]]; then
            local adb_path="$ANDROID_HOME/platform-tools/adb"
            if [[ -f "$adb_path" ]]; then
                log_info "Found adb at: $adb_path"
                log_info "Add $(dirname "$adb_path") to your PATH"
            fi
        fi
        all_good=false
    fi
    
    return $([[ $all_good == true ]] && echo 0 || echo 1)
}

# Main verification function
main() {
    log_info "Starting dependency verification..."
    echo
    
    local exit_code=0
    
    # Verify core requirements
    echo "=== Core Requirements ==="
    if ! verify_python; then
        exit_code=1
    fi
    
    if ! verify_java; then
        exit_code=1
    fi
    echo
    
    # Verify Python dependencies
    echo "=== Python Dependencies ==="
    if ! verify_python_deps; then
        exit_code=1
    fi
    echo
    
    # Verify external tools
    echo "=== External Tools ==="
    if ! verify_apktool; then
        exit_code=1
    fi
    
    if ! verify_jadx; then
        exit_code=1
    fi
    
    if ! verify_android_tools; then
        log_warning "Some Android tools are missing"
        log_info "Android tools are optional but recommended for full functionality"
    fi
    echo
    
    # Summary
    if [[ $exit_code -eq 0 ]]; then
        log_success "All required dependencies are installed and working!"
    else
        log_error "Some dependencies are missing or not working properly"
        log_info "Run 'make install-tools' to install external tools"
    fi
    
    exit $exit_code
}

# Run main function
main "$@"