import tkinter as tk
from tkinter import scrolledtext, font
from tkinter import ttk
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import google.generativeai as genai
import os

# Backend imports
import musiclibrary

# Configure API key
os.environ["GEMINI_API_KEY"] = "AIzaSyCQ322r0exnwSGgqVC8dFTXXwcZgAM1VVo"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Function to convert text to speech
def speak(a):
    engine = pyttsx3.init()
    engine.say(a)
    engine.runAndWait()

# Function to process commands
def processCommand(c, output_widget):
    output_widget.insert(tk.END, f"You: {c}\n", "user")
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        output_widget.insert(tk.END, "AI Model: Opening Google...\n", "ai")
    elif "open spotify" in c.lower():
        webbrowser.open("https://open.spotify.com/collection/tracks")
        output_widget.insert(tk.END, "AI Model: Opening Spotify...\n", "ai")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        output_widget.insert(tk.END, "AI Model: Opening YouTube...\n", "ai")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        output_widget.insert(tk.END, "AI Model: Opening LinkedIn...\n", "ai")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com/Atharvagaur")
        output_widget.insert(tk.END, "AI Model: Opening GitHub...\n", "ai")
    elif "thanks" in c.lower():
        speak("Thank you for using AI Assistant. Hope you have a great day!")
        output_widget.insert(tk.END, "AI Model: Thank you for using AI Assistant. Hope you have a great day!\n", "ai")
    elif c.lower().startswith("play"):
        song = c.lower().partition(" ")[2]
        link = musiclibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
            output_widget.insert(tk.END, f"AI Model: Playing {song}...\n", "ai")
        else:
            speak("Sorry, I couldn't find that song.")
            output_widget.insert(tk.END, "AI Model: Sorry, I couldn't find that song.\n", "ai")
    elif "news" in c.lower():
        APIKEY = "3bc255f066af4f0781a2df90d96258b3"
        url = "https://newsapi.org/v2/top-headlines"
        params = {"country": "us", "category": "technology", "apikey": APIKEY}
        response = requests.get(url, params=params)
        data = response.json()
        if data['status'] == 'ok' and 'articles' in data:
            articles = 7
            for idx, article in enumerate(data['articles'][:articles], start=1):
                speak(f"News {idx}: {article['title']}")
                output_widget.insert(tk.END, f"AI Model: News {idx}: {article['title']}\n", "ai")
        else:
            speak("Sorry, I couldn't fetch the news.")
            output_widget.insert(tk.END, "AI Model: Sorry, I couldn't fetch the news.\n", "ai")
    else:
        try:
            # Call the Gemini API for other queries
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(c)
            speak(response.text)
            output_widget.insert(tk.END, f"AI Model: {response.text}\n", "ai")
        except Exception as e:
            speak("Sorry, I encountered an error while processing your request.")
            output_widget.insert(tk.END, f"AI Model: Error - {e}\n", "error")

# GUI setup
def run_gui():
    def on_submit():
        command = input_entry.get()
        input_entry.delete(0, tk.END)
        processCommand(command, output_text)

    def listen_voice():
        def recognize():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                output_text.insert(tk.END, "Listening for a command...\n", "info")
                try:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source, timeout=10, phrase_time_limit=10)
                    command = r.recognize_google(audio)
                    output_text.insert(tk.END, f"Voice Command: {command}\n", "user")
                    processCommand(command, output_text)
                except sr.UnknownValueError:
                    output_text.insert(tk.END, "AI Model: Sorry, I didn't catch that.\n", "error")
                except sr.RequestError as e:
                    output_text.insert(tk.END, f"AI Model: Error - {e}\n", "error")
        threading.Thread(target=recognize).start()

    # Main window
    root = tk.Tk()
    root.title("AI Assistant")
    root.geometry("800x600")
    root.resizable(False, False)
    root.configure(bg="#f4f6f9")

    # Styling
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5, background="#4a90e2", foreground="blue")
    style.map("TButton", background=[("active", "#2d9cdb")])
    style.configure("TLabel", font=("Arial", 10), background="#f4f6f9", foreground="#2b2d42")

    title_font = font.Font(family="Helvetica", size=24, weight="bold")

    # Title
    title_label = tk.Label(root, text="AI Assistant", font=title_font, fg="#4a90e2", bg="#f4f6f9")
    title_label.pack(pady=20)

    # Input field
    input_frame = tk.Frame(root, bg="#f4f6f9")
    input_frame.pack(pady=10)

    input_label = ttk.Label(input_frame, text="Enter Command:")
    input_label.pack(side=tk.LEFT, padx=5)

    input_entry = ttk.Entry(input_frame, width=50, font=("Arial", 12))
    input_entry.pack(side=tk.LEFT, padx=5)

    submit_button = ttk.Button(input_frame, text="Submit", command=on_submit)
    submit_button.pack(side=tk.LEFT, padx=5)

    listen_button = ttk.Button(root, text="Listen (Voice Command)", command=listen_voice)
    listen_button.pack(pady=10)

    # Output area
    output_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD, bg="#ffffff", fg="#2b2d42", font=("Arial", 10))
    output_text.tag_configure("user", foreground="#4a90e2")
    output_text.tag_configure("ai", foreground="#2d9cdb")
    output_text.tag_configure("error", foreground="red")
    output_text.tag_configure("info", foreground="#ffcc00")
    output_text.pack(pady=10, padx=10)

    # Run the app
    root.mainloop()

# Run GUI
run_gui()
