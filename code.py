import sys
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont


# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Worker thread for speech recognition
class SpeechRecognitionThread(QThread):
    text_recognized = pyqtSignal(str)

    def run(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise once at the start
            while True:
                try:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)  # Continuous listening
                    text = recognizer.recognize_google(audio, show_all=False)  # No extra results for faster response
                    if text:  # Only emit recognized text if it's not empty
                        print(f"Recognized: {text}")
                        self.text_recognized.emit(text)
                except sr.UnknownValueError:
                    # Suppress error output if speech is not recognized
                    pass
                except sr.RequestError as e:
                    # Suppress error output if there's a request error
                    pass
                except sr.WaitTimeoutError:
                    # Suppress timeout errors
                    pass
                except Exception as e:
                    # Catch other potential errors
                    pass

# Main PyQt5 GUI
class SpeechToTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.recognition_thread = SpeechRecognitionThread()
        self.recognition_thread.text_recognized.connect(self.update_text)
        self.recognition_thread.start()

    def init_ui(self):
        self.setWindowTitle("Speech-to-Text")
        self.layout = QVBoxLayout()

        # Set up the label with a clean, modern font and a large size
        self.label = QLabel("Listening for speech...")
        font = QFont("Helvetica", 32, QFont.Bold)  # Set font to Helvetica, 32, bold
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)  # Center the text
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        # Set background color and text color for better contrast
        self.setStyleSheet("background-color: #f0f0f0;")
        self.label.setStyleSheet("color: #333333;")  # Dark text color for readability

        # Add some padding and set window size
        self.setLayout(self.layout)
        self.resize(800, 400)

    def update_text(self, text):
        self.label.setText(text)
        if text.lower() == "quit":
            self.close()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SpeechToTextApp()
    main_window.show()
    sys.exit(app.exec_())
