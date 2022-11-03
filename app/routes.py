from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import CityForm, AddForm, DeleteForm
from app import db
from app.models import Users
import sys
import app.api

from app import app as flask_app
@flask_app.route('/student-home', methods =['GET','POST'])
@login_required
def show_student_home():
     return render_template('student_home.html')

@flask_app.route('/cities', methods =['GET', 'POST'])
def list_cities_page():
    form = CityForm()
    if form.validate_on_submit():
        results = app.api.list_cities(form.min_population.data,form.max_population.data)
        return render_template('citiesresults.html', results=results)
    return render_template('cities.html', form=form)

@flask_app.route('/admin-home', methods =['GET','POST'])
@login_required 
def show_admin_home():
    if is_admin():
        return render_template('admin_home.html')



@flask_app.route('/evalform', methods = ['GET','POST'])
@login_required

def evaluation_form():
    return render_template('evalform.html')

def is_admin():
    if current_user:
        if current_user.is_admin == '1':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)





def is_student():
    if current_user:
        if current_user.is_student == '0':
            return True
        else:
            return False
    else:
        print('Student not authenticated.', file=sys.stderr)





@flask_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))






@flask_app.route('/', methods =['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user:
            if current_user.is_admin == '0':
                return redirect(url_for('show_student_home'))        
            else:                                   
                return redirect(url_for('show_admin_home'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(Users).filter_by(username=form.username.data).first()
        print(user, file=sys.stderr)
        if user is None or not user.password_hash == form.password.data:
            print('Login failed', file=sys.stderr)
            return redirect(url_for('login'))
        login_user(user)
        print('Login successful', file=sys.stderr)
        if current_user:
            if current_user.is_admin == '0':
                return redirect(url_for('show_student_home'))
            else:
                return redirect(url_for('show_admin_home'))
    return render_template('login.html', form=form)






@flask_app.route('/add', methods =['GET','POST']) #member mgmt
@login_required
def add_record():
    form = AddForm()
    if form.validate_on_submit():
        # Extract values from form
        user_id = form.user_id.data
        fname = form.fname.data
        lname = form.lname.data
        admin = form.admin.data
        username = form.username.data
        password = form.password.data

        # Create a city record to store in the DB
        u = Users(user_id=user_id, first_name=fname, last_name=lname, is_admin=admin, username=username, password_hash=password)

        # add record to table and commit changes
        db.session.add(u)
        db.session.commit()

        form.user_id.data = ''
        fname = ''
        lname = ''
        admin = ''
        username = ''
        password = ''

        return redirect(url_for('login'))
    return render_template('add_test.html', form=form)






@flask_app.route('/delete', methods=['GET', 'POST']) #member mgmt
@login_required
def delete_record():
    # Verifying that user is an admin
    if is_admin():
        form = DeleteForm()
        if form.validate_on_submit():

            to_delete = db.session.query(Users).filter_by(username=form.username.data).first()

            if to_delete is not None:
                db.session.delete(to_delete)
                db.session.commit()

            form.username.data = ''

            return redirect(url_for('/admin-home'))
        return render_template('delete_test.html', form=form)
    else:
        return render_template('unauthorized.html')





@flask_app.route('/create_event', methods =['GET','POST']) #create event
@login_required
def create():
    if is_admin():
        form = CreateForm()
        if form.validate_on_submit():

            return redirect(url_for('/admin-home'))
        return render_template('event.html', form=form)
    else:
        return render_template('unauthorized.html')





@flask_app.route('/edit_event', methods =['GET','POST']) #edit event
@login_required
def edit():
    if is_admin():
        form = EditForm()
        if form.validate_on_submit():

            return redirect(url_for('/admin-home'))
        return render_template('event.html', form=form)
    else:
        return render_template('unauthorized.html')





@flask_app.route('/do_eval', methods =['GET','POST']) #complete evaluations
@login_required
def do_eval():
    if is_student():
        form = EvalForm()
        if form.validate_on_submit():
            return redirect(url_for('/student-home'))
        return render_template('evaluation.html', form=form)
    else:
        return render_template('unauthorized.html')





@flask_app.route('/view_stats', methods =['GET','POST']) #view stats
@login_required
def view_stats():
    if is_student():
        #all = db.session.query(GPA).all()
        return render_template('stats.html', GPA=all)
    else:
        return render_template('unauthorized.html')





@flask_app.route('/view_responses', methods =['GET','POST']) #
@login_required
def view_responses():
    if is_admin():
        #all = db.session.query(GPA).all()
        return render_template('stats.html', GPA=all)
    else:
        return render_template('unauthorized.html')
