from . import pygn
import os

def find_genre(artist='', album='', track=''):

    userID = pygn.register(os.environ['PYGN_CLIENT_ID'])
    metaData = pygn.search(clientID=os.environ['PYGN_CLIENT_ID'], userID=userID, artist=artist, album=album, track=track)
    try:
        genre = metaData['genre']['1']['TEXT']
    except: 
        return None
    return genre