from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

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
