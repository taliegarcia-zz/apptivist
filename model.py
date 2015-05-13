"""Models and database functions for Apptivist project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class Meetup(db.Model):
    """Meetup.com object"""

    __tablename__ = "meetup" 

    meetup_id = db.Column(db.Integer, primary_key=True)
    meetup_name = db.Column(db.String(64), nullable=True)
    
    def __repr__(self):
        """Provide helpful representation when printed. """

        return "<Meetup meetup_id=%s meetup_name=%s>" % (self.meetup_id, self.meetup_name)

class GlobalGiving(db.Model):
    """Global Giving object"""

    __tablename__ = "giving" 

    gg_code = db.Column(db.String(64), primary_key=True)
    gg_name = db.Column(db.String(64), nullable=True)
    
    def __repr__(self):
        """Provide helpful representation when printed. """

        return "<GlobalGiving gg_code=%s gg_name=%s>" % (self.gg_code, self.gg_name)

# class Congress(db.Model):
#     """Congress contact object"""

#     __tablename__ = "congress" 

#     giving_code = db.Column(db.String(64), primary_key=True)
#     giving_name = db.Column(db.String(64), nullable=True)
    
#     def __repr__(self):
#         """Provide helpful representation when printed. """

#         return "<Giving giving_code=%s giving_name=%s>" % (self.giving_code, self.giving_name)
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tags.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."