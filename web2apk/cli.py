"""
Command-line interface for web2apk.
"""

import sys
from pathlib import Path
import click
from .logger import setup_logger, get_logger
from .config_loader import ConfigLoader, AppConfig
from .validators import InputValidator
from .dependency_checker import DependencyChecker


@click.group()
@click.version_option(version='0.1.0', prog_name='web2apk')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging (DEBUG level)')
@click.pass_context
def cli(ctx, verbose):
    """
    Web2APK - Convert websites to Android APK applications.
    
    Use 'web2apk COMMAND --help' for more information on a specific command.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    setup_logger(verbose=verbose)


@cli.command()
@click.option(
    '--config', '-c',
    required=True,
    type=click.Path(exists=True),
    help='Path to configuration file (YAML or JSON)'
)
@click.option(
    '--output', '-o',
    default='./dist',
    help='Output directory for generated APK (default: ./dist)',
    type=click.Path()
)
@click.option(
    '--skip-validation',
    is_flag=True,
    help='Skip asset file validation (not recommended)'
)
@click.pass_context
def build(ctx, config, output, skip_validation):
    """
    Build an APK from a website using the provided configuration.
    
    Example:
        web2apk build --config config.yml --output ./dist
    """
    logger = get_logger()
    
    logger.info("=" * 60)
    logger.info("Web2APK Builder v0.1.0")
    logger.info("=" * 60)
    
    logger.info(f"\nConfiguration: {config}")
    logger.info(f"Output Directory: {output}\n")
    
    logger.info("Step 1: Validating configuration file...")
    is_valid, error = InputValidator.validate_config_file(config)
    if not is_valid:
        logger.error(f"Configuration file validation failed: {error}")
        sys.exit(1)
    
    logger.info("Step 2: Loading and parsing configuration...")
    try:
        app_config = ConfigLoader.load_config(config)
        logger.success("✓ Configuration loaded successfully")
        logger.info(f"  - App Name: {app_config.app_name}")
        logger.info(f"  - Package ID: {app_config.package_id}")
        logger.info(f"  - URL: {app_config.url}")
        logger.info(f"  - Version: {app_config.version_name} (code: {app_config.version_code})")
        logger.info(f"  - Build Variant: {app_config.build_variant}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)
    
    if not skip_validation:
        logger.info("\nStep 3: Validating configuration values...")
        validation_errors = _validate_config_assets(app_config)
        if validation_errors:
            logger.error("Configuration validation failed:")
            for error in validation_errors:
                logger.error(f"  - {error}")
            sys.exit(1)
        logger.success("✓ Configuration validation passed")
    else:
        logger.warning("\nStep 3: Skipping asset validation (--skip-validation flag set)")
    
    logger.info("\nStep 4: Validating output directory...")
    is_valid, error = InputValidator.validate_output_dir(output)
    if not is_valid:
        logger.error(f"Output directory validation failed: {error}")
        sys.exit(1)
    logger.success(f"✓ Output directory ready: {Path(output).resolve()}")
    
    logger.info("\nStep 5: Checking dependencies...")
    checker = DependencyChecker()
    checker.check_all()
    checker.report()
    
    if not checker.all_dependencies_available():
        logger.error("Cannot proceed: Required dependencies are missing")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("Build Preparation Complete")
    logger.info("=" * 60)
    logger.info("\nNote: Actual APK building functionality will be implemented in future versions.")
    logger.info("The configuration has been validated and all dependencies are available.")
    
    logger.success("\n✓ Ready to build APK!")
    logger.info(f"\nBuild specification:")
    logger.info(f"  - Source URL: {app_config.url}")
    logger.info(f"  - Target Package: {app_config.package_id}")
    logger.info(f"  - Output: {Path(output).resolve()}")


@cli.command('init-config')
@click.option(
    '--format', '-f',
    type=click.Choice(['yaml', 'json'], case_sensitive=False),
    default='yaml',
    help='Configuration file format (default: yaml)'
)
@click.option(
    '--output', '-o',
    default=None,
    help='Output file path (default: config.yaml or config.json)',
    type=click.Path()
)
@click.option(
    '--force',
    is_flag=True,
    help='Overwrite existing file if it exists'
)
@click.pass_context
def init_config(ctx, format, output, force):
    """
    Generate a sample configuration file.
    
    Example:
        web2apk init-config --format yaml
        web2apk init-config --format json --output myconfig.json
    """
    logger = get_logger()
    
    logger.info("=" * 60)
    logger.info("Web2APK Configuration Generator")
    logger.info("=" * 60)
    
    format_lower = format.lower()
    
    if output is None:
        output = f"config.{format_lower}" if format_lower == 'yaml' else "config.json"
    
    output_path = Path(output)
    
    if output_path.exists() and not force:
        logger.error(f"Output file already exists: {output}")
        logger.error("Use --force to overwrite the existing file")
        sys.exit(1)
    
    logger.info(f"\nGenerating sample {format_lower.upper()} configuration...")
    
    try:
        config_content = ConfigLoader.generate_sample_config(format_type=format_lower)
        
        with open(output_path, 'w') as f:
            f.write(config_content)
        
        logger.success(f"✓ Sample configuration saved to: {output_path.resolve()}")
        logger.info("\nNext steps:")
        logger.info(f"  1. Edit {output_path} with your website details")
        logger.info(f"  2. Prepare icon and splash screen assets")
        logger.info(f"  3. Run: web2apk build --config {output_path}")
        
    except Exception as e:
        logger.error(f"Failed to generate configuration: {e}")
        sys.exit(1)


def _validate_config_assets(config: AppConfig) -> list:
    """
    Validate asset files referenced in configuration.
    
    Args:
        config: AppConfig object to validate
        
    Returns:
        List of validation error messages (empty if all valid)
    """
    errors = []
    
    if config.icons:
        icon_paths = {
            'mdpi': config.icons.mdpi,
            'hdpi': config.icons.hdpi,
            'xhdpi': config.icons.xhdpi,
            'xxhdpi': config.icons.xxhdpi,
            'xxxhdpi': config.icons.xxxhdpi,
        }
        
        for density, path in icon_paths.items():
            if path:
                is_valid, error = InputValidator.validate_image_file(path, f"Icon ({density})")
                if not is_valid:
                    errors.append(error)
    
    if config.splash and config.splash.image:
        is_valid, error = InputValidator.validate_image_file(
            config.splash.image, "Splash screen image"
        )
        if not is_valid:
            errors.append(error)
    
    if config.signing and config.signing.keystore_path:
        is_valid, error = InputValidator.validate_file_exists(
            config.signing.keystore_path, "Keystore file"
        )
        if not is_valid:
            errors.append(error)
    
    return errors


def main():
    """Main entry point for the CLI."""
    cli(obj={})


if __name__ == '__main__':
    main()
