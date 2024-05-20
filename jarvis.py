import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import random
import sys
from PyQt5.QtCore import QThread

import time
from transformers import pipeline, Conversation
import os
import requests
import cv2  # pip install opencv-python
from requests import get  # pip install requests
import smtplib  # pip install secure-smtplib
import pyjokes  # pip install pyjokes
import pyautogui  # pip install pyautogui
import PyPDF2  # pip install PyPDF2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import instaloader  # pip install instaloader
import operator  # for calculation using voice
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow
from jarvisUi import Ui_jarvisUi
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import qrcode  # pip install qrcode[pil]

# Initialize text to speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Text to speech function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Wish the user based on the time of the day
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour < 12:
        speak(f"Good morning, it's {tt}")
    elif 12 <= hour < 18:
        speak(f"Good afternoon, it's {tt}")
    else:
        speak(f"Good evening, it's {tt}")
    speak("I am online sir. Please tell me how may I help you")


# Send email function
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail('your_email@example.com', to, content)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send this email.")


# Get news updates
def news():
    api_key = 'your_newsapi_api_key'
    main_url = f'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={api_key}'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    headlines = []
    for ar in articles:
        headlines.append(ar["title"])
    for i, headline in enumerate(headlines[:10]):
        speak(f"Today's {['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth'][i]} news is: {headline}")


# Read PDF file
def pdf_reader():
    book_path = 'py3.pdf'
    if not os.path.exists(book_path):
        speak("Sorry, the specified book does not exist.")
        return

    book = open(book_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this book is {pages}")
    speak("Please enter the page number you want to read")
    pg = int(input("Please enter the page number: "))
    if pg < 0 or pg >= pages:
        speak("Invalid page number.")
        return
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)


# Generate QR code
def generate_qr_code(data, file_name):
    img = qrcode.make(data)
    img.save(file_name)
    speak(f"QR code saved as {file_name}")


# Get user location based on IP
def get_user_location():
    try:
        ip = requests.get('https://api.ipify.org').text
        url = f"https://get.geojs.io/v1/ip/geo/{ip}.json"
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()
        city = geo_data['city']
        country = geo_data['country']
        return f"{city}, {country}"
    except Exception as e:
        print(f"Error fetching user location: {e}")
        return "unknown"


