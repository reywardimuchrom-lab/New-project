# Web2APK

A Python-based tool for converting websites to Android APK applications.

## Features

- Convert any website to an Android APK application
- Configuration-based build system (YAML or JSON)
- Strict validation for package naming, permissions, and assets
- Support for app icons, splash screens, and custom settings
- Offline/cache configuration
- APK signing support
- Clean CLI interface using Click
- Comprehensive logging with verbose mode

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd web2apk
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install external dependencies:
   - **Java JDK 8+**: Required for Android build tools
   - **Android SDK**: Download from [Android Studio](https://developer.android.com/studio)
   - **Gradle**: Build automation tool (or use gradlew)
   - Set environment variables:
     - `ANDROID_HOME` or `ANDROID_SDK_ROOT`: Path to Android SDK

## Usage

### Generate a Sample Configuration

Create a sample configuration file to get started:

```bash
# Generate YAML config (default)
python web2apk.py init-config

# Generate JSON config
python web2apk.py init-config --format json

# Specify custom output path
python web2apk.py init-config --format yaml --output myapp.yml
```

### Build an APK

Build an APK from your website using a configuration file:

```bash
# Basic build
python web2apk.py build --config config.yml

# Custom output directory
python web2apk.py build --config config.yml --output ./build

# Skip asset validation (not recommended)
python web2apk.py build --config config.yml --skip-validation
```

### Enable Verbose Logging

Add the `--verbose` or `-v` flag to any command:

```bash
python web2apk.py --verbose build --config config.yml
python web2apk.py -v init-config
```

### Get Help

```bash
# General help
python web2apk.py --help

# Command-specific help
python web2apk.py build --help
python web2apk.py init-config --help
```

## Configuration File

The configuration file defines all settings for your web app conversion. Here's an example:

```yaml
# Website to convert
url: https://example.com

# App metadata
app_name: My Web App
package_id: com.example.mywebapp
version_name: 1.0.0
version_code: 1

# Android permissions
permissions:
  - android.permission.INTERNET
  - android.permission.ACCESS_NETWORK_STATE

# App icons (different densities)
icons:
  mdpi: assets/icon-mdpi.png
  hdpi: assets/icon-hdpi.png
  xhdpi: assets/icon-xhdpi.png
  xxhdpi: assets/icon-xxhdpi.png
  xxxhdpi: assets/icon-xxxhdpi.png

# Splash screen
splash:
  image: assets/splash.png
  background_color: '#FFFFFF'
  duration_ms: 2000

# Build configuration
build_variant: release  # or 'debug'

# APK signing (for release builds)
signing:
  keystore_path: path/to/keystore.jks
  keystore_password: your_keystore_password
  key_alias: your_key_alias
  key_password: your_key_password

# Offline and caching
cache:
  enable_offline: true
  cache_size_mb: 50
  cache_strategy: default

# App settings
orientation: portrait  # portrait, landscape, or unspecified
theme_color: '#2196F3'
user_agent: Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36
```

### Configuration Fields

#### Required Fields
- `url`: Website URL to convert (must start with http:// or https://)
- `app_name`: Application name (1-50 characters)
- `package_id`: Android package identifier (e.g., com.example.app)

#### Optional Fields
- `version_name`: Version string (default: "1.0.0")
- `version_code`: Version integer (default: 1)
- `permissions`: List of Android permissions (validated against allowed list)
- `icons`: Icon files for different screen densities
- `splash`: Splash screen configuration
- `build_variant`: "debug" or "release" (default: "release")
- `signing`: APK signing configuration
- `cache`: Offline and caching settings
- `orientation`: "portrait", "landscape", or "unspecified" (default: "portrait")
- `theme_color`: Primary theme color for the app
- `user_agent`: Custom user agent string for WebView

### Allowed Permissions

For security, only the following permissions are allowed:
- `android.permission.INTERNET`
- `android.permission.ACCESS_NETWORK_STATE`
- `android.permission.ACCESS_WIFI_STATE`
- `android.permission.WRITE_EXTERNAL_STORAGE`
- `android.permission.READ_EXTERNAL_STORAGE`
- `android.permission.CAMERA`
- `android.permission.ACCESS_FINE_LOCATION`
- `android.permission.ACCESS_COARSE_LOCATION`
- `android.permission.RECORD_AUDIO`
- `android.permission.VIBRATE`
- `android.permission.WAKE_LOCK`

## Project Structure

```
.
├── web2apk.py              # Main CLI entry point
├── web2apk/                # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # CLI commands (build, init-config)
│   ├── config_loader.py    # Configuration loading and validation
│   ├── validators.py       # Input validation
│   ├── dependency_checker.py  # External dependency checking
│   └── logger.py           # Logging configuration
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_config_loader.py
│   └── test_validators.py
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Requirements

### Python Requirements
- Python 3.7+
- See `requirements.txt` for package dependencies

### External Dependencies
- Java JDK 8 or higher
- Android SDK with build-tools
- Gradle or Gradlew
- zipalign (included in Android SDK)
- apksigner (included in Android SDK)

## Development

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_validators
python -m unittest tests.test_config_loader

# Run with verbose output
python -m unittest discover tests -v
```

### Development Status

This is an active development project focused on:
- ✅ Configuration system (YAML/JSON)
- ✅ Input validation
- ✅ Dependency checking
- ✅ CLI interface
- ✅ Unit tests
- ⏳ Actual APK building (coming soon)
- ⏳ WebView integration (coming soon)
- ⏳ Asset processing (coming soon)

## License

TBD
