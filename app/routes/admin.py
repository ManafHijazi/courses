from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Course
import os
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__)

# Allowed file extensions for profile picture
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin Panel Route
@admin.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))
    return render_template('admin.html')


# Add Course Route
# Add Course Route
@admin.route('/admin/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if not current_user.is_admin:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            image_url = request.form['image_url']
            video_url = request.form['video_url']
            price = request.form['price']
            languages = request.form['languages']
            category = request.form['category']
            location = request.form['location']

            new_course = Course(
                title=title,
                description=description,
                image_url=image_url,
                video_url=video_url,
                price=price,
                languages=languages,
                category=category,
                location=location,
                added_by=current_user.id  # Associate the course with the current user
            )
            db.session.add(new_course)
            db.session.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('admin.admin_panel'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding course: {e}', 'error')

    return render_template('add_course.html')


# Manage Users Route
@admin.route('/admin/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))

    try:
        users = User.query.all()
        return render_template('user_management.html', users=users)
    except Exception as e:
        flash(f'Error fetching users: {e}', 'error')
        return redirect(url_for('admin.admin_panel'))


# Delete User Route
@admin.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))

    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully', 'success')
        return redirect(url_for('admin.manage_users'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {e}', 'error')
        return redirect(url_for('admin.manage_users'))

# Edit User Route
@admin.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))

    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        try:
            user.username = request.form['username']
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']

            # Handle profile picture update
            profile_picture = request.files.get('profile_picture')
            if profile_picture and allowed_file(profile_picture.filename):
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join('app/static/images', filename))
                user.profile_picture = filename  # Store just the filename

            db.session.commit()
            flash('User updated successfully', 'success')
            return redirect(url_for('admin.manage_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {e}', 'error')

    return render_template('edit_user.html', user=user)

# Manage Courses Route
@admin.route('/manage_courses')
def manage_courses():
    courses = Course.query.all()
    return render_template('manage_courses.html', courses=courses)

# Edit Course Route
@admin.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if not current_user.is_admin:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        try:
            course.title = request.form['title']
            course.description = request.form['description']
            course.image_url = request.form['image_url']
            course.video_url = request.form['video_url']
            course.price = float(request.form['price'])  # Ensure the price is a float
            course.languages = request.form['languages']
            course.category = request.form['category']
            course.location = request.form['location']

            db.session.commit()
            flash('Course updated successfully!', 'success')
            return redirect(url_for('admin.manage_courses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating course: {e}', 'error')

    return render_template('edit_course.html', course=course)


# Delete Course Route
@admin.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('admin.manage_courses'))
