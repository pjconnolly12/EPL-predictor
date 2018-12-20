#################
#### imports ####
#################

from bs4 import BeautifulSoup
from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm
from project import db, bcrypt, selections
from project.models import User, Standing, User_choices
import requests


################
#### config ####
################

users_blueprint = Blueprint('users', __name__)


##########################
#### helper functions ####
##########################


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

def pick_selections():
    """Creates list of teams to be provided as pick options"""
    page = requests.get("https://www.sportsinteraction.com/soccer/england/premier-league-betting/")
    soup = BeautifulSoup(page.content, 'html.parser')
    matches = soup.find_all(class_="game")    
    pick_options = []
    for games in matches:
        teams = games.find_all(class_="name")
        if len(teams) == 0:
            continue
        else:
            for names in teams:
                    pick_options.append(names.get_text())
    return pick_options

def create_pick_db(data):
    count = 0
    for rows in range(int(len(data)/3)):
        db.session.add(
            User_choices(data[count], data[count+1], data[count+2])
        )
        count += 3
    db.session.commit()

def participants():
    return db.session.query(Standing).order_by(Standing.points.desc())


################
#### routes ####
################

@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('name', None)
    flash('Goodbye!')
    return redirect(url_for('users.login'))


@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    old_fixtures = db.session.query(User_choices)
    old_fixtures.delete()
    create_pick_db(pick_selections())
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and bcrypt.check_password_hash(
                    user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['name'] = user.name
                flash('Welcome!')
                return redirect(url_for('selections.selections'))
            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                bcrypt.generate_password_hash(form.password.data),
            )
            new_team = Standing(
                form.name.data, 0, 0, 0)
            try:
                db.session.add(new_user)
                db.session.add(new_team)
                db.session.commit()
                flash('Thanks for registering. Please login.')
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'That username and/or email already exist.'
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)


@users_blueprint.route('/standings/', methods=['GET', 'POST'])
def standings():
    return render_template('standings.html', participants=participants())