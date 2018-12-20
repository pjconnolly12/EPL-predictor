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
from project.models import User_choices, Picks


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

def user_choices():
	return db.session.query(User_choices)


##########################
########  routes #########
##########################

@selections_blueprint.route('/selections/', methods=['GET', 'POST'])
@login_required
def selections():
	return render_template(
		'selections.html',
	 	form=SelectionForm(request.form),
	 	user_choices=user_choices(),
	 )

@selections_blueprint.route('/picks/', methods=['GET', 'POST'])
@login_required
def picks():
	error = None
	form = SelectionForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_picks = Picks(
				form.selection.data)
			db.session.add(new_picks)
			db.session.commit()
			flash('Picks were entered successfully. Thanks!')
			return redirect(url_for('users.standings'))
	return render_template(
		'standings.html',
		participants=participants()
	)
