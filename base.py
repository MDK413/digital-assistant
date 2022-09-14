#speech recognition package from google api
from ast import main
import speech_recognition as sr
# to play saved mp3 file
import playsound
from gtts import gTTS # google text-to speech
import os
import wolframalpha # to calculate strings into formula
from selenium import webdriver # for browser control

num = 1
def assitant_speaks(output):
    global num

    #num to rename every audio file with different name to remove ambiguity
    num += 1
    print("Mohini : ", output)

    toSpeak = gTTS(text = output, lang='en', tld='co.in', slow=False)
    #saving the audio file given by google text to speech
    file = str(num)+".mp3"
    toSpeak.save(file)

    #play sound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Speak...")

        #recording audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit = 5)
    print("Stop.") # limit 5 secs

    try:
        text = rObject.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text

    except:
        assitant_speaks("Couldn't understand your audio , Please try again !")
        return 0


def process_text(input):
    try:
        if 'search' in input or 'play' in input:
            #a basic web crawler using selenium
            search_web(input)
            return

        elif "who are you" in input or "define yourself" in input:
            speak = '''Hello, I am Mohini Your personal Assistant.
            I am here to make your life easier. You can command me to perform various tasks such as calculating sums or opening application etcetra'''
            assitant_speaks(speak)
            return

            
        elif "Who made you" in input or "who create you" in input:
            speak = "I have been created by mr.deven kumbhani."
            assitant_speaks(speak)
            return
        
        elif "calculate" in input.lower():

            #wolframalpha app_id here
            app_id = "WOLFRAMALPHA_APP_ID"
            client = wolframalpha.Client(app_id)

            indx = input.lower().split().index('calculate')
            query = input.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            assitant_speaks("The answer is " + answer)
            return

        elif "open" in input:

            #another funtion to open different application available
            open_application(input.lower())
            return

        else:

            assitant_speaks("I can search the web for you, Do you want to continue?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(input)

            else:
                return
    except:

        assitant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or "yeah" in str(ans):
            search_web(input)


# Driver Code
if __name__ == "__main__":
    assitant_speaks("What's your name, Human?")
    name = "Human"
    name = get_audio()
    assitant_speaks("Hello, "+ name + '.')

    while(1):

        assitant_speaks("What can I do for you?")
        text = get_audio().lower()

        if text == 0:
            continue

        if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
            assitant_speaks("Ok bye, "+ name+'.')
            break

        #calling process_text to process the query
        process_text(text)