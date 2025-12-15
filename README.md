# APK Decompiler & Android WebView Wrapper Generator

A Python-based tool for decompiling and analyzing Android APK files, with capabilities to generate Android WebView wrapper applications.

## Features

### APK Decompiler
- Input validation for APK files
- Dependency checking for external tools
- Configurable logging with verbose mode
- Clean CLI interface using Click

### Android WebView Wrapper Generator
- Generate production-ready Android WebView wrapper projects
- Customizable package name, app name, and target URL
- Advanced WebView settings (JavaScript, DOM storage, caching, file access)
- Offline support with intelligent caching and fallback screens
- Custom user agent configuration
- Automatic icon generation for all densities (mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi)
- ProGuard configuration for release builds
- Targets API 21+ (Android 5.0+)
- Command-line buildable with Gradle wrapper included

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd apk-decompiler
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install external dependencies (optional but recommended):
   - **apktool**: APK reverse engineering tool
   - **jadx**: Dex to Java decompiler
   - **adb**: Android Debug Bridge
   - **aapt**: Android Asset Packaging Tool

## Usage

### APK Decompiler

Basic usage:
```bash
python decompiler.py <path_to_apk>
```

With custom output directory:
```bash
python decompiler.py <path_to_apk> --output-dir /path/to/output
```

With verbose logging:
```bash
python decompiler.py <path_to_apk> --verbose
```

Show help:
```bash
python decompiler.py --help
```

### Android WebView Wrapper Generator

Generate a basic wrapper:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App"
```

Generate with custom icon:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --icon ./icon.png
```

Generate with advanced options:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --icon ./icon.png \
  --user-agent "CustomAgent/1.0" \
  --offline \
  --file-access \
  --permission android.permission.CAMERA \
  --permission android.permission.ACCESS_FINE_LOCATION \
  --output-dir ./my_android_app \
  --verbose
```

Build the generated project:
```bash
cd my_android_app
./gradlew assembleDebug  # For debug build
./gradlew assembleRelease  # For release build
```

The generated APK will be in `app/build/outputs/apk/`

## Project Structure

```
.
├── decompiler.py           # APK decompiler CLI entry point
├── wrapper_generator.py    # Wrapper generator CLI entry point
├── apk_decompiler/         # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # APK decompiler CLI
│   ├── wrapper_cli.py      # Wrapper generator CLI
│   ├── template_manager.py # Template management and generation
│   ├── validator.py        # Input validation
│   ├── dependency_checker.py  # External dependency checking
│   └── logger.py           # Logging configuration
├── templates/              # Project templates
│   └── android_wrapper/    # Android WebView wrapper template
│       ├── app/            # Android app module
│       ├── gradle/         # Gradle wrapper
│       ├── build.gradle    # Root build script
│       ├── settings.gradle # Gradle settings
│       └── gradlew         # Gradle wrapper script
├── tests/                  # Unit and integration tests
├── requirements.txt        # Python dependencies
└── .gitignore             # Git ignore rules
```

## Requirements

- Python 3.7+
- See `requirements.txt` for Python package dependencies

## Development Status

### APK Decompiler
- ✅ Input validation
- ✅ Dependency checking
- ✅ Logging infrastructure
- ⏳ Actual decompilation (coming soon)

### Android WebView Wrapper Generator
- ✅ Template-based project generation
- ✅ Customizable package names and app names
- ✅ Advanced WebView configuration
- ✅ Offline support with caching
- ✅ Icon generation for all densities
- ✅ ProGuard configuration
- ✅ Unit and integration tests

## License

TBD
