

"""Utility file to seed Apptivist database from third-party API's"""

from model import connect_to_db, db
from model import Meetup, Article, Tag, GlobalGiving, User, article_tags
from server import app
import datetime

## Modules for API's ##
from apis.meetup import gen_meetup_dict
from apis.global_giving import gen_gg_dict

def load_users():
    """Load users from users.csv into database."""
    
    print "Loading Users..."

    for i, row in enumerate(open("seed_data/users.csv")):
        row = row.rstrip().split(",")
        user_id, name, email, password, zipcode = row

        user = User(name=name,
                    email=email, 
                    password=password,  
                    zipcode=zipcode)

        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print "On User row", i

    db.session.commit()
    print "Users table loaded."


def load_meetup():
    """Load Meetup Items from the Meetup site. 
    The items come from the Meetup module which sends a request to the Meetup API 
    and returns a dictionary"""

    meetup_dict = gen_meetup_dict()

    for item in meetup_dict.items():
        meetup_id_str, meetup_name = item
        meetup_id = int(meetup_id_str)
        new_meetup_item = Meetup(meetup_id=meetup_id,
                            meetup_name=meetup_name
                            )
        db.session.add(new_meetup_item)

    db.session.commit()
    print "Loaded Meetup IDs"


def load_giving():
    """Load Global Giving Items from the GG site. 
    The items come from the global_giving module which sends a request to the GG API 
    and returns a dictionary"""

    gg_dict = gen_gg_dict()

    for item in gg_dict.items():
        gg_code, gg_name = item
        new_gg_item = GlobalGiving(gg_code=gg_code,
                            gg_name=gg_name
                            )
        db.session.add(new_gg_item)

    db.session.commit()
    print "Loaded Giving IDs"   


###############################################################################
### Article Loads ###

def load_first_article():
    """Hardcoded first article load function. Test."""

    print "First Article loading..."
    article = Article(title="Mr. Smith Goes to Washington", 
                      url="http://www.google.com",
                      img_src="http://www.placekitten.com/300/300",
                      user_id=942)

    db.session.add(article)
    
    db.session.commit()
    print "First Article loaded."
    


def load_actual_articles():
    """This will load the ~40 articles from actual_articles.csv"""

    print "Actual Articles Loading..."

    for i, row in enumerate(open("seed_data/article_data/actual_articles.csv")):
        row = row.rstrip().split(",")
        article_id, title, url, empty_string, date_str, user_id = row

        if date_str:
            date = datetime.datetime.strptime(date_str, "%Y-%b-%d")
        else:
            date = None

        article = Article(
                    article_id=article_id,
                    title=title, 
                    url=url,
                    date=date,
                    user_id=user_id)
        db.session.add(article)

        # provide some sense of progress
        if i % 10 == 0:
            print i

    db.session.commit()
    print "Actual Articles loaded."

def load_short_articles():
    """This loads the few articles from short_article_list.csv
    These articles already have associated tags so they will be 
    good for experimenting with."""

    print "Short Articles Loading..."

    for i, row in enumerate(open("seed_data/article_data/short_article_list.csv")):
        row = row.rstrip().split(",")
        article_id, title, url, img_src, date_str, user_id = row

        # if date_str:
        #     date = datetime.datetime.strptime(date_str, "%Y-%b-%d")
        # else:
        #     date = None

        article = Article(
                    title=title, 
                    url=url,
                    img_src=img_src,
                    date="NULL",
                    user_id=user_id)

        db.session.add(article)

    db.session.commit()
    print "Short Articles table loaded."


###############################################################################
### Tag Loads ###


def load_tags():
    """Loads the few articletag connections I made already. 
    Good for experimenting!"""

    print "Tags Loading..."

    for i, row in enumerate(open("seed_data/tag_names.csv")):
        row = row.rstrip().split(",")
        tag_id, tag_name, meetup_id, gg_code = row

        tag = Tag(
                tag_name=tag_name,
                meetup_id=meetup_id,
                gg_code=gg_code
                )
        
        db.session.add(tag)     

    db.session.commit() 
    print "Tags table loaded."


def load_article_tags():
    """Loads the few articletag connections I made already. 
    Good for experimenting!"""

    print "ArticleTags Loading..."

    for i, row in enumerate(open("seed_data/articletags.csv")):
        row = row.rstrip().split(",")
        article_id, tag_id = row

        if Article.query.get(article_id):
            article = Article.query.get(article_id)
            tag = Tag.query.get(tag_id)
            article.tag_list.append(tag)

        db.session.commit()    

    print "ArticleTags table loaded."    


###############################################################################
if __name__ == "__main__":
    connect_to_db(app)
    
    db.create_all()
    print "Tables Set Up"
    
    load_users()
    
    load_short_articles()

    load_tags()
  
    load_meetup()
    
    load_giving()

    load_article_tags()
