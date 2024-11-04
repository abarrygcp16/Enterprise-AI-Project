# app/utils/test_ocr.py
from ocr import detect_text

def test_detect_text():
    # Use a sample image with known text
    image_path = "test_image_with_text.jpg"  
    text = detect_text(image_path)
    assert text.strip() == "Expected text", f"Expected text, got {text}"
