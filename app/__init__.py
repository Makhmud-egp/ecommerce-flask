import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config, config

# Database object, migration, Login manage objectlarini yasash
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name='development'):
    # Flask app yaratish
    app = Flask(__name__)

    # Config yuklash
    app.config.from_object(config[config_name])

    # Database ni app ga bo`g`lash
    # LoginManager ni app ga bo`g`lash
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask-Login Settings
    login_manager.login_view = 'auth.login'

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # ✅ Import blueprints INSIDE factory
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.categories import category_bp
    from app.routes.products import product_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import order_bp
    from app.routes.admin import admin_bp
    from app.routes.payment import payment_bp


    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(payment_bp, url_prefix='/payment')

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/shop.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('Shop startup')

    return app
