import pyttsx3                      # To select a voice for our virtual assistan form microsotft speech api
import datetime                     # Extracting Time to greet according to the timezone
import speech_recognition as sr     # to take input from user's microphone
import wikipedia
import webbrowser
import os
import smtplib


# setting up chrome path to so searches will be brwosed on chrome

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'



''' 

Setting Up this voice for jarvis

'''

jarvis = pyttsx3.init('sapi5')
voices = jarvis.getProperty('voices')
jarvis.setProperty('voice', voices[0].id)

''' uncommnet these line if you thnik jarvis is speaking very fastly '''

# newVoiceRate = 145
# jarvis.setProperty('rate', newVoiceRate)

'''  

speak funciton

'''

def speak(audio):
    jarvis.say(audio)
    jarvis.runAndWait()

''' 

funtion to greet the user according to the timezone

'''

def Greet():
    hours = int(datetime.datetime.now().hour)
    if hours >= 0 and hours < 12:
        speak('Good Morning')
        print('Good Mornoing')

    elif hours >= 12 and hours < 17:
        speak("Good Afternoon")
        print('Good Afternoon')

    else:
        speak('Good Evening')
        print('Good Evening')

    speak("My name is Jarvis and how can i help you")


''' 

function to take command from the microphone and recognizing it thorugh google speech recognizer

'''

def getCommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        command.pause_threshold = 1
        audio = command.listen(source)

    try:
        print('Recognizing...')
        query = command.recognize_google(audio, language='en')
        print(f' You said {query}')
    
    except Exception:
        print("Plz say that again")
        return 'None'

    return query


''' 

funciton to remove some umwanted keywords

'''

def query_corrections(query):
    if 'search' in query:
        query = query.replace('search', '')
    elif 'jarvis' in query:
        query = query.replace('jarvis', '')
    return query

'''

function to send email

'''

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email here', 'your password here') # better make a new fake gmail account and then use it
    server.sendmail('your email', to , content)
    server.close()

''' 

main function

'''


if __name__ == '__main__':
    Greet()
    while True:
        audio_query =  getCommand().lower()

        query = query_corrections(audio_query)

        if 'exit' in query:
            break
            
        elif 'wikipedia' in query:
            query  = query.replace('wikipedia' , '')
            speak('Searching Wikipedia')
            result  = wikipedia.summary(query, sentences = 1) # if your want more senteces from just change the value
            print(result)
            speak("according to wikipedia")
            speak(result)

        elif 'on youtube' in query:
            webbrowser.get(chrome_path).open(f"youtube.com/results?search_query={query}")

        elif 'open youtube' in query:
            webbrowser.get(chrome_path).open("youtube.com")
        
        elif 'open google' in query:
            webbrowser.get(chrome_path).open("google.com")

        elif 'on google' in query:
            webbrowser.get(chrome_path).open(f"google.com/search?q={query}")

        elif 'music' in query:
            music_dir = f'{os.getcwd()}\\songs'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'email to someone' in query:
            try:
                speak("what should i say") 
                content = getCommand()
                to = 'Reciever email here' # write email id of the person you want to send an email
                sendEmail(to, content)
                speak('email has been sent')

            except Exception:
                speak('sorry i am not able to sent this email')