# Get local time
def get_local_time(location):
    try:
        current_time = datetime.datetime.now()
        speak(f"The current time in {location} is {current_time.strftime('%H:%M:%S')}")
        return current_time.strftime('%H:%M:%S')
    except Exception as e:
        speak(f"Sorry, I couldn't fetch the time for {location} at the moment.")
        return "unknown"


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 0.5
            audio = r.listen(source, timeout=5, phrase_time_limit=18)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
        except Exception as e:
            
            return "none"
        return query.lower()

    def run(self):
        speak("Please say 'wake up' to continue")
        while True:
            self.query = self.takecommand()
            if "wake up" in self.query or "are you there" in self.query or "hello" in self.query:
                self.TaskExecution()

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand()

            # Logic building for tasks
            if "open notepad" in self.query:
                npath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            elif "adobe reader" in self.query:
                apath = "C:\\Program Files\\Adobe\Acrobat DC\\Acrobat\Acrobat.exe"
                os.startfile(apath)

            elif "open command prompt" in self.query:
                os.system("start cmd")

            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "play music" in self.query:
                music_dir = "E:\\Ddrive\\music"
                songs = os.listdir(music_dir)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("Searching Wikipedia...")
                query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)

            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "open facebook" in self.query:
                webbrowser.open("www.facebook.com")

            elif "open stackoverflow" in self.query:
                webbrowser.open("www.stackoverflow.com")

            elif "open google" in self.query:
                speak("Sir, what should I search on Google?")
                cm = self.takecommand()
                webbrowser.open(f"{cm}")

            elif "send email" in self.query:
                try:
                    speak("Please tell the recipient's email address:")
                    recipient = self.takecommand()  # User dictates the recipient's email address
                    speak("What should I say in the email?")
                    content = self.takecommand().lower()  # User dictates the email content
                    speak("Confirm sending email to " + recipient + ". Should I proceed?")
                    confirmation = self.takecommand().lower()  # User confirms sending the email
                    if "yes" in confirmation:
                        to = recipient  # Set the recipient's email address
                        sendEmail(to, content)  # Assuming you have a function named sendEmail to send emails
                        speak("Email has been sent to " + recipient)
                    else:
                        speak("Email sending cancelled")
                except Exception as e:
                    print(e)
                    speak("Sorry sir, I am not able to send this email")

            elif "you can sleep" in self.query or "sleep now" in self.query:
                speak("Okay sir, I am going to sleep. You can call me anytime.")
                break
                


            #to close any application
            elif "close notepad" in self.query:
                speak("okay sir, closing notepad")
                os.system("taskkill /f /im notepad.exe")

            #to set an alarm
            elif "set alarm" in self.query:
                nn = int(datetime.datetime.now().hour)
                if nn==22: 
                    music_dir = 'E:\\music'
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, songs[0]))
            #to find a joke
            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            # elif "shut down the system" in self.query:
            #     os.system("shutdown /s /t 5")

            # elif "restart the system" in self.query:
            #     os.system("shutdown /r /t 5")

            # elif "sleep the system" in self.query:
            #     os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "hello" in self.query or "hey" in self.query:
                speak("hello sir, may i help you with something.")
            
            elif "how are you" in self.query:
                speak("i am fine sir, what about you.")

            elif "thank you" in self.query or "thanks" in self.query:
                speak("it's my pleasure sir.")



            ###################################################################################################################################
            ###########################################################################################################################################



            elif 'switch the window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
                    

            elif "tell me news" in self.query:
                speak("please wait sir, feteching the latest news")
                news()


           

            ##########################################################################################################################################
            ###########################################################################################################################################

            elif "do some calculations" in self.query or "can you calculate" in self.query:            
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Say what you want to calculate, example: 3 plus 3")
                    print("listening.....")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string=r.recognize_google(audio)
                print(my_string)
                def get_operator_fn(op):
                    return {
                        '+' : operator.add,
                        '-' : operator.sub,
                        'x' : operator.mul,
                        'divided' :operator.__truediv__,
                        'Mod' : operator.mod,
                        'mod' : operator.mod,
                        '^' : operator.xor,
                        }[op]
                def eval_binary_expr(op1, oper, op2):
                    op1,op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)
                print(eval_binary_expr(*(my_string.split())))


            #-----------------To find my location using IP Address

            elif "where i am" in self.query or "where we are" in self.query:
                speak("wait sir, let me check")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    # print(geo_data)
                    city = geo_data['city']
                    # state = geo_data['state']
                    country = geo_data['country']
                    speak(f"sir i am not sure, but i think we are in {city} city of {country} country")
                except Exception as e:
                    speak("sorry sir, Due to network issue i am not able to find where we are.")
                    pass


            

            #-------------------To check a instagram profile----
            elif "instagram profile" in  self.query or "profile on instagram" in self.query:
                speak("sir please enter the user name correctly.")
                name = input("Enter username here:")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"Sir here is the profile of the user {name}")
                time.sleep(5)
                speak("sir would you like to download profile picture of this account.")
                condition = self.takecommand()
                if "yes" in condition:
                    mod = instaloader.Instaloader() #pip install instadownloader
                    mod.download_profile(name, profile_pic_only=True)
                    speak("i am done sir, profile picture is saved in our main folder. now i am ready for next command")
                else:
                    pass

            #-------------------  To take screenshot -------------
            elif "take screenshot" in self.query or "take a screenshot" in self.query:
                speak("sir, please tell me the name for this screenshot file")
                name = self.takecommand()
                speak("please sir hold the screen for few seconds, i am taking sreenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("i am done sir, the screenshot is saved in our main folder. now i am ready for next command")


            # speak("sir, do you have any other work")

            #-------------------  To Read PDF file -------------
            elif "read pdf" in self.query:
                pdf_reader()

            #--------------------- To Hide files and folder ---------------
            elif "hide all files" in self.query or "hide this folder" in self.query or "visible for everyone" in self.query:
                speak("sir please tell me you want to hide this folder or make it visible for everyone")
                condition = self.takecommand()
                if "hide" in condition:
                    os.system("attrib +h /s /d") #os module
                    speak("sir, all the files in this folder are now hidden.")                

                elif "visible" in condition:
                    os.system("attrib -h /s /d")
                    speak("sir, all the files in this folder are now visible to everyone. i wish you are taking this decision in your own peace.")
                    
                elif "leave it" in condition or "leave for now" in condition:
                    speak("Ok sir")

            elif "temperature" in self.query:
                search = "weather in delhi"
                url = f"https://www.google.com/search?q={search}"
                req = requests.get(url)
                save = BeautifulSoup(req.text,"html.parser")
                tempp = save.find("div",class_= "BNeawe").text
                speak(f"current {search} is {tempp}")

            elif "generate qr code" in self.query:
                speak("Please tell me the data for the QR code.")
                data = self.takecommand().lower()
                speak("Please tell me the file name to save the QR code as (e.g., 'my_qr_code.png').")
                file_name = self.takecommand().lower()
                generate_qr_code(data, file_name)


            elif "where am i" in self.query or "where we are" in self.query:
                speak("Wait sir, let me check")
                try:
                    location = get_user_location()
                    speak(f"Sir, I am not sure, but I think we are in {location}")
                except Exception as e:
                    speak("Sorry sir, due to network issue I am not able to find where we are.")
                    pass

            
            elif "email" in self.query:
                try:
                    speak("Please tell the recipient's email address:")
                    recipient = self.takecommand()  # User dictates the recipient's email address
                    speak("What should I say in the email?")
                    content = self.takecommand().lower()  # User dictates the email content
                    speak("Confirm sending email to " + recipient + ". Should I proceed?")
                    confirmation = self.takecommand().lower()  # User confirms sending the email
                    if "yes" in confirmation:
                        to = recipient  # Set the recipient's email address
                        sendEmail(to, content)  # Assuming you have a function named sendEmail to send emails
                        speak("Email has been sent to " + recipient)
                    else:
                        speak("Email sending cancelled")
                except Exception as e:
                    print(e)
                    speak("Sorry sir, I am not able to send this email")
                       

            elif "time" in self.query:
                if "now" in self.query:  # Check if the user wants to know the time in their location
                    user_location = get_user_location()
                    current_time = get_local_time(user_location)
                    speak(f"The current time in {user_location} is {current_time}")
                elif "in" in self.query:  # Check if the user wants to know the time in a specified location
                    country = self.query.split("in")[-1].strip().lower()
                    current_time = get_local_time(country)
                    speak(f"The current time in {country.capitalize()} is {current_time}")
                else:
                    speak("I'm sorry, I didn't catch that. Can you please repeat?")

    
            elif "volume up" in self.query or "increase" in self.query:
                pyautogui.press("volumeup")
            elif "volume down" in self.query or "decrease" in self.query:
                pyautogui.press("volumedown")
            elif "volume mute" in self.query or "mute" in self.query:
                pyautogui.press("volumemute")


            elif "shutdown" in self.query or "shut down" in self.query:
                speak("Thank you for using Jarvis. Have a good day, sir.")
                sys.exit()

            elif "you can sleep now" in self.query:
                speak("Thanks, sir you can call me anytime.")
                break           

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:\\Users\\gprash\\Downloads\\jarvis ui\\Motion Graphics.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("E:/wallpaper/jar/intial.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

#self.textBrowser.setText("Hello world")
 #       self.textBrowser.setAlignment(QtCore.Qt.AlignCenter)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())
