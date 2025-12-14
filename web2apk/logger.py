"""
Logging configuration for web2apk.
"""

import sys
from loguru import logger


def setup_logger(verbose=False):
    """
    Configure logging for the application.
    
    Args:
        verbose: If True, enable DEBUG level logging, otherwise INFO level
    """
    logger.remove()
    
    log_level = "DEBUG" if verbose else "INFO"
    
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=log_level,
        colorize=True,
    )
    
    return logger


def get_logger():
    """
    Get the configured logger instance.
    
    Returns:
        Logger instance
    """
    return logger
