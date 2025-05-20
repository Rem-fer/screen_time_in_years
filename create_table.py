from main import db, app
import sys

with app.app_context():
    db.create_all()
    print(" Tables created successfully.")

sys.exit(0)