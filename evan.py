import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit

listener = sr.Recognizer()
engine = pyttsx3.init()
def talk(text): 
    engine.say(text) 
    engine.runAndWait()

def get_instruction():
    global instruction
    try:
        with sr.Microphone(device_index=0) as origin:
            print("listening")
            listener.adjust_for_ambient_noise(origin,duration=1)
            speech = listener.listen(origin)
            instruction =listener.recognize_google(speech)
            instruction = instruction.lower()
            instruction =instruction.replace('EVAN', "")
            print(instruction)
            return instruction

    except sr.WaitTimeoutError:
        print("Timeout waiting for speech input")
    except sr.UnknownValueError: 
        print("Unable to recognize speech") 
    except sr.RequestError as e: 
        print("Error in request to speech recognition service; {0}".format(e))
class MyVirtualAssistantApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 500, 500)
        
        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)
        self.text_output.setFontPointSize(12)
        self.text_output.setGeometry(10, 10, 480, 400)  # Adjust text box size

        self.button = QPushButton("TRY EVAN", self)
        self.button.setGeometry(10, 420, 480, 50)  # Adjust button size
        self.button.clicked.connect(self.play_instruction)

        self.exit_button = QPushButton("EXIT", self)  # Add exit button
        self.exit_button.setGeometry(10, 480, 480, 50)  # Position of exit button
        self.exit_button.clicked.connect(self.exit_application)

        layout = QVBoxLayout()
        layout.addWidget(self.text_output)
        layout.addWidget(self.button)
        layout.addWidget(self.exit_button)  # Add exit button to layout
        self.setLayout(layout)
        
    def exit_application(self):
        talk("Goodbye! Have a good day!")
        self.text_output.append("Goodbye! Have a good day!")  # Display in the GUI
        QApplication.quit() 
        sys.exit()
        
    def play_instruction(self):
        instruction = get_instruction()
        if not instruction:
            output_text = "I didn't catch that. Could you repeat?"
            talk(output_text)
            self.text_output.append(output_text)
            return

        if "play" in instruction:
            song = instruction.replace('play', "").strip()
            talk("playing " + song)
            output_text = "Playing " + song
            pywhatkit.playonyt(song)
        elif 'hello' in instruction or 'hi' in instruction:
            talk('Hello, I am Evan, your virtual assistant.')
            output_text = 'Hello, I am Evan, your virtual assistant.'
        elif 'time' in instruction:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + time)
            output_text = 'The current time is ' + time
        elif 'date' in instruction:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            talk("Today's date is " + date)
            output_text = "Today's date is " + date
        elif 'how are you' in instruction:
            talk('I am good, how are you?')
            output_text = 'I am good, how are you?'
        elif 'who are you' in instruction or 'your name' in instruction:
            talk('I am Evan, your virtual assistant.')
            output_text = 'I am Evan, your virtual assistant.'
        elif 'who is' in instruction or 'what is' in instruction:
            thing = instruction.replace('who is', '').replace('what is', '').strip()
        elif 'bye' in instruction:
            self.exit_application()
            return
            try:
                info = wikipedia.summary(thing, sentences=2)
                talk(info)
                output_text = info
            except wikipedia.exceptions.PageError:
                output_text = f"Sorry, I couldn't find anything about {thing} on Wikipedia."
                talk(output_text)
            except wikipedia.exceptions.DisambiguationError:
                output_text = f"Sorry, there are multiple matches for {thing}. Please be more specific."
                talk(output_text)
        else:
            output_text = "Please repeat!"
            talk("Please repeat!")

        self.text_output.append(output_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyVirtualAssistantApp()
    window.show()
    sys.exit(app.exec_())

play_instruction()