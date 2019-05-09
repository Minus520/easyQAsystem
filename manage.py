# coding: utf-8
from flask import session, g
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from db import db
from models import User, Question, Answer

import app

app = app.create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


# 钩子函数
@app.context_processor
def my_context_processor():
    user_name = session.get('user_name')
    if user_name:
        user = User.query.filter(User.userName == user_name).first()
        if user:
            g.current_user = user
            return {'user': user}
    else:
        return {}


if __name__ == '__main__':
    manager.run()
