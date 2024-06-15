from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User
from app import db

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

def init_auth_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

def load_user(user_id):
    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    return user

def authorize_user(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = None
            user_id = kwargs.get("user_id")
            if user_id:
                user = load_user(user_id)
            if not current_user.can(action, user):
                flash("Недостаточно прав для доступа к странице", "warning")
                return redirect(url_for("home"))
            return func(*args, **kwargs)
        return wrapper
    return decorator

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            user = db.session.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно аутентифицированы.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('auth/login.html')


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
