from flask import Flask, jsonify, request, render_template,redirect, url_for, flash
import os, random, math, psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# POSTGRES = {
#     'user': os.getenv('PSQL_USER'),
#     'pw': os.getenv('PSQL_PWD'),
#     'db': os.getenv('PSQL_DB'),
#     'host': os.getenv('PSQL_HOST'),
#     'port': os.getenv('PSQL_PORT'),
# }

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

app.config['SECRET_KEY '] = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exs')
def list():
    exs = Excerpt.query.all()
    exsArray = []
    for e in exs:
        exsArray.append(e.text)
    return jsonify(exsArray)
    

class Excerpt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    scores = db.relationship('Score', backref="excerpt", lazy=True)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wpm = db.Column(db.Integer)
    excerpt_id = db.Column(db.Integer, db.ForeignKey('excerpt.id'))

    def __ref__(self):
        return '<score %r>' % self.id


@app.route('/excerpt/random')
def get_ex():
    exs = Excerpt.query.all()
    random_num = math.floor(random.random()*len(exs))
    score_count = Score.query.filter_by(excerpt_id=exs[random_num].id).count()
    top_scores = Score.query.filter_by(excerpt_id=exs[random_num].id).order_by(Score.wpm.desc()).limit(3).all()
    scores = []
    for score in top_scores:
        scores.append({"score": {"id": score.id , "value": score.wpm }})
    return jsonify({"id": exs[random_num].id, "text": exs[random_num].text, "top_scores": scores, "score_count": score_count })



@app.route('/score', methods = ['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = request.get_json()
        score = Score(wpm=data['wpm'], excerpt_id=data['excerpt_id'])
        db.session.add(score)
        db.session.commit()
        scores = Score.query.filter_by(excerpt_id=data['excerpt_id']).order_by(Score.wpm.desc()).all()
        total_score = len(scores)
        ranking = scores.index(score) + 1
        top_scores = Score.query.filter_by(excerpt_id=data['excerpt_id']).order_by(Score.wpm.desc()).limit(3).all()
        topScores = []
        for score in top_scores:
            topScores.append({"scor{'message':'score created',e": {"id": score.id , "value": score.wpm }})
        return jsonify( 'wpm': score.wpm, 'ranking': ranking , 'total_score': total_score, 'top_scores': topScores }), 200
    return jsonify({'message':'failed'}), 401


@app.route('/admin/create_score', methods=['GET', 'POST'])
def create_score():
    num = Excerpt.query.count()
    if request.method == 'POST':
        excerpt_id = int(request.form['excerpt_id'])
        wpm = int(request.form['wpm'])
        score = Score(wpm=wpm, excerpt_id=excerpt_id)
        db.session.add(score)
        db.session.commit()
        scores = Score.query.filter_by(excerpt_id=excerpt_id).order_by(Score.wpm.desc()).all()
        total_score = len(scores)
        ranking = scores.index(score) + 1
        top_scores = Score.query.filter_by(excerpt_id=excerpt_id).order_by(Score.wpm.desc()).limit(3).all()
        topScores = []
        congra = "Congratulations! " + str(wpm) + "WPM is the #" + str(ranking) + " best score out of " + str( total_score ) + "."
        for score in top_scores:
            topScores.append({"score": {"id": score.id , "value": score.wpm }})
        return jsonify({'message':'score created', 'wpm': score.wpm, 'ranking': ranking , 'total_score': total_score, 'top_scores': topScores, 'congra' : congra }), 200
    return render_template('create_score.html', num=num)

@app.route('/admin/add_excerpt', methods=['GET', 'POST'])
def add_excerpt():
    if request.method == 'POST':
        create_excerpt(request.form['text'])
        flash('an excerpt is created')
    return render_template('add_ex.html')


def create_excerpt(text):
    e = Excerpt(text=text)
    db.session.add(e)
    db.session.commit()

