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
####### Some notes about the Meetup URL ###############
# return defaults to JSON, unless the request is followed by .xml
# ie: /2/open_events.xml? # I just used /2/open_events?zip... to get a default json return
# zip='' # pass a zipcode into the url


####### time=Return events scheduled within the given time range, 
# defined by two times separated with a single comma. 
# Each end of the range may be specified with relative dates, 
# such as "1m" for one month from now, or by absolute time in milliseconds 
# since the epoch. If an endpoint is omitted, the range is unbounded 
# on that end. The default value is unbounded on both ends 
# (though restricted to the search window described above). 
# Note: to retrieve past events you must also update status value\

# topics at Meetup: urlkey is the unique identifier of topic 
search_topic = 'environment'
topics_url = 'https://api.meetup.com/topics?search=%s&key=%s' % (search_topic, meetup_api_key)
request_topic_results = requests.get(topics_url)

# try by topic_id
topic_id = '89' # for environment
topic_id_url = 'https://api.meetup.com/topics?id=%s&key=%s' % (topic_id, meetup_api_key)
request_topic_id = requests.get(topic_id_url)
topicid_dict = json.loads(request_topic_id.text)
# does not work. 

# try narrowing scope of search_topic by adding other search terms
search_topic = 'environment+sustainability+climate'
topics_url = 'https://api.meetup.com/topics?search=%s&key=%s' % (search_topic, meetup_api_key)
request_topic_results = requests.get(topics_url)
topic_dict = json.loads(request_topic_results.text)

# be more specific...
urlkey = 'environment'
urlkey_search = 'https://api.meetup.com/urlkey=%s?&key=%s' % (urlkey, meetup_api_key)
request_urlkey = requests.get(urlkey_search)
urlkey_dict = json.loads(request_urlkey.text)
# cannot search by urlkey this way...
