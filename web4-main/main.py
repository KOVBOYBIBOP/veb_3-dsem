from flask import Flask, render_template, redirect, url_for, request, session, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class UserAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def set_password(self, password):
        self.hashed_password = hashlib.md5(password.encode()).hexdigest()

    def validate_password(self, password):
        result = self.hashed_password == password
        return result

    
class UserAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, message='Username must be at least 5 characters long'),
        Regexp('^[A-Za-z0-9]+$', message='Username can only contain letters and numbers')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=128),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&^_-])[A-Za-z\\d@$!%*?&^_-]{8,}$',
               message="Password must contain at least 8 characters, one uppercase, one lowercase, one digit, and one special character @$!%*?&^_-")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    last_name = StringField('Last Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name')
    role_id = SelectField('Role', coerce=int, validators=[DataRequired()], default=2)

class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, max=128),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&^_-])[A-Za-z\\d@$!%*?&^_-]{8,}$',
               message="Password must contain at least 8 characters, one uppercase, one lowercase, one digit, and one special character @$!%*?&^_-")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if user.validate_password(form.current_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password successfully changed', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid current password', 'error')
    return render_template('password.html', form=form)

def get_role_name(role_id):
    role = UserRole.query.get(role_id)
    return role.role_name if role else "Unknown"

@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        
        user = UserAccount.query.filter_by(username=user_name).first()
        if user and user.validate_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/users')
@login_required
def manage_users():
    if current_user.role_id == 1:
        all_users = UserAccount.query.all()
    else:
        all_users = [current_user]
    
    return render_template('users.html', users=all_users, get_role_name=get_role_name)

@app.route('/user/<int:user_id>')
def user_details(user_id):
    user = UserAccount.query.get_or_404(user_id)
    return render_template('view_user.html', user=user)

@app.route('/user/new', methods=['GET', 'POST'])
@login_required
def new_user():
    form = UserAccountForm()
    roles = UserRole.query.all()
    form.role_id.choices = [(role.id, role.role_name) for role in roles]
    if form.validate_on_submit():
        new_user = UserAccount(
            username=form.username.data,
            last_name=form.last_name.data,
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            role_id=form.role_id.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User successfully created', 'success')
        return redirect(url_for('manage_users'))
    return render_template('create_user.html', form=form, roles=roles)

@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = UserAccount.query.get_or_404(user_id)
    roles = UserRole.query.all()

    if request.method == 'POST':
        user.last_name = request.form['last_name']
        user.first_name = request.form['first_name']
        user.middle_name = request.form['middle_name']
        user.role_id = request.form['role_id']
        db.session.commit()
        flash('User details updated successfully', 'success')
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', user=user, roles=roles)

@app.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = UserAccount.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User successfully deleted', 'success')
    return redirect(url_for('manage_users'))

@app.route('/user/<int:user_id>/confirm_delete', methods=['GET'])
@login_required
def confirm_delete(user_id):
    user = UserAccount.query.get_or_404(user_id)
    return render_template('confirm_delete.html', user=user)

def validate_user_input(form):
    password = form.password.data
    if not (any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            not any(char.isspace() for char in password) and
            len(password) >= 8 and
            len(password) <= 128):
        form.password.errors.append('Password does not meet the requirements')
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True)
