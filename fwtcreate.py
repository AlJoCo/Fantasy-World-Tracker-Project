  
from fwtapp import db,location,Character

db.drop_all()
db.create_all()

dummyentry_c = Character(cname="Strider")
dummyentry_l = location(lname="Bree")
#dummyentry_t = time(1)
db.session.add(dummyentry_c)
db.session.add(dummyentry_l)
#db.session.add(dummyentry_t)
db.session.commit()