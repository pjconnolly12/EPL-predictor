# project/db_create.py

from project import db, bcrypt
from project.models import User, Standing

# create the database and the db table
db.create_all()

# db.session.add(
# 	User("tester1", "test@test.com", bcrypt.generate_password_hash("password1"))
# )

db.session.add(
	Standing("tester1", 0, 0, 0))

#commit the changes
db.session.commit()