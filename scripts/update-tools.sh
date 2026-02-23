#!/bin/bash

# APK Decompiler CLI - Update External Tools Script
# Updates all external tools to their latest versions

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
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Backup existing installations
backup_existing_tools() {
    log_info "Backing up existing tool installations..."
    
    local backup_dir="$HOME/.local/bin/backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_dir"
    
    local tools=("apktool" "jadx")
    for tool in "${tools[@]}"; do
        local tool_path=$(command -v "$tool" 2>/dev/null)
        if [[ -n "$tool_path" ]]; then
            cp "$tool_path" "$backup_dir/" 2>/dev/null || true
            log_info "Backed up $tool to $backup_dir"
        fi
    done
    
    log_success "Backup completed in $backup_dir"
}

# Update apktool
update_apktool() {
    log_info "Updating apktool..."
    
    if ! command_exists apktool; then
        log_warning "apktool is not installed, skipping update"
        return 0
    fi
    
    # Remove existing installation
    local existing_apktool=$(command -v apktool)
    rm -f "$existing_apktool"
    
    # Reinstall using install script
    bash scripts/install-tools.sh apktool-only
    log_success "apktool updated"
}

# Update jadx
update_jadx() {
    log_info "Updating jadx..."
    
    if ! command_exists jadx; then
        log_warning "jadx is not installed, skipping update"
        return 0
    fi
    
    # Remove existing installation
    local existing_jadx=$(command -v jadx)
    rm -f "$existing_jadx"
    
    # Reinstall using install script
    bash scripts/install-tools.sh jadx-only
    log_success "jadx updated"
}

# Update Android SDK tools
update_android_tools() {
    log_info "Updating Android SDK tools..."
    
    if [[ -z "$ANDROID_HOME" ]]; then
        log_warning "ANDROID_HOME is not set, skipping Android SDK update"
        return 0
    fi
    
    local sdkmanager="$ANDROID_HOME/latest/bin/sdkmanager"
    
    if [[ ! -f "$sdkmanager" ]]; then
        log_warning "Android SDK command line tools not found"
        return 0
    fi
    
    # Update command line tools first
    log_info "Updating Android SDK command line tools..."
    yes | "$sdkmanager" --sdk_root="$ANDROID_HOME" "cmdline-tools;latest"
    
    # Update platform tools and build tools
    log_info "Updating platform tools and build tools..."
    yes | "$sdkmanager" --sdk_root="$ANDROID_HOME" "platform-tools" "build-tools;34.0.0"
    
    log_success "Android SDK tools updated"
}

# Update system package manager installations
update_package_manager_tools() {
    log_info "Checking for package manager installations..."
    
    # Update Homebrew packages (macOS)
    if command_exists brew; then
        log_info "Updating Homebrew packages..."
        brew update
        brew upgrade apktool 2>/dev/null || true
        log_success "Homebrew packages updated"
    fi
    
    # Update apt packages (Linux)
    if command_exists apt-get; then
        log_info "Updating apt packages..."
        sudo apt-get update
        sudo apt-get upgrade -y 2>/dev/null || true
        log_success "apt packages updated"
    fi
    
    # Update yum packages (RHEL/CentOS)
    if command_exists yum; then
        log_info "Updating yum packages..."
        sudo yum update -y 2>/dev/null || true
        log_success "yum packages updated"
    fi
}

# Verify all tools after update
verify_after_update() {
    log_info "Verifying tools after update..."
    
    # Run the verification script
    bash scripts/verify-tools.sh
}

# Clean up temporary files
cleanup() {
    log_info "Cleaning up temporary files..."
    
    # Remove temporary files
    rm -rf /tmp/jadx* /tmp/apktool* 2>/dev/null || true
    
    # Clean package manager caches
    if command_exists brew; then
        brew cleanup 2>/dev/null || true
    fi
    
    if command_exists apt-get; then
        sudo apt-get autoremove -y 2>/dev/null || true
        sudo apt-get autoclean 2>/dev/null || true
    fi
    
    log_success "Cleanup completed"
}

# Main update function
main() {
    log_info "Starting external tools update..."
    
    # Check if running with proper permissions
    if [[ $EUID -eq 0 ]]; then
        log_warning "Running as root. This is not recommended for development tools."
    fi
    
    # Parse command line arguments
    local tools_only=false
    local sdk_only=false
    local verify_only=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --tools-only)
                tools_only=true
                shift
                ;;
            --sdk-only)
                sdk_only=true
                shift
                ;;
            --verify-only)
                verify_only=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [options]"
                echo "Options:"
                echo "  --tools-only    Update only apktool and jadx"
                echo "  --sdk-only      Update only Android SDK tools"
                echo "  --verify-only   Only verify existing installations"
                echo "  --help, -h      Show this help message"
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    # Backup existing tools
    if [[ "$verify_only" != true ]]; then
        backup_existing_tools
    fi
    
    if [[ "$verify_only" == true ]]; then
        verify_after_update
    elif [[ "$sdk_only" == true ]]; then
        update_android_tools
        update_package_manager_tools
    elif [[ "$tools_only" == true ]]; then
        update_apktool
        update_jadx
    else
        # Full update
        update_package_manager_tools
        update_apktool
        update_jadx
        update_android_tools
    fi
    
    # Verify everything is working
    if [[ "$verify_only" != true ]]; then
        verify_after_update
    fi
    
    # Cleanup
    if [[ "$verify_only" != true ]]; then
        cleanup
    fi
    
    log_success "Update process completed!"
}

# Run main function
main "$@"