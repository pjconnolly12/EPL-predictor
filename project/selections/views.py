# project/selections/views.py

#################
#### imports ####
#################

from bs4 import BeautifulSoup
from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from .forms import SelectionForm
from project import db
import requests


################
#### config ####
################

selections_blueprint = Blueprint('selections', __name__)


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
        		message.append(names.get_text())
    return pick_options


##########################
########  routes #########
##########################

@users_blueprint.route('/selections/', methods=['GET', 'POST'])
def selections():
    pick_selections()
    return render_template('selections.html')