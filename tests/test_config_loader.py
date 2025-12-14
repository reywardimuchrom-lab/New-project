"""
Unit tests for config_loader module.
"""

import unittest
import tempfile
import json
import yaml
from pathlib import Path
from pydantic import ValidationError
from web2apk.config_loader import ConfigLoader, AppConfig


class TestConfigLoader(unittest.TestCase):
    """Test cases for ConfigLoader class."""
    
    def test_load_config_yaml_valid(self):
        """Test loading valid YAML config."""
        config_data = {
            'url': 'https://example.com',
            'app_name': 'Test App',
            'package_id': 'com.example.testapp',
            'version_name': '1.0.0',
            'version_code': 1,
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            yaml.dump(config_data, tmp)
            tmp_path = tmp.name
        
        try:
            config = ConfigLoader.load_config(tmp_path)
            self.assertEqual(config.url, 'https://example.com')
            self.assertEqual(config.app_name, 'Test App')
            self.assertEqual(config.package_id, 'com.example.testapp')
            self.assertEqual(config.version_name, '1.0.0')
            self.assertEqual(config.version_code, 1)
        finally:
            Path(tmp_path).unlink()
    
    def test_load_config_json_valid(self):
        """Test loading valid JSON config."""
        config_data = {
            'url': 'https://example.com',
            'app_name': 'Test App',
            'package_id': 'com.example.testapp',
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(config_data, tmp)
            tmp_path = tmp.name
        
        try:
            config = ConfigLoader.load_config(tmp_path)
            self.assertEqual(config.url, 'https://example.com')
            self.assertEqual(config.app_name, 'Test App')
            self.assertEqual(config.package_id, 'com.example.testapp')
        finally:
            Path(tmp_path).unlink()
    
    def test_load_config_file_not_found(self):
        """Test loading config from non-existent file."""
        with self.assertRaises(FileNotFoundError):
            ConfigLoader.load_config('/nonexistent/config.yaml')
    
    def test_load_config_invalid_format(self):
        """Test loading config with unsupported format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            tmp.write("some text")
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(ValueError) as context:
                ConfigLoader.load_config(tmp_path)
            self.assertIn("Unsupported config file format", str(context.exception))
        finally:
            Path(tmp_path).unlink()
    
    def test_load_config_empty_file(self):
        """Test loading empty config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(ValueError) as context:
                ConfigLoader.load_config(tmp_path)
            self.assertIn("empty", str(context.exception).lower())
        finally:
            Path(tmp_path).unlink()
    
    def test_load_config_invalid_yaml(self):
        """Test loading invalid YAML syntax."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            tmp.write("invalid: yaml: syntax:\n  - broken")
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(ValueError) as context:
                ConfigLoader.load_config(tmp_path)
            self.assertIn("YAML", str(context.exception))
        finally:
            Path(tmp_path).unlink()
    
    def test_load_config_invalid_json(self):
        """Test loading invalid JSON syntax."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp.write('{"invalid": json syntax}')
            tmp_path = tmp.name
        
        try:
            with self.assertRaises(ValueError) as context:
                ConfigLoader.load_config(tmp_path)
            self.assertIn("JSON", str(context.exception))
        finally:
            Path(tmp_path).unlink()
    
    def test_validate_permissions_valid(self):
        """Test validation of allowed permissions."""
        permissions = [
            'android.permission.INTERNET',
            'android.permission.CAMERA',
        ]
        ConfigLoader._validate_permissions(permissions)
    
    def test_validate_permissions_invalid(self):
        """Test validation with invalid permission."""
        permissions = [
            'android.permission.INTERNET',
            'android.permission.INVALID_PERMISSION',
        ]
        with self.assertRaises(ValueError) as context:
            ConfigLoader._validate_permissions(permissions)
        self.assertIn("not allowed", str(context.exception))
    
    def test_generate_sample_config_yaml(self):
        """Test generating sample YAML config."""
        config_str = ConfigLoader.generate_sample_config('yaml')
        self.assertIsInstance(config_str, str)
        self.assertIn('url:', config_str)
        self.assertIn('app_name:', config_str)
        self.assertIn('package_id:', config_str)
        
        config_data = yaml.safe_load(config_str)
        self.assertIn('url', config_data)
        self.assertIn('app_name', config_data)
        self.assertIn('package_id', config_data)
    
    def test_generate_sample_config_json(self):
        """Test generating sample JSON config."""
        config_str = ConfigLoader.generate_sample_config('json')
        self.assertIsInstance(config_str, str)
        
        config_data = json.loads(config_str)
        self.assertIn('url', config_data)
        self.assertIn('app_name', config_data)
        self.assertIn('package_id', config_data)


class TestAppConfig(unittest.TestCase):
    """Test cases for AppConfig model."""
    
    def test_app_config_valid_minimal(self):
        """Test creating AppConfig with minimal valid data."""
        config = AppConfig(
            url='https://example.com',
            app_name='Test App',
            package_id='com.example.testapp',
        )
        self.assertEqual(config.url, 'https://example.com')
        self.assertEqual(config.app_name, 'Test App')
        self.assertEqual(config.package_id, 'com.example.testapp')
        self.assertEqual(config.version_name, '1.0.0')
        self.assertEqual(config.version_code, 1)
    
    def test_app_config_invalid_url_no_protocol(self):
        """Test creating AppConfig with URL without protocol."""
        with self.assertRaises(ValidationError):
            AppConfig(
                url='example.com',
                app_name='Test App',
                package_id='com.example.testapp',
            )
    
    def test_app_config_invalid_url_empty(self):
        """Test creating AppConfig with empty URL."""
        with self.assertRaises(ValidationError):
            AppConfig(
                url='',
                app_name='Test App',
                package_id='com.example.testapp',
            )
    
    def test_app_config_invalid_package_id_single_segment(self):
        """Test creating AppConfig with single segment package ID."""
        with self.assertRaises(ValidationError):
            AppConfig(
                url='https://example.com',
                app_name='Test App',
                package_id='testapp',
            )
    
    def test_app_config_invalid_package_id_starts_with_number(self):
        """Test creating AppConfig with package ID starting with number."""
        with self.assertRaises(ValidationError):
            AppConfig(
                url='https://example.com',
                app_name='Test App',
                package_id='com.1example.testapp',
            )
    
    def test_app_config_invalid_package_id_invalid_chars(self):
        """Test creating AppConfig with invalid characters in package ID."""
        with self.assertRaises(ValidationError):
            AppConfig(
                url='https://example.com',
                app_name='Test App',
                package_id='com.example.test-app',
            )
    
    def test_app_config_invalid_build_variant(self):
        """Test creating AppConfig with invalid build variant."""
        with self.assertRaises(ValidationError):
            AppConfig(
                url='https://example.com',
                app_name='Test App',
                package_id='com.example.testapp',
                build_variant='invalid',
            )
    
    def test_app_config_valid_build_variant_debug(self):
        """Test creating AppConfig with debug build variant."""
        config = AppConfig(
            url='https://example.com',
            app_name='Test App',
            package_id='com.example.testapp',
            build_variant='debug',
        )
        self.assertEqual(config.build_variant, 'debug')
    
    def test_app_config_invalid_orientation(self):
        """Test creating AppConfig with invalid orientation."""
        with self.assertRaises(ValidationError):
            AppConfig(
                url='https://example.com',
                app_name='Test App',
                package_id='com.example.testapp',
                orientation='invalid',
            )
    
    def test_app_config_valid_orientation_landscape(self):
        """Test creating AppConfig with landscape orientation."""
        config = AppConfig(
            url='https://example.com',
            app_name='Test App',
            package_id='com.example.testapp',
            orientation='landscape',
        )
        self.assertEqual(config.orientation, 'landscape')
    
    def test_app_config_with_permissions(self):
        """Test creating AppConfig with permissions."""
        config = AppConfig(
            url='https://example.com',
            app_name='Test App',
            package_id='com.example.testapp',
            permissions=['android.permission.INTERNET', 'android.permission.CAMERA'],
        )
        self.assertEqual(len(config.permissions), 2)
        self.assertIn('android.permission.INTERNET', config.permissions)
    
    def test_app_config_with_icons(self):
        """Test creating AppConfig with icon configuration."""
        config = AppConfig(
            url='https://example.com',
            app_name='Test App',
            package_id='com.example.testapp',
            icons={
                'mdpi': 'icon-mdpi.png',
                'hdpi': 'icon-hdpi.png',
            },
        )
        self.assertIsNotNone(config.icons)
        self.assertEqual(config.icons.mdpi, 'icon-mdpi.png')
        self.assertEqual(config.icons.hdpi, 'icon-hdpi.png')
    
    def test_app_config_with_splash(self):
        """Test creating AppConfig with splash configuration."""
        config = AppConfig(
            url='https://example.com',
            app_name='Test App',
            package_id='com.example.testapp',
            splash={
                'image': 'splash.png',
                'background_color': '#FF0000',
                'duration_ms': 3000,
            },
        )
        self.assertIsNotNone(config.splash)
        self.assertEqual(config.splash.image, 'splash.png')
        self.assertEqual(config.splash.background_color, '#FF0000')
        self.assertEqual(config.splash.duration_ms, 3000)
    
    def test_app_config_with_cache(self):
        """Test creating AppConfig with cache configuration."""
        config = AppConfig(
            url='https://example.com',
            app_name='Test App',
            package_id='com.example.testapp',
            cache={
                'enable_offline': True,
                'cache_size_mb': 100,
            },
        )
        self.assertIsNotNone(config.cache)
        self.assertTrue(config.cache.enable_offline)
        self.assertEqual(config.cache.cache_size_mb, 100)
    
    def test_app_config_version_code_negative(self):
        """Test creating AppConfig with negative version code."""
        with self.assertRaises(ValidationError):
            AppConfig(
                url='https://example.com',
                app_name='Test App',
                package_id='com.example.testapp',
                version_code=-1,
            )


if __name__ == '__main__':
    unittest.main()
