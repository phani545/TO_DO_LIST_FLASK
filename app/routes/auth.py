from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.models import Task, User, create_user, get_user_by_username
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth' , __name__)

@auth_bp.route('/', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists, Please Login", "danger")
            return redirect(url_for('auth.login'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template("register.html")

@auth_bp.route('/login', methods=["GET","POST"])
def login():

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user'] = user.username
            flash("Login successful", "success")
            return redirect(url_for('tasks.view_tasks'))

        flash("Invalid username or password", "danger")

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.pop('user' , None)
    flash('Logged out' , 'info')
    return redirect(url_for('auth.login'))