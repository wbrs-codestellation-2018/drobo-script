import os
import subprocess
from acrcloud.recognizer import ACRCloudRecognizer
import json
if os.path.isfile('../environ.py'):
    print("EXECUTING")
    exec(open('./environ.py').read() )

config = {
        #Replace "xxxxxxxx" below with your project's host, access_key and access_secret.
        'host': os.environ['ACR_HOST'],
        'access_key': os.environ['ACR_ACCESS_KEY'], 
        'access_secret': os.environ['ACR_ACCESS_SECRET'],
        'timeout':10 # seconds
    }
recognizer = ACRCloudRecognizer(config)

# Artist
# Track
def getMetadataFromFile(filename):
    returned_orig = recognizer.recognize_by_file(filename, 0)
    returned = json.loads(returned_orig)

    if returned['status']['msg'] == "No result":
        return None
    print(returned_orig)
    return {'artist': returned['metadata']['music'][0]['external_metadata']['spotify']['artists'][0]['name'],
            'track': returned['metadata']['music'][0]['external_metadata']['spotify']['track']['name']}


