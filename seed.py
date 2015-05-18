

"""Utility file to seed Apptivist database from third-party API's"""

from model import connect_to_db, db
from model import Meetup, Article, Tag, GlobalGiving, User, article_tags
from server import app

## Modules for API's ##
from apis.meetup import gen_meetup_dict
from apis.global_giving import gen_gg_dict

def load_users():
    """Load users from users.csv into database."""
    
    print "Loading Users..."

    for i, row in enumerate(open("seed_data/users.csv")):
        row = row.rstrip().split(",")
        user_id, name, email, password, zipcode = row

        user = User(user_id=user_id,
                    name=name,
                    email=email, 
                    password=password,  
                    zipcode=zipcode)

        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    db.session.commit()


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


###############################################################################
### Seed Data Based on CSV Files ###

def load_first_article():
    """Hardcoded first article load function. Test."""

    article = Article(title="Mr. Smith Goes to Washington", 
                      url="http://www.google.com",
                      img_src="http://www.placekitten.com/300/300",
                      user_id=942)

    db.session.add(article)
    
    db.session.commit()
    


def load_actual_articles():
    """This will load the ~40 articles from actual_articles.csv"""

    print "Articles Loading..."

    for i, row in enumerate(open("seed_data/article_data/actual_articles.csv")):
        row = row.rstrip().split(",")
        article_id, title, url, empty_string, date, user_id = row

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

def load_short_articles():
    """This loads the few articles from short_article_list.csv
    These articles already have associated tags so they will be 
    good for experimenting with."""

    print "Articles Loading..."

    for i, row in enumerate(open("seed_data/article_data/short_article_list.csv")):
        row = row.rstrip().split(",")
        article_id, title, url, img_src, date, user_id = row

        article = Article(
                    article_id=article_id,
                    title=title, 
                    url=url,
                    img_src=img_src,
                    date=date,
                    user_id=user_id)

        db.session.add(article)

    db.session.commit()


def load_article_tags():
    """Loads the few articletag connections I made already. 
    Good for experimenting!"""

    print "ArticleTags Loading..."

    for i, row in enumerate(open("seed_data/articletags.csv")):
        row = row.rstrip().split(",")
        article_id, tag_id = row

        article = Article.query.get(article_id)
        article.tag_list.append(tag_id)

        db.session.commit()        



if __name__ == "__main__":
    connect_to_db(app)
    
    db.create_all()
    print "Created Tables"
    
    load_users()
    print "Loaded Users"
    
    load_short_articles()
    print "Loaded Short Articles"
    
    load_meetup()
    print "Loaded Meetup IDs"
    
    load_giving()
    print "Loaded Giving IDs"   