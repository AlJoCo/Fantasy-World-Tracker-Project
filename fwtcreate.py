  
from fwtapp import db,location,Characters,time

db.drop_all()
db.create_all()

dummyentry_c = Characters(cname="Strider")
dummyentry_l = location(lname="Bree")
dummyentry_t = time()
db.session.add(dummyentry_c)
db.session.add(dummyentry_l)
db.session.commit()