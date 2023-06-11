from pickletools import pylist
import shutil
import sys
import requests
import wolframalpha
import wikipedia
import pyttsx3
import cv2
import os
#import face_recognition
import numpy as np
import webbrowser
import speech_recognition as sr
import datetime
import random
import PyPDF2
from pywikihow import search_wikihow
import pywhatkit as kit
import pyautogui
import pyjokes
import keyboard
#from PyDictionary import PyDictionary as pd
from playsound import playsound
from googletrans import Translator
from prsaw import RandomStuff
from bs4 import BeautifulSoup
import psutil
import pytube
import time
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
from instabot import Bot
import speedtest

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voices', voices[1].id)
engine.setProperty('rate', 180)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

path = 'ImageDirectory'
images = []
classnames = []
 #myList = os.listdir(path)
print(pylist)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classnames.append(os.path.splitext(cl)[0])
    print(classnames)


def face_recognizer():
    """This Function recognizes the face by calculating the minimum face encodings"""
    try:
        success, img = cap.read()
        time.sleep(0.5)
        img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

        encodeListKnown = find_encodings(images)
        print('Encoding Completed')

        facesCurFrame = face_recognition.face_locations(img_small)
        encodeCurFrame = face_recognition.face_encodings(img_small, facesCurFrame)
        print(facesCurFrame)
        print(encodeCurFrame)
        for encodeFace, faceloc in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDistance)

            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                name = classnames[matchIndex].upper()
                print(name)
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y1 - 35), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                speak("Face detected")
                wishMe(name)
                cap.release()
                cv2.destroyAllWindows()
            else:
                print("Unknown user!!")
                person_not_known()

    except:
        speak("Camera error")
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            speak(f"Good Morning!")
        elif 12 <= hour < 18:
            speak(f"Good Afternoon!")
        elif hour > 18:
            speak(f"Good Evening!")
        else:
            speak(f"Unknown time!")
        speak("I am Zira. Please tell me, How can i help you!")


def find_encodings(image):
    """This function is used toh find the encodings of the faces"""
    encodeList = []
    for img in image:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        return encodeList


def person_not_known():
    """This function is for the unknown faces or the new user"""
    en_name = input("Enter your name: ")
    return_value, image = cap.read()
    val = en_name + '.jpg'
    cv2.imwrite(val, image)
    shutil.move(val, path)
    wishMe(en_name)
    images.append(val)
    cap.release()
    cv2.destroyAllWindows()
    find_encodings(images)


