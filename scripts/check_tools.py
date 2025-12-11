#!/usr/bin/env python3

"""APK Decompiler CLI - Tools and Dependencies Verification Script.

This script checks for all required external tools and Python dependencies.
Can be run on Windows, macOS, and Linux.
"""

import subprocess
import sys
from pathlib import Path
from typing import Tuple, List


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_header(text: str) -> None:
    """Print a section header."""
    print(f"\n{Colors.BLUE}>>> {text}{Colors.NC}")


def print_success(text: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")


def print_warning(text: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.NC}")


def print_error(text: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗ {text}{Colors.NC}")


def command_exists(command: str) -> bool:
    """Check if a command exists in the system PATH."""
    try:
        subprocess.run(
            [command] if sys.platform != "win32" else f"where {command}",
            capture_output=True,
            check=False,
            timeout=2
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_command_version(command: str, *args) -> Tuple[bool, str]:
    """Get the version of a command.
    
    Args:
        command: Command to run
        *args: Arguments to pass to the command
    
    Returns:
        Tuple of (success, version_string)
    """
    try:
        result = subprocess.run(
            [command] + list(args),
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, result.stdout.strip().split('\n')[0]
        return False, result.stderr.strip().split('\n')[0] if result.stderr else ""
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return False, str(e)


def check_python() -> bool:
    """Check Python installation and version.
    
    Returns:
        True if Python 3.9+ is available, False otherwise
    """
    print_header("Python Installation")
    
    major, minor, micro = sys.version_info[:3]
    version = f"{major}.{minor}.{micro}"
    
    if major > 3 or (major == 3 and minor >= 9):
        print_success(f"Python 3.9+ found: {version}")
        return True
    else:
        print_error(f"Python 3.9+ required, found: {version}")
        return False


def check_java() -> bool:
    """Check Java installation.
    
    Returns:
        True if Java is available, False otherwise
    """
    print_header("Java Installation")
    
    if not command_exists("java"):
        print_error("Java not found (required for apktool and jadx)")
        print_warning("Install from: https://www.oracle.com/java/technologies/downloads/")
        return False
    
    success, version = get_command_version("java", "-version")
    if success:
        print_success(f"Java found: {version}")
        return True
    return False


def check_apktool() -> bool:
    """Check APKTool installation.
    
    Returns:
        True if APKTool is available, False otherwise
    """
    print_header("APKTool Installation")
    
    if not command_exists("apktool"):
        print_error("apktool not found")
        print_warning("Install from: https://ibotpeaches.github.io/Apktool/install/")
        return False
    
    success, version = get_command_version("apktool", "--version")
    if success:
        print_success(f"apktool found: {version}")
        return True
    else:
        print_success("apktool found in PATH")
        return True


def check_jadx() -> bool:
    """Check JADX installation.
    
    Returns:
        True if JADX is available, False otherwise
    """
    print_header("JADX Installation")
    
    if not command_exists("jadx"):
        print_error("jadx not found")
        print_warning("Install from: https://github.com/skylot/jadx")
        return False
    
    success, version = get_command_version("jadx", "--version")
    if success:
        print_success(f"jadx found: {version}")
        return True
    else:
        print_success("jadx found in PATH")
        return True


def check_aapt() -> bool:
    """Check AAPT installation (optional).
    
    Returns:
        True if AAPT is available, False otherwise
    """
    print_header("AAPT Installation")
    
    if not command_exists("aapt"):
        print_warning("aapt not found (optional, part of Android SDK)")
        print_warning("Install from: https://developer.android.com/studio/command-line")
        return False
    
    print_success("aapt found in PATH")
    return True


def check_adb() -> bool:
    """Check ADB installation (optional).
    
    Returns:
        True if ADB is available, False otherwise
    """
    print_header("ADB Installation")
    
    if not command_exists("adb"):
        print_warning("adb not found (optional, part of Android SDK)")
        print_warning("Install from: https://developer.android.com/studio/command-line")
        return False
    
    success, version = get_command_version("adb", "version")
    if success:
        print_success(f"adb found: {version}")
        return True
    else:
        print_success("adb found in PATH")
        return True


def check_python_dependencies() -> bool:
    """Check critical Python dependencies.
    
    Returns:
        True if all critical dependencies are installed, False otherwise
    """
    print_header("Python Dependencies")
    
    critical_deps = [
        "click",
        "pydantic",
        "androguard",
    ]
    
    missing = []
    
    for dep in critical_deps:
        try:
            __import__(dep)
            print_success(dep)
        except ImportError:
            print_error(dep)
            missing.append(dep)
    
    if missing:
        print_warning(f"{len(missing)} Python dependencies missing")
        print_warning("Install with: pip install -r requirements.txt")
        return False
    
    print_success("All critical Python dependencies installed")
    return True


def main() -> int:
    """Run all verification checks.
    
    Returns:
        Exit code (0 if successful, 1 if any critical check failed)
    """
    print_header("APK Decompiler CLI - Dependency Check")
    
    # Track results
    results = {
        "Python": check_python(),
        "Java": check_java(),
        "APKTool": check_apktool(),
        "JADX": check_jadx(),
        "AAPT": check_aapt(),
        "ADB": check_adb(),
        "Python Dependencies": check_python_dependencies(),
    }
    
    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    critical_checks = ["Python", "Java", "APKTool", "JADX", "Python Dependencies"]
    critical_failed = any(not results[check] for check in critical_checks)
    
    for check, passed in results.items():
        status = "✓" if passed else "✗"
        color = Colors.GREEN if passed else Colors.RED
        print(f"{color}{status} {check}{Colors.NC}")
    
    print()
    
    if critical_failed:
        print_error("Some critical dependencies are missing or incorrect versions")
        print()
        print("Please follow the installation guide in SETUP.md")
        return 1
    else:
        print_success("All critical dependencies are installed!")
        print()
        print("Environment is ready for development.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
