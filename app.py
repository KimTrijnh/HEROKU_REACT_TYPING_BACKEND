from flask import Flask, jsonify, request
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
app.config['SECRET_KEY '] = 'abc'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/exs')
def list():
    return jsonify(
        [ 
  "The enormous room on the ground floor faced towards the north. Cold for all the summer beyond the panes, for all the tropical heat of the room itself, a harsh thin light glared through the windows, hungrily seeking some draped lay figure, some pallid shape of academic goose-flesh, but finding only the glass and nickel and bleakly shining porcelain of a laboratory.",

 "Wintriness responded to wintriness. The overalls of the workers were white, their hands gloved with a pale corpse-coloured rubber. The light was frozen, dead, a ghost. Only from the yellow barrels of the microscopes did it borrow a certain rich and living substance, lying along the polished tubes like butter, streak after luscious streak in long recession down the work tables.",

"Bent over their instruments, three hundred Fertilizers were plunged, as the Director of Hatcheries and Conditioning entered the room, in the scarcely breathing silence, the absent-minded, soliloquizing hum or whistle, of absorbed concentration.",

"Each of them carried a notebook, in which, whenever the great man spoke, he desperately scribbled. Straight from the horse's mouth. It was a rare privilege. The D. H. C. for Central London always made a point of personally conducting his new students round the various departments.",

"Tall and rather thin but upright, the Director advanced into the room. He had a long chin and big rather prominent teeth, just covered, when he was not talking, by his full, floridly curved lips. Old, young? Thirty? Fifty? Fifty-five? It was hard to say. And anyhow the question didn't arise; in this year of stability, A. F. 632, it didn't occur to you to ask it.",

"One egg, one embryo, one adult-normality. But a bokanovskified egg will bud, will proliferate, will divide. From eight to ninety-six buds, and every bud will grow into a perfectly formed embryo, and every embryo into a full-sized adult. Making ninety-six human beings grow where only one grew before. Progress.",

"For in nature it takes thirty years for two hundred eggs to reach maturity. But our business is to stabilize the population at this moment, here and now. Dribbling out twins over a quarter of a century–what would be the use of that?",

"Obviously, no use at all. But Podsnap's Technique had immensely accelerated the process of ripening. They could make sure of at least a hundred and fifty mature eggs within two years.",

"In the Bottling Room all was harmonious bustle and ordered activity. Flaps of fresh sow's peritoneum ready cut to the proper size came shooting up in little lifts from the Organ Store in the sub-basement.",

"And in effect the sultry darkness into which the students now followed him was visible and crimson, like the darkness of closed eyes on a summer's afternoon.",

"The bulging flanks of row on receding row and tier above tier of bottles glinted with innumerable rubies, and among the rubies moved the dim red spectres of men and women with purple eyes and all the symptoms of lupus. The hum and rattle of machinery faintly stirred the air.",

"Didn't need and didn't get it. But though the Epsilon mind was mature at ten, the Epsilon body was not fit to work till eighteen. Long years of superfluous and wasted immaturity. If the physical development could be speeded up till it was as quick, say, as a cow's, what an enormous saving to the Community!",

"He became rather technical; spoke of the abnormal endocrine co-ordination which made men grow so slowly; postulated a germinal mutation to account for it. Could the effects of this germinal mutation be undone?",

"On Rack 10 rows of next generation's chemical workers were being trained in the toleration of lead, caustic soda, tar, chlorine. The first of a batch of two hundred and fifty embryonic rocket-plane engineers was just passing the eleven hundred metre mark on Rack 3. A special mechanism kept their containers in constant rotation."

]
    )

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


@app.route('/excerpt/random', methods=['GET', 'POST'])
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
            topScores.append({"score": {"id": score.id , "value": score.wpm }})

        return jsonify({'message':'score created', 'wpm': score.wpm, 'ranking': ranking , 'total_score': total_score, 'top_scores': topScores }), 200
    return jsonify({'message':'failed'}), 401

def create_excerpt(text):
    e = Excerpt(text=text)
    db.session.add(e)
    db.session.commit()