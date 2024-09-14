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

import pygame
from dotenv import load_dotenv

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
