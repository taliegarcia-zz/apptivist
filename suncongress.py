import requests
import os
import json

sunlight_api_key=os.environ['SUNLIGHT_KEY']
headers = {'X-APIKEY': sunlight_api_key}

### Sends Request to API ###
def gen_rep_list(zipcode_str):
    """This function returns a list of dictionaries 
    of the contact information of every congress member 
    based on an input zipcode"""
    
    url = 'https://congress.api.sunlightfoundation.com/legislators/locate?zip=%s' % zipcode_str
    
    r = requests.get(url, headers=headers)
    request_dict = json.loads(r.text)
    congress_list = request_dict['results']

    return congress_list 

#### Test Run: ####'
if __name__ == "__main__":
    my_dict = gen_rep_list('94070')
    print(my_dict)


