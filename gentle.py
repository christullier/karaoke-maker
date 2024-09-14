import requests
from dotenv import load_dotenv

load_dotenv()
from os import getenv, path

SONG_FOLDER = getenv("SONG_FOLDER")


url = "http://localhost:8765/transcriptions"
data = {
    "audio": open(f"{SONG_FOLDER}/vocals.mp3", "rb"),
    "transcript": open(f"{SONG_FOLDER}/lyrics/real_lyrics.txt", "r"),
}
response = requests.post(url, files=data)

int_counter = 1
gentle_file = f"{SONG_FOLDER}/lyrics/gentle.json"

while path.exists(gentle_file):
    gentle_file = f"{SONG_FOLDER}/lyrics/gentle_int{int_counter}.json"
    int_counter += 1

with open(gentle_file, "wb") as f:
    f.write(response.content)
