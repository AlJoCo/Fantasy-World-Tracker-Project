from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = 'fgsdfsedsegcvbnjyhjtyutwqz'

db = SQLAlchemy(app) 

class Character(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    #time = db.relationship('time', backref='Character')
    #conflict = db.relationship('conflict', backref='Character')
    cname = db.Column(db.String(50), nullable=False)

class location(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    #time = db.relationship('time', backref='location')
    #conflict = db.relationship('conflict', backref='location')
    lname = db.Column(db.String(50), nullable=False)

# class time(db.Model):
#     cid = db.Column(db.Integer, db.ForeignKey('Character.cid'))
#     tid = db.Column(db.Integer, primary_key=True)
#     conflict = db.relationship('conflict', backref='time')
#     lid = db.Column(db.Integer, db.ForeignKey('location.lid'))

# class conflict(db.Model):
#     conid = db.Column(db.Integer, primary_key=True)
#     tid = db.Column(db.Integer, db.ForeignKey('time.tid'))
#     lid = db.Column(db.Integer, db.ForeignKey('location.lid'))
#     cid = db.Column(db.Integer, db.ForeignKey('Character.cid'))

class cform(FlaskForm):
    cname = StringField("Character Name")
    submit = SubmitField("New Character")

class lform(FlaskForm):
    lname = StringField("Location Name")
    submit = SubmitField("New Location")

@app.route('/')
def home():
    return redirect ('new-character')

@app.route('/new-character', methods=["GET", "POST"])
def newcharacter():
    form = cform()
    if form.validate_on_submit():
        new_character = Character(cname = form.cname.data)
        db.session.add(new_character)
        db.session.commit()
        return redirect('location')
    return render_template('newcharacter.html', form=form)

@app.route('/new-location', methods=["GET", "POST"])
def newlocation():
    form = lform()
    if form.validate_on_submit():
        new_location = location(form.lname.data)
        db.session.add(new_location)
        db.session.commit()
        return redirect('location')
    return render_template('newlocation.html', form=form)

@app.route('/update-character/<int:cid>', methods=["GET", "POST"])
def updatechar(cid):
    form = cform()
    update_char = Character.query.get(cid)
    if form.validate_on_submit():
        update_char.cname = form.cname.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.cname.data = update_char.cname
    return render_template("updatecharacter.html", form=form)

@app.route('/update-location/<int:lid>', methods=["GET", "POST"])
def updateloc(lid):
    form = lform()
    update_loc = location.query.get(lid)
    if form.validate_on_submit():
        update_loc.lname = form.lname.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.lname.data = update_loc.lname
    return render_template("updatelocation.html", form=form)

@app.route('/delete-character/<int:cid>')
def deletechar(cid):
    condemned_char = (Character.query.get(cid))
    db.session.delete(condemned_char)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete-location/<int:lid>')
def deleteloc(lid):
    condemned_loc = (location.query.get(lid))
    db.session.delete(condemned_loc)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/index', methods=["GET", "POST"])
def index():

    cqueryall = Character.query.all()
    return render_template('index.html', cqueryall=cqueryall)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')