from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # 설정파일 불러오기
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    # blueprint
    from .views import main_views, movies_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(movies_views.bp)

    return app
