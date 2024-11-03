# app/utils/ocr.py
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
from io import BytesIO
from PIL import Image

# Replace 'your_key' and 'your_endpoint' with your Azure Computer Vision API key and endpoint
AZURE_CV_KEY = "6aErkreLYeA7lb6REqmktno97PVYWHaZBCmowsfmTt8LQNrR6GLRJQQJ99AKACYeBjFXJ3w3AAAFACOGTZCo"
AZURE_CV_ENDPOINT = "https://enterprise-ai-project.cognitiveservices.azure.com/"

# Initialize the Computer Vision client
client = ComputerVisionClient(AZURE_CV_ENDPOINT, CognitiveServicesCredentials(AZURE_CV_KEY))

def detect_text(image_path):
    """
    Uses Azure Computer Vision to perform OCR on a given image file.
    :param image_path: str - Path to the image file
    :return: str - Extracted text
    """
    # Load the image
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Perform OCR on the image
    ocr_result = client.read_in_stream(BytesIO(image_data), raw=True)
    operation_id = ocr_result.headers["Operation-Location"].split("/")[-1]

    # Check the operation status until it is completed
    while True:
        result = client.get_read_result(operation_id)
        if result.status not in [OperationStatusCodes.not_started, OperationStatusCodes.running]:
            break

    # Process the OCR result
    text = ""
    if result.status == OperationStatusCodes.succeeded:
        for page in result.analyze_result.read_results:
            for line in page.lines:
                text += line.text + "\n"
    return text
