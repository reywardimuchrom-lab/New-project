# Android WebView Wrapper Generator - User Guide

## Overview

The Android WebView Wrapper Generator is a tool that creates production-ready Android applications that wrap any website in a native WebView. It provides advanced features like offline support, caching, and custom configurations.

## Quick Start

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Verify installation:
```bash
python wrapper_generator.py --help
```

### Basic Usage

Generate a basic wrapper:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App"
```

This creates a folder `android_wrapper` with a complete Android project.

### Building the Generated Project

1. Navigate to the generated project:
```bash
cd android_wrapper
```

2. Build a debug APK:
```bash
./gradlew assembleDebug
```

3. The APK will be in:
```
app/build/outputs/apk/debug/app-debug.apk
```

## Advanced Usage

### Custom Output Directory

Specify where to create the project:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --output-dir ./my_android_app
```

### Adding a Custom Icon

The tool can generate icons for all Android densities from a single source image:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --icon ./icon.png
```

**Icon Requirements:**
- Format: PNG or JPEG
- Recommended size: 512x512 or larger
- Square aspect ratio
- Will be automatically resized to: 48, 72, 96, 144, 192 pixels

### Custom User Agent

Set a custom user agent string:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --user-agent "MyCustomApp/1.0 (Android)"
```

### Offline Support

Enable intelligent caching for offline access:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --offline
```

Disable offline mode:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --no-offline
```

### File Access

Enable file access in the WebView (use with caution):
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --file-access
```

### Additional Permissions

Add extra Android permissions:
```bash
python wrapper_generator.py \
  --url https://example.com \
  --package com.example.myapp \
  --name "My App" \
  --permission android.permission.CAMERA \
  --permission android.permission.ACCESS_FINE_LOCATION \
  --permission android.permission.RECORD_AUDIO
```

### Complete Example

```bash
python wrapper_generator.py \
  --url https://mywebsite.com \
  --package com.mycompany.webwrapper \
  --name "My Website App" \
  --icon ./assets/logo.png \
  --user-agent "MyWebsiteApp/1.0" \
  --offline \
  --permission android.permission.CAMERA \
  --permission android.permission.ACCESS_FINE_LOCATION \
  --output-dir ./MyWebsiteApp \
  --verbose
