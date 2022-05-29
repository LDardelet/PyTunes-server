from .download import FileHandler
from .metadata import MetaHandler
from library.models import Music, YtRef

TEST_ID_PREFIX = 'test'

class MainHandler:
    def __init__(self):
        self.FH = FileHandler() # Only inputs and outputs relative filenames, apart from its abs function
        self.MH = MetaHandler() # only works with absolute filenames

    def add(self, yt_id):
        is_test = (TEST_ID_PREFIX in yt_id)
        filename = self.FH.download(yt_id, is_test)
        if not filename:
            return False, False
        metadata = self.MH(self.absolute_path(filename))
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
        ref.is_test = True
        ref.save()
        return True, True

    def remove(self, music):
        ans = self.FH.remove(music.filename)
        music.delete()
        return ans

    def absolute_path(self, relative_path):
        return self.FH.abs(relative_path)

    def get_filename(self, music):
        return self.absolute_path(music.filename)
