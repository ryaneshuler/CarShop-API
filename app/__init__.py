from flask import Flask, jsonify
from .extensions import db, ma
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp

def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')

    @app.route('/test')
    def test():
        return jsonify({"status": "ok"})

    with app.app_context():
        db.create_all()

    return app
