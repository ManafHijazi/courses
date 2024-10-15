from flask import Blueprint, render_template
from app.models import Course

main = Blueprint('main', __name__)

@main.route('/')
def home():
    courses = Course.query.all()  # Fetch all courses from the database
    return render_template('home.html', courses=courses)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/blogs')
def blogs():
    return render_template('blogs.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/all_courses')
def all_courses():
    courses = Course.query.all()  # Fetch all courses from the database
    return render_template('all_courses.html', courses=courses)
