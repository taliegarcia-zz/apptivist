"""Apptivist Server"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Article, Tag, Meetup, GlobalGiving, connect_to_db, db

from apis.suncongress import gen_rep_list

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
    ### Congress Lookup Page ###

# FIXME: make it so the app.route is "/congress/<zipcode>"
@app.route("/congress", methods=["POST"])
def display_congress():
    """This function is only callable from the user's personal profile page,
    and if they are logged in. It returns a congress page with a list of 
    contact info for each of the congress members associated with the user's zipcode."""

    user_id = session.get("user_id")
    
    user = User.query.filter_by(user_id=user_id).first()
    congress_list = gen_rep_list(user.zipcode)
    
    return render_template('congress.html', congress_list=congress_list)


###############################################################################
    ### Article Posting Pages ###

@app.route("/new_post", methods=["GET", "POST"])
def post_an_article():

    if request.args:
        url = request.args.get('url')
        title = request.args.get('title')
        img_src = request.args.get('img_src')
        date_str = request.args.get('date')
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        tags = request.args.getlist('tag')
        # TODO: consider changing the values of tags in the HTML to the tag_id numbers!
        # right now the tags are strings/code names. 

        print "()()()() This is the URL ()()()()", url
        print "()()()() These are the tags: ()()()()", tags

        if not request.args:
            return render_template("new_post.html")

        ### Add New Article to the articles table ###
        new_article = Article(title=title,
                            url=url,
                            img_src=img_src,
                            date=date,
                            user_id=session['user_id'])
        db.session.add(new_article)
        db.session.commit() # needs to be committed here before it can be added to article_tags table below

        ### Append New ArticleTag Association(s) to the articletags tables ###
        for tag_name in tags:
            tag = Tag.query.filter_by(tag_name=tag_name).first()
            tag.children.append(new_article)

        db.session.commit()
    
    return render_template("new_post.html")

# INTERNAL - this is an internal web form for me to add articles to my db quickly & easily       
@app.route("/add_article", methods=["GET", "POST"])
def add_article():

    if request.args:
        title = request.args.get('title')
        url = request.args.get('url')
        img_src = request.args.get('img_src')
        # date_str = request.args.get('date')
        # date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        new_article = Article(title=title,
                            url=url,
                            img_src=img_src,
                            # date=date,
                            user_id=session['user_id'])

        db.session.add(new_article)
        db.session.commit()

        print "()()()() Added:", new_article.title

        # TODO: this should eventually redirect to new article page:
        # redirect("/article/<int:id>")
        return redirect("/") 

    return render_template("add_article.html")


###############################################################################
    ### Article Page ###

@app.route("/article/<int:article_id>", methods=['GET'])
def article_detail(article_id):
    """Show individual article page.

    If a user is logged in, let them view possible actions.
    """

    article = Article.query.get(article_id)

    user_id = session.get("user_id")

    if user_id:
        user = User.query.get(user_id)
    

    # else:
    #     user_action = None

    return render_template("article.html",
                           user=user,
                           article=article)


###############################################################################
    ### Article Page ###

if __name__ == "__main__":
    # Run in debug mode
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()


