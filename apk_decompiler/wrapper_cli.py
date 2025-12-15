import sys
import click
from pathlib import Path
from .logger import setup_logger, get_logger
from .template_manager import TemplateManager


@click.command()
@click.option(
    '--url', '-u',
    required=True,
    help='Target URL to load in the WebView'
)
@click.option(
    '--package', '-p',
    required=True,
    help='Android package name (e.g., com.example.myapp)'
)
@click.option(
    '--name', '-n',
    required=True,
    help='Application name'
)
@click.option(
    '--output-dir', '-o',
    default='./android_wrapper',
    help='Output directory for the generated project',
    type=click.Path()
)
@click.option(
    '--icon', '-i',
    help='Path to app icon (PNG/JPEG, will be resized for all densities)',
    type=click.Path(exists=True)
)
@click.option(
    '--user-agent',
    help='Custom user agent string',
    default=None
)
@click.option(
    '--offline/--no-offline',
    default=True,
    help='Enable offline caching support'
)
@click.option(
    '--file-access/--no-file-access',
    default=False,
    help='Enable file access in WebView'
)
@click.option(
    '--permission',
    multiple=True,
    help='Additional Android permissions (can be specified multiple times)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose logging'
)
def generate_wrapper(
    url: str,
    package: str,
    name: str,
    output_dir: str,
    icon: str,
    user_agent: str,
    offline: bool,
    file_access: bool,
    permission: tuple,
    verbose: bool
):
    """
    Generate an Android WebView wrapper project from template.
    
    Creates a complete Android project that wraps a web URL in a native WebView
    with offline support, custom settings, and production-ready configuration.
    
    Example:
        apk-wrapper generate-wrapper \\
            --url https://example.com \\
            --package com.example.myapp \\
            --name "My App" \\
            --icon ./icon.png \\
            --offline
    """
    setup_logger(verbose=verbose)
    logger = get_logger()
    
    logger.info("=" * 60)
    logger.info("Android WebView Wrapper Generator")
    logger.info("=" * 60)
    
    if not TemplateManager.validate_package_name(package):
        logger.error(f"Invalid package name: {package}")
        logger.error("Package name must follow Java package naming conventions:")
        logger.error("  - Start with lowercase letter")
        logger.error("  - Contain at least one dot")
        logger.error("  - Use only lowercase letters, numbers, and underscores")
        logger.error("  - Example: com.example.myapp")
        sys.exit(1)
    
    logger.info(f"\nConfiguration:")
    logger.info(f"  URL: {url}")
    logger.info(f"  Package: {package}")
    logger.info(f"  Name: {name}")
    logger.info(f"  Output: {output_dir}")
    logger.info(f"  Offline Mode: {offline}")
    logger.info(f"  File Access: {file_access}")
    if user_agent:
        logger.info(f"  User Agent: {user_agent}")
    if icon:
        logger.info(f"  Icon: {icon}")
    if permission:
        logger.info(f"  Extra Permissions: {', '.join(permission)}")
    logger.info("")
    
    try:
        manager = TemplateManager(output_dir)
        
        manager.configure(
            package_name=package,
            app_name=name,
            target_url=url,
            user_agent=user_agent,
            enable_offline=offline,
            enable_file_access=file_access,
            extra_permissions=list(permission) if permission else None
        )
        
        manager.generate()
        
        if icon:
            manager.add_icon(icon)
        
        logger.info("=" * 60)
        logger.success("✓ Android wrapper generated successfully!")
        logger.info("=" * 60)
        logger.info(f"\nNext steps:")
        logger.info(f"  1. cd {output_dir}")
        logger.info(f"  2. ./gradlew assembleDebug")
        logger.info(f"  3. Find APK in: app/build/outputs/apk/debug/")
        logger.info("")
        logger.info(f"For release build:")
        logger.info(f"  ./gradlew assembleRelease")
        logger.info("")
        
    except FileNotFoundError as e:
        logger.error(f"Template not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to generate wrapper: {e}")
        if verbose:
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    generate_wrapper()
