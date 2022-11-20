from pytube import YouTube
from pytube import Playlist


def download_best_audio(link, output_dir=None):
    yt = YouTube(link)
    print("Title of video:   ", yt.title)
    print("Length of video:  ", yt.length, "seconds")
    print("Best audio:  ", yt.streams.get_audio_only())

    ys = yt.streams.get_audio_only()
    print("Downloading...")
    ys.download(output_dir)
    print("Download completed!!\n")


def get_playlist_links(link):
    p = Playlist(link)
    return p.video_urls
