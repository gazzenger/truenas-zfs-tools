from enum import Enum
import getpass
import json
from dotenv import load_dotenv
import os
import requests
import sys
import time
import urllib3  

class ActionEnum(Enum):
    UNLOCK = 1
    LOCK = 2
    CHECK = 3
    
    @classmethod
    def from_arg(cls, action_str):
        return cls[action_str.upper()]

def VerifyDatasetState(url, headers, dataset_name):
    response = requests.get(url, headers=headers, verify=False)
    result = None

    try:
        data = response.json()
        result = data[0]['locked']
    except:
        print('Failed to verify dataset state')
        exit()

    dataset_state = 'locked' if result else 'unlocked'
    print(f'The current state of {dataset_name} is {dataset_state}')


# Parse dotenv file and variables
load_dotenv()
api_key=os.getenv('API_KEY')
server=os.getenv('SERVER')

if not api_key:
    print('API_KEY not provided')
    print()
    exit()

if not server:
    print('SERVER not provided')
    print()
    exit()

# Parse arguments
args = sys.argv
dataset = ''
action = None

if len(args) != 3:
    print('Wrong number of arguments provided')
    print('Arguments to be provided are: [dataset-name] [action]')
    print('    [dataset-name]: string')
    print('    [action]: unlock, lock or check')
    print()
    print('i.e. $ python zfs-unlock-web.py datapool1/dataset1 unlock')
    print()
    exit()

else:
    try:
        dataset = str(args[1])
        action = ActionEnum.from_arg(args[2])
    except:
        print('Failed parsing arguments')
        print('Arguments to be provided are: [dataset-name] [action]')
        print('    [dataset-name]: string')
        print('    [action]: unlock, lock or check')
        print()
        print('i.e. $ python zfs-unlock-web.py datapool1/dataset1 unlock')
        print()
        exit()

passphrase = getpass.getpass(f'Enter passphrase for {dataset}:') if action == ActionEnum.UNLOCK else ''
host = f'https://{server}'
url_unlock=f'{host}/api/v2.0/pool/dataset/unlock'
url_lock=f'{host}/api/v2.0/pool/dataset/lock'
url_query=f'{host}/api/v2.0/pool/dataset?id={dataset}'

headers = {
    'content-type': 'application/json',
    'accept': '*/*',
    'Authorization': f'Bearer {api_key}',
}

lock_payload = {
    'id': dataset,
}

unlock_payload = {
    'id': dataset,
    'unlock_options': {
        'key_file': False,
        'recursive': True,
        'toggle_attachments': False,
        'datasets': [
            { 
                'name' : dataset,
                'passphrase' : passphrase,
            }
        ]
    }
}

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

if action == ActionEnum.UNLOCK:
    requests.post(url_unlock, data=json.dumps(unlock_payload), headers=headers, verify=False)
    time.sleep(3)
    VerifyDatasetState(url_query, headers, dataset)

elif action == ActionEnum.LOCK:
    requests.post(url_lock, data=json.dumps(lock_payload), headers=headers, verify=False)
    time.sleep(3)
    VerifyDatasetState(url_query, headers, dataset)

elif action == ActionEnum.CHECK:
    VerifyDatasetState(url_query, headers, dataset)