```

## Features

### WebView Configuration
- ✅ JavaScript enabled
- ✅ DOM storage enabled
- ✅ Web storage (database + localStorage)
- ✅ Intelligent caching
- ✅ Custom user agent
- ✅ Hardware acceleration
- ✅ Zoom controls (hidden UI)
- ✅ Mixed content support

### Offline Support
- ✅ Automatic caching of static resources
- ✅ CSS, JavaScript, images, fonts cached
- ✅ 24-hour cache validity
- ✅ MD5-based cache keys
- ✅ Offline fallback screen
- ✅ Request interception

### UI Features
- ✅ Material Design 3
- ✅ Swipe to refresh
- ✅ Progress bar
- ✅ Offline screen with retry button
- ✅ Back button navigation
- ✅ External link handling

### Build Features
- ✅ Debug and release builds
- ✅ ProGuard optimization
- ✅ Resource shrinking
- ✅ Code minification
- ✅ Gradle wrapper included

## Package Naming

Android package names must follow these rules:
- Start with lowercase letter
- Contain at least one dot
- Use only lowercase letters, numbers, underscores
- Follow reverse domain notation

**Valid Examples:**
- `com.example.myapp`
- `io.github.username`
- `net.mycompany.mobile.app`

**Invalid Examples:**
- `myapp` (no dot)
- `com.Example` (uppercase)
- `Com.example` (uppercase at start)

## Building for Production

### Debug Build

```bash
cd your_android_app
./gradlew assembleDebug
```

**Output:** `app/build/outputs/apk/debug/app-debug.apk`

**Features:**
- Debuggable
- Not optimized
- Larger file size
- For testing only

### Release Build

1. Create a keystore (first time only):
```bash
keytool -genkey -v -keystore my-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias my-key-alias
```

2. Add signing config to `app/build.gradle`:
```gradle
android {
    signingConfigs {
        release {
            storeFile file("../my-release-key.jks")
            storePassword "your_store_password"
            keyAlias "my-key-alias"
            keyPassword "your_key_password"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            // ... existing config
        }
    }
}
```

3. Build release APK:
```bash
./gradlew assembleRelease
```

**Output:** `app/build/outputs/apk/release/app-release.apk`

**Features:**
- ProGuard optimized
- Resources shrunk
- Code minified
- Production-ready
- Smaller file size

## Customization

### Changing the URL

After generation, you can change the URL in `app/build.gradle`:
```gradle
buildConfigField "String", "TARGET_URL", "\"https://newurl.com\""
```

### Modifying WebView Settings

Edit `app/src/main/java/<your_package>/MainActivity.kt`:
```kotlin
private fun setupWebView() {
    webView.apply {
        settings.apply {
            // Modify settings here
            javaScriptEnabled = true
            // ... add more settings
        }
    }
}
```

### Customizing Offline Page

Replace `app/src/main/assets/offline.html` with your custom HTML.

### Adjusting Cache Duration

Edit `app/src/main/java/<your_package>/OfflineHandler.kt`:
```kotlin
private const val MAX_CACHE_AGE_MS = 48 * 60 * 60 * 1000L // 48 hours
```

### Changing Theme Colors

Edit `app/src/main/res/values/themes.xml`:
```xml
<item name="colorPrimary">#6200EE</item>
<item name="colorSecondary">#03DAC5</item>
```

## Troubleshooting

### Build Errors

**Problem:** `Android SDK not found`
```
Solution: Set ANDROID_HOME environment variable:
export ANDROID_HOME=/path/to/android-sdk
```

**Problem:** `Gradle build fails`
```
Solution: Try with --stacktrace for more details:
./gradlew assembleDebug --stacktrace
```

**Problem:** `Out of memory`
```
Solution: Increase Gradle memory in gradle.properties:
org.gradle.jvmargs=-Xmx4096m
```

### Runtime Issues

**Problem:** `Blank white screen`
```
Solution: Check that JavaScript is enabled and URL is correct
Check Android logcat: adb logcat
```

**Problem:** `Certificate errors`
```
Solution: Ensure using HTTPS URLs
For testing, add cleartext traffic to AndroidManifest.xml
```

**Problem:** `App crashes on launch`
```
Solution: Check logcat for errors:
adb logcat | grep -E "AndroidRuntime|YourPackageName"
```

## Testing

### Install to Device

1. Enable USB debugging on Android device
2. Connect device via USB
3. Install app:
```bash
./gradlew installDebug
```

### Using Emulator

1. Start Android emulator
2. Install app:
```bash
./gradlew installDebug
```

### View Logs

```bash
adb logcat | grep WebView
```

## Requirements

### Development Machine
- Python 3.7+
- Pillow (for icon generation)

### Building Android App
- Android SDK (API 21+)
- Java 8 or higher
- Gradle 7.6+ (included via wrapper)

### Target Devices
- Android 5.0 (API 21) or higher
- Internet permission (automatically added)

## Security Best Practices

1. **Use HTTPS**: Always use HTTPS URLs in production
2. **Validate URLs**: Only load trusted domains
3. **Disable File Access**: Unless absolutely necessary
4. **Certificate Pinning**: Consider for sensitive applications
5. **ProGuard**: Always use for release builds
6. **Permissions**: Only request necessary permissions
7. **JavaScript Interface**: Don't expose unless required

## Support

For issues or questions:
1. Check the generated `README.md` in your project
2. Review `TEMPLATE_INFO.md` in the template directory
3. Check Android documentation: https://developer.android.com

## License

This tool generates Android applications based on the provided template.
Generated applications are yours to use and modify as needed.
