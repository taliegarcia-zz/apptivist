"""Apptivist Server"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Article, Tag, Meetup, GlobalGiving, connect_to_db, db

from apis.suncongress import gen_rep_list
from apis.meetup import list_events
from apis.global_giving import list_giving_projs

#FIXME: This is just for temporarily adding articles through webform
import datetime

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

###############################################################################
    ### Homepage ###
    
@app.route('/')
def show_newsfeed():
    """Display newsfeed on Homepage"""

    articles = Article.query.all()
   
    return render_template("newsfeed.html", articles=articles)

###############################################################################
    ### User Registration ###
@app.route('/registration', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("reg_form.html")


@app.route('/registration', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    zipcode = request.form["zipcode"]

    new_user = User(name=name, email=email, password=password, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    # automatically log in the new user:
    session["user_id"] = new_user.user_id

    flash("Welcome to the movement, %s. You are now logged in and ready to get active!" % name)

    print User.query.filter_by(name=name).first()

    return redirect("/")

###############################################################################
    ### User Login/Logout ###

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    name = request.form["name"]
    password = request.form["password"]

    user = User.query.filter_by(name=name).first()

    if not user:
        print "No such user"
        return redirect("/login")

    if user.password != password:
        print "Incorrect password"
        return redirect("/login")

    session["user_id"] = user.user_id

    print "Logged in"

    return redirect("/apptivist/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

###############################################################################
    ### User Profile Page ###

@app.route("/apptivist/<int:id>")
def get_user_by_id(id):
    """Display user info page by user_id
    """
    user = User.query.get(id)

    return render_template("profile.html", user=user)


###############################################################################
    ### Post New Article Pages ###

# FIXME. new articles should be posted by "POST" method, not "GET", since it is communicating with my db
@app.route("/new_post", methods=["GET", "POST"])
def post_an_article():

    if request.args:
        url = request.args.get('url')
        title = request.args.get('title')
        img_src = request.args.get('img_src')
        date_str = request.args.get('date')
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        ### Add New Article to the articles table ###
        article = Article(title=title,
                            url=url,
                            img_src=img_src,
                            date=date,
                            user_id=session['user_id'])
        db.session.add(article)
        db.session.commit() # needs to be committed here before it can be added to article_tags table below

        ### Append New ArticleTag Association(s) to the articletags tables ###
        tags = request.args.getlist('tag')
        # TODO: consider changing the values of tags in the HTML to the tag_id numbers!

        for tag_name in tags:
            tag = Tag.query.filter_by(tag_name=tag_name).first()
            article.tag_list.append(tag.tag_id)

        db.session.commit()
            
    return render_template("new_post.html")

# INTERNAL - this is an internal web form for me to add articles to my db quickly & easily  
# FIXME. new articles should be posted by "POST" method, not "GET", since it is communicating with my db     
@app.route("/add_article", methods=["GET", "POST"])
def add_article():

    if request.args:
        title = request.args.get('title')
        url = request.args.get('url')
        img_src = request.args.get('img_src')
        # date_str = request.args.get('date')
        # date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        article = Article(title=title,
                            url=url,
                            img_src=img_src,
                            # date=date,
                            user_id=session['user_id'])

        db.session.add(article)
        db.session.commit()

        print "()()()() Added:", article.title

        # TODO: this should eventually redirect to new article page:
        # redirect("/article/<int:id>")
        return redirect("/") 

    return render_template("add_article.html")


###############################################################################
    ### Display Article Page ###

@app.route("/article/<title>", methods=['GET'])
def display_article(title):
    """Show individual article page.

    If a user is logged in, let them view possible actions.
    """

    article = Article.query.filter_by(title=title).first()

    for tag in article.tag_list:
        print "()()()() The type of thing is: ", type(tag)
        print "()()()() This is an associated tag: ", tag.tag_name
        

    user_id = session.get("user_id")

    if user_id:
        user = User.query.get(user_id)

    return render_template("article.html",
                           user=user,
                           article=article,
                        )


###############################################################################
    ### API Results Pages ###

@app.route("/meet/<title>", methods=['GET'])
def display_meetups(title):
    """This will display meetup info based on 
    tags associated with this article.
    meetup_dict_by_tag keeps the tag object with the generated meetup info,
    this keeps things organized and separate on the results page."""

    article = Article.query.filter_by(title=title).first()

    user = User.query.get(session['user_id'])

    if user:
        meetup_dict_by_tag = {}
        for tag in article.tag_list:
            meetup_dict_by_tag[tag] = list_events(user.zipcode, tag.meetup_topic)

    return render_template("meet.html", article=article, meetup_dict=meetup_dict_by_tag)


@app.route("/give/<title>", methods=['GET'])
def display_giving_projs(title):
    """This will display list of Global Giving Projects"""

    article = Article.query.filter_by(title=title).first()

    user = User.query.get(session['user_id'])

    if user:
        giving_dict_by_tag = {}
        for tag in article.tag_list:
            giving_dict_by_tag[tag] = list_giving_projs(tag.gg_code)

           
    if not giving_dict_by_tag:
        giving_dict_by_tag["Error"] = "Sorry no results found."

    return render_template("give.html", article=article, giving_projs=giving_dict_by_tag)


@app.route("/congress/<zipcode>", methods=["GET"])
def lookup_congress(zipcode):
    """This returns a congress page with a list of 
    contact info for each of the congress members associated 
    with the user's zipcode."""

    congress_list = gen_rep_list(zipcode)
    
    return render_template('congress.html', congress_list=congress_list)

###############################################################################
    ### Tracking Routes - Tracking Usage Behaviour on the site ###


# @app.route('/action/<action_object>', methods=['POST'])
# def add_action_to_db(action_object):
    
    
#     db.session.add(new_action)
#     db.session.commit()
#     return "Added action to db" 


###############################################################################
    ### Run Server ###

if __name__ == "__main__":
    # Run in debug mode
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()


