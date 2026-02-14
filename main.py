"""Main entry point for the SmartSurveillance application."""

import sys
import logging
from src.gui import main as gui_main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('smartsurveillance.log'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    try:
        gui_main()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
