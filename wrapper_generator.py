#!/usr/bin/env python3
"""
Android WebView Wrapper Generator - Entry point

Generates Android WebView wrapper projects from templates.
"""

from apk_decompiler.wrapper_cli import generate_wrapper

if __name__ == '__main__':
    generate_wrapper()
