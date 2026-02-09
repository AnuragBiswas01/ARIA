"""
ARIA Logging Setup
Provides a rich, colorful logging experience for development and production.
"""
import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console

from config.settings import settings

# Ensure log directory exists
LOG_DIR = Path("./data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "aria.log"


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Sets up the root logger with Rich console handler and file handler.
    
    Args:
        level: The logging level (default: INFO).
        
    Returns:
        The configured root logger.
    """
    console = Console()

    # Rich console handler for beautiful terminal output
    console_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        rich_tracebacks=True,
        tracebacks_show_locals=settings.debug,
    )
    console_handler.setLevel(level)

    # File handler for persistent logs
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # Log everything to file
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Suppress noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Gets a logger with the specified name.
    
    Args:
        name: The name of the logger (usually __name__).
    
    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name)
