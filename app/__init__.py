from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
 
db = SQLAlchemy()
login_manager = LoginManager()
 
login_manager.login_view = 'routes.login'
login_manager.login_message_category = "info"
 
def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
 
    db.init_app(app)
    login_manager.init_app(app)
 
    from .models import User, OperationLog
 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
 
    with app.app_context():
        db.create_all()
 
    from .routes import bp
    app.register_blueprint(bp)
 
    return app
 
