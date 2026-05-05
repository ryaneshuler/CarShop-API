from flask import Flask, jsonify
from .extensions import db, ma, limiter, cache
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.customer import customer_bp
from .blueprints.inventory import inventory_bp

def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    @app.route('/test')
    def test():
        return jsonify({"status": "ok"})

    with app.app_context():
        db.create_all()

    return app
