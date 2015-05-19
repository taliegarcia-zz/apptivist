
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

def list_climate_orgs(gg_code):
    projects_url = 'https://api.globalgiving.org/api/public/projectservice/themes/%s/projects/active?api_key=%s' % (gg_code, gg_api_key)
    r = requests.get(projects_url, headers=headers)


if __name__ == "__main__":
    # print(gen_gg_dict())
    gg_code = 'climate'


