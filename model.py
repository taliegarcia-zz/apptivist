"""Models and database functions for Apptivist project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
    ### Association Tables ###

# Association between an article and a tag keyword
article_tags = db.Table('articletags',
    db.Column("articletag_id", db.Integer, autoincrement=True, primary_key=True),
    db.Column("article_id", db.Integer, db.ForeignKey('articles.article_id')),
    db.Column("tag_id", db.Integer, db.ForeignKey('tags.tag_id')))

# Association between two similar tag keywords
sim_tags = db.Table('simtags',
    db.Column("simtag_id", db.Integer, autoincrement=True, primary_key=True),
    db.Column('primary_tag_id', db.Integer, db.ForeignKey('tags.tag_id')),
    db.Column('secondary_tag_id', db.Integer, db.ForeignKey('tags.tag_id'))
)

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

class Article(db.Model):
    """News article posted by user."""

    __tablename__ = "articles" 

    article_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    img_src = db.Column(db.String(200), nullable=True, default="http://placekitten.com/220/220")
    date = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User", backref=db.backref("articles", order_by=article_id))

    tag_list = db.relationship("Tag", secondary=article_tags)

class Tag(db.Model):
    """Tag - a keyword used to distinguish topics on the Apptivist news site."""

    __tablename__ = "tags" 

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tag_name = db.Column(db.String(20), nullable=False, unique=True)
    meetup_topic = db.Column(db.String(64), db.ForeignKey('meetups.meetup_code'))
    gg_code = db.Column(db.String(64), db.ForeignKey('giving.gg_code'))

    meetup = db.relationship("Meetup", backref=db.backref("tags", order_by=tag_id))
    giving = db.relationship("GlobalGiving", backref=db.backref("tags", order_by=tag_id))

    sim_tag_list = db.relationship("Tag", secondary=sim_tags)

    
##############################################################################
    ### Models relying on API's ###

# TODO: Change this to be Meetup topics, not Meetup category_ids
class Meetup(db.Model):
    """Meetup.com object, with topic and name from the meetup website.
    This might become obsolete if I just hardcode the topics into the Tag table.
    Seems redundant."""

    __tablename__ = "meetups" 

    meetup_id = db.Column(db.Integer, primary_key=True)
    # TODO: Set up Meetup topic field. 
    meetup_name = db.Column(db.String(64), nullable=True)
    
    def __repr__(self):
        """Provide helpful representation when printed. """

        return "<Meetup meetup_id=%s meetup_name=%s>" % (self.meetup_id, self.meetup_name)


class GlobalGiving(db.Model):
    """Global Giving object referncing the global giving code and name,
    organized by Theme from Global Giving website"""

    __tablename__ = "giving" 

    gg_code = db.Column(db.String(64), primary_key=True)
    gg_name = db.Column(db.String(64), nullable=True)
    
    def __repr__(self):
        """Provide helpful representation when printed. """

        return "<GlobalGiving gg_code=%s gg_name=%s>" % (self.gg_code, self.gg_name)


##############################################################################
    ### Helper Functions ###

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tags_0517.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."