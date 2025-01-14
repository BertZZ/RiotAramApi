import requests

RIOT_BASE_URL = 'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'

# DO NOT COMMIT THIS TO GITHUB IDIOT
RIOT_API_KEY = ''

class Client():

    def __init__(self, username):
        self.username = username

    
    def call(self):
        response = requests.get(RIOT_BASE_URL+username, auth=('user', 'pass'))
        print("DONE")

