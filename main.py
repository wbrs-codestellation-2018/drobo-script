# import paramiko
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()
   
from songname import getMetadataFromFile
from songgenre.find_genre import find_genre
# for each file in drobo: 
#   read file into temporary storage
#   get metadata from file
#   get genres from metadata
#   move song to genre folder

BASE_PATH = '/mnt/drobo/\'WBRS Automation\''
DEST_PATH = '/mnt/drobo/Genres2'
cmd = "if [ ! -d %s ]; then mkdir %s; fi; cp %s %s"
# ssh = paramiko.SSHClient()
# print(os.environ['ACR_HOST'])
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('129.64.82.25', username="WBRS", password=os.environ['SERVER_PASSWORD'])
# _, stdout, _ = ssh.exec_command("find %s -name *.mp3" % BASE_PATH)
# files = list(map(lambda x : x.strip(), stdout.readlines()))
print("STARTING")
stdout = subprocess.run(f'find {BASE_PATH} -name *.mp3', 
            shell=True, stdout=subprocess.PIPE, text=True).stdout
files = list(map(lambda x : x.strip(), stdout.split("\n")))
# print(files)
try: 
    # ftp_client=ssh.open_sftp()
    for f in files:
        print("PROCESSING", f)
        # system_file_path = os.path.join('/tmp', f.split('/')[-1])
        # print(system_file_path)
        # ftp_client.get(f, system_file_path)
        x = getMetadataFromFile(f)
        if x:
            genre = find_genre(artist=x['artist'], track=x['track'])
            genre_dir = "'%s'" % os.path.join(DEST_PATH, genre)
            command = subprocess.run(cmd % (genre_dir,genre_dir,"'%s'" % f, genre_dir),
                                shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(command.stdout, command.stderr)
            # print(cmd % (genre_dir,genre_dir,f, genre_dir))
            # _, stdout, stder = ssh.exec_command(cmd % (genre_dir,genre_dir,"'%s'" % f, genre_dir))
            # print(stdout.readlines())
            # print(stderr.readlines())
        else:
            genre_dir = "'%s'" % os.path.join(DEST_PATH, "unknown")
            command = subprocess.run(cmd % (genre_dir,genre_dir,"'%s'" % f, genre_dir),
                                shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(command.stdout, command.stderr)
            # print(cmd % (genre_dir,genre_dir,f, genre_dir))
            # _, stdout, stderr = ssh.exec_command(cmd % (genre_dir,genre_dir,"'%s'" % f, genre_dir))
            # print(stdout.readlines())
            # print(stderr.readlines())
        # os.remove(system_file_path)
    subprocess.run('echo "success" | sendmail binaryman00010@gmail.com -')
except e:
    subprocess.run(f'echo "e" | sendmail binaryman00010@gmail.com -')
    # ftp_client.close()
print("CLOSING")
# ssh.close()