"""
Unit tests for validators module.
"""

import unittest
import tempfile
import os
from pathlib import Path
from web2apk.validators import InputValidator


class TestInputValidator(unittest.TestCase):
    """Test cases for InputValidator class."""
    
    def test_validate_url_valid_http(self):
        """Test validation of valid HTTP URL."""
        is_valid, error = InputValidator.validate_url("http://example.com")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_url_valid_https(self):
        """Test validation of valid HTTPS URL."""
        is_valid, error = InputValidator.validate_url("https://example.com")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_url_with_path(self):
        """Test validation of URL with path."""
        is_valid, error = InputValidator.validate_url("https://example.com/path/to/page")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_url_with_port(self):
        """Test validation of URL with port."""
        is_valid, error = InputValidator.validate_url("http://example.com:8080")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_url_empty(self):
        """Test validation of empty URL."""
        is_valid, error = InputValidator.validate_url("")
        self.assertFalse(is_valid)
        self.assertIn("cannot be empty", error)
    
    def test_validate_url_no_protocol(self):
        """Test validation of URL without protocol."""
        is_valid, error = InputValidator.validate_url("example.com")
        self.assertFalse(is_valid)
        self.assertIn("must start with", error)
    
    def test_validate_url_invalid_format(self):
        """Test validation of invalid URL format."""
        is_valid, error = InputValidator.validate_url("https://")
        self.assertFalse(is_valid)
        self.assertIn("Invalid URL format", error)
    
    def test_validate_package_id_valid(self):
        """Test validation of valid package ID."""
        is_valid, error = InputValidator.validate_package_id("com.example.app")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_package_id_valid_with_underscores(self):
        """Test validation of package ID with underscores."""
        is_valid, error = InputValidator.validate_package_id("com.example.my_app")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_package_id_empty(self):
        """Test validation of empty package ID."""
        is_valid, error = InputValidator.validate_package_id("")
        self.assertFalse(is_valid)
        self.assertIn("cannot be empty", error)
    
    def test_validate_package_id_single_segment(self):
        """Test validation of single segment package ID."""
        is_valid, error = InputValidator.validate_package_id("example")
        self.assertFalse(is_valid)
        self.assertIn("at least two segments", error)
    
    def test_validate_package_id_starts_with_number(self):
        """Test validation of package ID segment starting with number."""
        is_valid, error = InputValidator.validate_package_id("com.1example.app")
        self.assertFalse(is_valid)
        self.assertIn("must start with a letter", error)
    
    def test_validate_package_id_invalid_characters(self):
        """Test validation of package ID with invalid characters."""
        is_valid, error = InputValidator.validate_package_id("com.example.app-name")
        self.assertFalse(is_valid)
        self.assertIn("invalid characters", error)
    
    def test_validate_package_id_java_keyword(self):
        """Test validation of package ID with Java keyword."""
        is_valid, error = InputValidator.validate_package_id("com.class.app")
        self.assertFalse(is_valid)
        self.assertIn("Java keyword", error)
    
    def test_validate_output_dir_existing(self):
        """Test validation of existing output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_valid, error = InputValidator.validate_output_dir(tmpdir, create_if_missing=False)
            self.assertTrue(is_valid)
            self.assertEqual(error, "")
    
    def test_validate_output_dir_create(self):
        """Test validation with directory creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "new_output")
            is_valid, error = InputValidator.validate_output_dir(new_dir, create_if_missing=True)
            self.assertTrue(is_valid)
            self.assertEqual(error, "")
            self.assertTrue(os.path.exists(new_dir))
    
    def test_validate_output_dir_empty(self):
        """Test validation of empty output directory path."""
        is_valid, error = InputValidator.validate_output_dir("")
        self.assertFalse(is_valid)
        self.assertIn("cannot be empty", error)
    
    def test_validate_file_exists_valid(self):
        """Test validation of existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            is_valid, error = InputValidator.validate_file_exists(tmp_path)
            self.assertTrue(is_valid)
            self.assertEqual(error, "")
        finally:
            os.unlink(tmp_path)
    
    def test_validate_file_exists_missing(self):
        """Test validation of non-existing file."""
        is_valid, error = InputValidator.validate_file_exists("/nonexistent/file.txt")
        self.assertFalse(is_valid)
        self.assertIn("does not exist", error)
    
    def test_validate_image_file_png(self):
        """Test validation of PNG image file."""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            is_valid, error = InputValidator.validate_image_file(tmp_path)
            self.assertTrue(is_valid)
            self.assertEqual(error, "")
        finally:
            os.unlink(tmp_path)
    
    def test_validate_image_file_invalid_format(self):
        """Test validation of image with invalid format."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            is_valid, error = InputValidator.validate_image_file(tmp_path)
            self.assertFalse(is_valid)
            self.assertIn("must be one of", error)
        finally:
            os.unlink(tmp_path)
    
    def test_validate_config_file_yaml(self):
        """Test validation of YAML config file."""
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            is_valid, error = InputValidator.validate_config_file(tmp_path)
            self.assertTrue(is_valid)
            self.assertEqual(error, "")
        finally:
            os.unlink(tmp_path)
    
    def test_validate_config_file_json(self):
        """Test validation of JSON config file."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            is_valid, error = InputValidator.validate_config_file(tmp_path)
            self.assertTrue(is_valid)
            self.assertEqual(error, "")
        finally:
            os.unlink(tmp_path)
    
    def test_validate_config_file_invalid_format(self):
        """Test validation of config file with invalid format."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            is_valid, error = InputValidator.validate_config_file(tmp_path)
            self.assertFalse(is_valid)
            self.assertIn("must be one of", error)
        finally:
            os.unlink(tmp_path)
    
    def test_validate_app_name_valid(self):
        """Test validation of valid app name."""
        is_valid, error = InputValidator.validate_app_name("My Web App")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_app_name_empty(self):
        """Test validation of empty app name."""
        is_valid, error = InputValidator.validate_app_name("")
        self.assertFalse(is_valid)
        self.assertIn("cannot be empty", error)
    
    def test_validate_app_name_too_long(self):
        """Test validation of too long app name."""
        long_name = "A" * 51
        is_valid, error = InputValidator.validate_app_name(long_name)
        self.assertFalse(is_valid)
        self.assertIn("too long", error)
    
    def test_validate_app_name_whitespace_only(self):
        """Test validation of whitespace-only app name."""
        is_valid, error = InputValidator.validate_app_name("   ")
        self.assertFalse(is_valid)
        self.assertIn("whitespace", error)


if __name__ == '__main__':
    unittest.main()
