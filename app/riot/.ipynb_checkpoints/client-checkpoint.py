import requests

RIOT_BASE_URL = ''

# DO NOT COMMIT THIS TO GITHUB IDIOT
RIOT_API_KEY = ''

class Client():

    def __init__(self, username):
        self.username = username

    
    def call(self):
        response = requests.get(RIOT_BASE_URL, auth=('user', 'pass'))
        print("DONE")

