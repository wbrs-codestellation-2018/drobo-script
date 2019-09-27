import subprocess
BASE_PATH = '/mnt/drobo/\'All automation\''

stdout = subprocess.run(f'find {BASE_PATH} -name *.mp3', shell=True, stdout=subprocess.PIPE, text=True).stdout
files = list(map(lambda x: x.strip(), stdout.readlines()))