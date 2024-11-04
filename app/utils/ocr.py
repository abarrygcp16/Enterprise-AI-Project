from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
import os

# Replace 'with_subscription_key' and 'subscrition_endpoint' with Azure Computer Vision API key and endpoint.
subscription_key = ""
endpoint = ""

def extract_text_from_image(image_path):
    # Initialize the Computer Vision client
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # Read the image file
    with open(image_path, "rb") as image_stream:
        # Send the image to the Computer Vision API for OCR
        read_operation = computervision_client.read_in_stream(image_stream, raw=True)

    # Get the operation location (operation ID)
    operation_location = read_operation.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # Wait for the OCR operation to complete
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in [OperationStatusCodes.running]:
            break
        time.sleep(1)

    # Collect and return text
    text = ""
    if read_result.status == OperationStatusCodes.succeeded:
        for page in read_result.analyze_result.read_results:
            for line in page.lines:
                text += line.text + "\n"

    return text

