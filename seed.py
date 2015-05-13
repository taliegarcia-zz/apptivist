"""Utility file to seed Apptivist database from third-party API's"""

from model import connect_to_db, db
from model import Meetup, GlobalGiving #, Congress
from server import app

## Modules for API's ##
from meetup import gen_meetup_dict
from global_giving import gen_gg_dict

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

def load_congress():
    pass


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_meetup()
    load_giving()