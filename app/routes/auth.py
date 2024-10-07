from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db, bcrypt
from app.models import User
from flask_login import login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)

# Allowed file extensions for profile picture
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()

            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash(f'Welcome back, {user.first_name}!', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Invalid username or password. Please try again.', 'error')
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')

    return render_template('login.html')


# Sign Up Route
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')

            # Handling profile picture
            profile_picture = request.files.get('profile_picture')
            profile_picture_filename = None

            if profile_picture and allowed_file(profile_picture.filename):
                # Secure the filename and save it in the static/images directory
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join('app/static/images', filename))
                profile_picture_filename = filename  # Store just the filename in the DB

            # Create a new user
            new_user = User(username=username, first_name=first_name, last_name=last_name, password=password, profile_picture=profile_picture_filename)
            db.session.add(new_user)
            db.session.commit()

            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during signup: {e}', 'error')

    return render_template('signup.html')

# Logout Route
@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
