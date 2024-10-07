# init_db.py
from app import db, create_app
from app.models import Course, User

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized and tables created.")
