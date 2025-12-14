"""
Input validation for web2apk.
"""

import os
import re
from pathlib import Path
from typing import Tuple, Optional
from .logger import get_logger

logger = get_logger()


class InputValidator:
    """Validate input paths, URLs, and parameters."""
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """
        Validate URL format.
        
        Args:
            url: URL string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return False, "URL cannot be empty"
        
        if not (url.startswith('http://') or url.startswith('https://')):
            return False, "URL must start with http:// or https://"
        
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            return False, f"Invalid URL format: {url}"
        
        logger.debug(f"✓ URL is valid: {url}")
        return True, ""
    
    @staticmethod
    def validate_package_id(package_id: str) -> Tuple[bool, str]:
        """
        Validate Android package identifier format.
        
        Args:
            package_id: Package identifier to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not package_id:
            return False, "Package ID cannot be empty"
        
        parts = package_id.split('.')
        if len(parts) < 2:
            return False, "Package ID must have at least two segments (e.g., com.example)"
        
        for part in parts:
            if not part:
                return False, "Package ID segments cannot be empty"
            
            if not part[0].isalpha():
                return False, f"Package ID segment must start with a letter: {part}"
            
            if not all(c.isalnum() or c == '_' for c in part):
                return False, f"Package ID segment contains invalid characters: {part}"
            
            if part in ['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
                       'char', 'class', 'const', 'continue', 'default', 'do', 'double',
                       'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
                       'goto', 'if', 'implements', 'import', 'instanceof', 'int',
                       'interface', 'long', 'native', 'new', 'package', 'private',
                       'protected', 'public', 'return', 'short', 'static', 'strictfp',
                       'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
                       'transient', 'try', 'void', 'volatile', 'while']:
                return False, f"Package ID segment cannot be a Java keyword: {part}"
        
        logger.debug(f"✓ Package ID is valid: {package_id}")
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
    def validate_file_exists(file_path: str, file_description: str = "File") -> Tuple[bool, str]:
        """
        Validate that a file exists.
        
        Args:
            file_path: Path to the file
            file_description: Description of the file for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_path:
            return False, f"{file_description} path cannot be empty"
        
        file = Path(file_path)
        
        if not file.exists():
            return False, f"{file_description} does not exist: {file_path}"
        
        if not file.is_file():
            return False, f"{file_description} path is not a file: {file_path}"
        
        logger.debug(f"✓ {file_description} exists: {file_path}")
        return True, ""
    
    @staticmethod
    def validate_image_file(image_path: str, file_description: str = "Image") -> Tuple[bool, str]:
        """
        Validate that an image file exists and is a supported format.
        
        Args:
            image_path: Path to the image file
            file_description: Description of the image for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        is_valid, error = InputValidator.validate_file_exists(image_path, file_description)
        if not is_valid:
            return False, error
        
        supported_formats = ['.png', '.jpg', '.jpeg', '.webp']
        image_file = Path(image_path)
        
        if image_file.suffix.lower() not in supported_formats:
            return False, f"{file_description} must be one of {', '.join(supported_formats)}: {image_path}"
        
        logger.debug(f"✓ {file_description} format is valid: {image_path}")
        return True, ""
    
    @staticmethod
    def validate_config_file(config_path: str) -> Tuple[bool, str]:
        """
        Validate that a configuration file exists and has correct extension.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        is_valid, error = InputValidator.validate_file_exists(config_path, "Configuration file")
        if not is_valid:
            return False, error
        
        config_file = Path(config_path)
        supported_formats = ['.yaml', '.yml', '.json']
        
        if config_file.suffix.lower() not in supported_formats:
            return False, f"Configuration file must be one of {', '.join(supported_formats)}: {config_path}"
        
        logger.debug(f"✓ Configuration file format is valid: {config_path}")
        return True, ""
    
    @staticmethod
    def validate_app_name(app_name: str) -> Tuple[bool, str]:
        """
        Validate application name.
        
        Args:
            app_name: Application name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not app_name:
            return False, "Application name cannot be empty"
        
        if len(app_name) > 50:
            return False, f"Application name is too long (max 50 characters): {len(app_name)}"
        
        if not app_name.strip():
            return False, "Application name cannot be only whitespace"
        
        logger.debug(f"✓ Application name is valid: {app_name}")
        return True, ""
