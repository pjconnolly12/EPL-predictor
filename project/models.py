# projects/models.py

from project import db

class User(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	

	def __init__(self, name=None, email=None, password=None, role=None):
		self.name = name
		self.email = email
		self.password = password

	def __repr__(self):
		return '<User {0}>'.format(self.name)

class Standing(db.Model):
	
	__tablename__ = 'standings'

	name = db.Column(db.String, primary_key=True, unique=True, nullable=False)
	wins = db.Column(db.Integer, unique=False, nullable=False)
	losses = db.Column(db.Integer, unique=False, nullable=False)
	points = db.Column(db.Integer, unique=False, nullable=False)

	def __init__(self, name=None, wins=None, losses=None, points=None):
		self.name = name
		self.wins = wins
		self.losses = losses
		self.points = points

	def __repr__(self):
		return '<Standing {0}>'.format(self.name)

class User_choices(db.Model):

	__tablename__ = 'user_choices'

	home = db.Column(db.String, primary_key=True, unique=False, nullable=False)
	draw = db.Column(db.String, unique=False, nullable=False)
	away = db.Column(db.String, unique=False, nullable=False)

	def __init__(self, home=None, draw=None, away=None):
		self.home = home
		self.draw = draw
		self.away = away

	def __repr__(self):
		return '<User_choices {0}>'.format(self.home)

class Picks(db.Model):

	__tablename__ = 'picks'

	pick = db.Column(db.String, primary_key=True, unique=False, nullable=False)

	def __init__(self, pick=None):
		self.pick = pick

	def __repr__(self):
		return '<Picks {0}>'.format(self.pick)