import paramiko
import os
if os.path.isfile('environ.py'):
    exec(open('./environ.py').read())
   
from songname import getMetadataFromFile
from songgenre.find_genre import find_genre
# for each file in drobo: 
#   read file into temporary storage
#   get metadata from file
#   get genres from metadata
#   move song to genre folder

BASE_PATH = '/mnt/DroboFS/Shares/Music/WBRS\ Automation'
DEST_PATH = '/mnt/DroboFS/Shares/Music/Genres'
cmd = "if [ ! -d %s ]; then mkdir %s; fi; cp %s %s"
ssh = paramiko.SSHClient()
# print(os.environ['ACR_HOST'])
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('129.64.82.25', username="WBRS", password=os.environ['SERVER_PASSWORD'])
_, stdout, _ = ssh.exec_command("find %s -name *.mp3" % BASE_PATH)
files = list(map(lambda x : x.strip(), stdout.readlines()))
try: 
    ftp_client=ssh.open_sftp()
    for f in files:
        
        system_file_path = os.path.join('/tmp', f.split('/')[-1])
        print(system_file_path)
        ftp_client.get(f, system_file_path)
        x = getMetadataFromFile(system_file_path)
        if x:
            genre = find_genre(artist=x['artist'], track=x['track'])
            ssh.exec_command("if")
        else:
        os.remove(system_file_path)

finally:
    ftp_client.close()

ssh.close()