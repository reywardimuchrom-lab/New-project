"""
Command-line interface for the APK decompiler.
"""

import sys
from pathlib import Path
import click
from .logger import setup_logger, get_logger
from .validator import InputValidator
from .dependency_checker import DependencyChecker


@click.command()
@click.argument('apk_path', type=click.Path(exists=True))
@click.option(
    '--output-dir', '-o',
    default='./output',
    help='Output directory for decompiled files (default: ./output)',
    type=click.Path()
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose logging (DEBUG level)'
)
@click.version_option(version='0.1.0', prog_name='APK Decompiler')
def main(apk_path: str, output_dir: str, verbose: bool):
    """
    APK Decompiler - Decompile and analyze Android APK files.
    
    APK_PATH: Path to the APK file to decompile
    """
    setup_logger(verbose=verbose)
    logger = get_logger()
    
    logger.info("=" * 60)
    logger.info("APK Decompiler v0.1.0")
    logger.info("=" * 60)
    
    logger.info(f"\nAPK File: {apk_path}")
    logger.info(f"Output Directory: {output_dir}\n")
    
    is_valid, error = InputValidator.validate_inputs(apk_path, output_dir)
    if not is_valid:
        logger.error(f"Validation failed: {error}")
        sys.exit(1)
    
    checker = DependencyChecker()
    checker.check_all()
    checker.report()
    
    if not checker.all_dependencies_available():
        logger.warning("Some dependencies are missing. The tool may not function properly.")
        logger.warning("Please install missing dependencies before proceeding with decompilation.")
    
    logger.info("=" * 60)
    logger.info("Setup Complete - Ready for Decompilation")
    logger.info("=" * 60)
    logger.info("\nNote: Actual decompilation functionality will be implemented in future versions.")
    
    apk_name = Path(apk_path).stem
    logger.info(f"APK: {apk_name}")
    logger.info(f"Output will be saved to: {Path(output_dir).resolve()}")
    
    logger.success("\n✓ Validation and dependency checks completed successfully!")


if __name__ == '__main__':
    main()
