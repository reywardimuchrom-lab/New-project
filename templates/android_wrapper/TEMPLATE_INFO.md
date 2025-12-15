# Android WebView Wrapper Template

## Overview

This template provides a complete Android application that wraps a web URL in a native WebView with advanced features including offline support, custom caching, and production-ready configuration.

## Template Placeholders

The following placeholders are replaced during generation:

| Placeholder | Description | Example |
|------------|-------------|---------|
| `{{PACKAGE_NAME}}` | Android package name | `com.example.myapp` |
| `{{APP_NAME}}` | Application display name | `My App` |
| `{{TARGET_URL}}` | URL to load in WebView | `https://example.com` |
| `{{USER_AGENT}}` | Custom user agent string | `CustomAgent/1.0` |
| `{{ENABLE_OFFLINE_MODE}}` | Enable offline caching | `true` or `false` |
| `{{ENABLE_FILE_ACCESS}}` | Enable file access | `true` or `false` |
| `{{EXTRA_PERMISSIONS}}` | Additional permissions XML | Permission entries |

## Features

### WebView Configuration
- **JavaScript Enabled**: Full JavaScript support
- **DOM Storage**: Enabled for modern web apps
- **Web Storage**: Database and local storage enabled
- **Caching**: Smart caching strategy based on offline mode
- **File Access**: Optional file access permissions
- **Mixed Content**: Allows both HTTP and HTTPS content
- **Zoom Controls**: Built-in zoom with hidden controls
- **Hardware Acceleration**: Enabled for better performance

### Offline Support
- **Intelligent Caching**: Automatically caches static resources (CSS, JS, images, fonts)
- **Request Interception**: Custom WebViewClient intercepts requests
- **Cache Management**: MD5-based cache keys, 24-hour cache validity
- **Fallback Screen**: Custom offline.html displayed when connection fails
- **Service Worker Ready**: Assets folder prepared for PWA support

### UI Features
- **Swipe to Refresh**: Pull-down gesture to reload page
- **Progress Indicator**: Visual feedback during page loading
- **Back Navigation**: Hardware back button navigates WebView history
- **Offline Screen**: Material Design fallback with retry button
- **External Intent Handling**: Opens non-HTTP URLs in external apps

### Build Configuration
- **Debug Build**: Unminified, debuggable
- **Release Build**: ProGuard enabled, optimized, shrunk
- **Build Config Fields**: URL and settings injected at compile time
- **API Level**: Minimum API 21 (Android 5.0), Target API 33

## File Structure

```
.
├── app/
│   ├── build.gradle                    # App-level build configuration
│   ├── proguard-rules.pro              # ProGuard rules for release builds
│   └── src/main/
│       ├── AndroidManifest.xml         # App manifest with permissions
│       ├── java/{{PACKAGE_PATH}}/
│       │   ├── MainActivity.kt         # Main WebView activity
│       │   └── OfflineHandler.kt       # Caching and offline logic
│       ├── res/
│       │   ├── layout/
│       │   │   └── activity_main.xml   # Main activity layout
│       │   ├── values/
│       │   │   ├── strings.xml         # String resources
│       │   │   └── themes.xml          # Material3 theme
│       │   └── mipmap-*/               # App icons (generated)
│       └── assets/
│           └── offline.html            # Offline fallback page
├── gradle/wrapper/                     # Gradle wrapper files
├── build.gradle                        # Root build configuration
├── settings.gradle                     # Project settings
├── gradle.properties                   # Gradle properties
├── gradlew                            # Unix Gradle wrapper script
└── gradlew.bat                        # Windows Gradle wrapper script
```

## Dependencies

The template uses these Android libraries:
- `androidx.core:core-ktx` - Kotlin extensions
- `androidx.appcompat:appcompat` - App compatibility
- `com.google.android.material:material` - Material Design components
- `androidx.constraintlayout:constraintlayout` - Layout system
- `androidx.swiperefreshlayout:swiperefreshlayout` - Pull to refresh

## Building

### Requirements
- Android SDK with API 21+ (Android 5.0+)
- Gradle 7.6+
- Kotlin 1.8+
- Java 8+

### Commands
```bash
# Debug build
./gradlew assembleDebug

# Release build (requires signing configuration)
./gradlew assembleRelease

# Install to connected device
./gradlew installDebug

# Run tests
./gradlew test
./gradlew connectedAndroidTest

# Lint check
./gradlew lint
```

## Customization

### Adding Permissions
Permissions can be added via the `{{EXTRA_PERMISSIONS}}` placeholder or directly in `AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

### Modifying WebView Settings
Edit `MainActivity.kt` in the `setupWebView()` method to adjust WebView settings.

### Custom Offline Page
Replace `app/src/main/assets/offline.html` with your custom offline page.

### Caching Strategy
Modify `OfflineHandler.kt` to adjust:
- `MAX_CACHE_AGE_MS`: Cache validity duration
- `shouldCache()`: Which file types to cache
- `getMimeType()`: MIME type detection

### Theme Customization
Edit `app/src/main/res/values/themes.xml` to change colors and styles.

## Known Limitations

1. **File Upload**: File input requires additional `WebChromeClient` configuration
2. **Downloads**: Download functionality requires `DownloadListener` implementation
3. **Notifications**: Web notifications require FCM integration
4. **Geolocation**: Requires permission handling and `WebChromeClient.onGeolocationPermissionsShowPrompt`
5. **Camera/Microphone**: Requires runtime permission requests

## Security Considerations

1. **HTTPS Recommended**: Always use HTTPS URLs for production
2. **Certificate Pinning**: Consider implementing for sensitive data
3. **ProGuard**: Enabled by default for release builds
4. **JavaScript Interface**: Not exposed by default (add with caution)
5. **File Access**: Disabled by default, enable only if necessary
6. **Mixed Content**: Allowed by default, consider restricting in production

## License

This template is provided as-is for generating Android WebView wrapper applications.
