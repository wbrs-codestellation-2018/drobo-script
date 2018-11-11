import paramiko
import os
if os.path.isfile('environ.py'):
    exec(open('./environ.py').read())
from songname import getMetadataFromFile
from songgenre.find_genre import find_genre



basePath = input("Input path to files")
destPath = input("Input path where to store files")
fileList = os.listdir(basePath)
files = []
for file in fileList:
        if file[-3:] == ".mp3":
            files.append(file)
cmd = "if [ ! -d %s ]; then mkdir %s; fi; cp %s %s"
for f in files:
    x = getMetadataFromFile(system_file_path)
    if x:
        genre = find_genre(artist=x['artist'], track=x['track'])
        print(genre)
        pathToGenreFolder = destPath+os.pathsep+genre
        if os.path.exists(pathToGenreFolder) and os.path.isdir(pathToGenreFolder):
        # place in folder
        else:
            os.makedir(genre)
            #place in folder

