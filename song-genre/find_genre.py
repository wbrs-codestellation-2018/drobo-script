import pygn

def find_genre(ClientID='', artist='', album='', track=''):

    userID = pygn.register(clientID)
    metaData = pygn.search(clientID=clientID, userID=userID, artist=artist, album=album, track=track)
    genre = metaData['genre']['1']['TEXT']

    return genre