# app/utils/tts.py
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os


# Loading environment variables from .env file since this repository is public
load_dotenv

def speak_text(text):
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_SUBSCRIPTION"), region=os.getenv("AZURE_RESION"))
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    synthesizer.speak_text_async(text).get()
