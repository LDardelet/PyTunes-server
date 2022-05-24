import requests
import base64
from pydub import AudioSegment
import json
import random

URL = "https://shazam.p.rapidapi.com/songs/v2/detect"
DEFAULT_SIZE_BYTES = 499000
START_TIMESTAMP_SECONDS = 30
TIMEZONE = "Europe/Paris"

SONG_MAX_DURATION_SECONDS = 10*60

USEFUL_FIELDS = ('title', 'artist', 'album')

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
        data = self.get_data(filename)
        self.clean_response(data)
        if data:
            self.populate_default(data)
            self.write(filename, data)
        return data

    def FakeResponse(self, filename):
        print(f"Creating fake metadata for file {filename}")
        return {'title':f'FakeTitle_{random.randint(0,10)}',
                'artist':f'FakeArtist_{random.randint(0,2)}',
                'album':f'FakeAlbum_{random.randint(0,2)}'}

    def get_data(self, filename):
        if not self.ActivateShazam:
            return self.FakeResponse(filename)
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

    def clean_response(self, data): # We dont want to populate data with default values here, in order to know if we actually retrieved data
        for key in list(data.keys()):
            if key not in USEFUL_FIELDS:
                del data[key]

    def populate_default(self, data):
        for field in USEFUL_FIELDS:
            data.setdefault(field, f"Unknown {field}")

    def write(self, filename, data):
        audio = AudioSegment.from_mp3(filename)
        audio.export(filename, format="mp3", tags={'artist':data.get('artist'), 'title':data.get('artist')})
