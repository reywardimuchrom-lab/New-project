# Android WebView Wrapper Template

This is a template Android application that wraps a web URL in a native WebView with advanced features.

## Features

- **WebView with JavaScript Support**: Full JavaScript, DOM storage, and web storage enabled
- **Offline Support**: Intelligent caching and offline fallback screen
- **Custom User Agent**: Configurable user agent string
- **File Access**: Optional file access permissions
- **Swipe to Refresh**: Pull-down to refresh functionality
- **External Intent Handling**: Proper handling of external URLs and intents
- **ProGuard Ready**: Production-ready ProGuard configuration

## Configuration

The template uses placeholder values that are replaced during generation:

- `{{PACKAGE_NAME}}`: Application package name (e.g., com.example.myapp)
- `{{APP_NAME}}`: Application display name
- `{{TARGET_URL}}`: The URL to load in the WebView
- `{{USER_AGENT}}`: Custom user agent string
- `{{ENABLE_OFFLINE_MODE}}`: Enable/disable offline caching (true/false)
- `{{ENABLE_FILE_ACCESS}}`: Enable/disable file access (true/false)
- `{{EXTRA_PERMISSIONS}}`: Additional Android permissions

## Building

### Debug Build
```bash
./gradlew assembleDebug
```

### Release Build
```bash
./gradlew assembleRelease
```

### Running Tests
```bash
./gradlew test
./gradlew connectedAndroidTest
```

## Requirements

- Android SDK with API 21+ (Android 5.0+)
- Gradle 7.6+
- Kotlin 1.8+

## Directory Structure

```
.
├── app/
│   ├── build.gradle
│   ├── proguard-rules.pro
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           ├── java/com/template/webview/
│           │   ├── MainActivity.kt
│           │   └── OfflineHandler.kt
│           ├── res/
│           │   ├── layout/
│           │   ├── values/
│           │   └── mipmap-*/
│           └── assets/
│               └── offline.html
├── build.gradle
├── settings.gradle
└── gradlew
```