def wishMe(newname):
    """This function wishes the user"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print(f"Good Morning!{newname}")
        speak(f"Good Morning!{newname}")
    elif 12 <= hour < 18:
        print(f"Good Afternoon!{newname}")
        speak(f"Good Afternoon!{newname}")
    elif hour > 18:
        print(f"Good Evening!{newname}")
        speak(f"Good Evening!{newname}")
    else:
        print(f"Unknown time {newname}")
        speak(f"Unknown time {newname}")
    print("I am Zira. Please tell me, How can i help you!")
    speak("I am Zira. Please tell me, How can i help you!")


def speak(audio):
    """This Function provides an engine to speech"""
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    """This function takes command from the user and recognize it with the help of google"""
    # it takes microphone information and returns strings as output
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # r.energy_threshold = 500
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            # print(e)
            print("Say that again please...")
            speak("Say that again please...")
            return "None"
        query = query.lower()
        return query


def OpenApps():
    """This function is used to open applications"""
    print("Ok, wait a second!")
    speak("Ok, wait a second!")
    if 'pycharm' in query:
        os.startfile("C:\\Program Files\\JetBrains\\PyCharm Community Edition 2021.2.2\\bin\\pycharm64.exe")
    elif 'visual studio code' in query:
        os.startfile("C:\\Users\\91888\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
    elif 'chrome' in query:
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif 'Telegram' in query:
        os.startfile("C:\\Users\\91888\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")
    elif 'Grammarly' in query:
        os.startfile("C:\\Users\\91888\\AppData\\Local\\GrammarlyForWindows\\GrammarlyForWindows.exe")

    print("Command successfully executed..")
    speak("Command successfully executed..")


def CloseApps():
    """This function is used to close applications"""
    print("Ok, wait a second")
    speak("Ok, wait a second")
    if 'pycharm' in query:
        os.system("TASKKILL /f /im pycharm64.exe")
    elif 'chrome' in query:
        os.system("TASKKILL /f /im chrome.exe")
    elif 'visual studio code' in query:
        os.system("TASKKILL /f /im Code.exe")
    elif 'notepad' in query:
        os.system("TASKKILL /f /im notepad.exe")
    elif 'Telegram' in query:
        os.system("TASKKILL /f /im Telegram.exe")
    elif 'Grammarly' in query:
        os.system("TASKKILL /f /im GrammarlyForWindows.exe")
    print("Done!")
    speak("Done!")


def Dict():
    """This function is used to access dictionary, which can also be used for synonym and antonym"""
    print("Activated Dictionary!")
    speak("Activated Dictionary!")
    print("Tell me the problem.. I am there to help you!")
    speak("Tell me the problem.. I am there to help you!")
    problem = takeCommand()
    if 'meaning' in problem:
        problem = problem.replace("what is the", "")
        problem = problem.replace("zira", "")
        problem = problem.replace("meaning of", "")
        result = pd.meaning(problem)
        print(f"The meaning for {problem} is {result}")
        speak(f"The meaning for {problem} is {result}")

    elif 'synonym' in problem:
        problem = problem.replace("what is the", "")
        problem = problem.replace("zira", "")
        problem = problem.replace("synonym of", "")
        result = pd.synonym(problem)
        print(f"The synonym for {problem} is {result}")
        speak(f"The synonym for {problem} is {result}")

    elif 'synonym' in problem:
        problem = problem.replace("what is the", "")
        problem = problem.replace("zira", "")
        problem = problem.replace("antonym of", "")
        sol = pd.antonym(problem)
        print(f"The antonym for {problem} is {sol}")
        speak(f"The antonym for {problem} is {sol}")


def TakeHindi():
    """This function is to take command in hindi from the user"""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 500
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='hi')
            print(f"User said: {query}\n")

        except Exception as e:
            # print(e)
            print("Say that again please...")
            speak("Say that again please...")
            return "None"
        return query


def tran():
    """This function is used to translate the hindi lines into english"""
    try:
        print("Tell Me the line!")
        speak("Tell Me the line!")
        line = TakeHindi()
        translate = Translator()
        result = translate.translate(line)
        text = result.text

        print(f"The translation for this line is: {text}")
        speak(f"The translation for this line is: {text}")

    except:
        print("Sorry, Cannot translate right now")
        speak("Sorry, Cannot translate right now")


def chatBot():
    """This function uses RandomStuff API for inbuilt chatbot which is text based."""
    rs = RandomStuff('dvIl9hpZ5vJl')

    def lets_talk():
        while True:
            userinput = input("You: ")
            response = rs.get_ai_response(userinput)[0]['message']
            print(f"Zira: {response}")
            # rs.close()
            if "quit" in userinput.lower():
                break

    lets_talk()


def wolfram():
    """This function uses WolframAplha API for computational intelligence and scientific calculations"""
    Ask = str(input('Query:'))
    client = wolframalpha.Client('A33PEG-7QYT3WTW58')
    if 1:
        res = client.query(Ask)
        Output = next(res.results).text
        speak(Output)


def pdf_reader():
    """This function is used to read pdf."""
    input1 = input("Enter the name pdf(with .pdf extension): ")
    book = open(input1, 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    print(f"Total number of pages in this pdf {pages}")
    speak(f"Total number of pages in this pdf {pages}")
    print("Please enter the page number that i have to read")
    speak("Please enter the page number that i have to read")
    pg = int(input("Please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)


def news():
    """This function uses NewsAPI to get daily news."""
    query_params = {
        "source": "bbc-news",
        "sortBy": "top",
        "apiKey": "2b7e49b3b76c48d49b2dafce5801a76f"
    }

    main_url = "https://newsapi.org/v1/articles"

    res = requests.get(main_url, params=query_params)
    open_bbc_news = res.json()

    articles = open_bbc_news['articles']

    answer = []

    for ar in articles:
        answer.append(ar['title'])
    for i in range(len(answer)):
        print(i + 1, answer[i])

    speak(answer)


def temperature():
    """This function tells you the current Tempreature of your city"""
    search = query
    search = search.replace("what", "")
    search = search.replace("is", "")
    search = search.replace("the", "")
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text, "html.parser")
    temp = data.find("div", class_="BNeawe").text
    print(f"Current {search} is {temp}")
    speak(f"Current {search} is {temp}")


def cpu():
    """This function tells you CPU percentage and Battery percentage using psutil module."""
    print("Wait a minute let me check..")
    speak("Wait a minute let me check..")
    usage = str(psutil.cpu_percent())
    print(f"CPU is at {usage}")
    speak(f"CPU is at {usage}")

    battery = psutil.sensors_battery()
    print(f"Battery is at {battery.percent}")
    speak(f"Battery is at {battery.percent}")


def WhatsappMsg():
    """This function is used to automate Whatsapp Messenger."""
    print("Enter the number of the person")
    speak("Enter the number of the person")
    user_input = str(input("Enter the number of the person(+918267479383234): "))
    print("What is the message?")
    speak("What is the message?")
    enter_msg = takeCommand()
    # enter_msg = str(input("Enter your message: "))
    print("Schedule time")
    speak("Schedule time")
    user_input1 = int(input("Enter the time(hour): "))
    user_input2 = int(input("Enter the time(minute): "))

    kit.sendwhatmsg(user_input, enter_msg, user_input1, user_input2)
    # time.sleep(20)
    # keyboard.press('enter')
    print("Sending message")
    speak("Sending message")


def Googlemaps(place):
    """This function the distance of the place that you searched for."""
    print("Opening Google Maps")
    speak("Opening Google Maps")
    urls = f"https://www.google.com/maps/place/{str(place)}"
    webbrowser.open(urls)
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)
    target_latlon = location.latitude, location.longitude

    location = location.raw['address']
    target = {'city': location.get('city', ''),
              'state': location.get('state', ''),
              'country': location.get('country', '')}
    current_loca = geocoder.ip('me')
    current_latlon = current_loca.latlng

    distance = str(great_circle(current_latlon, target_latlon))
    distance = str(distance.split(' ', 1)[0])
    distance = round(float(distance), 2)
    speak(target)
    print(f'{place} is {distance} kilometers away from your location')
    speak(f'{place} is {distance} kilometers away from your location')


def Instagram():
    """This function is used to automate Instagram i.e. Upload Picture, follow someone, send message, get followers."""
    bot = Bot()
    user_input = input("Enter your username: ")
    user_input1 = input("Enter your password: ")
    bot.login(username=user_input, password=user_input1)
    query = takeCommand()
    if 'upload picture' in query or 'upload image' in query:
        pic_upload = input("Enter the image path: ")
        print("tell me the Caption you want to add..")
        speak("tell me the Caption you want to add..")
        caption_upload = takeCommand()
        bot.upload_photo(pic_upload, caption=caption_upload)
    elif 'follow' in query:
        follow_whom = input("Enter the username of the person: ")
        bot.follow(follow_whom)
    elif 'send message' in query:
        msg_to = input("Enter the user name to whom you want to send message: ")
        print("What should i say..")
        speak("What should i say..")
        msg = takeCommand()
        bot.send_message(msg, msg_to)
    elif 'get followers' in query:
        user = input("Enter the username of the person: ")
        followers = bot.get_user_followers(user)
        for follower in followers:
            print(bot.get_user_info(follower))


def video_capture():
    """This function is used for home security system using webcam"""
    speak("Home security Activated!")

    cam = cv2.VideoCapture(0)

    while cam.isOpened():
        ret, frame1 = cam.read()
        ret, frame2 = cam.read()
        diff = cv2.absdiff(frame1, frame2)
        grey = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(grey, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            for i in range(5):
                return_value, image = cam.read()
                cv2.imwrite('opencv' + str(i) + '.png', image)
                speak("Object Dectected")
                speak("Get out of my room!")

        if cv2.waitKey(10) == ord('q'):
            break
        cv2.imshow('Security Cam', frame1)


def random_pass():
    """This function is used to generate the random password"""
    speak("Give me a Second!")
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"
    symbols = "[]{}@#$%^&*()!"
    All = lower + upper + numbers + symbols
    length = 9
    password = "".join(random.sample(All, length))
    print(f"The Password you Generated is: {password}")
    speak("Your password is ready to use!")


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    print(res['slip']['advice'])
    return speak(res['slip']['advice'])


def alarm():
    alarmH = int(input("Enter the hour you want the alarm to ring: "))
    alarmM = int(input("Enter the minute you want the alarm to ring: "))
    ampm = input("am or pm? ")

    print("Waiting for alarm", alarmH, alarmM, ampm)
    if ampm == "pm":
        alarmH = alarmH + 12
    while 1 == 1:
        if (alarmH == datetime.datetime.now().hour and
                alarmM == datetime.datetime.now().minute):
            print("Time To wake up!")
            playsound('twirling-intime-lenovo-k8-note-alarm-tone-41440.mp3')
            break


if __name__ == '__main__':
    while True:
        print("To activate Zira please say 'Activate Zira' or 'Wake up Zira or 'Hi Zira' or 'Hey Zira'")
        permission = takeCommand()
        # cv2.destroyAllWindows()
        if 'wake up' in permission or 'activate' in permission or 'hi' in permission or 'hey' in permission:
            # speak("Activating Zira..")
            print("Initializing Zira")
            speak("Initializing Zira")
            print("Starting all systems and applications")
            speak("Starting all systems and applications")
            print("Checking internet connection")
            speak("Checking internet connection")
            print("Hello")
            speak("Hello")
            print("Please look at the camera, so that i can recognize you..")
            speak("Please look at the camera, so that i can recognize you..")
            face_recognizer()
            while True:
                # if 1:
                query = takeCommand()

                # Logic for executing tasks based in query

                if 'wikipedia' in query:
                    print('Searching Wikipedia...')
                    speak('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    print("According to Wikipedia")
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                elif 'how are you' in query:
                    print("I am fine! What about you?")
                    speak("I am fine! What about you?")

                elif 'fine' in query or "i am good" in query:
                    print("It's good to hear that you are fine!")
                    speak("It's good to hear that you are fine!")

                elif 'youtube search' in query:
                    print("This is what i found for your search!")
                    speak("This is what i found for your search!")
                    query = query.replace("zira", "")
                    query = query.replace("youtube search", "")
                    web = "https://www.youtube.com/results?search_query=" + query
                    webbrowser.open(web)
                    time.sleep(5)
                    print(f"Playing latest video of {query}!")
                    speak(f"Playing latest video of {query}!")
                    kit.playonyt(web)
                    print("Done!")
                    speak("Done!")

                elif 'You need a break' in query:
                    print("Ok. You Can call me anytime!")
                    speak("Ok. You Can call me anytime!")
                    break

                elif 'search' in query:
                    import wikipedia as googleScrap

                    query = query.replace("zira", "")
                    query = query.replace("search", "")
                    kit.search(query)
                    print("This is what i found on the internet..")
                    speak("This is what i found on the internet..")

                    try:
                        result = googleScrap.summary(query, 2)
                        print(result)
                        speak(result)
                    except:
                        print("No speakable data available..")
                        speak("No speakable data available..")

                elif 'website' in query:
                    print("Launching..")
                    speak("Launching..")
                    query = query.replace("zira", "")
                    query = query.replace("website", "")
                    query = query.replace(" ", "")
                    web1 = query.replace("open", "")
                    web2 = 'https://www.' + web1 + '.com'
                    webbrowser.open(web2)
                    print("Launched")
                    speak("Launched")

                elif 'launch' in query:
                    print("Wait a second")
                    speak("Wait a second")
                    new_name = query.replace("launch", "")
                    v = new_name.replace(" ", "")

                    web = 'https:/www.' + v + '.com'
                    webbrowser.open(web)
                    print("Here it is..")
                    speak("Here it is..")

                elif 'screenshot' in query:
                    pyautogui._snapshot(None, folder='D:\\ScreenRecordings')
                    print("Screenshot saved successfully!")
                    speak("Screenshot saved successfully!")

                elif 'open youtube' in query:
                    print("Opening Youtube...")
                    speak("Opening Youtube...")
                    webbrowser.open("youtube.com")

                elif 'open notepad' in query:
                    npath = "C:\\WINDOWS\\system32\\notepad.exe"

                elif 'command prompt' in query:
                    os.startfile('cmd')

                elif 'instagram' in query:
                    print("Opening Instagram...")
                    speak("Opening Instagram...")
                    webbrowser.open("instagram.com")
                    Instagram()

                elif 'flipkart' in query:
                    speak("Opening flipkart...")
                    webbrowser.open("flipkart.in")

                elif 'open pycharm' in query:
                    OpenApps()

                elif 'open visual studio code' in query:
                    OpenApps()

                elif 'open chrome' in query:
                    OpenApps()

                elif 'open Telegram' in query:
                    OpenApps()

                elif 'open Grammarly' in query:
                    OpenApps()

                elif 'close pycharm' in query:
                    CloseApps()

                elif 'close visual studio code' in query:
                    CloseApps()

                elif 'close chrome' in query:
                    CloseApps()

                elif 'close Telegram' in query:
                    CloseApps()

                elif 'close Grammarly' in query:
                    CloseApps()

                elif 'blogger' in query:
                    print("Opening blogger...")
                    speak("Opening blogger...")
                    webbrowser.open("blogger.com")

                elif 'song on youtube' in query:
                    speak("playing a song in youtube")
                    song = ["https://www.youtube.com/watch?v=jn77BhLMGc8",
                            "https://www.youtube.com/watch?v=2eliQ_KR8yA",
                            "https://www.youtube.com/watch?v=P8PWN1OmZOA",
                            "https://www.youtube.com/watch?v=jMFBpCpilWQ",
                            "https://www.youtube.com/watch?v=TUawyJn7dws",
                            "https://www.youtube.com/watch?v=bWBki437qvg"]
                    choice = random.choice(song)
                    webbrowser.open(choice)

                elif 'the time' in query:
                    # localtime = time.asctime(time.localtime(time.time()))
                    # speak(localtime)
                    strtime = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"Umm..., the time is {strtime}")
                    speak(f"Umm..., the time is {strtime}")

                elif 'alpha' in query or 'computational intelligence' in query:
                    print("Activating Wolfram Alpha")
                    speak("Activating Wolfram Alpha")
                    wolfram()

                elif 'shutdown' in query:
                    print("shutting down")
                    speak("shutting down")
                    os.system('shutdown -s')

                elif "what's up" in query or 'how are you' in query:
                    stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy',
                              'i am okay! How are you']
                    ans_q = random.choice(stMsgs)
                    print(ans_q)
                    speak(ans_q)

                elif 'made you' in query or 'created you' in query or 'developed you' in query:
                    ans_m = "For your information A Group Created me ! I am very thankful to them "
                    print(ans_m)
                    speak(ans_m)

                elif 'who are you' in query or 'about you' in query or 'your details' in query:
                    about = "I am Zira an AI based computer program but i can help you lot like a close friend ! "
                    print(about)
                    speak(about)

                elif 'what can you' in query:
                    print("I can search for you on the internet!")
                    speak("I can search for you on the internet!")
                    print("I can play songs for you!")
                    speak("I can play songs for you!")
                    print("I can tell latest news")
                    speak("I can tell latest news")
                    print("I can crack some jokes!")
                    speak("I can crack some jokes!")
                    print("I can do Youtube search!")
                    speak("I can do Youtube search!")
                    print("I can chat with you..")
                    speak("I can chat with you..")
                    print("I can remember things for you!")
                    speak("I can remember things for you!")
                    print("I can send whatsapp messages!")
                    speak("I can send whatsapp messages!")
                    print("I can do mathematical operations and other things just using Wolfram Alpha ")
                    speak("I can do mathematical operations and other things just using Wolfram Alpha ")
                    print("I can be your dictionary, where ever or when ever you find words to be difficult!")
                    speak("I can be your dictionary, where ever or when ever you find words to be difficult!")
                    print("I can be your video downloader!")
                    speak("I can be your video downloader!")
                    print("I can be your pdf reader!")
                    speak("I can be your pdf reader!")
                    print("I can set alarm")
                    speak("I can set alarm")
                    print("I can tell you the tempreature of your city!")
                    speak("I can tell you the tempreature of your city!")
                    print(
                        "I can increase your desktop volume or i can decrease it, I can tell you the battery percentage")
                    speak(
                        "I can increase your desktop volume or i can decrease it, I can tell you the battery percentage")
                    print("I can open apps for you and websites too! ")
                    speak("I can open apps for you and websites too! ")
                    print("What else you want??")
                    speak("What else you want??")
                    print("So lets begin!")
                    speak("So lets begin!")

                elif 'hello' in query or 'hello Zira' in query or 'hey' in query:
                    hel = "Hello! How May i Help you.."
                    print(hel)
                    speak(hel)

                elif 'send message' in query:
                    print("Just a second!")
                    speak("Just a second!")
                    WhatsappMsg()

                elif 'you can sleep' in query or 'no thanks' in query:
                    ex_exit = 'ok, i am going to sleep now, you can call me anytime..'
                    print(ex_exit)
                    speak(ex_exit)
                    break

                elif "let's chat" in query or 'can we chat' in query or 'want to chat with you' in query:
                    print("Why not..")
                    speak("Why not..")
                    print("Wait a second..")
                    speak("Wait a second..")
                    print("Transforming Virtual Assistant Zira into Chat Bot Zira")
                    speak("Transforming Virtual Assistant Zira into Chat Bot Zira")
                    chatBot()

                elif 'remember that' in query:
                    rememberMsg = query.replace("remember that", "")
                    rememberMsg = rememberMsg.replace("zira", "")
                    rememberMsg = rememberMsg.replace("I", "You")
                    speak("You tell me to Remind you that:" + rememberMsg)
                    remember = open('rem.txt', 'w')
                    remember.write(rememberMsg)
                    remember.close()

                elif 'you to remember' in query:
                    remember = open('rem.txt', 'r')
                    print(f"You tell me to remember that {remember.read()}")
                    speak(f"You tell me to remember that {remember.read()}")

                elif 'pause' in query:
                    keyboard.press('space bar')

                elif 'play' in query:
                    keyboard.press('space bar')

                elif 'close tab' in query:
                    keyboard.press_and_release('ctrl + w')

                elif 'shift tab' in query:
                    keyboard.press_and_release('ctrl + tab')

                elif 'new tab' in query:
                    keyboard.press_and_release('ctrl + t')

                elif 'new window' in query:
                    keyboard.press_and_release('ctrl + n')

                elif 'history' in query:
                    keyboard.press_and_release('ctrl + h')

                elif 'homepage' in query:
                    keyboard.press_and_release('Alt + Home')

                elif 'reload' in query:
                    keyboard.press_and_release('ctrl + r')

                elif 'save this page' in query or 'bookmark' in query:
                    keyboard.press_and_release('ctrl + d')
                    keyboard.press('enter')

                elif 'download' in query:
                    keyboard.press_and_release('ctrl + j')

                elif 'incognito' in query:
                    keyboard.press_and_release('ctrl + Shift + n')

                elif 'joke' in query:
                    get = pyjokes.get_joke()
                    print(get)
                    speak(get)

                elif 'repeat my words' in query:
                    print("Ok! I am listening you")
                    speak("Ok! I am listening you")
                    jj = takeCommand()
                    print(f"You said that: {jj}")
                    speak(f"You said that: {jj}")

                elif 'dictionary' in query:
                    Dict()

                elif 'set alarm' in query:
                    print("Tell me the time!")
                    speak("Tell me the time!")
                    alarm()

                elif 'translate' in query:
                    tran()

                elif 'temperature' in query:
                    temperature()

                elif 'read this pdf' in query or 'pdf reader' in query:
                    print("Running pdf reader..")
                    speak("Running pdf reader..")
                    pdf_reader()

                elif 'news' in query:
                    print("Fetching news...Wait a second!")
                    speak("Fetching news...Wait a second!")
                    news()

                elif 'hide all files' in query or 'hide this folder' in query or 'hide' in query:
                    print("Ok, hiding files... Please wait")
                    speak("Ok, hiding files... Please wait")
                    os.system("attrib +h /s /d")
                    print("All the files in this folder is now hidden for everyone..")
                    speak("all the files in this folder is now hidden for everyone..")

                elif 'visible for everyone' in query or 'visible' in query or 'unhide' in query:
                    os.system("attrib -h /s /d")
                    print("All the files in this folder are now visible to everyone..")
                    speak("All the files in this folder are now visible to everyone..")

                elif 'how to' in query:
                    speak("Getting data from the internet..")
                    op = query.replace("zira", "")
                    max_result = 1
                    how_to_func = search_wikihow(op, max_result)
                    assert len(how_to_func) == 1
                    how_to_func[0].print()
                    speak(how_to_func[0].summary)

                elif 'increase volume' in query or 'volume up' in query:
                    pyautogui.press("volumeup")

                elif 'decrease volume' in query or 'volume down' in query:
                    pyautogui.press("volumedown")

                elif 'mute' in query or 'volume mute' in query:
                    pyautogui.press("volumemute")

                elif 'battery' in query:
                    cpu()

                elif 'where is' in query:
                    Place = query.replace("zira", "")
                    Place = Place.replace("where is", "")
                    Googlemaps(Place)


                elif 'download this video' in query or 'video downloader' in query:
                    speak("Accessing Youtube Video Downloader..")
                    video_url = input("Enter the youtube video url: ")
                    youtube = pytube.YouTube(video_url)
                    video = youtube.streams.first()
                    video.download(str(input("Please enter the path for the video to be saved: ")))
                    print("Done! Please Check it..")
                    speak("Done! Please Check it..")

                elif 'goodbye' in query or 'abort' in query or 'bye' in query or 'quit' in query or 'terminate' in query or 'exit' in query:
                    print("Thanks for using me, have a good day!")
                    speak("Thanks for using me, have a good day!")
                    sys.exit()

                elif 'i love you' in query or 'love you' in query:
                    print("It is hard to understand love, I can be your good friend")
                    speak("It is hard to understand love, I can be your good friend")

                elif 'i like you' in query or 'like you' in query:
                    print("I also like you as a person!")
                    speak("I also like you as a person!")

                elif 'busy' in query or 'nothing' in query:
                    print("Let me do something for you!")
                    speak("Let me do something for you!")
                    print("If yoy want to hear few songs to refresh your mind, then say play song in youtube..")
                    speak("If yoy want to hear few songs to refresh your mind, then say play song in youtube..")

                elif 'morning' in query:
                    print("A warm Good Morning!")
                    speak("A warm Good Morning!")
                    print("How are you?")
                    speak("How are you?")

                elif 'afternoon' in query:
                    print("Good Afternoon")
                    speak("Good Afternoon")
                    print("How is it going?")
                    speak("How is it going?")

                elif 'evening' in query or 'evening' in query:
                    print("Good evening")
                    speak("Good evening")
                    print("How is it going?")
                    speak("How is it going?")

                elif 'night' in query or 'i am going to bed' in query or 'i am going to sleep' in query:
                    print("Good Night!")
                    speak("Good Night!")
                    print("I will be right there in the morning for you service")
                    speak("I will be right there in the morning for you service")
                    print("Good Bye!")
                    speak("Good Bye!")

                elif 'change name' in query:
                    speak("What would you like to call me?")
                    ass_name = input("Enter name for me: ")
                    print(f"Thanks for naming me... as {ass_name}")
                    speak(f"Thanks for naming me... as {ass_name}")
                    # if 'what is your name'

                elif 'what is your name' in query or "what's your name" in query:
                    print("My friend call me mini!")
                    speak("My friend call me mini!")
                    print("Not even my friends, my Developers, my colleagues and everyone call me mini!")
                    speak("Not even my friends, my Developers, my colleagues and everyone call me mini!")

                elif 'who am i' in query:
                    print("If you can talk then you are definitely human!")
                    speak("If you can talk then you are definitely human!")

                elif 'why you came' in query or 'why you came into this world' in query:
                    print("It's a secret!")
                    speak("It's a secret!")

                elif 'is love' in query:
                    print("It's the seventh sense, that destroy all other senses")
                    speak("It's the seventh sense, that destroy all other senses")

                elif 'internet speed' in query:
                    speak("Wait a second!, let me check..")
                    st = speedtest.Speedtest()
                    dl = st.download()
                    up = st.upload()
                    print(f"We have{dl} bit per second downloading speed and {up} bit per second uploading speed")
                    speak(f"We have{dl} bit per second downloading speed and {up} bit per second uploading speed")

                elif 'home security' in query:
                    video_capture()

                elif "switch the window" in query or "switch window" in query:
                    print("Okay, Switching the window")
                    speak("Okay, Switching the window")
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.keyUp("alt")

                elif "generate a password" in query or "password" in query:
                    random_pass()

                elif 'give an advice' in query or 'advice' in query:
                    get_random_advice()

                elif 'maximize' in query or 'maximize window' in query:
                    import ctypes
                    user32 = ctypes.WinDLL('user32')
                    SW_MAXIMISE = 3
                    hWnd = user32.GetForegroundWindow()
                    user32.ShowWindow(hWnd, SW_MAXIMISE)

                elif 'minimise' in query or 'minimise window' in query:
                    import ctypes
                    user32 = ctypes.WinDLL('user32')
                    SW_MINIMIZE = 10
                    hWnd = user32.GetForegroundWindow()
                    user32.ShowWindow(hWnd, SW_MINIMIZE)

                # speak("Do you have Any other work?")
        elif 'exit' in permission or 'terminate' in permission:
            print("Terminating...")
            speak("Terminating...")
            print("Thanks for using me..!")
            speak("Thanks for using me..!")
            sys.exit()
