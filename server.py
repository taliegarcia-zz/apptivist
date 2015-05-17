"""Apptivist Server"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Article, Meetup, GlobalGiving, connect_to_db, db

from apis.suncongress import gen_rep_list

#FIXME: This is just for temporarily adding articles through webform
import datetime

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined




@app.route('/')
def index():
    """Display the homepage."""

    return render_template("homepage.html")


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



@app.route("/apptivist/<int:id>")
def get_user_by_id(id):
    """Display user info page by user_id
    """
    user = User.query.get(id)

    return render_template("profile.html", user=user)


@app.route("/congress")
def display_congress():
    """This function is only callable from the user's personal profile page,
    and if they are logged in. It returns a congress page with a list of 
    contact info for each of the congress members associated with the user's zipcode."""

    user_id = session.get("user_id")
    
    user = User.query.filter_by(user_id=user_id).first()
    congress_list = gen_rep_list(user.zipcode)
    
    return render_template('congress.html', congress_list=congress_list)

@app.route("/new_post")
def post_an_article():
    url = request.args.get('url')

    tags = request.args.getlist('tag')
    # TODO: consider changing the values of tags in the HTML to the tag_id numbers!
    # right now the tags are strings/code names. 


    print "()()()() This is the URL ()()()()", url
    print "()()()() These are the tags: ()()()()", tags

    return render_template("new_post.html")

    ### Add New Article to the articles table ###
    new_article = Article(title=title,
                        url=url,
                        img_src=img_src,
                        date=date,
                        user_id=session['user_id'])

    db.session.add(new_article)

    ### Append New ArticleTag Association(s) to the articletags tables ###
    for tag_name in tags:
        tag = Tag.query.filter_by(tag_name=tag_name)).first()
        tag.children.append(new_article)

    db.session.commit()
    
    return redirect("/article/%s" % new_article.article_id)
        
@app.route("/add_article", methods=["GET", "POST"])
def add_article():

    if request.args:
        title = request.args.get('title')
        url = request.args.get('url')
        img_src = request.args.get('img_src')
        date_str = request.args.get('date')
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

        new_article = Article(title=title,
                            url=url,
                            img_src=img_src,
                            date=date,
                            user_id=session['user_id'])

        db.session.add(new_article)
        db.session.commit()

        print "()()()() Added:", new_article.title

    return render_template("add_article.html")

# @app.route("/article/<int:id>")
# def get_user_by_id(id):
#     pass


if __name__ == "__main__":
    # Run in debug mode
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()


