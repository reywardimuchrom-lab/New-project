"""
APK Decompiler CLI

A comprehensive command-line tool for decompiling APK files using multiple 
decompilation engines including apktool, jadx, aapt, and adb.

This package provides a unified interface for various APK analysis tools
and batch processing capabilities.
"""

__version__ = "0.1.0"
__author__ = "Development Team"
__email__ = "dev@example.com"
__description__ = "A comprehensive CLI tool for decompiling APK files using multiple decompilers"

# Import main components for convenience
from apk_decompiler.cli import main
from apk_decompiler.core.decompiler import Decompiler
from apk_decompiler.config.settings import Settings

__all__ = [
    "main",
    "Decompiler", 
    "Settings",
    "__version__",
]