# Make sure you have installed pytube3 on your system. If not done, follow these steps:-
# Open your anaconda or python3 app and use the following command:
# pip install pytubeX
# This will install the pytubeX which will be required.
import os

from pytube import YouTube

from toolkit.youtube.youtube_utils import download_best_audio


def is_already_downloaded(_link):
    already_downloaded = os.listdir('files/download_audio')
    title = YouTube(_link).title
    for downloaded in already_downloaded:
        if downloaded.startswith(title):
            return True
    return False


if __name__ == "__main__":

    # Asking for all the video links
    links = []

    with open("files/download_audio/to_download.txt", 'r') as f:
        links.extend(f.read().split('\n'))
    n = len(links)
    print(links)

    # Showing all details for videos and downloading them one by one
    for i in range(0, n):
        link = links[i]
        print(f"{link: ^50}")
        if not link.startswith('http'):
            print('SKIPPED: Invalid link')
            continue

        if is_already_downloaded(link):
            print('SKIPPED: Already download_audio')
            continue



        download_best_audio(link, 'files/download_audio')
