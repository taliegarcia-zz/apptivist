#Apptivist
#####Saving the world one click at a time!
Apptivist is an interactive social news app for passionate activists to participate in current events. Apptivist creates a pipeline for direct action when readers are inspired by the news they read. No longer will a reader be limited to “like”, “share”, or “comment” on a story that interests them. Now, when users post an article on the Apptivist site, the article automatically links to real world activities — enabling readers to find related in-person events, charities seeking support, and pertinent contact information of local government representatives. The site also stores and tracks usage information so that users can visualize their impact.



####Tech Stack
Python, Flask, Jinja, Marshmallow, SQLAlchemy, SQLite, JavaScript, d3, jQuery, HTML, CSS, AJAX, BootStrap

####API's
Meetup.com API, GlobalGiving.org API, Sunlight Congress RESTful API


####User Features:
> **Ability for the user to:**

> - Post a news article to the site
  * View preview of article before posting
> - Tag articles with keywords from eight different categories
> - Read news articles posted by o†her users 
  * In newsfeed, sorted by date posted
  * Can optionally be sorted by category too
> - Take one of three actions after reading an interesting article:
  * Look up related Meetup.com events 
  * Find related GlobalGiving.org charity projects
  * Contact their local govt representative 
> - View user profiles with the following details:
  * Influence: A data tree representing their influence on the site: articles they have posted, and actions that other users have taken since reading those articles
  * Actions: A list of the user's actions made when interacting with the site
  * Articles: listing all articles the user has posted to the site


####Server-side Features:
> **Ability for the app to:**

> - Display newsfeed either by date or by category tag, after querying database in SQLite
> - Preview article posts by parsing header tags in the new url for Open Graph Protocol data. Return the result to the browser for the user to preview their post.
> - Use the database associating Apptivist category tags to categories on Meetup and Global Giving sites. 
> - Use the associated terms to send requests to Meetup API and Global Giving API. Results are returned in JSON, then rendered in browser for user
> - Based on the user's zipcode, send request to Sunlight Congress API for contact information on all the user's local government officials
> - Track and store user's actions on the site. Everytime a user clicks on an official Meetup, Global Giving, or Congress link, send the information of that event back to the server to be added to a database of user actions
> - Nestle the tracked user data into a tree object to be rendered by d3 javascript into a collapsible graph on the user's profile page - the Influence tree!







##Install Apptivist

Clone or fork this repo: 

```
https://github.com/taliegarcia/apptivist.git

```

Create and activate a virtual environment inside your project directory: 

```

virtualenv env

source env/bin/activate

```

Install the requirements:

```
pip install -r requirements.txt

```

Get your own secret keys for Meetup.com, GlobalGiving.org, and Sunlight Labs and save them to a file <kbd>secrets.sh</kbd>. You should also set your own secret key for Flask. 
	
Source your secret keys:

```
source keys.sh

```

Run the app:

```
python server.py

```
Navigate to localhost:5000/ to view the news Apptivist newsfeed!
