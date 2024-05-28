from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@database:3306/test_db'
db = SQLAlchemy(app)

#engine = create_engine('mysql+pymysql://root:root@localhost:3306/test_db')
engine = create_engine('mysql://root:root@database:3306/test_db')
metadata = MetaData()

user_table = Table(
    'user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(80), unique=True, nullable=False),
    Column('points', Integer, default=0)
)

metadata.create_all(engine)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['username'] = username
        return redirect(url_for('clicker'))
    return render_template('index.html')

@app.route('/clicker')
def clicker():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    user = User.query.filter_by(username=username).first()
    return render_template('clicker.html', user=user)

@app.route('/click', methods=['POST'])
def click():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user:
            user.points += 1
            db.session.commit()
    return '', 204

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.points.desc()).all()
    return render_template('leaderboard.html', users=users)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
