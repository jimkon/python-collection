# Make sure you have installed pytube3 on your system. If not done, follow these steps:-
# Open your anaconda or python3 app and use the following command:
# pip install pytubeX
# This will install the pytubeX which will be required.
import os

from pytube import YouTube

from my_toolkit.youtube.youtube_utils import download_best_audio, get_playlist_links


DESTINATION_FOLDER = 'files/download_audio_playlist'


def is_already_downloaded(_link):
    try:
        already_downloaded = os.listdir(DESTINATION_FOLDER)
        title = YouTube(_link).title
        for downloaded in already_downloaded:
            if downloaded.startswith(title):
                return True
    except Exception as e:
        print(f"ERROR ({e}): is_already_downloaded failed")
    return False


if __name__ == "__main__":

    # Asking for all the video links
    links = get_playlist_links(input("Playlist link:"))
    print(f"{len(links)}: {links=}")

    n = len(links)

    # Showing all details for videos and downloading them one by one
    for i in range(0, n):
        link = links[i]
        print(f"{i}: {link: ^50}")
        if not link.startswith('http'):
            print('SKIPPED: Invalid link')
            continue

        # if is_already_downloaded(link):
        #     print('SKIPPED: Already download_audio')
        #     continue

        try:
            download_best_audio(link, DESTINATION_FOLDER)
        except Exception as e:
            print(f"ERROR ({e}): Link {link} failed...")
