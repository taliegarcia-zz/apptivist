

"""Utility file to seed Apptivist database from third-party API's"""

from model import connect_to_db, db
from model import Meetup, Article, Tag, GlobalGiving, User, article_tags
from server import app

## Modules for API's ##
from apis.meetup import gen_meetup_dict
from apis.global_giving import gen_gg_dict

def load_articles():
    article = Article(title="Mr. Smith Goes to Washington", 
                      url="http://www.google.com",
                      img_src="http://www.placekitten.com/300/300",
                      user_id=942
                    )
    db.session.add(article)
    db.session.commit()
    

def load_users():
    """Load users from u.user into database."""
    open_file = open("./seed_data/u.user")

    for line in open_file:
        user_info = line.rstrip().split("|") # creates a list of the items on the line
        movie_user_id, age, zipcode = user_info[0], user_info[1], user_info[-1]
        new_user = User(name="name%s" % movie_user_id,
                        email="NULL", 
                        password="NULL",  
                        zipcode=zipcode)

        db.session.add(new_user)

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



if __name__ == "__main__":
    connect_to_db(app)
    
    db.create_all()
    print "Created Tables"
    
    load_users()
    print "Loaded Users"
    
    load_articles()
    print "Loaded Articles"
    
    load_meetup()
    print "Loaded Meetup IDs"
    
    load_giving()
    print "Loaded Giving IDs"   