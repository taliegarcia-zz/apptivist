import requests
import os
import json

AFG_KEY=os.environ['ALLFORGOOD_KEY']
# headers = {'Accept': 'application/json', 'Content-Type': 'application/json'} # returns json
zipcode = '94110'
search_term = 'environment'

url = 'http://api2.allforgood.org/api/volopps?q=%s&vol_loc=%s&output=json&key=%s' % (search_term, zipcode, AFG_KEY)

r = requests.get(url)

mydict = json.loads(r.text)

mydict.get('items') # returns a list of dictionaries

mydict.get('items')[0] # first item in that dictionary

for d in mydict.get('items'):
    print "Sponsor: ", d['sponsoringOrganizationName']
    print "Title: ", d['title']
    print "Link: ", d['url_short']

    