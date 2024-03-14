from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///counter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    counter = Counter.query.first()
    if not counter:
        counter = Counter()
        db.session.add(counter)
        db.session.commit()
    return render_template('index.html', counter=counter)

@app.route('/increment')
def increment():
    counter = Counter.query.first()
    counter.value += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/decrement')
def decrement():
    counter = Counter.query.first()
    counter.value -= 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    counter = Counter.query.first()
    counter.value = 0
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
