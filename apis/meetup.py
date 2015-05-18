import requests
import os
import json

meetup_api_key=os.environ['MEETUP_KEY']


def gen_meetup_dict():
    categories_url = 'https://api.meetup.com/2/categories?key=%s&&sign=true' % meetup_api_key
    request_categories = requests.get(categories_url)
    # TODO check status code 2xx aka "OK!" so that it doesnt return error message to the user of the site
    categories_dict = json.loads(request_categories.text)
    categories_list = categories_dict.get('results') 

    meetup_dict = {}
    for category in categories_list:

        meetup_dict[str(category['id'])] = str(category['shortname']) 

    return meetup_dict

if __name__ == "__main__":
    my_dict = gen_meetup_dict()
    print(my_dict)


#### Exploration of Meetup API for Upcoming Events ####
## using python -i meetup.py ##
events_url = "https://api.meetup.com/2/open_events?zip=94110&time=,1w&key=%s" % meetup_api_key
request_events = requests.get(events_url)


# NVM. topic = climate-change delivers the best results for topics.
climate = 'climate-change'
zipcode = '10012'
climate_topics_url = 'https://api.meetup.com/2/open_events?zip=%s&topic=%s&page=20&key=%s' % (zipcode, climate, meetup_api_key)
climate_results = requests.get(climate_topics_url)
climate_dict = json.loads(climate_results.text)