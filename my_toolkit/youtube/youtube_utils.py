import os

from pytube import YouTube
from pytube import Playlist


def download_best_audio(link, output_dir=None):
    def _filter_filename(fn):
        return fn.replace("'", '').replace('"', '').replace('.', '').replace('/', '')

    yt = YouTube(link)
    print("Title of video:   ", _filter_filename(yt.title))

    if any([(_filter_filename(yt.title)) in file for file in os.listdir(output_dir)]):
        print(f"SKIP: Audio file {yt.title} is already downloaded.\n")

        return

    print("Length of video:  ", yt.length, "seconds")
    print("Best audio:  ", yt.streams.get_audio_only())

    ys = yt.streams.get_audio_only()
    print("Downloading...")
    ys.download(output_dir)
    print("Download completed!!\n")


def get_playlist_links(link):
    p = Playlist(link)
    return p.video_urls
