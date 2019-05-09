# coding: utf-8
from flask import Flask
import config
from flask_bootstrap import Bootstrap
from datetime import timedelta
from flask_mail import Mail
from db import db

bootstrap = Bootstrap()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=45)  # 配置45min有效

    from main import my_main as main_blueprint
    from center import my_center as center_blueprint
    from error import my_error as error_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(center_blueprint)
    app.register_blueprint(error_blueprint)

    return app
