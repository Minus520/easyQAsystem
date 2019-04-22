from flask import Flask, render_template, request, redirect, url_for, session
import config
from db import db
from models import User, Post
from decorators import login_required
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_name = request.form.get('userName')
        user_password = request.form.get('userPassword')
        user = User.query.filter(User.userName == user_name, User.userPassword == user_password).first()
        if user:
            session['user_name'] = user.userName
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '账号或者密码错误'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        user_name = request.form.get('userName')
        user_password = request.form.get('userPassword')

        admin = User.query.filter(User.userName == user_name).first()
        if admin:
            return '账号已注册'
        else:
            user = User(user_name, user_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_name')
    return redirect(url_for('index'))


@app.context_processor
def my_context_processor():
    user_name = session.get('user_name')
    if user_name:
        user = User.query.filter(User.userName == user_name).first()
        if user:
            return {'user': user}
    else:
        return {}


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'GET':
        return render_template('post.html')
    else:
        post_topic = request.form.get('postTopic')
        post_content = request.form.get('postContent')
        my_post = Post(postTopic=post_topic, postContent=post_content)
        user_name = session.get('user_name')
        user = User.query.filter(User.userName == user_name).first()
        my_post.user = user
        db.session.add(my_post)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
