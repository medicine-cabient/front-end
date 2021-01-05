from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class Mjrecomendationform(FlaskForm):
    getrecomendations = StringField("Simply type anything")
    submit = SubmitField('Get Recomendations')