import unittest
import tempfile
import shutil
from pathlib import Path
from apk_decompiler.template_manager import TemplateManager


class TestTemplateManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "test_output"

    def tearDown(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_validate_package_name(self):
        self.assertTrue(TemplateManager.validate_package_name("com.example.app"))
        self.assertTrue(TemplateManager.validate_package_name("com.example.my.app"))
        self.assertTrue(TemplateManager.validate_package_name("io.github.user"))
        
        self.assertFalse(TemplateManager.validate_package_name("example"))
        self.assertFalse(TemplateManager.validate_package_name("Example.com"))
        self.assertFalse(TemplateManager.validate_package_name("com.Example"))
        self.assertFalse(TemplateManager.validate_package_name("com..example"))

    def test_template_copy(self):
        manager = TemplateManager(str(self.output_dir))
        manager.configure(
            package_name="com.test.app",
            app_name="Test App",
            target_url="https://test.com"
        )
        
        manager.copy_template()
        
        self.assertTrue(self.output_dir.exists())
        self.assertTrue((self.output_dir / "build.gradle").exists())
        self.assertTrue((self.output_dir / "settings.gradle").exists())
        self.assertTrue((self.output_dir / "app" / "build.gradle").exists())

    def test_placeholder_replacement(self):
        manager = TemplateManager(str(self.output_dir))
        manager.configure(
            package_name="com.test.myapp",
            app_name="My Test App",
            target_url="https://example.org"
        )
        
        manager.copy_template()
        manager.replace_placeholders()
        
        build_gradle = self.output_dir / "app" / "build.gradle"
        content = build_gradle.read_text()
        
        self.assertIn("com.test.myapp", content)
        self.assertIn("https://example.org", content)
        self.assertNotIn("{{PACKAGE_NAME}}", content)
        self.assertNotIn("{{TARGET_URL}}", content)

    def test_package_rename(self):
        manager = TemplateManager(str(self.output_dir))
        manager.configure(
            package_name="io.github.test",
            app_name="Test",
            target_url="https://test.com"
        )
        
        manager.copy_template()
        manager.replace_placeholders()
        manager.rename_package()
        
        expected_path = self.output_dir / "app" / "src" / "main" / "java" / "io" / "github" / "test"
        self.assertTrue(expected_path.exists())
        self.assertTrue((expected_path / "MainActivity.kt").exists())
        
        old_path = self.output_dir / "app" / "src" / "main" / "java" / "com" / "template" / "webview"
        self.assertFalse(old_path.exists())

    def test_full_generation(self):
        manager = TemplateManager(str(self.output_dir))
        manager.configure(
            package_name="com.example.test",
            app_name="Test App",
            target_url="https://google.com",
            enable_offline=True,
            enable_file_access=False
        )
        
        manager.generate()
        
        self.assertTrue(self.output_dir.exists())
        
        expected_files = [
            "build.gradle",
            "settings.gradle",
            "gradlew",
            "app/build.gradle",
            "app/proguard-rules.pro",
            "app/src/main/AndroidManifest.xml",
            "app/src/main/java/com/example/test/MainActivity.kt",
            "app/src/main/java/com/example/test/OfflineHandler.kt",
            "app/src/main/res/layout/activity_main.xml",
            "app/src/main/res/values/strings.xml",
            "app/src/main/assets/offline.html",
        ]
        
        for file_path in expected_files:
            full_path = self.output_dir / file_path
            self.assertTrue(full_path.exists(), f"Missing file: {file_path}")

    def test_config_values_in_build_gradle(self):
        manager = TemplateManager(str(self.output_dir))
        manager.configure(
            package_name="com.config.test",
            app_name="Config Test",
            target_url="https://config.test",
            user_agent="CustomAgent/1.0",
            enable_offline=False,
            enable_file_access=True
        )
        
        manager.generate()
        
        build_gradle = self.output_dir / "app" / "build.gradle"
        content = build_gradle.read_text()
        
        self.assertIn('buildConfigField "String", "TARGET_URL", "\\"https://config.test\\""', content)
        self.assertIn('buildConfigField "String", "USER_AGENT", "\\"CustomAgent/1.0\\""', content)
        self.assertIn('buildConfigField "boolean", "ENABLE_OFFLINE_MODE", "false"', content)
        self.assertIn('buildConfigField "boolean", "ENABLE_FILE_ACCESS", "true"', content)


if __name__ == '__main__':
    unittest.main()
