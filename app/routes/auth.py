from flask import Blueprint,render_template,redirect,request,url_for,flash,session
from app.models import User
from app import db

auth_bp = Blueprint('auth',__name__)


@auth_bp.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists', 'danger')

        else:
            new_user = User(username=username, password=password)

            db.session.add(new_user)

            db.session.commit()

            session['user'] = new_user.id

            flash('Signup successful!', 'success')

            return redirect(url_for('tasks.view_tasks'))

    return render_template('signup.html')



@auth_bp.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            session['user'] = user.id

            flash('Login Successful', 'success')

            return redirect(url_for('tasks.view_tasks'))

        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))
