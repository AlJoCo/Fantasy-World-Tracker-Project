from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectField
from os import getenv

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:lotrpassword@34.134.60.2/fwt_db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config['SECRET_KEY'] = getenv("SECRET_KEY")
app.config['SECRET_KEY'] = "fgsdfsedsegcvbnjyhjtyutwqz"

db = SQLAlchemy(app) 

class Characters(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    time = db.relationship("time", backref="Characters")
    cname = db.Column(db.String(50), nullable=False)

class location(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    time = db.relationship("time", backref="location")
    lname = db.Column(db.String(50), nullable=False)

class time(db.Model):    
    tid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey("characters.cid"))
    lid = db.Column(db.Integer, db.ForeignKey("location.lid"))
    t_increment = db.Column(db.Integer)

class cform(FlaskForm):
    cname = StringField("Character Name")
    submit = SubmitField("Enter Character Name")

class lform(FlaskForm):
    lname = StringField("Location Name")
    submit = SubmitField("Enter Location Name")

class tform(FlaskForm):
    submit = SubmitField("Additional Stage")

class jform(FlaskForm):
    submit = SubmitField("Submit Journey")
    l_dropdown = SelectField("Select Location", coerce=int)
    c_dropdown = SelectField("Select Character", coerce=int)
    t_dropdown = SelectField("Select Time Increment", choices=[1,2,3,4,5,6,7,8,9,10])

@app.route('/')
def home():
    return redirect ('new-character')

@app.route('/new-character', methods=["GET", "POST"])
def newcharacter():
    form = cform()
    cqueryall = Characters.query.all()
    if form.validate_on_submit():
        new_character = Characters(cname = form.cname.data)
        db.session.add(new_character)
        db.session.commit()
        return redirect('new-character')
    return render_template('newcharacter.html', cqueryall=cqueryall, form=form)

@app.route('/new-location', methods=["GET", "POST"])
def newlocation():
    form = lform()
    lqueryall = location.query.all()
    if form.validate_on_submit():
        new_location = location(lname = form.lname.data)
        db.session.add(new_location)
        db.session.commit()
        return redirect('new-location')
    return render_template('newlocation.html', lqueryall=lqueryall, form=form)


@app.route('/journey', methods=["GET", "POST"])
def journey():
    form = jform()
    tqueryall = time.query.all()
    cqueryall = Characters.query.all()
    lqueryall = location.query.all()
    l_list=[(i.lid,i.lname) for i in lqueryall]
    form.l_dropdown.choices = l_list
    c_list=[(i.cid,i.cname) for i in cqueryall]
    form.c_dropdown.choices = c_list
    if form.validate_on_submit():
        journey_increment = time(cid = form.c_dropdown.data, lid = form.l_dropdown.data, t_increment = form.t_dropdown.data)
        db.session.add(journey_increment)
        db.session.commit()
        return redirect('journey')
    return render_template('journey.html',tqueryall=tqueryall, cqueryall=cqueryall, lqueryall=lqueryall, form=form)

@app.route('/encounters', methods=["GET", "POST"])
def encounters():
    tqueryall = time.query.all()
    cqueryall = Characters.query.all()
    lqueryall = location.query.all()
    return render_template('encounters.html',tqueryall=tqueryall, cqueryall=cqueryall, lqueryall=lqueryall)

@app.route('/update-character/<int:cid>', methods=["GET", "POST"])
def updatechar(cid):
    form = cform()
    update_char = Characters.query.get(cid)
    if form.validate_on_submit():
        update_char.cname = form.cname.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.cname.data = update_char.cname
    return render_template("newcharacter.html", form=form)

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
    return render_template("newlocation.html", form=form)

@app.route('/delete-character/<int:cid>')
def deletechar(cid):
    condemned_char = (Characters.query.get(cid))
    db.session.delete(condemned_char)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete-location/<int:lid>')
def deleteloc(lid):
    condemned_loc = (location.query.get(lid))
    db.session.delete(condemned_loc)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete-stage/<int:tid>')
def deletestage(tid):
    condemned_stage = (time.query.get(tid))
    db.session.delete(condemned_stage)
    db.session.commit()
    return redirect(url_for("journey"))

@app.route('/index', methods=["GET", "POST"])
def index():
    cqueryall = Characters.query.all()
    lqueryall = location.query.all()
    return render_template('index.html', cqueryall=cqueryall, lqueryall=lqueryall)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')