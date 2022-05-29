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

ARTIST_FOLDER = True
ALBUM_FOLDER = True

TEST_FILE = 'Test.mp3'

YOUTUBE_DL_METADATA = "--add-metadata"

class FileHandler:
    def download(self, yt_id, is_test):
        if is_test:
            return self.FakeDownload(yt_id)
        print(f"Downloading {yt_id}")
        relative_path = f"{DOWNLOAD_SUBFOLDER}{yt_id}.mp3"
        os.system(f"youtube-dl --extract-audio --audio-format mp3 -o {self.abs(relative_path)} {YOUTUBE_DL_METADATA} {YOUTUBE_URL}/watch?v={yt_id}")
        return relative_path

    @property
    def FilesFolder(self):
        return str(MUSIC_PATH)

    def FakeDownload(self, yt_id):
        print(f"Fake download of {yt_id}")
        relative_path = f"{DOWNLOAD_SUBFOLDER}{yt_id}.mp3"
        os.system(f"cp {TEST_FILE} {self.abs(relative_path)}")
        return relative_path

    def remove(self, relative_path):
        print(f"Removing {self.abs(relative_path)}")
        try:
            os.remove(self.abs(relative_path))
            return True
        except FileNotFoundError:
            return False

    def move(self, old_relative_filename, metadata):
        relative_path_parts = self.StandardLocation(metadata)
        
        relative_path = ''
        for path_part in relative_path_parts[:-1]:
            relative_path += path_part
            if not (self.abs(relative_path)).exists():
                os.mkdir(self.abs(relative_path))
        relative_path += relative_path_parts[-1]
        os.rename(self.abs(old_relative_filename), self.abs(relative_path))
        return relative_path

    @staticmethod
    def StandardLocation(Metadata):
        Title = Metadata.get('title')
        Artist = Metadata.get('artist')
        Album = Metadata.get('album')
        return (ARTIST_FOLDER*f"{Artist}/"), (ALBUM_FOLDER*f"{Album}/"), f"{Title} - {Artist}.mp3"

    @staticmethod
    def abs(relative_path):
        return MUSIC_PATH / relative_path

