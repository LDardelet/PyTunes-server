from .download import FileHandler
from .metadata import MetaHandler
from library.models import Music, YtRef

class MainHandler:
    def __init__(self):
        self.FH = FileHandler()
        self.MH = MetaHandler()

    def add(self, yt_id):
        filename = self.FH.download(yt_id)
        if not filename:
            return False, False
        metadata = self.MH(filename)
        if not metadata:
            return True, False
        filename = self.FH.move(filename, metadata)
        music = Music(title = metadata.get('title'),
                      artist = metadata.get('artist'),
                      album = metadata.get('album'),
                      filename = filename)
        music.save()
        ref = YtRef.objects.get(yt_id = yt_id)
        ref.music = music
        ref.save()
        return True, True

    def remove(self, filename):
        self.FH.remove(filename)
