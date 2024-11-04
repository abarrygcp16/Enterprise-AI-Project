import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from kivy.core.window import Window
import azure.cognitiveservices.speech as speechsdk
from utils.ocr import extract_text_from_image  # This is the OCR function


kivy.require('2.0.0')

# This is setting the windows size for the application
Window.size = (800, 600)

class MainApp(App):
    def build(self):
        # Main layout container
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Camera widget setup
        self.camera = Camera(play=True, resolution=(640, 480))
        self.camera.size_hint = (1, 0.6)  # 60% of the window height
        self.layout.add_widget(self.camera)

        # Label to display extracted text
        self.text_label = Label(text='', size_hint=(1, 0.1), font_size=18)
        self.layout.add_widget(self.text_label)

        # Capture Button to capture the labels on objects
        capture_button = Button(text='Capture label', size_hint=(1, 0.1), font_size=18)
        capture_button.bind(on_press=self.capture_image)
        self.layout.add_widget(capture_button)

        # Speak Button to read out the capture labels on objects
        speak_button = Button(text='Read label', size_hint=(1, 0.1), font_size=18)
        speak_button.bind(on_press=self.speak_text)
        self.layout.add_widget(speak_button)

        print("App built successfully!")
        return self.layout
    
    def capture_image(self, instance):
        # Capture a frame from the camera
        self.camera.export_to_png("captured_image.png")
        # Extract text from the captured image
        extracted_text = extract_text_from_image("captured_image.png")
        self.text_label.text = extracted_text or "No text detected."

    def speak_text(self, instance):
        # Speak the text displayed in the text_label
        text_to_read = self.text_label.text
        if text_to_read:
            self.speak(text_to_read)

    def speak(self, text):
        # Set up Azure Speech SDK for text-to-speech
        speech_config = speechsdk.SpeechConfig(subscription="", region="eastus")
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        synthesizer.speak_text_async(text).get()

if __name__ == "__main__":
    MainApp().run()
