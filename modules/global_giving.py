
import requests
import os
import json

gg_api_key=os.environ['GLOBAL_GIVING_KEY']
headers = {'Accept': 'application/json'} # returns json

def gen_gg_dict():
    """First attempts experimenting with Global Giving API.
    Returns a dictionary of Global Giving's broad category/theme codes
    for all projects."""

    themes_url = 'https://api.globalgiving.org/api/public/projectservice/themes?api_key=%s' % gg_api_key
    req_all_themes = requests.get(themes_url, headers=headers) 

    themes_dict = json.loads(req_all_themes.text)
    themes_list = themes_dict.get('themes').values()[0]

    gg_dict = {}

    for theme in themes_list:

        gg_dict[str(theme['id'])] = str(theme['name']) 

    return gg_dict

def list_giving_projs(gg_code):
    """Returns a list of dictionaries, each dictionary containing details of a 
    Global Giving project. The results returned depend on the search code used,
    the gg_code."""

    projects_url = 'https://api.globalgiving.org/api/public/projectservice/themes/%s/projects/active?api_key=%s' % (gg_code, gg_api_key)
    r = requests.get(projects_url, headers=headers)
    dictionary = json.loads(r.text)
    list_of_project_dictionaries = dictionary['projects']['project']

    for project in list_of_project_dictionaries:
        print project

    return list_of_project_dictionaries


if __name__ == "__main__":
    print "Dictionary of Global Giving's Theme Codes for Projects: ", gen_gg_dict()
    gg_code = 'climate'