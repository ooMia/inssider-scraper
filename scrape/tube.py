from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "https://youtu.be/LAQZfeETFbg"

yt = YouTube(url, on_progress_callback=on_progress)
print(yt.title)

ys = yt.streams.get_audio_only()
ys.download()
