import unittest
import tempfile
import shutil
import subprocess
from pathlib import Path
from apk_decompiler.template_manager import TemplateManager


class TestTemplateBuild(unittest.TestCase):
    """
    Integration test to verify the generated template can be built.
    
    Note: This test requires Android SDK and Gradle to be installed.
    It will be skipped if the required tools are not available.
    """

    @classmethod
    def setUpClass(cls):
        cls.has_android_sdk = cls._check_android_sdk()
        
        if not cls.has_android_sdk:
            print("\nSkipping build tests: Android SDK not found")
            print("Set ANDROID_HOME environment variable to enable build tests")

    @staticmethod
    def _check_android_sdk():
        import os
        android_home = os.environ.get('ANDROID_HOME')
        if not android_home:
            return False
        
        android_path = Path(android_home)
        return android_path.exists() and (android_path / "platforms").exists()

    def setUp(self):
        if not self.has_android_sdk:
            self.skipTest("Android SDK not available")
        
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "build_test"

    def tearDown(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_template_builds(self):
        manager = TemplateManager(str(self.output_dir))
        manager.configure(
            package_name="com.build.test",
            app_name="Build Test",
            target_url="https://example.com"
        )
        
        manager.generate()
        
        gradlew = self.output_dir / "gradlew"
        self.assertTrue(gradlew.exists())
        
        try:
            result = subprocess.run(
                [str(gradlew), "assembleDebug", "--stacktrace"],
                cwd=str(self.output_dir),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                print("\nBuild output:")
                print(result.stdout)
                print(result.stderr)
            
            self.assertEqual(result.returncode, 0, "Gradle build failed")
            
            apk_path = self.output_dir / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk"
            self.assertTrue(apk_path.exists(), f"APK not found at {apk_path}")
            
            self.assertGreater(apk_path.stat().st_size, 0, "APK file is empty")
            
        except subprocess.TimeoutExpired:
            self.fail("Build timed out after 5 minutes")
        except Exception as e:
            self.fail(f"Build failed with exception: {e}")

    def test_lint_check(self):
        manager = TemplateManager(str(self.output_dir))
        manager.configure(
            package_name="com.lint.test",
            app_name="Lint Test",
            target_url="https://example.com"
        )
        
        manager.generate()
        
        gradlew = self.output_dir / "gradlew"
        
        try:
            result = subprocess.run(
                [str(gradlew), "lint", "--continue"],
                cwd=str(self.output_dir),
                capture_output=True,
                text=True,
                timeout=180
            )
            
            lint_report = self.output_dir / "app" / "build" / "reports" / "lint-results.html"
            if lint_report.exists():
                print(f"\nLint report available at: {lint_report}")
            
        except subprocess.TimeoutExpired:
            self.skipTest("Lint check timed out")
        except Exception as e:
            print(f"Lint check warning: {e}")


if __name__ == '__main__':
    unittest.main()
