#!/usr/bin/env python3
"""
Setup validation script for APK Decompiler CLI
This script validates that the environment is properly configured
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import importlib.util

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_success(message):
    """Print a success message"""
    print(f"✓ {message}")

def print_warning(message):
    """Print a warning message"""
    print(f"⚠ {message}")

def print_error(message):
    """Print an error message"""
    print(f"✗ {message}")

def print_info(message):
    """Print an info message"""
    print(f"ℹ {message}")

def check_python_version():
    """Check Python version compatibility"""
    print_header("Python Version Check")
    
    version = sys.version_info
    print_info(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print_success("Python version is compatible (3.9+ required)")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} is not supported (3.9+ required)")
        return False

def check_system_tools():
    """Check for required system tools"""
    print_header("System Tools Check")
    
    tools = {
        'git': 'Git version control',
        'wget': 'Wget download utility',
        'curl': 'Curl HTTP client',
        'unzip': 'Unzip utility'
    }
    
    all_found = True
    for tool, description in tools.items():
        try:
            result = subprocess.run(['which', tool], capture_output=True, text=True)
            if result.returncode == 0:
                print_success(f"{tool} - {description}")
            else:
                print_error(f"{tool} - {description} (NOT FOUND)")
                all_found = False
        except FileNotFoundError:
            print_error(f"{tool} - {description} (NOT FOUND)")
            all_found = False
    
    return all_found

def check_java():
    """Check Java installation"""
    print_header("Java Installation Check")
    
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            java_version = result.stderr.split('\n')[0]
            print_success(f"Java found: {java_version}")
            
            # Check JAVA_HOME
            java_home = os.environ.get('JAVA_HOME')
            if java_home:
                print_info(f"JAVA_HOME: {java_home}")
                if Path(java_home).exists():
                    print_success("JAVA_HOME directory exists")
                else:
                    print_warning("JAVA_HOME directory does not exist")
            else:
                print_warning("JAVA_HOME is not set")
            
            return True
        else:
            print_error("Java is installed but not working")
            return False
    except FileNotFoundError:
        print_error("Java is not installed")
        return False

def check_project_files():
    """Check for required project files"""
    print_header("Project Files Check")
    
    required_files = [
        'requirements.txt',
        'pyproject.toml', 
        '.env.example',
        '.gitignore',
        'Makefile',
        'README.md'
    ]
    
    required_dirs = [
        'src',
        'scripts',
        'tests'
    ]
    
    all_good = True
    
    # Check files
    for file in required_files:
        if Path(file).exists():
            print_success(f"{file} exists")
        else:
            print_error(f"{file} is missing")
            all_good = False
    
    # Check directories
    for dir in required_dirs:
        if Path(dir).is_dir():
            print_success(f"{dir}/ directory exists")
        else:
            print_warning(f"{dir}/ directory does not exist")
    
    return all_good

def check_python_dependencies():
    """Check if Python dependencies can be imported"""
    print_header("Python Dependencies Check")
    
    # List of required dependencies
    dependencies = [
        'click',
        'colorama', 
        'tqdm',
        'yaml',
        'requests'
    ]
    
    missing_deps = []
    
    for dep in dependencies:
        try:
            # Special handling for yaml module
            if dep == 'yaml':
                spec = importlib.util.find_spec('yaml')
            else:
                spec = importlib.util.find_spec(dep)
            
            if spec is not None:
                print_success(f"{dep} is available")
            else:
                print_error(f"{dep} is missing")
                missing_deps.append(dep)
        except ImportError:
            print_error(f"{dep} is missing")
            missing_deps.append(dep)
    
    if missing_deps:
        print_info(f"To install missing dependencies: pip install -r requirements.txt")
        return False
    else:
        print_success("All required dependencies are available")
        return True

def check_external_tools():
    """Check for external tools"""
    print_header("External Tools Check")
    
    tools = ['apktool', 'jadx', 'aapt', 'adb']
    
    found_tools = []
    missing_tools = []
    
    for tool in tools:
        try:
            result = subprocess.run(['which', tool], capture_output=True, text=True)
            if result.returncode == 0:
                print_success(f"{tool} is in PATH")
                found_tools.append(tool)
            else:
                print_warning(f"{tool} is not in PATH")
                missing_tools.append(tool)
        except FileNotFoundError:
            print_warning(f"{tool} is not in PATH")
            missing_tools.append(tool)
    
    if missing_tools:
        print_info(f"To install missing tools: make install-tools")
    
    return len(missing_tools) == 0

def check_permissions():
    """Check file permissions"""
    print_header("File Permissions Check")
    
    # Check script permissions
    scripts_dir = Path('scripts')
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob('*.sh'))
        if scripts:
            executable_count = sum(1 for script in scripts if os.access(script, os.X_OK))
            if executable_count == len(scripts):
                print_success(f"All {len(scripts)} scripts are executable")
            else:
                print_warning(f"Only {executable_count}/{len(scripts)} scripts are executable")
                print_info("Run: chmod +x scripts/*.sh")
        else:
            print_info("No scripts found to check")
    
    return True

def test_pip_installation():
    """Test if pip can install packages"""
    print_header("Pip Installation Test")
    
    try:
        # Test if pip can list packages
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_success("pip is working")
            return True
        else:
            print_error("pip is not working properly")
            return False
    except Exception as e:
        print_error(f"pip test failed: {e}")
        return False

def generate_setup_instructions():
    """Generate setup instructions based on what's missing"""
    print_header("Setup Instructions")
    
    instructions = []
    
    # Check Python version
    if sys.version_info < (3, 9):
        instructions.append("- Install Python 3.9 or later")
    
    # Check system tools
    missing_system_tools = []
    for tool in ['git', 'wget', 'curl', 'unzip']:
        try:
            subprocess.run(['which', tool], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            missing_system_tools.append(tool)
    
    if missing_system_tools:
        instructions.append(f"- Install system tools: {', '.join(missing_system_tools)}")
    
    # Check Java
    try:
        subprocess.run(['java', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        instructions.append("- Install Java 11 or later")
    
    # Check Python dependencies
    missing_deps = []
    for dep in ['click', 'colorama', 'tqdm', 'yaml', 'requests']:
        if importlib.util.find_spec(dep) is None:
            missing_deps.append(dep)
    
    if missing_deps:
        instructions.append("- Install Python dependencies: pip install -r requirements.txt")
    
    # Check external tools
    missing_tools = []
    for tool in ['apktool', 'jadx', 'aapt', 'adb']:
        try:
            subprocess.run(['which', tool], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            missing_tools.append(tool)
    
    if missing_tools:
        instructions.append("- Install external tools: make install-tools")
    
    # Check environment file
    if not Path('.env').exists() and Path('.env.example').exists():
        instructions.append("- Copy environment file: cp .env.example .env")
    
    if instructions:
        print_info("Complete the setup with these commands:")
        for instruction in instructions:
            print_info(instruction)
    else:
        print_success("Your environment appears to be properly configured!")
    
    return len(instructions) == 0

def main():
    """Main validation function"""
    print_header("APK Decompiler CLI - Environment Validation")
    print_info(f"Platform: {platform.system()} {platform.release()}")
    print_info(f"Architecture: {platform.machine()}")
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("System Tools", check_system_tools), 
        ("Java Installation", check_java),
        ("Project Files", check_project_files),
        ("Python Dependencies", check_python_dependencies),
        ("External Tools", check_external_tools),
        ("File Permissions", check_permissions),
        ("Pip Installation", test_pip_installation)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"{name} check failed: {e}")
            results.append((name, False))
    
    # Generate setup instructions
    all_configured = generate_setup_instructions()
    
    # Final summary
    print_header("Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print_info(f"Checks passed: {passed}/{total}")
    
    if all_configured and passed == total:
        print_success("Environment is fully configured and ready!")
        return 0
    else:
        print_warning("Environment needs some configuration")
        print_info("Follow the setup instructions above")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)