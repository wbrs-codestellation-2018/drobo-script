# import paramiko
import os
import subprocess
from dotenv import load_dotenv
import shutil
load_dotenv()
   
from songname import getMetadataFromFile
from songgenre.find_genre import find_genre
# for each file in drobo: 
#   read file into temporary storage
#   get metadata from file
#   get genres from metadata
#   move song to genre folder

manifest = {}
with open('manifest.csv', 'r') as f:
    for line in f:
        print(line)
        path, status = line.split(':')
        manifest[path] = int(status)
BASE_PATH = '/mnt/drobo/\'All automation\''
DEST_PATH = '/mnt/drobo/Genres2'
cmd = "if [ ! -d %s ]; then mkdir %s; fi; cp %s %s"
# ssh = paramiko.SSHClient()
# print(os.environ['ACR_HOST'])
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('129.64.82.25', username="WBRS", password=os.environ['SERVER_PASSWORD'])
# _, stdout, _ = ssh.exec_command("find %s -name *.mp3" % BASE_PATH)
# files = list(map(lambda x : x.strip(), stdout.readlines()))
print("STARTING")
# stdout = subprocess.run(f'find {BASE_PATH} -name *.mp3', shell=True, stdout=subprocess.PIPE, text=True).stdout
# files = map(lambda x : x.strip(), stdout.split("\n"))
# print(files)
try: 
    # ftp_client=ssh.open_sftp()
    for f in manifest:
        print("PROCESSING", f)
        # system_file_path = os.path.join('/tmp', f.split('/')[-1])
        # print(system_file_path)
        # ftp_client.get(f, system_file_path)
        if manifest[f] == 1:
            continue
        try:
            x = getMetadataFromFile(f)
        except Exception as e:
            subprocess.run(f'echo "{e}" | sendmail binaryman00010@gmail.com -', shell=True)
        if x:
            genre = find_genre(artist=x['artist'], track=x['track'])
            genre_dir = "'%s'" % os.path.join(DEST_PATH, genre)
            command = subprocess.run(cmd % (genre_dir,genre_dir,"'%s'" % f, genre_dir),
                                shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("MOVED TO", genre_dir)
            print(command.stdout, command.stderr)
            # print(cmd % (genre_dir,genre_dir,f, genre_dir))
            # _, stdout, stder = ssh.exec_command(cmd % (genre_dir,genre_dir,"'%s'" % f, genre_dir))
            # print(stdout.readlines())
            # print(stderr.readlines())
        else:
            genre_dir = "'%s'" % os.path.join(DEST_PATH, "unknown")
            print("MOVED TO", genre_dir)
            command = subprocess.run(cmd % (genre_dir,genre_dir,"'%s'" % f, genre_dir),
                                shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(command.stdout, command.stderr)
            # print(cmd % (genre_dir,genre_dir,f, genre_dir))
            # _, stdout, stderr = ssh.exec_command(cmd % (genre_dir,genre_dir,"'%s'" % f, genre_dir))
            # print(stdout.readlines())
            # print(stderr.readlines())
        manifest[f] = 1
        # os.remove(system_file_path)
    subprocess.run('echo "success" | sendmail binaryman00010@gmail.com -', shell=True)
    print("COMPLETE")
except Exception as e:
    subprocess.run(f'echo "{e}" | sendmail binaryman00010@gmail.com -', shell=True)
    print(e)
    # ftp_client.close()
finally:
    shutil.copyfile('manifest.csv', 'manifest.csv.bak')
    with open('manifest.csv', 'w') as f:
        for x in manifest:
            f.write(f'{x}:{manifest[x]}\n')
print("CLOSING")
# ssh.close()   
