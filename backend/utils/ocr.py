"""
ARIA OCR Utility
Wrapper around Tesseract OCR.
"""
import pytesseract
from PIL import Image
from config.settings import settings
from utils.logger import get_logger
import os

logger = get_logger(__name__)

# Set Tesseract path
if os.path.exists(settings.tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path
else:
    logger.warning(f"Tesseract executable not found at {settings.tesseract_path}")

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from an image file using Tesseract.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"OCR failed for {image_path}: {e}")
        return ""

def check_tesseract_available() -> bool:
    """Checked if Tesseract is configured and runnable."""
    try:
        return os.path.exists(settings.tesseract_path)
    except Exception:
        return False
