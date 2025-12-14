"""
Configuration loader for web2apk.
Handles YAML and JSON config files with Pydantic validation.
"""

import json
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from .logger import get_logger

logger = get_logger()


class SigningConfig(BaseModel):
    """APK signing configuration."""
    keystore_path: Optional[str] = None
    keystore_password: Optional[str] = None
    key_alias: Optional[str] = None
    key_password: Optional[str] = None


class IconConfig(BaseModel):
    """Icon configuration for different densities."""
    mdpi: Optional[str] = None
    hdpi: Optional[str] = None
    xhdpi: Optional[str] = None
    xxhdpi: Optional[str] = None
    xxxhdpi: Optional[str] = None


class SplashConfig(BaseModel):
    """Splash screen configuration."""
    image: Optional[str] = None
    background_color: Optional[str] = "#FFFFFF"
    duration_ms: Optional[int] = 2000


class CacheConfig(BaseModel):
    """Offline and caching configuration."""
    enable_offline: bool = False
    cache_size_mb: int = 50
    cache_strategy: str = "default"


class AppConfig(BaseModel):
    """Main application configuration model."""
    url: str = Field(..., description="Website URL to convert to APK")
    app_name: str = Field(..., description="Application name", min_length=1, max_length=50)
    package_id: str = Field(..., description="Android package identifier (e.g., com.example.app)")
    version_name: str = Field(default="1.0.0", description="Version name")
    version_code: int = Field(default=1, description="Version code", ge=1)
    
    permissions: List[str] = Field(default_factory=list, description="Android permissions")
    
    icons: Optional[IconConfig] = None
    splash: Optional[SplashConfig] = None
    
    build_variant: str = Field(default="release", description="Build variant (debug/release)")
    
    signing: Optional[SigningConfig] = None
    
    cache: Optional[CacheConfig] = None
    
    user_agent: Optional[str] = None
    
    orientation: str = Field(default="portrait", description="Screen orientation")
    theme_color: Optional[str] = None
    
    @field_validator('package_id')
    @classmethod
    def validate_package_id(cls, v: str) -> str:
        """Validate Android package identifier format."""
        if not v:
            raise ValueError("Package ID cannot be empty")
        
        parts = v.split('.')
        if len(parts) < 2:
            raise ValueError("Package ID must have at least two segments (e.g., com.example)")
        
        for part in parts:
            if not part:
                raise ValueError("Package ID segments cannot be empty")
            if not part[0].isalpha():
                raise ValueError(f"Package ID segment must start with a letter: {part}")
            if not all(c.isalnum() or c == '_' for c in part):
                raise ValueError(f"Package ID segment contains invalid characters: {part}")
        
        return v
    
    @field_validator('url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL format."""
        if not v:
            raise ValueError("URL cannot be empty")
        
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError("URL must start with http:// or https://")
        
        return v
    
    @field_validator('build_variant')
    @classmethod
    def validate_build_variant(cls, v: str) -> str:
        """Validate build variant."""
        allowed_variants = ['debug', 'release']
        if v.lower() not in allowed_variants:
            raise ValueError(f"Build variant must be one of: {', '.join(allowed_variants)}")
        return v.lower()
    
    @field_validator('orientation')
    @classmethod
    def validate_orientation(cls, v: str) -> str:
        """Validate screen orientation."""
        allowed_orientations = ['portrait', 'landscape', 'unspecified']
        if v.lower() not in allowed_orientations:
            raise ValueError(f"Orientation must be one of: {', '.join(allowed_orientations)}")
        return v.lower()


class ConfigLoader:
    """Load and validate configuration files."""
    
    ALLOWED_PERMISSIONS = [
        'android.permission.INTERNET',
        'android.permission.ACCESS_NETWORK_STATE',
        'android.permission.ACCESS_WIFI_STATE',
        'android.permission.WRITE_EXTERNAL_STORAGE',
        'android.permission.READ_EXTERNAL_STORAGE',
        'android.permission.CAMERA',
        'android.permission.ACCESS_FINE_LOCATION',
        'android.permission.ACCESS_COARSE_LOCATION',
        'android.permission.RECORD_AUDIO',
        'android.permission.VIBRATE',
        'android.permission.WAKE_LOCK',
    ]
    
    @staticmethod
    def load_config(config_path: str) -> AppConfig:
        """
        Load configuration from YAML or JSON file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Validated AppConfig object
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config format is invalid or validation fails
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        if not config_file.is_file():
            raise ValueError(f"Configuration path is not a file: {config_path}")
        
        suffix = config_file.suffix.lower()
        
        try:
            with open(config_file, 'r') as f:
                if suffix in ['.yaml', '.yml']:
                    config_data = yaml.safe_load(f)
                elif suffix == '.json':
                    config_data = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {suffix}. Use .yaml, .yml, or .json")
            
            if not config_data:
                raise ValueError("Configuration file is empty")
            
            config = AppConfig(**config_data)
            
            ConfigLoader._validate_permissions(config.permissions)
            
            logger.debug(f"✓ Configuration loaded and validated from: {config_path}")
            return config
            
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML config: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON config: {e}")
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {e}")
    
    @staticmethod
    def _validate_permissions(permissions: List[str]) -> None:
        """
        Validate that all requested permissions are in the allowed list.
        
        Args:
            permissions: List of permission strings
            
        Raises:
            ValueError: If any permission is not allowed
        """
        for permission in permissions:
            if permission not in ConfigLoader.ALLOWED_PERMISSIONS:
                raise ValueError(
                    f"Permission not allowed: {permission}\n"
                    f"Allowed permissions: {', '.join(ConfigLoader.ALLOWED_PERMISSIONS)}"
                )
    
    @staticmethod
    def generate_sample_config(format_type: str = 'yaml') -> str:
        """
        Generate a sample configuration file content.
        
        Args:
            format_type: Output format ('yaml' or 'json')
            
        Returns:
            Sample configuration as string
        """
        sample_config = {
            'url': 'https://example.com',
            'app_name': 'My Web App',
            'package_id': 'com.example.mywebapp',
            'version_name': '1.0.0',
            'version_code': 1,
            'permissions': [
                'android.permission.INTERNET',
                'android.permission.ACCESS_NETWORK_STATE',
            ],
            'icons': {
                'mdpi': 'assets/icon-mdpi.png',
                'hdpi': 'assets/icon-hdpi.png',
                'xhdpi': 'assets/icon-xhdpi.png',
                'xxhdpi': 'assets/icon-xxhdpi.png',
                'xxxhdpi': 'assets/icon-xxxhdpi.png',
            },
            'splash': {
                'image': 'assets/splash.png',
                'background_color': '#FFFFFF',
                'duration_ms': 2000,
            },
            'build_variant': 'release',
            'signing': {
                'keystore_path': 'path/to/keystore.jks',
                'keystore_password': 'keystore_password',
                'key_alias': 'key_alias',
                'key_password': 'key_password',
            },
            'cache': {
                'enable_offline': True,
                'cache_size_mb': 50,
                'cache_strategy': 'default',
            },
            'orientation': 'portrait',
            'theme_color': '#2196F3',
            'user_agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
        }
        
        if format_type.lower() == 'json':
            return json.dumps(sample_config, indent=2)
        else:
            return yaml.dump(sample_config, default_flow_style=False, sort_keys=False)
