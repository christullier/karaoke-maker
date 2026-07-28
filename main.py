# models:
# base
# large-v2
# medium
# small.en # small
# tiny.en

# models: base, large-v2, medium, small.en, small, tiny.en
import csv
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pygame
from dotenv import load_dotenv
from matplotlib.animation import FuncAnimation
from pydub import AudioSegment

load_dotenv()

SONG_FOLDER = os.getenv("SONG_FOLDER")


def load_lyrics(file_path):
    lyrics = []
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")

        for row in reader:
            start_time = int(row[0]) if row[0].isdigit() else 0
            end_time = int(row[1]) if row[1].isdigit() else 0
            text = row[2]
            lyrics.append((start_time, end_time, text))
    return lyrics


# Function to display lyrics in sync with the song
def display_lyrics_in_time(lyrics):
    for start_time, end_time, text in lyrics:
        current_time_ms = pygame.mixer.music.get_pos()
        # Wait until the song time matches the lyric's start time
        while current_time_ms < start_time:
            current_time_ms = pygame.mixer.music.get_pos()
            time.sleep(0.01)  # To prevent busy-waiting
            # Print the lyric when the time matches
            time.sleep(0.01)
        print(text)


# Initialize pygame mixer for audio playback
pygame.mixer.init()


# Initialize pygame mixer
pygame.mixer.init()

# Load the song and play it
audio_file = f"{SONG_FOLDER}/vocals.mp3"
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play()

# Load the MP3 file using pydub
audio = AudioSegment.from_mp3(audio_file)

# Get raw data as a bytestring
raw_data = np.array(audio.get_array_of_samples())

# Calculate time values for the x-axis
time = np.linspace(0, len(raw_data) / audio.frame_rate, num=len(raw_data))

# Initialize the plot
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(time, raw_data, label="Waveform")
ax.set_title("Waveform of vocals.mp3")
ax.set_ylabel("Amplitude")
ax.set_xlabel("Time (seconds)")
line = ax.axvline(0, color="r")  # Moving bar (initial position at 0 seconds)


# Function to update the position of the bar
def update(frame):
    # Get the current time of the song in seconds
    current_time = pygame.mixer.music.get_pos() / 1000  # in seconds

    # Update the position of the vertical line (bar)
    line.set_xdata(current_time)

    return (line,)


# Animate the bar
ani = FuncAnimation(fig, update, blit=True, interval=100)

plt.show()
# Load and play the song
pygame.mixer.music.load(f"{SONG_FOLDER}/vocals.mp3")
pygame.mixer.music.play()

# Load the lyrics from the .tsv file
lyrics = load_lyrics(f"{SONG_FOLDER}/lyrics/lyrics.tsv")

# Start displaying lyrics in sync with the song
display_lyrics_in_time(lyrics)

# Wait for the song to finish
while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Song finished!")

# curl -F "audio=@music/probably_up/vocals.mp3" -F "transcript=@music/probably_up/lyrics/lyrics.txt" "http://localhost:8765/transcriptions?async=false"
