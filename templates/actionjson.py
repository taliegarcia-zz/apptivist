
@app.route("/apptivist/<name>")

user_id = session['user_id']



######
var data = [
    { "name" : "Level 2: A", "parent":"Top Level" },
    { "name" : "Top Level", "parent":"null" },
    { "name" : "Son of A", "parent":"Level 2: A" },
    { "name" : "Daughter of A", "parent":"Level 2: A" },
    { "name" : "Level 2: B", "parent":"Top Level" }
    ];

var data = [
    { "name" : "Article 1", "parent":"User" },
    { "name" : "User", "parent":"null" },
    { "name" : "Action A", "parent":"Article 1" },
    { "name" : "Action B", "parent":"Article 1" },
    { "name" : "Article 2", "parent":"User" }
    ];
######

# influences = {}
from serializer import UserSerializer, ArticleSerializer, ActionSerializer

@app.route("/influencetree")
def get_influences_json(user_id):
    influences = {}

    user = User.query.get(session["user_id"])

    user_info = UserSerializer(user).data

    influences['user'] = user_info

    influences['user']['articles'] = []

    articles = Article.query.filter_by(user_id=session["user_id"]).all

    for a in articles
        influences['user']['articles'].append(ArticleSerializer(a).data)
       
        influences['user']['articles']['actions'] = []
       
        actions = Action.query.filter_by(article_id=a.article_id).all()
       
            if actions:
                for act in actions:
                    influences['user']['articles']['actions'].append(ActionSerializer(act).data)

    return influences 




@app.route("/influencetree")
def get_influences_json(user_id):
    influences = {}

    influences['user_id'] = user_id
    influences['children'] = [] # for all article objects

    articles = Article.query.filter_by(user_id=user_id).all

    if articles:
	    for a in articles:
	        influences['children'].append({
                'article_id': a.article_id,
	            'title': a.title,
	            'tags': a.tag_list,
                'children': [] # for all action objects
	        })

            actions = Action.query.filter_by(article_id=a.article_id).all()
	        
	        if actions:
	        	for act in actions:
                    influences['children'][a.article_id]['children'].append(
                        {'name': act.action_type, 
                        'user_id': act.action_user
                        })
		        	