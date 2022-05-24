import os
from pathlib import Path

from library.models import Music

YOUTUBE_URL = 'https://www.youtube.com'
MUSIC_FOLDER = '~/Music/PyTunes/'
DOWNLOAD_SUBFOLDER = 'fresh/'

MUSIC_PATH = Path(MUSIC_FOLDER).expanduser()
DOWNLOAD_PATH = MUSIC_PATH / DOWNLOAD_SUBFOLDER
if not DOWNLOAD_PATH.exists():
    if not MUSIC_PATH.exists():
        os.mkdir(MUSIC_PATH)
    os.mkdir(DOWNLOAD_PATH)

ARTIST_FOLDERS = True

TEST_ID = 'test'
TEST_FILE = 'Test.mp3'

class FileHandler:
    def download(self, yt_id):
        if yt_id == TEST_ID:
            return self.FakeDownload(yt_id)
        print(f"Downloading {yt_id}")
        filename = f"{DOWNLOAD_SUBFOLDER}{yt_id}.mp3"
        filepath = MUSIC_PATH / filename
        os.system(f"youtube-dl --extract-audio --audio-format mp3 -o {filepath} {YOUTUBE_URL}/watch?v={yt_id}")
        return str(filepath)

    def FakeDownload(self, yt_id):
        print(f"Fake download of {yt_id}")
        filename = f"{DOWNLOAD_SUBFOLDER}{yt_id}.mp3"
        filepath = MUSIC_PATH / filename
        os.system(f"cp {TEST_FILE} {filepath}")
        return str(filepath)

    def remove(self, filename):
        print(f"Removing {filename}")
        try:
            os.remove(filename)
            return True
        except FileNotFoundError:
            return False

    def move(self, filename, metadata):
        new_folder, new_filename = self.StandardLocation(metadata)
        new_path = MUSIC_PATH / new_folder
        if not (new_path).exists():
            os.mkdir(new_path)
        os.rename(filename, new_path / new_filename) 
        return new_path / new_filename

    @staticmethod
    def StandardLocation(Metadata):
        Title = Metadata.get('title')
        Artist = Metadata.get('artist')
        return (ARTIST_FOLDERS*f"{Artist}/"), f"{Title} - {Artist}.mp3"
