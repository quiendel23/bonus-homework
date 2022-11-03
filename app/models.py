#Will create all tables as long as the db exists event if the tables dont

from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import AddForm


class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_admin = db.Column(db.String(1))
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))

    def get_id(self):
        return self.user_id
    
    def set_password(self, password):
        # Store hashed (encrypted) password in database
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)\
            
    def create_user(self):
        form = AddForm()
        if form.validate_on_submit():
            # Extract values from form
            user = db.session.query(Users).last()
            user_id  = 1+ user.user_id
            fname = form.fname.data
            lname = form.lname.data
            admin = form.admin.data
            sername = form.username.data
            password = form.password.data

            # Create a city record to store in the DB
            u = Users(user_id=user_id, first_name=fname, last_name=lname, is_admin=admin, username=username, password_hash=password)
            db.session.add(u)
            db.session.commit()

# load_user is a function that's used by flask_login to manage the session.
# It simply returns the object associated with the authenticated user.




#Events DB table
class Events(UserMixin,db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255))
    
    def get_event_name(self):
        return self.event_name
    
    
    def get_event_id(self):
        return self.event_id
    
        


#Results DB Table

class Results(UserMixin,db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    overall_participation_score = db.Column(db.Integer)
    overall_communication_score = db.Column(db.Integer)
    overall_quality_score = db.Column(db.Integer)
    overall_attitude_score = db.Column(db.Integer)
    
    
    
#Evaluations DB Table

class Evaluations(UserMixin, db.Model):
    evaluation_id = db.Column(db.Integer,primary_key=True)
    event_id = db.Column(db.Integer)
    to_user_id = db.Column(db.Integer)
    from_user_id = db.Column(db.Integer)
    participation_score = db.Column(db.Integer)
    communication_score = db.Column(db.Integer)
    quality_score = db.Column(db.Integer)
    attitude_score = db.Column(db.Integer)
    release_data = db.Column(db.Integer)
    short_response = db.Column(db.String(1500))
    



@login.user_loader
def load_user(user_id):
    return db.session.query(Users).get(int(user_id))