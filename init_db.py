# init_db.py
from app import db, create_app, bcrypt
from app.models import User, Course

app = create_app()

with app.app_context():
    db.create_all()

    # Check if the admin user already exists
    admin_user = User.query.filter_by(username="admin").first()

    if not admin_user:
        # Create admin user
        hashed_password = bcrypt.generate_password_hash("root").decode('utf-8')
        admin_user = User(
            username="admin",
            first_name="Admin",
            last_name="User",
            password=hashed_password,
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with username: 'admin' and password: 'root'.")
    else:
        print("Admin user already exists.")

    print("Database initialized and tables created.")
