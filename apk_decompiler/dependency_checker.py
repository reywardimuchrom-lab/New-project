"""
Dependency checker for external binaries required by the APK decompiler.
"""

import shutil
from typing import Dict, List
from .logger import get_logger

logger = get_logger()


class DependencyChecker:
    """Check for required external binary dependencies."""
    
    REQUIRED_BINARIES = ["apktool", "jadx", "adb", "aapt"]
    
    def __init__(self):
        self.missing_dependencies = []
        self.available_dependencies = []
    
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
    
    def check_all(self) -> Dict[str, bool]:
        """
        Check all required dependencies.
        
        Returns:
            Dictionary mapping binary names to their availability status
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
        return len(self.missing_dependencies) == 0
    
    def report(self):
        """Print a summary report of dependency check results."""
        logger.info("\n" + "=" * 50)
        logger.info("Dependency Check Summary")
        logger.info("=" * 50)
        
        if self.available_dependencies:
            logger.info(f"\n✓ Available ({len(self.available_dependencies)}):")
            for dep in self.available_dependencies:
                logger.info(f"  - {dep}")
        
        if self.missing_dependencies:
            logger.warning(f"\n✗ Missing ({len(self.missing_dependencies)}):")
            for dep in self.missing_dependencies:
                logger.warning(f"  - {dep}")
            logger.warning("\nPlease install missing dependencies to use all features.")
        else:
            logger.success("\n✓ All required dependencies are available!")
        
        logger.info("=" * 50 + "\n")
