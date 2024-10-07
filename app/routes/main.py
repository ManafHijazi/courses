from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Course

main = Blueprint('main', __name__)

@main.route('/')
@login_required  # Ensure only logged-in users can access this route
def home():
    courses = Course.query.all()  # Fetch all courses from the database
    return render_template('home.html', courses=courses)

@main.route('/about')
@login_required  # Ensure only logged-in users can access this route
def about():
    return render_template('about.html')
