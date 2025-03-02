import pandas as pd
import json

# opens JSON downloaded from riot containing champ data
with open("champs.json", "r") as file:
    json_data = json.load(file)

#assign the json-level containing champ data
champ_data = json_data['data']

### 
# champ_key  =  unique number value - same as pulled from local client.  eg. "21"
# champ_name =  name of champion seen in game.  eg. Miss Fortune
# champ_id =  stringname of champion used when spaces get in the way.  eg. MissFortune
# note: Riot handles some champ_ids differently eg. Renata Glasc is simply Renata
###

#for each champ in json, create dict based on champ_key for name and id eg "21":{champ_id:"MissFortune", champ_name:"Miss Fortune"} 
champ_dict = {champ['key']:(champ['name'],champ['id']) for champ in champ_data.values()}

#convert dict to df
df = pd.DataFrame.from_dict(champ_dict, orient="index", columns=["champ_name","champ_id"])

#move champkey index into column and rename
df = df.reset_index().rename(columns={'index':'champ_key'})

#create function to take a champ_id and generate the url of the tile-image
def generate_img_url(champ):
    #big old caveat - the game patch is baked into the url - although it looks like old urls are still maintained - functional for now!
    url = f"https://ddragon.leagueoflegends.com/cdn/15.4.1/img/champion/{champ}.png"
    return url

#create new column in dataframe to holding the generated img url for each champion
df['img_url'] = df['champ_id'].apply(lambda x: generate_img_url(x))

#reset champ key to index, then each index gets a dict of the remaining columns - this creates easier to access json structure
df.set_index('champ_key', inplace=True)
json_dict = df.to_dict(orient='index')

#dump to dict to json with champ_key as top-level key 
with open ("champ_refs.json", "w") as file:
    json.dump(json_dict, file, indent=4)