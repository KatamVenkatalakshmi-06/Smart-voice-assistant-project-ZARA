# Smart Virtual Assistant - Advanced Version (ZARA)

import speech_recognition as sr
import random
import pyttsx3
import datetime
import webbrowser
import wikipedia
import time
import requests
import re
import os

engine = pyttsx3.init()
engine.setProperty('rate', 150)

ASSISTANT_NAME = "ZARA"

def speak(text):
    print(f"{ASSISTANT_NAME} : {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print(" Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f" You: {query}\n")
    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query.lower()

def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greet = "Good Morning"
    elif hour < 18:
        greet = "Good Afternoon"
    else:
        greet = "Good Evening"
    speak(f"{greet}! I am {ASSISTANT_NAME}, your smart assistant. Say 'help' to know what I can do.")

def get_weather(city):
    try:
        api_key =  "1b804d89ea2dfb6633bbb99e1b2affb1" # Replace with your OpenWeatherMap API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()
        print("API response:", data)  # Debug: print the API response
        if data.get("cod") != 200:
            speak("Sorry, I couldn't find that city.")
            return
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        speak(f"The weather in {city} is {desc} with {temp}°C.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather.")
        print("Exception:", e)  # Debug: print the exception

import threading

def set_reminder(msg, seconds):
    def remind():
        time.sleep(seconds)
        speak(f"⏰ Reminder: {msg}")
    threading.Thread(target=remind).start()
    speak(f"Reminder set. I will remind you in {seconds} seconds.")

def save_note(note):
    with open("zara_notes.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {note}\n")
    speak("I have saved your note.")

def read_notes():
    if not os.path.exists("zara_notes.txt"):
        speak("You have no saved notes.")
        return
    with open("zara_notes.txt", "r") as f:
        notes = f.readlines()
    print("Notes found:", notes)  # Add this line
    if notes:
        speak("Here are your saved notes:")
        for n in notes[-5:]:
            speak(n.strip())
    else:
        speak("You have no saved notes.")

def search_notes(word):
    if not os.path.exists("zara_notes.txt"):
        speak("No notes found.")
        return
    with open("zara_notes.txt", "r") as f:
        found = [n for n in f if word.lower() in n.lower()]
    if found:
        speak("Found notes:")
        for note in found:
            speak(note.strip())
    else:
        speak("No matching notes.")


def delete_notes():
    if os.path.exists("zara_notes.txt"):
        os.remove("zara_notes.txt")
        speak("All your notes have been deleted.")
    else:
        speak("There are no notes to delete.")


def tell_joke(mood):
    jokes = {
        "happy": [
            "Why don’t eggs tell each other secrets? Because they might crack up! 🥚😂"
        ],
        "sad": [
            "Why did the phone break up with the charger? Because it felt drained all the time. 📱💔🔋"
        ],
        "angry": [
            "Why did the math book look angry? Because it had too many problems! ➕➖😠"
        ],
        "bored": [
            "Why don’t YouTubers get bored? Because they always have clicks to keep them going! 🎬😅"
        ],
        "tired": [
            "Why was the bed always so popular? Because it gave people resting vibes! 🛏️😴"
        ],
        "funny": [
            "What do you call a fish with no eyes? Fsh! 🐟🤣"
        ]
    }

    mood = mood.lower()
    if mood in jokes:
        speak(random.choice(jokes[mood]))
    else:
        speak("I don't have jokes for that mood, but here's one anyway!")


def spoken_to_url(text):
    text = text.lower()

    # Step 1: Replace multi-word phrases first
    text = text.replace("double slash", "//")
    text = text.replace("forward slash", "/")
    text = text.replace("colon", ":")
    text = text.replace(" dot ", ".")
    text = text.replace(" dot", ".")
    text = text.replace("dot ", ".")
    text = text.replace(" space ", "")
    
    # Step 2: Remove remaining spaces
    text = text.replace(" ", "")
    
    return text

import random

