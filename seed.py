"""Utility file to seed Apptivist database from third-party API's"""

from model import connect_to_db, db
from model import Meetup #, Giving, Congress
from server import app

from meetup import gen_meetup_dict

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
    pass

def load_congress():
    pass


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    mud = load_meetup()