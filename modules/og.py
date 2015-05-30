
import requests
import urllib
from HTMLParser import HTMLParser

url = "http://www.theguardian.com/commentisfree/2015/may/22/caesarean-rates-are-too-high-we-should-not-treat-birth-as-a-medical-procedure"

class PyOpenGraph(object):
   
    types = {'activity':['activity', 'sport'],
        'business':['bar', 'company', 'cafe', 'hotel', 'restaurant'],
        'group':['cause' 'sports_league' 'sports_team'],
        'organization':['band', 'government', 'non_profit', 'school', 'university'],
        'person':['actor', 'athlete', 'author', 'director', 'musician', 'politician', 'public_figure'],
        'place':['city', 'country', 'landmark', 'state_province'],
        'product':['album', 'book', 'drink', 'food', 'game', 'isbn', 'movie', 'product', 'song', 'tv_show', 'upc'],
        'website':['article', 'blog', 'website']}
    
    def __init__(self, url):
        f = urllib.urlopen(url)
        contents = f.read()
        f.close()
        p = PyOpenGraphParser()
        p.feed(contents)
        p.close()
        self.metadata = p.properties
    
    def is_valid(self):
        required = set(['title', 'type', 'image', 'url'])
        if (set(self.metadata.keys()).intersection(required)) == required:
            return True
        else:
            return False
    
    def __str__(self):
        return self.metadata['title']
    
class PyOpenGraphParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.properties = {}
    
    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            attrdict = dict(attrs)
            if attrdict.has_key('property') and attrdict['property'].startswith('og:') and attrdict.has_key('content'):
                self.properties[attrdict['property'].replace('og:', '')] = attrdict['content']

    def handle_endtag(self, tag):
        pass
    
    def error(self, msg):
        pass

if __name__ == '__main__':
    # Usage
    og = PyOpenGraph(url)
    print og.metadata
    print og.metadata['title']