from marshmallow import Serializer, fields

##** Interesting...this is for serializing into JSON later...
# this is great for converting to JSON. but its better to pass the actual objects to Jinja for templating
# the JSON is good for js stuff like d3

class UserSerializer(Serializer):
    class Meta:
        fields = ("user_id", "name", "zipcode")
 
class ArticleSerializer(Serializer):
    user = fields.Nested(UserSerializer)
 
    class Meta:
        fields = ("article_id", "title", "url", "img_src", "date", "user_id")

class ActionSerializer(Serializer):
    article = fields.Nested(ArticleSerializer)

    class Meta:
        fields = ("action_id", "tag_id", "article_id", "action_user", "action_type")
    