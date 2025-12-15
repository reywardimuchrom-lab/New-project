import os
import shutil
import re
from pathlib import Path
from typing import Dict, Optional
from .logger import get_logger

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

logger = get_logger()


class TemplateManager:

    TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "android_wrapper"
    
    PLACEHOLDER_MAP = {
        "PACKAGE_NAME": "com.template.webview",
        "APP_NAME": "WebView App",
        "TARGET_URL": "https://example.com",
        "USER_AGENT": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
        "ENABLE_OFFLINE_MODE": "true",
        "ENABLE_FILE_ACCESS": "false",
        "EXTRA_PERMISSIONS": "",
    }
    
    MIPMAP_SIZES = {
        "mdpi": 48,
        "hdpi": 72,
        "xhdpi": 96,
        "xxhdpi": 144,
        "xxxhdpi": 192,
    }

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.config: Dict[str, str] = self.PLACEHOLDER_MAP.copy()

    def configure(
        self,
        package_name: str,
        app_name: str,
        target_url: str,
        user_agent: Optional[str] = None,
        enable_offline: bool = True,
        enable_file_access: bool = False,
        extra_permissions: Optional[list] = None,
    ):
        self.config["PACKAGE_NAME"] = package_name
        self.config["APP_NAME"] = app_name
        self.config["TARGET_URL"] = target_url
        
        if user_agent:
            self.config["USER_AGENT"] = user_agent
        
        self.config["ENABLE_OFFLINE_MODE"] = "true" if enable_offline else "false"
        self.config["ENABLE_FILE_ACCESS"] = "true" if enable_file_access else "false"
        
        if extra_permissions:
            permissions_xml = "\n    ".join([
                f'<uses-permission android:name="{perm}" />' 
                for perm in extra_permissions
            ])
            self.config["EXTRA_PERMISSIONS"] = permissions_xml

    def copy_template(self):
        if not self.TEMPLATE_DIR.exists():
            raise FileNotFoundError(f"Template directory not found: {self.TEMPLATE_DIR}")
        
        logger.info(f"Copying template from {self.TEMPLATE_DIR} to {self.output_dir}")
        
        if self.output_dir.exists():
            logger.warning(f"Output directory exists, removing: {self.output_dir}")
            shutil.rmtree(self.output_dir)
        
        shutil.copytree(self.TEMPLATE_DIR, self.output_dir)
        logger.success("Template copied successfully")

    def replace_placeholders(self):
        logger.info("Replacing placeholders in template files")
        
        for root, dirs, files in os.walk(self.output_dir):
            for filename in files:
                if filename.endswith(('.kt', '.java', '.xml', '.gradle', '.pro', '.properties')):
                    file_path = Path(root) / filename
                    self._replace_in_file(file_path)
        
        logger.success("Placeholders replaced successfully")

    def _replace_in_file(self, file_path: Path):
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            for placeholder, value in self.config.items():
                pattern = f"{{{{{placeholder}}}}}"
                content = content.replace(pattern, value)
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                logger.debug(f"Updated: {file_path.relative_to(self.output_dir)}")
        
        except Exception as e:
            logger.warning(f"Failed to process {file_path}: {e}")

    def rename_package(self):
        logger.info(f"Renaming package to {self.config['PACKAGE_NAME']}")
        
        old_package = "com.template.webview"
        new_package = self.config["PACKAGE_NAME"]
        
        old_path = self.output_dir / "app" / "src" / "main" / "java" / "com" / "template" / "webview"
        new_path_parts = new_package.split(".")
        new_path = self.output_dir / "app" / "src" / "main" / "java" / Path(*new_path_parts)
        
        if old_path.exists():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_path), str(new_path))
            
            old_parent = old_path.parent
            while old_parent != self.output_dir / "app" / "src" / "main" / "java":
                if old_parent.exists() and not list(old_parent.iterdir()):
                    old_parent.rmdir()
                    old_parent = old_parent.parent
                else:
                    break
            
            logger.success(f"Package structure renamed to {new_package}")
        else:
            logger.warning(f"Original package path not found: {old_path}")

    def add_icon(self, icon_path: str):
        if not PILLOW_AVAILABLE:
            logger.warning("Pillow not installed. Cannot generate app icons.")
            logger.warning("Install with: pip install Pillow")
            return
        
        icon_source = Path(icon_path)
        if not icon_source.exists():
            logger.error(f"Icon file not found: {icon_path}")
            return
        
        logger.info(f"Generating app icons from {icon_path}")
        
        try:
            img = Image.open(icon_source)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            for density, size in self.MIPMAP_SIZES.items():
                mipmap_dir = self.output_dir / "app" / "src" / "main" / "res" / f"mipmap-{density}"
                mipmap_dir.mkdir(parents=True, exist_ok=True)
                
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                
                launcher_path = mipmap_dir / "ic_launcher.png"
                resized.save(launcher_path, "PNG")
                
                round_launcher_path = mipmap_dir / "ic_launcher_round.png"
                self._create_round_icon(resized, round_launcher_path, size)
                
                logger.debug(f"Created icons for {density}")
            
            logger.success("App icons generated successfully")
        
        except Exception as e:
            logger.error(f"Failed to generate icons: {e}")

    def _create_round_icon(self, img: Image.Image, output_path: Path, size: int):
        from PIL import ImageDraw
        
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        output.paste(img, (0, 0))
        output.putalpha(mask)
        
        output.save(output_path, "PNG")

    def add_permissions(self, permissions: list):
        manifest_path = self.output_dir / "app" / "src" / "main" / "AndroidManifest.xml"
        
        if not manifest_path.exists():
            logger.error(f"AndroidManifest.xml not found: {manifest_path}")
            return
        
        logger.info(f"Adding {len(permissions)} permissions to manifest")
        
        try:
            content = manifest_path.read_text(encoding='utf-8')
            
            permissions_xml = "\n    ".join([
                f'<uses-permission android:name="{perm}" />' 
                for perm in permissions
            ])
            
            if "{{EXTRA_PERMISSIONS}}" in content:
                content = content.replace("{{EXTRA_PERMISSIONS}}", permissions_xml)
            else:
                manifest_tag = content.find("<manifest")
                if manifest_tag != -1:
                    insert_pos = content.find(">", manifest_tag) + 1
                    content = content[:insert_pos] + f"\n\n    {permissions_xml}" + content[insert_pos:]
            
            manifest_path.write_text(content, encoding='utf-8')
            logger.success("Permissions added successfully")
        
        except Exception as e:
            logger.error(f"Failed to add permissions: {e}")

    def generate(self):
        self.copy_template()
        self.replace_placeholders()
        self.rename_package()
        logger.success(f"Template generated successfully at {self.output_dir}")

    @staticmethod
    def validate_package_name(package_name: str) -> bool:
        pattern = r'^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$'
        return bool(re.match(pattern, package_name))
