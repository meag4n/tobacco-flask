import pymysql
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

app = Flask(__name__)
application = app

app.config['SECRET_KEY'] = 'ex'

username = 'ex'
password = 'ex'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server  = 'meagandipolo.com'
dbname   = '/meaganre_tobacco'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

db = SQLAlchemy(app)

class Tobacco(db.Model):
    __tablename__ = 'youth_tobacco'
    id = db.Column(db.Integer, primary_key=True)
    county = db.Column(db.String)
    tobacco = db.Column(db.String)
    cigarettes = db.Column(db.String)
    cigars = db.Column(db.String)
    smokeless = db.Column(db.String)
    hookah = db.Column(db.String)
    evape = db.Column(db.String)
    education = db.Column(db.String)
    rank = db.Column(db.String)
    population = db.Column(db.Integer)
    retailers = db.Column(db.Integer)
    density = db.Column(db.Float)

counties = Tobacco.query.order_by(Tobacco.county).all()

pairs_list = []
for county in counties:
    pairs_list.append((county.id, county.county))

class CountySelect(FlaskForm):
    select = SelectField("Choose a county", choices=pairs_list)
    submit = SubmitField("Submit")

@app.route('/')
def index():
    form = CountySelect()
    return render_template("index.html", form=form)

@app.route('/county', methods = ['POST'])
def info():
    county_id = request.form['select']
    page = Tobacco.query.filter_by(id=county_id).first()
    return render_template("county.html", page=page)

    # get a list of unique values in the style column
    # counties = Tobacco.query.with_entities(Tobacco.county).distinct()
    # return render_template('index.html', counties=counties)

# @app.route('/<ID>')
# def link(ID):
#     county = Tobacco.county
#     page = Tobacco.query.filter_by(Tobacco.ID==ID).first()
#     return render_template("county.html", page=page)

if __name__ == '__main__':
    app.run(debug=True)
