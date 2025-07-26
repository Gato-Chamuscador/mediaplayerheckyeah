import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilename
import customtkinter as ctk
from mutagen.mp3 import MP3
import time
import os
#hide pygame message in console
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


global filepath
audiolength = None
audioisplaying = False
current_time = 0.0
pos = 0.0
start_time = 0.0 
pause_time = 0.0 #Time when the music has been paused
paused_total = 0.0 #Total time the music has been paused
#init pygme mixer
pygame.mixer.init()

#this function asks to open the file and loads it to the pygame mixer
def loadfile():
    global audiolength, filepath, pos
    try:
        filepath = askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        #checks mp3 from the filepath and takes the audio length from it
        audiolength = MP3(filepath).info.length
        if filepath:
            pos = 0
            pygame.mixer.music.load(filepath)
            print("Audio loaded successfully")
        else:
            print("No file selected")
    except Exception as e:
        print(f"Error loading file {e}")

#play/pause toggle
def toggle_play_pause():
    global pos, start_time, pause_time, paused_total, audioisplaying
    try:
        if audioisplaying:
            pygame.mixer.music.pause()
            pause_time = time.time() #When the music paused
            play_btn.configure(text = "▶")
            audioisplaying = False
            print("pausing audio")
        else:
            if start_time <= 0:
                pygame.mixer.music.play()
                play_btn.configure(text = "⏸")
                start_time = time.time() #When the music started playing(For the first time)
                calculate_progress_bar()
                audioisplaying = True
                print("playing audio")
            else:
                pygame.mixer.music.unpause()
                play_btn.configure(text = "⏸")
                paused_total += time.time() - pause_time  #Calculate the time the music has been stopped
                calculate_progress_bar()
                audioisplaying = True
                print("unpsausing audio")

    except Exception as e:
        print(f"{e}")
    

#stop the audio, unload track and take the audiotime to the start
def stopaudio():
    global pos, audioisplaying, paused_total, start_time, pause_time
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        app.title("MEDIAPLAYERHECKYEAH")
        paused_total = 0
        start_time = 0
        pause_time = 0
        pos = 0
        audioisplaying = False
    except Exception as e:
        print(f"Cannot stop audio {e}")




#calculate the bar progress
def calculate_progress_bar():
    global start_time, paused_total, audioisplaying, pos, audiolength, filepath, current_time
    if not filepath or audiolength is None:
        return 

    if audioisplaying:
        #Makes the bar move
        current_time = (time.time() - start_time) - paused_total
    else:
        #Makes bar stop
        current_time = pause_time - start_time - paused_total

    bar_percentage = current_time / audiolength
    progressbar.set(bar_percentage)
    app.after(200, calculate_progress_bar)

    if current_time >= audiolength:
        current_time = audiolength
        pos = 0
        progressbar.set(1.0)
        pygame.mixer.music.stop()
        print("Audio finished")
        return
    
    


def forward():
    global current_time, audiolength, audioisplaying
    if filepath and audiolength:
        new_pos = current_time + 10
        if new_pos >= audiolength:
            new_pos = audiolength - 0.1 
        pygame.mixer.music.play(start=new_pos)
        play_btn.configure(text = "⏸")
        audioisplaying = True
        global start_time, paused_total
        start_time = time.time() - new_pos
        paused_total = 0
        current_time = new_pos
        print(f"Forwarded to {int(new_pos)}s")


def rewind():
    global current_time, audiolength, audioisplaying
    if filepath and audiolength:
        new_pos = current_time - 10
        if new_pos <= 0:
            new_pos = 0 
        pygame.mixer.music.play(start=new_pos)
        audioisplaying = True
        play_btn.configure(text = "⏸")
        global start_time, paused_total
        start_time = time.time() - new_pos
        paused_total = 0
        current_time = new_pos
        print(f"Rewinded to {int(new_pos)}s")


#key controlls
def on_space(event):
    toggle_play_pause()

def on_right_key(event):
    forward()

def on_left_key(event):
    rewind()

def on_ctrl_q(event):
    on_closing()

#This functions use (event) to avoid getting broken by tkinter when the function is called on app.bind("key") and tkinter gives it an argument

#close all processes
def on_closing():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    app.destroy()


#create app
app = ctk.CTk()
app.title("MEDIAPLAYERHECKYEAH")
app.geometry("400x400")
app.resizable(False, False)
ctk.set_appearance_mode("dark")
#buttons
load_btn = ctk.CTkButton(app, text="Load Audio", command=loadfile)
load_btn.place(x=130, y=100)

play_btn = ctk.CTkButton(app, text="▶", width=5, height=30, command=toggle_play_pause)
play_btn.place(x=190, y=150)

stop_btn = ctk.CTkButton(app, text="⏹", command=stopaudio)
stop_btn.place(x=130, y=190)

forward_btn = ctk.CTkButton(app, text="⏩", width=10, height=30, command=forward)
forward_btn.place(x=238, y=150)

rewind_btn = ctk.CTkButton(app, text="⏪", width=10, height=30, command=rewind)
rewind_btn.place(x=130, y=150)

#progress bar
progressbar = ctk.CTkProgressBar(app, orientation="horizontal")
progressbar.place(x =110 ,y=240)
progressbar.set(0)


#detect if space is pressed
app.bind("<space>", on_space)

app.bind("<Right>", on_right_key)

app.bind("<Left>", on_left_key)

app.bind("<Control-q>", on_ctrl_q)


#close app when window is closed
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()