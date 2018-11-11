import paramiko
import os
import shutil
if os.path.isfile('environ.py'):
    exec(open('./environ.py').read())
from songname import getMetadataFromFile
from songgenre.find_genre import find_genre



basePath = input("Input path to files")
fileList = os.listdir(basePath)
# print(fileList)
files = []
for file in fileList:
    # print(file[-3:  ])
    if file[-3:] == "mp3":
        files.append(file)
            # print(file)
# cmd = "if [ ! -d %s ]; then mkdir %s; fi; cp %s %s"
for f in files:
    x = getMetadataFromFile(f)
    # print(x)
    if x:
        genre = find_genre(artist=x['artist'], track=x['track'])
        print(genre)
        pathToGenreFolder = os.path.join(basePath,genre)
        
        if os.path.exists(pathToGenreFolder) and os.path.isdir(pathToGenreFolder):
        # place in folder
            print("TRUE")
            shutil.copyfile(f,pathToGenreFolder)
        else:
            print("false")
            os.makedir(genre)
            shutil.copyfile(f,pathToGenreFolder)
            #place in folder