def mini_quiz():
    quiz = {
        "What is the capital of India?": "new delhi",
        "How many days are there in a week?": "7",
        "What color is the sky on a clear day?": "blue",
        "How many legs does a spider have?": "8",
        "What is the boiling point of water in Celsius?": "100",
        "Who is the President of India?": "droupadi murmu",
        "How many hours are there in a day?": "24",
        "Which planet is known as the Red Planet?": "mars",
        "Which animal is known as the King of the Jungle?": "lion",
        "How many letters are there in the English alphabet?": "26",
        "Which festival is known as the festival of lights?": "diwali",
        "Which gas do we need to breathe?": "oxygen",
        "Which fruit keeps the doctor away if eaten daily?": "apple",
        "How many colors are there in a rainbow?": "7",
        "Which shape has four equal sides?": "square",
        "Which is the largest ocean on Earth?": "pacific",
        "What is the smallest prime number?": "2",
        "What is the result of 5 times 6?": "30",
        "Which continent is India in?": "asia",
        "Which day comes after Friday?": "saturday",
        "How many wheels does a car have?": "4",
        "Which is the tallest animal?": "giraffe",
        "Which is the fastest land animal?": "cheetah",
        "How many bones are in the human body?": "206",
        "What do bees make?": "honey"
    }

    speak("Let's begin the quiz. I will ask you five questions. Answer by speaking.")
    score = 0
    asked = random.sample(list(quiz.items()), 5)

    for question, answer in asked:
        speak(question)
        user_answer = take_command()

        if user_answer == "":
            speak("I didn't catch that. Please say your answer again.")
            user_answer = take_command()

        if user_answer == "":
            speak("No answer received. The correct answer is " + answer + ".")
            continue

        if answer.lower() in user_answer:
            speak("Correct!")
            score += 1
            continue  # Go to next question immediately

        # Only if incorrect, give a second chance
        speak("Oops! Try once more!")
        user_answer2 = take_command()
        if answer.lower() in user_answer2:
            speak("Correct on your second try!")
            score += 1
        else:
            speak(f"Oops! The correct answer is {answer}.")

    speak(f"Your final score is {score} out of 5.")
    if score == 5:
        speak("Perfect! You're brilliant!")
    elif score >= 3:
        speak("Good job! You did well.")
    else:
        speak("Keep practicing and you'll improve!")

import re
import webbrowser


def emoji_game():
    questions = [
        {"emoji": "🐍💻", "answer": "python"},
        {"emoji": "🍎📱", "answer": "apple"},
        {"emoji": "🎬🍿", "answer": "movie"},
        {"emoji": "🚗💨", "answer": "car"},
        {"emoji": "🌍📚", "answer": "geography"},
        {"emoji": "🎵🎤", "answer": "music"},
        {"emoji": "⚽🥅", "answer": "football"},
        {"emoji": "🦁👑", "answer": "lion king"},
        {"emoji": "🧊❄️", "answer": "ice"},
        {"emoji": "🐘👂", "answer": "elephant"},
        {"emoji": "🐒🍌", "answer": "monkey"},
        {"emoji": "🌞😎", "answer": "sun"},
        {"emoji": "🐶🐾", "answer": "dog"},
        {"emoji": "🐱🐾", "answer": "cat"},
        {"emoji": "🦒🌳", "answer": "giraffe"},
        {"emoji": "🍔🍟", "answer": "burger and fries"},
        {"emoji": "🎂🎉", "answer": "birthday"},
        {"emoji": "🎓📚", "answer": "graduation"},
        {"emoji": "🧑‍🏫📖", "answer": "teacher"},
        {"emoji": "🧑‍🎨🎨", "answer": "artist"},
        {"emoji": "🧑‍🔬🔬", "answer": "scientist"},
        {"emoji": "🧑‍💻💻", "answer": "programmer"},
        {"emoji": "🧑‍🚀🚀", "answer": "astronaut"},
        {"emoji": "🧑‍🍳🍳", "answer": "chef"},
        {"emoji": "🧑‍🚒🔥", "answer": "firefighter"},
        {"emoji": "🧑‍⚕️💉", "answer": "doctor"},
        {"emoji": "🧑‍✈️✈️", "answer": "pilot"},
        {"emoji": "🧑‍🌾🌱", "answer": "farmer"}
    ]
    rounds = 3
    asked = random.sample(questions, rounds)
    for q in asked:
        speak("Guess the word or phrase from the emojis I am showing you.")
        print(f"EMOJIS: {q['emoji']}")  # This will display the emojis in the console for the user to see
        user = take_command()
        if q['answer'] in user.lower():
            speak("🎉 Correct! You're an emoji master!")
            continue  # Go to next question immediately
        # Only if incorrect, give a second chance
        else:
            speak("Oops! Try once more!")
        user2 = take_command()
        if q['answer'] in user2.lower():
            speak("🎉 Correct on your second try!")
        else:
            speak(f"Sorry, the answer was '{q['answer']}'. Better luck next time!")

# In your run_assistant() loop:

def open_site(site):
    urls = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "github": "https://github.com",
        "linkedin": "https://linkedin.com",
        "facebook": "https://facebook.com",
        "stack overflow": "https://stackoverflow.com",
        "twitter": "https://twitter.com",
        "whatsapp": "https://web.whatsapp.com",
        "spotify": "https://spotify.com",
        "amazon": "https://amazon.com",
        "netflix": "https://netflix.com",
        "wikipedia": "https://wikipedia.org",
        "pinterest": "https://pinterest.com",
        "telegram": "https://telegram.org",
        "stackoverflow": "https://stackoverflow.com",
        "zomato": "https://zomato.com",
        "flipkart": "https://flipkart.com",
        "booking": "https://booking.com",
        "telegram": "https://telegram.org",
        "calculator": "https://calculator.com",
        "news": "https://news.com",

    }
    site_key = site.lower().replace(" ", "")
    if site_key in urls:
        webbrowser.open(urls[site_key])
        speak(f"Opening {site_key}")
    else:
        url = spoken_to_url(site)
        print("Converted URL:", url)  # Debug: see the result

        if re.match(r"https?://", url):
            webbrowser.open(url)
            speak(f"Opening {url}")
        else:
            speak("I don't know that site. But you can say 'open' followed by a full URL.")


import urllib.parse
import yt_dlp

def play_specific_song():
    speak("Which song do you want to play? You can also say an artist or mood.")
    song = take_command()
    if not song or song == "none":
        speak("I didn't catch the song name.")
        return

    # Mood-based quick picks
    moods = {
        "happy": ["Pharrell Williams Happy", "Katy Perry Firework"],
        "sad": ["Adele Someone Like You", "Sam Smith Too Good At Goodbyes"],
        "energetic": ["Eye of the Tiger", "Uptown Funk"],
        "romantic": ["Perfect Ed Sheeran", "All of Me John Legend"],
        "relaxed": ["Weightless Marconi Union", "Let Her Go Passenger"]
    }
    for mood in moods:
        if mood in song:
            pick = random.choice(moods[mood])
            song = pick
            break

    query = f"{song} song"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': 'in_playlist',
        'default_search': 'ytsearch1',
        'forcejson': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video_url = f"https://www.youtube.com/watch?v={info['entries'][0]['id']}"
                speak(f"Playing {song} on YouTube.")
                webbrowser.open(video_url)
            else:
                speak("Sorry, I couldn't find that song on YouTube.")
    except Exception as e:
        speak("Sorry, I couldn't play the song right now.")
        print("Error:", e)

def translate_text(text, target_lang):
    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
    return translated

from gtts import gTTS
from playsound import playsound
import tempfile
import os
from deep_translator import GoogleTranslator

def speak_in_language(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_path = fp.name
        tts.save(temp_path)
        playsound(temp_path)
        os.remove(temp_path)
    except Exception as e:
        speak("Sorry, I couldn't pronounce that in the target language.")
        speak(text)

def translate_word():
    speak("Which word or sentence do you want to translate?")
    text = take_command().strip()
    if not text or text == "none":
        speak("I didn't catch that. Please say the word or sentence again.")
        return

    speak("Which language do you want to translate to? ")
    lang = take_command().strip().lower()
    lang_map = {
        "hindi": "hi",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "chinese": "zh-cn",
        "japanese": "ja",
        "russian": "ru",
        "arabic": "ar",
        "italian": "it",
        "portuguese": "pt",
        "telugu": "te",
        "tamil": "ta",
        "kannada": "kn",
        "malayalam": "ml",
        "bengali": "bn",
        "marathi": "mr",
        "punjabi": "pa",
        "urdu": "ur",
    }
    if lang not in lang_map:
        speak("Sorry, I can translate to Hindi, Spanish, French, German, Chinese, Japanese, Russian, Arabic, Italian, or Portuguese only.")
        return

    translator = GoogleTranslator()
    try:
        translated = GoogleTranslator(source='auto', target=lang_map[lang]).translate(text)
        speak(f"The translation in {lang} is: {translated}")
        speak_in_language(translated, lang_map[lang])
    except Exception as e:
        speak("Sorry, I couldn't translate that right now.")


        
def show_help():
    speak("You can ask me to search Wikipedia, get the weather, tell the time or date, open websites, set reminders, save or read notes, tell a joke, or play a quiz. Just say what you need!")

def run_assistant():
    wish_user()
    while True:
        query = take_command()
        if query == "none":
            continue

        # Only respond if the command starts with "zara"
        if not query.startswith("zara"):
            continue

        # Remove "zara" from the start so commands work as before
        query = query.replace("zara", "", 1).strip()

        # ...rest of your code...

        if 'help' in query:
            show_help()

        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            try:
                topic = query.replace("wikipedia", "").strip()
                if not topic:
                    speak("What should I search on Wikipedia?")
                    topic = take_command()
                result = wikipedia.summary(topic, sentences=2)
                speak(result)
            except Exception as e:
                speak("I couldn't find anything on Wikipedia.")

        elif 'weather' in query:
            speak("Which city?")
            city = take_command()
            if city != "none":
                get_weather(city)

        elif 'time' in query:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {now}")

        elif 'date' in query:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            speak(f"Today's date is {today}")

        elif query.startswith('open '):
            site = query.replace('open ', '').strip()
            open_site(site)

        elif 'remind me' in query:
            speak("What should I remind you?")
            reminder = take_command()
            speak("In how many seconds?")
            try:
                seconds = int(take_command())
                set_reminder(reminder, seconds)
            except:
                speak("Couldn't understand the time.")

        elif 'read notes' in query:
            read_notes()

        elif 'search notes' in query:
            speak("What word should I search for in your notes?")
            word = take_command()
            if word != "none":
                search_notes(word)

        elif 'delete notes' in query:
            speak("Are you sure you want to delete all your notes?")
            confirm = take_command()
            if 'yes' in confirm:
                delete_notes()
            else:
                speak("Okay, I won't delete your notes.")

        elif 'note' in query:
            speak("What should I write?")
            note = take_command()
            save_note(note)
        
        elif 'joke' in query or 'funny' in query:
            speak("How are you feeling? Happy, sad, angry, bored, tired or funny?")
            mood = take_command()
            tell_joke(mood)

        elif 'mini quiz' in query:
                speak("Let's play a mini quiz. Are you ready?")
                mini_quiz()

        elif 'emoji game' in query:
            speak("Let's play an emoji game. Guess the word or phrase from the emojis I give you.")
            emoji_game()

        elif 'play song' in query or 'play a song' in query or 'play specific song' in query:
            play_specific_song()

        elif 'translate' in query or 'translation' in query:
            translate_word()

        

        elif 'bye' in query or 'exit' in query:
            speak("Do you want me to shut down?")
            confirm = take_command()
            if 'yes' in confirm:
                speak("Goodbye! Have a great day.")
                break
            else:
                speak("Alright, still here.")

        else:
            speak("Sorry, I didn’t get that. Say 'help' to know what I can do.")

if __name__ == "__main__":
    run_assistant()