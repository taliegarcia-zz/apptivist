

"""Utility file to seed Apptivist database from Mockaroo CSV's"""

from model import connect_to_db, db
from model import Article, Tag, User, Action, article_tags
from server import app
import datetime


def load_mock_users():
    """Load users from users.csv into database."""
    
    print "Loading Mock Users..."

    for i, row in enumerate(open("seed_data/mockaroo/users-50-topcities.csv")):
        row = row.rstrip().split(",")
        user_id, name, email, password, zipcode = row

        user = User(name=name,
                    email=email, 
                    password=password,  
                    zipcode=zipcode)

        db.session.add(user)

    db.session.commit()
    print "Mock users table loaded."


###############################################################################
### Article Loads ###

def load_mock_articles():
    """This loads the few articles from short_article_list.csv
    These articles already have associated tags so they will be 
    good for experimenting with."""

    print "Mockaroo Articles Loading..."

    for i, row in enumerate(open("seed_data/mockaroo/articles100.csv")):
        row = row.rstrip().split(",")
        article_id, title, url, img_src, date_str, user_id = row

        date = datetime.datetime.strptime(date_str, "%Y-%b-%d")

        article = Article(
                    title=title, 
                    url=url,
                    img_src=img_src,
                    date=date,
                    user_id=user_id)

        db.session.add(article)

    db.session.commit()
    print "Mockaroo Articles table loaded."


###############################################################################
### Tag Loads ###


def load_tags():
    """Loads the few articletag connections I made already. 
    Good for experimenting!"""

    print "Tags Loading..."

    for i, row in enumerate(open("seed_data/tagnames.csv")):
        row = row.rstrip().split(",")
        tag_id, tag_name, meetup_topic, gg_code = row

        tag = Tag(
                tag_name=tag_name,
                meetup_topic=meetup_topic,
                gg_code=gg_code
                )
        
        db.session.add(tag)     

    db.session.commit() 
    print "Tags table loaded."


def load_mock_article_tags():
    """This loads mocked articletag associations"""

    print "Mock ArticleTags Loading..."

    for i, row in enumerate(open("seed_data/mockaroo/articletags.csv")):
        row = row.rstrip().split(",")
        article_id, tag_id = row

        if Article.query.get(article_id):
            article = Article.query.get(article_id)
            tag = Tag.query.get(tag_id)
            article.tag_list.append(tag)

        db.session.commit()    

    print "Mock ArticleTags table loaded."    

###############################################################################
### Action Items to Load ###

def load_mock_actions():
    """This loads mocked action items"""

    print "Mockaroo Actions Loading..."

    for i, row in enumerate(open("seed_data/mockaroo/actionitems.csv")):
        row = row.rstrip().split(",")
        action_id,tag_id,article_id,action_user,action_type = row

        action = Action(
                    action_id=action_id,
                    tag_id=tag_id,
                    article_id=article_id,
                    action_user=action_user,
                    action_type=action_type
                    )

        db.session.add(action)

    db.session.commit()
    print "Mocked actions table loaded."


##############################################################################
    ### Helper Functions ###

if __name__ == "__main__":

    connect_to_db(app)
    print "Connected to DB."    

    # db.create_all()