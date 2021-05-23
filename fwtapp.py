from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectField
from os import getenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = getenv("SECRET_KEY")

db = SQLAlchemy(app) 

class Characters(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    time = db.relationship("time", backref="Characters")
    cname = db.Column(db.String(50), nullable=False)
#Character Table: ID, and character name

class location(db.Model):
    lid = db.Column(db.Integer, primary_key=True)
    time = db.relationship("time", backref="location")
    lname = db.Column(db.String(50), nullable=False)
#Locations Table: ID, and place name

class time(db.Model):    
    tid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey("characters.cid"))
    lid = db.Column(db.Integer, db.ForeignKey("location.lid"))
    t_increment = db.Column(db.Integer)
#Combination Table, accepting the IDs for characters and locations, with a corresponding to a point in time (arbitrarily assigned, and up to the user to interpret)

class cform(FlaskForm):
    cname = StringField("Character Name")
    submit = SubmitField("Enter Character Name")
#Character forms, accepting a name

class lform(FlaskForm):
    lname = StringField("Location Name")
    submit = SubmitField("Enter Location Name")
#Locations forms, accepting a name

class jform(FlaskForm):
    submit = SubmitField("Submit Journey")
    l_dropdown = SelectField("Select Location", coerce=int)
    c_dropdown = SelectField("Select Character", coerce=int)
    t_dropdown = SelectField("Select Time Increment", choices=[1,2,3,4,5,6,7,8,9,10])
#Journies form, accepting a character name and location name (dynamically generated), with a corresponding time assignment for when the character visits the location in the story.

@app.route('/')
def home():
    return redirect ('new-character')
#If no direct route is given, the user is redirected to the 'new character' route to add their list of characters.
#All pages have a set of header hyperlinks to navigate between the essential areas: adding characters, adding locations, creating journies, viewing encounters, and an index for viewing, deleting and updating entries.

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
#Provides a list of existing characters, and a text box and submit button to add new characters

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
#Provides a list of existing locations, and a text box and submit button to add new locations


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
    #Generates select field (dropdown box) options, based on the stored values in the character and location tables
    if form.validate_on_submit():
        journey_increment = time(cid = form.c_dropdown.data, lid = form.l_dropdown.data, t_increment = form.t_dropdown.data)
        db.session.add(journey_increment)
        #After accepting the options selected from the  time increment, location, and characters selection after submission, they are added to the journey table, alongside an auto-incrementing time ID
        db.session.commit()
        return redirect('journey')
    return render_template('journey.html',tqueryall=tqueryall, cqueryall=cqueryall, lqueryall=lqueryall, form=form)

@app.route('/encounters', methods=["GET", "POST"])
def encounters():
    tqueryall = time.query.all()
    cqueryall = Characters.query.all()
    lqueryall = location.query.all()
    return render_template('encounters.html',tqueryall=tqueryall, cqueryall=cqueryall, lqueryall=lqueryall)
#Once the journies have been submitted, the encounters page will show all instances where there are multiple characters in the same location at the same time, which can be interpreted by the user and used as a record of sorts.
#There is currently a known bug whereby all encounters will be listed twice, once from the perspective of each character.

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
#Accessible most easily via the index; characters and locations will be listed, with buttons to delete or update the entries. For updating, the current value will be displayed, to be replaced by the user.

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
#The delete stage or delete journey button appears in the journey page, next to each existing journey

@app.route('/index', methods=["GET", "POST"])
def index():
    cqueryall = Characters.query.all()
    lqueryall = location.query.all()
    return render_template('index.html', cqueryall=cqueryall, lqueryall=lqueryall)
#The index displays all location and character entries, and acts as the hub for deleting and updating them

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')