import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name=__name__, log_level=logging.INFO):
    """Configure a logger with file rotation and console output.
    
    Args:
        name: Logger name (usually __name__)
        log_level: Defaults to INFO
        
    Returns:
        Configured logger instance
    """
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # File handler (rotates when >5MB)
    file_handler = RotatingFileHandler(
        'logs/twitter.log',
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler (shows warnings+)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger