##Smart-voice-assistant-project-ZARA
ZARA is a Python-based voice assistant that responds to spoken commands and performs various tasks like retrieving weather information, playing songs, translating languages, managing notes, setting reminders, and more. Built with speech_recognition, pyttsx3, gTTS, and integrated with APIs like Wikipedia, OpenWeatherMap, YouTube, and Google Translate.


## 🌟 Features
- 🎙️ Voice-controlled interaction  
- 📅 Time-based greetings  
- 🌤️ Real-time weather updates (OpenWeatherMap API)  
- 📚 Wikipedia summaries  
- 🗒️ Save, read, search, and delete notes  
- ⏰ Reminders with threading  
- 🤣 Mood-based jokes  
- 🧠 Mini quiz & emoji guessing game  
- 🎵 YouTube music playback (`yt_dlp`)  
- 🌐 Open websites or spoken URLs  
- 🌍 Multilingual translation with pronunciation (`gTTS`)  
- 🆘 Built-in help and exit via voice  

---

## 🧑‍💻 Technologies Used
- Python 3.x  
- `speech_recognition`  
- `pyttsx3`  
- `gtts`, `playsound`  
- `deep_translator`  
- `yt_dlp`  
- `wikipedia`, `requests`, `webbrowser`  
- `threading`, `datetime`  

---

## 🚀 Getting Started

### 🔧 Installation
Install the required dependencies:

```bash
pip install speechrecognition pyttsx3 wikipedia requests gtts playsound deep_translator yt_dlp

python app3.py
🗣️ Example Commands
Zara, what is the weather in Mumbai?

Zara, play a happy song

Zara, translate hello to Spanish

Zara, set a reminder in 30 seconds

Zara, open YouTube

📌 Notes
Works best with a microphone and English language input

Internet connection required for Wikipedia, weather, YouTube, and translation features

📄 License
This project is licensed under the MIT License.

yaml
Copy
Edit

---

## 📂 **Suggested Folder Structure**
Smart-Virtual-Assistant-ZARA/
│
├── app3.py # Main assistant code
├── requirements.txt # List of all dependencies
├── README.md # Project documentation
├── LICENSE # MIT license file
├── zara_notes.txt # (Auto-created) file for saving notes
├── assets/ # (Optional) Images, icons, sample input/output

 📦 5. **requirements.txt**

```txt
speechrecognition==3.8.1
pyttsx3==2.90
wikipedia==1.4.0
requests==2.31.0
gtts==2.5.1
playsound==1.2.2
deep-translator==1.11.4
yt-dlp==2024.05.27
Install with:

bash
Copy
Edit
pip install -r requirements.txt



