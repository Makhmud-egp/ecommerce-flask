from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config



# Database object yaratish (hali app ga bog`lanmagan)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Flask app yaratish
    app = Flask(__name__)

    # Config yuklash
    app.config.from_object(Config)

    #Database ni app ga bo`g`lash
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprint register qilish
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    # App qaytarish
    return app