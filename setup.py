#!/usr/bin/env python3
"""Setup script for APK Decompiler CLI."""

from setuptools import setup, find_packages

setup(
    packages=find_packages(include=['apk_decompiler', 'apk_decompiler.*']),
)
