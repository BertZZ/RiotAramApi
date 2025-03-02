import subprocess
import requests
# import json
import base64


class LobbyData():

    def __init__(self, player_puuid):
        self.player_puuid = player_puuid

    def call(self):
        lobby_data = self.data()
        avalible_champs = lobby_data['benchChampions']
        player_data = self.find_player_data(self.player_puuid, lobby_data)
        return avalible_champs, player_data

    def get_lcu_credentials(self):
        try:
            # Run command to get LCU process details
            result = subprocess.check_output('wmic process where "name=\'LeagueClientUx.exe\'" get CommandLine', shell=True).decode()
            lines = result.split("\n")
            
            port, token = None, None
            for line in lines:
                if "--app-port=" in line:
                    port = line.split("--app-port=")[1].split()[0][:-1]
                if "--remoting-auth-token=" in line:
                    token = line.split("--remoting-auth-token=")[1].split()[0][:-1]
                    print(port, token)
            return port, token
        
        except Exception as e:
            print("Error getting LCU credentials:", e)
            return None, None
    
    def get_aram_lobby_data(self, port, token):
        url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"
        auth_str = f"riot:{token}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_auth}"
        }
        print(url)
        
        try:
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                return response.json()
            else:
                print("Error:", response.status_code, response.text)
                return None
        except Exception as e:
            print("Request failed:", e)
            return None

    def data(self):
        port, token = self.get_lcu_credentials()
        if port and token:
            print(f"LCU API running on port {port}")
            return self.get_aram_lobby_data(port, token)
        else:
            print("League Client not running or credentials not found.")

    def find_player_data(player_puuid, lobby_data):
        return [player for player in lobby_data["myTeam"] if player['puuid'] == player_puuid]
