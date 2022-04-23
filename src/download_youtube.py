from pytube import YouTube
from pathlib import Path
import os
from colorama import init, Fore

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

def on_complete(stream, file_path):
    """Print sucess message and file path once download completed"""
    print('Download completed.')
    print(file_path)

def on_progress(stream, chunk, bytes_remaining):
    """Print progress during downloading"""
    print(f'{round(100 - (bytes_remaining / stream.filesize * 100),2)}%')

init()
link = input('Youtube link: ')
video_object = YouTube(link, on_complete_callback= on_complete, on_progress_callback= on_progress)
path_to_download_folder = get_download_path()

#information
#\033[39m return the color to white 
print(Fore.RED + f'Title       : \033[39m {video_object.title}')
print(Fore.RED + f'Author      : \033[39m {video_object.author}')
print(Fore.RED + f'Publish Date: \033[39m {video_object.publish_date}')
print(Fore.RED + f'Length      : \033[39m {round(video_object.length/ 60, 2)} minutes')
print(Fore.RED + f'Views       : \033[39m {video_object.views / 1000000} million')

#download
print(
    Fore.RED + 'Download: ' + 
    Fore.GREEN + '(b)est \033[39m| ' + 
    Fore.YELLOW + '(w)orst \033[39m| ' + 
    Fore.BLUE + '(a)udio \033[39m| (e)xit'
    )
download_choice = input('Choice: ')

match download_choice:
    case 'b':
        video_object.streams.get_highest_resolution().download(path_to_download_folder)
    case 'w':
        video_object.streams.get_lowest_resolution().download(path_to_download_folder)
    case 'a':
        video_object.streams.get_audio_only().download(path_to_download_folder)
