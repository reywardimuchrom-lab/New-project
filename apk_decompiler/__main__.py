"""Entry point for APK Decompiler CLI when run as a module."""

import sys
from apk_decompiler.cli import main

if __name__ == "__main__":
    sys.exit(main())
