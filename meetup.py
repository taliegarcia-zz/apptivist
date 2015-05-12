import requests
import os
import json

meetup_api_key=os.environ['MEETUP_KEY']


def gen_meetup_dict():
    categories_url = 'https://api.meetup.com/2/categories?key=%s&&sign=true' % meetup_api_key
    request_categories = requests.get(categories_url)
    categories_dict = json.loads(request_categories.text)
    categories_list = categories_dict.get('results') 

    meetup_dict = {}
    for category in categories_list:

        meetup_dict[str(category['id'])] = str(category['shortname']) 

    return meetup_dict

if __name__ == "__main__":
    my_dict = gen_meetup_dict()
    print(my_dict)

