"""
Input validation for the APK decompiler.
"""

import os
from pathlib import Path
from typing import Tuple
from .logger import get_logger

logger = get_logger()


class InputValidator:
    """Validate input paths and parameters."""
    
    @staticmethod
    def validate_apk_path(apk_path: str) -> Tuple[bool, str]:
        """
        Validate that the APK path exists and is a valid file.
        
        Args:
            apk_path: Path to the APK file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not apk_path:
            return False, "APK path cannot be empty"
        
        apk_file = Path(apk_path)
        
        if not apk_file.exists():
            return False, f"APK file does not exist: {apk_path}"
        
        if not apk_file.is_file():
            return False, f"Path is not a file: {apk_path}"
        
        if not apk_path.lower().endswith('.apk'):
            logger.warning(f"File does not have .apk extension: {apk_path}")
        
        logger.debug(f"✓ APK path is valid: {apk_path}")
        return True, ""
    
    @staticmethod
    def validate_output_dir(output_dir: str, create_if_missing: bool = True) -> Tuple[bool, str]:
        """
        Validate that the output directory exists or can be created.
        
        Args:
            output_dir: Path to the output directory
            create_if_missing: If True, create the directory if it doesn't exist
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not output_dir:
            return False, "Output directory path cannot be empty"
        
        output_path = Path(output_dir)
        
        if output_path.exists():
            if not output_path.is_dir():
                return False, f"Output path exists but is not a directory: {output_dir}"
            
            if not os.access(output_path, os.W_OK):
                return False, f"Output directory is not writable: {output_dir}"
            
            logger.debug(f"✓ Output directory exists and is writable: {output_dir}")
            return True, ""
        
        if create_if_missing:
            try:
                output_path.mkdir(parents=True, exist_ok=True)
                logger.debug(f"✓ Created output directory: {output_dir}")
                return True, ""
            except Exception as e:
                return False, f"Failed to create output directory: {e}"
        else:
            return False, f"Output directory does not exist: {output_dir}"
    
    @staticmethod
    def validate_inputs(apk_path: str, output_dir: str) -> Tuple[bool, str]:
        """
        Validate all inputs for the decompiler.
        
        Args:
            apk_path: Path to the APK file
            output_dir: Path to the output directory
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        logger.info("Validating input parameters...")
        
        is_valid, error = InputValidator.validate_apk_path(apk_path)
        if not is_valid:
            return False, error
        
        is_valid, error = InputValidator.validate_output_dir(output_dir)
        if not is_valid:
            return False, error
        
        logger.info("✓ All input parameters are valid")
        return True, ""
