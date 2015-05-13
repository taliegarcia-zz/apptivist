import requests
import os
import json

sunlight_api_key=os.environ['SUNLIGHT_KEY']
headers = {'X-APIKEY': sunlight_api_key}
# zipcode_lookup_url = 'https://congress.api.sunlightfoundation.com/legislators/locate?zip=%s'
url = 'https://congress.api.sunlightfoundation.com/legislators/locate?zip=%s' % '94070'
    
r = requests.get(url, headers=headers)

for rep in r_dict.get('results'):
    print "First Name: ", rep['first_name']
    print "Last Name: ", rep['last_name']
    print "Phone: ", rep['phone']
    print "Email: ", rep['oc_email']
    print "Facebook: ", rep['facebook_id']
    print "Twitter: ", rep['twitter_id']
    print "Youtube: ", rep['youtube_id']
    print "Contact Form: ", rep['contact_form']
    print "Website: ", rep['contact_form']

    # print """***STATE RANK*** """, rep['state_rank'] - Not Working.


def gen_congress_dict():
    """This function creates a dictionary from the JSON string returned by Sunglight's Congress API"""
    # r = requests.get(url, headers=headers)

    # congress_dict = {}
    # id_num = 0 # could use this to initialize db id#s
    pass


def show_congress_contacts():
    """This function displays the contact information for congress members based on an input zipcode"""
    zipcode = raw_input("What is your zipcode? > ")
    url = 'https://congress.api.sunlightfoundation.com/legislators/locate?zip=%s' % zipcode
    
    r = requests.get(url, headers=headers)

    r # returns request object
    r.text # returns unicode string
    r_dict = json.loads(r.text) # creates dictionary!
    r_dict.keys() # returns keys: count, results, page
    r_dict.get('results') # returns list of legislator info


    ### this will loop through and 
    for i in range(r_dict.get('count')):
        print "Name: ", r_dict.get('results')[i]['first_name'], r_dict.get('results')[i]['last_name']
        print "Phone: ", r_dict.get('results')[i]['phone']



