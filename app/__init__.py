from flask import Flask, jsonify
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

    from .models import OperationLog, User

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import bp
    app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resursa nu a fost gasita"}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({"error": "Cerere invalida."}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Eroare interna a serverului."}), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Metoda HTTP nu este permisa."}), 405

    return app
