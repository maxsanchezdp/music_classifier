import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request
import os
from dotenv import load_dotenv
load_dotenv()

if not ("CID" or "SECRET") in os.environ:
    raise ValueError("You should have a valid Client ID and Client Secret for Spotify for devs in os.environ. "
                     "Check https://developer.spotify.com/")

CID=os.environ['CID']
SECRET=os.environ['SECRET']

def play_song(path):
    os.system("mpg123 " + path)


# Spotipy functions:

def get_songs():
    client_credentials_manager = SpotifyClientCredentials(client_id=CID, client_secret=SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    while True:
        try:
            artist = input("\nArtist: ")
            song = input("Song: ")
            search = sp.search(q='artist:' + artist + ' track:' + song, type='track')
            top = search['tracks']['items'][:10]
            assert (len(top) != 0)
            break
        except AssertionError:
            print("\nSorry, artist/song not found :( Try again!")
    lista = []
    for element in top:
        elemento = []
        elemento.append(element['name'])
        lista.append(elemento)
        artistas = []
        for a in element['artists']:
            artistas.append(a['name'])
        elemento.append(artistas)
        elemento.append(element['id'])
    return lista


def select_song(lista):
    for i, el in enumerate(lista):
        print(f'\n{i}. {el[0]} - {el[1]}')
    choice = int(input("\nChoose your song (number): "))
    song_id = lista[choice][2]
    return song_id

def get_url(song_id):
    client_credentials_manager = SpotifyClientCredentials(client_id=CID, client_secret=SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    track = sp.track(song_id)
    url=[]
    url.append(track['preview_url'])
    # if len(url) == 0 or url[0] == None:
    #     print ("\nSorry, there's no preview available for your song :(")
    # else:
    return url[0]


def download_song(url):
    print('\nBeginning file download with urllib2...')
    path = './Data/unlabelled_songs/song.mp3'
    urllib.request.urlretrieve(url, f'./Data/unlabelled_songs/song.mp3')
    print('\nFile downloaded')
    return path


# FUNCTIONS TO INCLUDE in main.py:


def execute_spoti():
    while True:
        try:
            lista = get_songs()
            song = select_song(lista)
            url = get_url(song)
            assert (url != None)
            break
        except AssertionError:
            print("\nSorry, there's no preview available for your song :( Try again!")
    path = download_song(url)
    return path
