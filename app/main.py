import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from utils.tts import speak  # Import the speak function from tts.py
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from kivy.core.window import Window
import azure.cognitiveservices.speech as speechsdk
from utils.ocr import extract_text_from_image  # OCR function
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

kivy.require('2.0.0')

# Set window size
Window.size = (800, 600)

class MainApp(App):
    def build(self):
        self.camera_active = False
        # Main layout container
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Camera widget setup
        self.camera = Camera(play=False)
        self.layout.add_widget(self.camera)

        # Start/Stop Camera Button
        self.camera_button = Button(text='Start Camera', size_hint=(1, 0.1))
        self.camera_button.bind(on_press=self.toggle_camera)
        self.layout.add_widget(self.camera_button)

        # Capture Button to capture the labels on objects
        capture_button = Button(text='Capture label', size_hint=(1, 0.1))
        capture_button.bind(on_press=self.capture_image)
        self.layout.add_widget(capture_button)

        # Display box to display the captured text
        self.text_display_box = BoxLayout(size_hint=(1, 0.3), padding=5)
        self.text_label = TextInput(text='', readonly=True, font_size=16, background_color=(0.9, 0.9, 0.9, 1), foreground_color=(0, 0, 0, 1))
        self.text_display_box.add_widget(self.text_label)
        self.layout.add_widget(self.text_display_box)

        # Speak Button to read out the capture labels on objects
        speak_button = Button(text='Read label', size_hint=(1, 0.1))
        speak_button.bind(on_press=self.speak_text)
        self.layout.add_widget(speak_button)

        # Close App Button
        close_button = Button(text='Close App', size_hint=(1, 0.1))
        close_button.bind(on_press=self.stop_app)
        self.layout.add_widget(close_button)

        print("App built successfully!")
        return self.layout
    
    # Function to start or stop the camera based on camera state
    def toggle_camera(self, instance):
        if self.camera_active:
            self.camera.play = False
            self.camera_button.text = 'Start Camera'
            self.camera_active = False
        else:
            self.camera.play = True
            self.camera_button.text = 'Stop Camera'
            self.camera_active = True

    def capture_image(self, instance):
        if self.camera_active:
            image_path = "captured_image.png"
            self.camera.export_to_png(image_path)
            print("Image captured and saved successfully!")

            # Show a popup to indicate capture success
            popup_content = BoxLayout(orientation='vertical')
            popup_content.add_widget(Label(text="Image captured successfully!"))
            close_button = Button(text="Close", size_hint=(1, 0.3))
            close_button.bind(on_press=lambda x: self.popup.dismiss())
            popup_content.add_widget(close_button)

            self.popup = Popup(title="Success", content=popup_content, size_hint=(0.6, 0.4))
            self.popup.open()

            # Schedule popup to auto-dismiss after 2 seconds
            Clock.schedule_once(lambda dt: self.popup.dismiss(), 2)

            # Extract text from the captured image
            extracted_text = self.extract_text(image_path)
            self.text_label.text = extracted_text if extracted_text else "No text found."
        else:
            error_popup = Popup(title='Error', content=Label(text='Please start the camera first.'), size_hint=(0.6, 0.4))
            error_popup.open()

    def extract_text(self, image_path):
        # Ensure image exists before processing
        if not os.path.exists(image_path):
            print("Image file does not exist.")
            return None

        # Call the OCR function and handle errors
        try:
            extracted_text = extract_text_from_image(image_path)
            print("Extracted Text:", extracted_text)
            return extracted_text
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None

    def speak_text(self, instance):
        """Invoke TTS to speak the captured text."""
        text_to_read = self.text_label.text
        if text_to_read:
            speak(text_to_read)  # Directly call speak from tts.py


    def stop_app(self, instance):
        App.get_running_app().stop()

if __name__ == "__main__":
    MainApp().run()
