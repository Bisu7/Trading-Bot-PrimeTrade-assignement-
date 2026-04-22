import sys
from loguru import logger
import os

def setup_logging():
    """Configure loguru for both console and file logging."""
    # Ensure logs directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Remove default handler
    logger.remove()

    # Console handler (Clean and informative)
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )

    # File handler (Detailed for debugging and audit)
    logger.add(
        os.path.join(log_dir, "trade_log.log"),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB"
    )

    return logger
