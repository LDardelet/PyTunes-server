import requests
import base64
from pydub import AudioSegment
from pydub.utils import mediainfo
import json
import random

URL = "https://shazam.p.rapidapi.com/songs/v2/detect"
DEFAULT_SIZE_BYTES = 499000
START_TIMESTAMP_SECONDS = 30
TIMEZONE = "Europe/Paris"

SONG_MAX_DURATION_SECONDS = 10*60

TITLE, ARTIST, ALBUM = USEFUL_FIELDS = ('title', 'artist', 'album')
FILLED = 'filled'

class MetaHandler:
    ActivateShazam = False
    def __init__(self):
        try:
            with open("./api-key", "r") as f:
                self.API_KEY = f.read()
                self.ValidKey = True
        except FileNotFoundError:
            self.ValidKey = False

    def __call__(self, filename):
        data = self.check_data(filename)  # We check if metadata are already present
        if data[FILLED]:
            print(f"Metadata already exists for file {filename}")
            return data                   # If so, we send it immediately
        else:
            data = self.get_data(filename)# Else, we try to retrieve it ourselves
        if data[FILLED]:
            print(f"Saving metadata for file {filename}")
            self.write(filename, data)    # In this case, we save it inside the file
        return data

    def fake_response(self, filename):
        print(f"Creating fake metadata for file {filename}")
        return {TITLE: f'FakeTitle_{random.randint(0,10)}',
                ARTIST:f'FakeArtist_{random.randint(0,2)}',
                ALBUM: f'FakeAlbum_{random.randint(0,2)}'}

    def check_data(self, filename):
        data = mediainfo(filename).get('TAG',None)
        return self.clean_response(data)

    def get_data(self, filename):
        if not self.ActivateShazam:
            return self.clean_response(self.fake_response(filename))
        else:
            return self.clean_response(self.shazam_response(filename))

    def shazam_response(self, filename):
        if not self.ValidKey:
            print("No valid key found (./api-key)")
            return {}
        #segment = AudioSegment.from_mp3(filename).set_channels(1)
        segment = AudioSegment.from_mp3(filename).split_to_mono()
        if segment.duration_seconds > SONG_MAX_DURATION_SECONDS:
            print("File does not fit the duration of a standard music. Aborting shazam match")
            return {}
        data = base64.b64encode(segment[START_TIMESTAMP_SECONDS*1000:(START_TIMESTAMP_SECONDS+10)*1000]._data)
        payload = data[:int((DEFAULT_SIZE_BYTES / sys.getsizeof(data)) * len(data))]
        
        headers = {
            "content-type": "text/plain",
            "X-RapidAPI-Host": "shazam.p.rapidapi.com",
            "X-RapidAPI-Key": self.API_KEY
        }
        querystring = {"timezone":TIMEZONE,"locale":"en-US"}

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        try:
            return self.clean_response(response.json())
        except json.JSONDecodeError:
            print(f"Failed to retrieve metadata for file {filename}")
            return {}

    def clean_response(self, data):
        clean_data = {FILLED: (TITLE in data)}
        for field in USEFUL_FIELDS:
            clean_data[field] = data.get(field, f"Unknown {field}")
            clean_data[f"{field}_{FILLED}"] = (field in data)
        return clean_data

    def write(self, filename, data):
        audio = AudioSegment.from_mp3(filename)
        audio.export(filename, format="mp3", tags={field:data.get(field) for field in USEFUL_FIELDS})
