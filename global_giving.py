
import requests
import os
import json

gg_api_key=os.environ['GLOBAL_GIVING_KEY']
headers = {'Accept': 'application/json'} # returns json

def gen_gg_dict():
    themes_url = 'https://api.globalgiving.org/api/public/projectservice/themes?api_key=%s' % gg_api_key
    req_all_themes = requests.get(themes_url, headers=headers) 

    themes_dict = json.loads(req_all_themes.text)
    themes_list = themes_dict.get('themes').values()[0]

    gg_dict = {}

    for theme in themes_list:

        gg_dict[str(theme['id'])] = str(theme['name']) 

    return gg_dict


if __name__ == "__main__":
    print(gen_gg_dict())



