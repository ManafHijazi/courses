from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Course, User

user = Blueprint('user', __name__)

# Profile page to show user's profile and favorite courses
@user.route('/profile')
@login_required
def profile():
    favorite_courses = current_user.favorite_courses
    return render_template('profile.html', user=current_user, favorite_courses=favorite_courses)

@user.route('/toggle_favorite/<int:course_id>', methods=['POST'])
@login_required
def toggle_favorite(course_id):
    course = Course.query.get_or_404(course_id)

    if course in current_user.favorite_courses:
        current_user.favorite_courses.remove(course)
        flash('Course removed from favorites.', 'success')
    else:
        current_user.favorite_courses.append(course)
        flash('Course added to favorites.', 'success')

    db.session.commit()
    return redirect(request.referrer or url_for('main.home'))

