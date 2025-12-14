"""
Dependency checker for external binaries and environment variables required by web2apk.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from .logger import get_logger

logger = get_logger()


class DependencyChecker:
    """Check for required external binary dependencies and environment variables."""
    
    REQUIRED_BINARIES = ["java", "zipalign", "apksigner"]
    OPTIONAL_BINARIES = ["gradle", "gradlew"]
    ANDROID_ENV_VARS = ["ANDROID_HOME", "ANDROID_SDK_ROOT"]
    
    def __init__(self):
        self.missing_dependencies = []
        self.available_dependencies = []
        self.missing_gradle = []
        self.available_gradle = []
        self.env_vars_status = {}
    
    def check_binary(self, binary_name: str) -> bool:
        """
        Check if a binary is available in the system PATH.
        
        Args:
            binary_name: Name of the binary to check
            
        Returns:
            True if binary is available, False otherwise
        """
        binary_path = shutil.which(binary_name)
        if binary_path:
            logger.debug(f"✓ Found {binary_name} at: {binary_path}")
            return True
        else:
            logger.warning(f"✗ {binary_name} not found in PATH")
            return False
    
    def check_java_version(self) -> Optional[str]:
        """
        Check Java version.
        
        Returns:
            Java version string if available, None otherwise
        """
        try:
            result = subprocess.run(
                ['java', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version_output = result.stderr if result.stderr else result.stdout
            
            if version_output:
                version_line = version_output.split('\n')[0]
                logger.debug(f"Java version: {version_line}")
                return version_line
            return None
        except Exception as e:
            logger.debug(f"Failed to get Java version: {e}")
            return None
    
    def check_gradle(self) -> bool:
        """
        Check for Gradle or Gradlew.
        
        Returns:
            True if either gradle or gradlew is available
        """
        gradle_found = self.check_binary("gradle")
        gradlew_found = self.check_binary("gradlew")
        
        if gradle_found:
            self.available_gradle.append("gradle")
        else:
            self.missing_gradle.append("gradle")
        
        if gradlew_found:
            self.available_gradle.append("gradlew")
        else:
            self.missing_gradle.append("gradlew")
        
        return gradle_found or gradlew_found
    
    def check_android_sdk_env(self) -> Dict[str, Optional[str]]:
        """
        Check for Android SDK environment variables.
        
        Returns:
            Dictionary mapping env var names to their values (None if not set)
        """
        env_status = {}
        
        for env_var in self.ANDROID_ENV_VARS:
            value = os.environ.get(env_var)
            env_status[env_var] = value
            
            if value:
                logger.debug(f"✓ {env_var} is set: {value}")
                if Path(value).exists():
                    logger.debug(f"  - Path exists: {value}")
                else:
                    logger.warning(f"  - Path does not exist: {value}")
            else:
                logger.warning(f"✗ {env_var} is not set")
        
        self.env_vars_status = env_status
        return env_status
    
    def check_android_build_tools(self) -> bool:
        """
        Check if Android build tools are accessible via SDK.
        
        Returns:
            True if build tools are found, False otherwise
        """
        android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
        
        if not android_home:
            logger.warning("Cannot check build tools: Android SDK environment variable not set")
            return False
        
        build_tools_dir = Path(android_home) / 'build-tools'
        
        if not build_tools_dir.exists():
            logger.warning(f"Build tools directory not found: {build_tools_dir}")
            return False
        
        try:
            versions = [d.name for d in build_tools_dir.iterdir() if d.is_dir()]
            if versions:
                latest_version = sorted(versions)[-1]
                logger.debug(f"✓ Found Android build tools version: {latest_version}")
                return True
            else:
                logger.warning("No build tools versions found")
                return False
        except Exception as e:
            logger.warning(f"Failed to check build tools: {e}")
            return False
    
    def check_all(self) -> Dict[str, bool]:
        """
        Check all required dependencies.
        
        Returns:
            Dictionary mapping dependency names to their availability status
        """
        logger.info("Checking for required external dependencies...")
        
        results = {}
        
        for binary in self.REQUIRED_BINARIES:
            available = self.check_binary(binary)
            results[binary] = available
            
            if available:
                self.available_dependencies.append(binary)
            else:
                self.missing_dependencies.append(binary)
        
        if "java" in self.available_dependencies:
            java_version = self.check_java_version()
            if java_version:
                results["java_version"] = True
        
        gradle_available = self.check_gradle()
        results["gradle_or_gradlew"] = gradle_available
        
        self.check_android_sdk_env()
        results["android_sdk"] = any(self.env_vars_status.values())
        
        if results.get("android_sdk"):
            build_tools_available = self.check_android_build_tools()
            results["android_build_tools"] = build_tools_available
        
        return results
    
    def get_missing_dependencies(self) -> List[str]:
        """
        Get list of missing dependencies.
        
        Returns:
            List of missing binary names
        """
        return self.missing_dependencies
    
    def get_available_dependencies(self) -> List[str]:
        """
        Get list of available dependencies.
        
        Returns:
            List of available binary names
        """
        return self.available_dependencies
    
    def all_dependencies_available(self) -> bool:
        """
        Check if all required dependencies are available.
        
        Returns:
            True if all dependencies are available, False otherwise
        """
        gradle_ok = len(self.available_gradle) > 0
        android_sdk_ok = any(self.env_vars_status.values())
        
        return (len(self.missing_dependencies) == 0 and 
                gradle_ok and 
                android_sdk_ok)
    
    def report(self):
        """Print a summary report of dependency check results."""
        logger.info("\n" + "=" * 60)
        logger.info("Dependency Check Summary")
        logger.info("=" * 60)
        
        if self.available_dependencies:
            logger.info(f"\n✓ Available Required Tools ({len(self.available_dependencies)}):")
            for dep in self.available_dependencies:
                logger.info(f"  - {dep}")
        
        if self.missing_dependencies:
            logger.warning(f"\n✗ Missing Required Tools ({len(self.missing_dependencies)}):")
            for dep in self.missing_dependencies:
                logger.warning(f"  - {dep}")
        
        if self.available_gradle or self.missing_gradle:
            logger.info("\nGradle Status:")
            if self.available_gradle:
                logger.info(f"  ✓ Available: {', '.join(self.available_gradle)}")
            if len(self.available_gradle) == 0:
                logger.warning("  ✗ Neither gradle nor gradlew found in PATH")
        
        logger.info("\nAndroid SDK Environment:")
        for env_var, value in self.env_vars_status.items():
            if value:
                logger.info(f"  ✓ {env_var}: {value}")
            else:
                logger.warning(f"  ✗ {env_var}: Not set")
        
        if not any(self.env_vars_status.values()):
            logger.warning("\n⚠ Android SDK not configured!")
            logger.warning("  Set ANDROID_HOME or ANDROID_SDK_ROOT environment variable")
        
        if self.all_dependencies_available():
            logger.success("\n✓ All required dependencies are available!")
        else:
            logger.error("\n✗ Some required dependencies are missing!")
            logger.error("Please install missing dependencies before building APKs.")
            
            if self.missing_dependencies:
                logger.error("\nRequired tools installation:")
                logger.error("  - Java: Install JDK 8 or higher")
                logger.error("  - Android SDK: Download from https://developer.android.com/studio")
                logger.error("  - zipalign & apksigner: Included in Android SDK build-tools")
                logger.error("  - Gradle: Install from https://gradle.org/ or use gradlew")
        
        logger.info("=" * 60 + "\n")
    
    def fail_if_missing(self):
        """
        Exit the application if required dependencies are missing.
        
        Raises:
            SystemExit: If any required dependencies are missing
        """
        if not self.all_dependencies_available():
            logger.error("Cannot proceed: Required dependencies are missing")
            raise SystemExit(1)
