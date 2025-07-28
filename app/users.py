from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()

    admin = User(username="admin", role="admin")
    admin.set_password("admin123")

    user = User(username="user", role="user")
    user.set_password("user123")

    db.session.add_all([admin, user])
    db.session.commit()
