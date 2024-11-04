# app/utils/tts.py
import azure.cognitiveservices.speech as speechsdk

def speak_text(text):
    speech_config = speechsdk.SpeechConfig(subscription="", region="eastus")
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    synthesizer.speak_text_async(text).get()
