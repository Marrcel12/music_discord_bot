from pytube import YouTube 

import tempfile


    

def yt_mp3(link):
    yt = YouTube(link) 
    stream = yt.streams.filter(only_audio=True).first()
    stream.download()
    return [stream.get_file_path(),stream.title]

