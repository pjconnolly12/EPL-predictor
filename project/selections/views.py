# project/selections/views.py

#################
#### imports ####
#################

from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from .forms import SelectionForm
from project import db


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

