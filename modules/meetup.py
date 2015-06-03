import requests
import os
import json

meetup_api_key=os.environ['MEETUP_KEY']

###############################################################################
### Looking for upcoming events related to Topics ###

def climate_events(zipcode):
    """Based on a zipcode, this will return a list of specific climate-change
    event info. Each climate-change event's info is organized into dictionaries 
    inside the master list. Right now it also prints the name of each group and the url to their event."""

    search_term = 'climate-change'
    url = 'https://api.meetup.com/2/open_events?zip=%s&topic=%s&page=20&key=%s' % (zipcode, climate, meetup_api_key)
    r = requests.get(url)
    json_results = json.loads(r.text)
    events_list = json_results['results']

    for event in events_list:
        print event['group']['name'].lstrip('0123456789')
        print event['event_url']

    return events_list

def list_events(zipcode, topic):
    """Based on a zipcode and search_term, 
    this will return a list of event info.
    Each event's info is organized into dictionaries inside the master list.
    Right now it also prints (in the console) the name of each group and the url to their event."""

    url = 'https://api.meetup.com/2/open_events?zip=%s&topic=%s&page=20&key=%s' % (zipcode, topic, meetup_api_key)
    r = requests.get(url)
    json_results = json.loads(r.text)

    # FIXME: Might also want to include if 200 AND json_results['results']:
    # right now it looks like the request can get a 200 response code but still have empty results list
    if r.status_code == 200:
        events_list = json_results['results']

        # for event in events_list:
        #     print event['group']['name'].lstrip('0123456789')
        #     print event['event_url']

    else:
        print "No events found."
        events_list = []

    return events_list


###############################################################################

if __name__ == "__main__":
    zipcode = '94043'
    search_term = 'politics'
    upcoming_events = list_events(zipcode, search_term)

