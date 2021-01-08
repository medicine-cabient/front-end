from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class Mjrecomendationform(FlaskForm):
    getrecomendations = StringField("Type how you're feeling, and we'll recomend some strains")
    submit = SubmitField('Lets Toke!')