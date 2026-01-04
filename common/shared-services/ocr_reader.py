#!/usr/bin/env python3
"""
OCR Script to extract text from PNG images
Requires: pytesseract, Pillow
Install with: pip install pytesseract Pillow
"""

import pytesseract
from PIL import Image
import sys
import os

def extract_text_from_image(image_path):
    """
    Extract text from an image file using OCR
    """
    try:
        # Open the image file
        image = Image.open(image_path)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(image)
        
        return text
    except Exception as e:
        return f"Error processing image: {str(e)}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python ocr_reader.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found")
        sys.exit(1)
    
    print(f"Extracting text from: {image_path}")
    print("=" * 50)
    
    extracted_text = extract_text_from_image(image_path)
    
    if extracted_text:
        print(extracted_text)
    else:
        print("No text could be extracted from the image.")

if __name__ == "__main__":
    main()
