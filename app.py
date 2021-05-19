from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app) 

class character(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    time = db.relationship('time', backref='character')
    conflict = db.relationship('conflict', backref='character')
    cname = db.Column(db.String(50), nullable=False)

class location(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    time = db.relationship('time', backref='location')
    conflict = db.relationship('conflict', backref='location')
    lname = db.Column(db.String(50), nullable=False)

class time(db.Model):
    cid = db.Column(db.Integer, db.Foreignkey('character.cid'))
    tid = db.Column(db.Integer, primary_key=True)
    conflict = db.relationship('conflict', backref='time')
    lid = db.Column(db.Integer, db.Foreignkey('location.lid'))

class conflict(db.Model):
    conid = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer, db.Foreignkey('time.tid'))
    lid = db.Column(db.Integer, db.Foreignkey('location.lid'))
    cid = db.Column(db.Integer, db.Foreignkey('character.cid'))

class cform(FlaskForm):
    charname = StringField("Character Name")
    submit = SubmitField("New Character")

class lform(FlaskForm):
    locname = StringField("Location Name")
    submit = SubmitField("New Location")

@app.route('/')
def home():
    return redirect ('newcharacter')

@app.route('/new-character', methods=["GET", "POST"])
def newcharacter():
    form = cform()
    if form.validate_on_submit():
        new_character = character(cname=form.charname.data)
        db.session.add(new_character)
        db.session.commit()
        return redirect('location')
    return render_template('newchar.html', form=form)

@app.route('/new-location', methods=["GET", "POST"])
def newlocation():
    form = lform()
    if form.validate_on_submit():
        new_location = location(lname=form.lname.data)
        db.session.add(new_location)
        db.session.commit()
        return redirect('location')
    return render_template('newloc.html', form=form)

@app.route('/update-character/<int:cid>', methods=["GET", "POST"])
def update(cid):
    form = cform()
    update_char = character.query.get(cid)
    if form.validate_on_submit():
        update_char.cname = form.charname.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.cname.data = update_char.cname
    return render_template("updatechar.html", form=form)

@app.route('/update-location/<int:lid>', methods=["GET", "POST"])
def update(lid):
    form = lform()
    update_loc = location.query.get(lid)
    if form.validate_on_submit():
        update_loc.lname = form.lname.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.lname.data = update_loc.lname
    return render_template("updatechar.html", form=form)

@app.route('/delete-character/<int:cid>')
def delete(cid):
    condemned_char = (character.query.get(cid))
    db.session.delete(condemned_char)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete-location/<int:lid>')
def delete(lid):
    condemned_loc = (location.query.get(lid))
    db.session.delete(condemned_loc)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/index', methods=["GET", "POST"])
def index():

    cqueryall = character.query.all()
    return render_template('index.html', queryall=cqueryall)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')