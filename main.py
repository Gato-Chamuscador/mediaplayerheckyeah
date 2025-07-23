import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
#hide pygame message in console
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

filepath = None

#this function asks to open the file and loads it to the pygame mixer
def loadfile():
    global filepath
    filepath = askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])

    if filepath:
        #init pygme mixer
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        print("Audio loaded successfully")
    else:
        print("Cannot load audio")

def playfile():
    try:
        pygame.mixer.music.play()
        app.title(f"Playing {filepath}")
    except:
        print("No audio loaded")

def stopaudio():
    try:
        pygame.mixer.music.stop()
        app.title("MEDIAPLAYERHECKYEAH")
    except:
        print("Cannot stop audio")


#create app
app = ctk.CTk()
app.title("MEDIAPLAYERHECKYEAH")
app.geometry("400x400")
app.resizable(False, False)

# Buttons
load_btn = ctk.CTkButton(app, text="Load Audio", command=loadfile)
load_btn.pack(pady=40)

play_btn = ctk.CTkButton(app, text="Play", command=playfile)
play_btn.pack(pady=30)

stop_btn = ctk.CTkButton(app, text="Stop", command=stopaudio)
stop_btn.pack(pady=20)

app.mainloop()