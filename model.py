"""Models and database functions for Apptivist project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
    ### Front End Models ###

class User(db.Model):
    """User of Apptivist website"""

    __tablename__ = "users" 

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(30), nullable=True)
    zipcode = db.Column(db.String(20), nullable=False) # essential for lookup, joining

class Story(db.Model):
    """Information on the news story posted by a user."""

    __tablename__ = "stories" 

    story_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    img_src = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User", backref=db.backref("stories", order_by=story_id))

class Tag(db.Model):
    """Tags tabl. The tag options are not yet defined on the website. 
    User will be able to select multiple tag objects per story they post to the website."""

    __tablename__ = "tags" 

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    meetup_id = db.Column(db.Integer, db.ForeignKey('meetups.meetup_id'))
    gg_code = db.Column(db.String(64), db.ForeignKey('giving.gg_code'))

    meetup = db.relationship("Meetup", backref=db.backref("tags", order_by=tag_id))
    giving = db.relationship("GlobalGiving", backref=db.backref("tags", order_by=tag_id))


##############################################################################
    ### Association Models ###
#FIXME
## Do NOT make Association Models. See Flask-SQLAlchemy for references on how to handle many-to-many relationships:
## https://pythonhosted.org/Flask-SQLAlchemy/models.html?highlight=many%20many 

class StoryTag(db.Model):
    """Association between news stories and tags"""

    __tablename__ = "storytags" 

    storytag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.story_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
   
    story = db.relationship("Story", backref=db.backref("storytags", order_by=storytag_id))
    tag = db.relationship("Tag", backref=db.backref("storytags", order_by=storytag_id))


class SimilarTag(db.Model):
    """Association between 2 similar tags"""

    __tablename__ = "similartags" 

    similar_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    primary_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
    secondary_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'))
   
    story = db.relationship("Story", backref=db.backref("storytags", order_by=storytag_id))
    tag = db.relationship("Tag", backref=db.backref("storytags", order_by=storytag_id))

##############################################################################
    ### Models relying on API's ###

class Meetup(db.Model):
    """Meetup.com object"""

    __tablename__ = "meetups" 

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


class Congress(db.Model):
    """Congress contact object"""

    __tablename__ = "congress" 

    congress_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(64), nullable=True)
    lname = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    fb = db.Column(db.String(64), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    zipcode = db.Column(db.String(20), nullable=False) # essential for lookup, joining



    def __repr__(self):
        """Provide helpful representation when printed. """

        return "<Congress congress_id=%s congress_email=%s>" % (self.congress_id, self.congress_email)

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