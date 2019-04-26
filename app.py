# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import config
from db import db
from models import User, Question, Answer
from decorators import login_required
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm, QuestionForm
from flask_paginate import get_page_parameter
from datetime import datetime, timedelta
from utils import login_log
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
bootstrap = Bootstrap(app)
mail = Mail(app)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=45)  # 配置45min有效


@app.route('/')
def index():
    # PER_PAGE = 5
    # total = Question.query.count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # start = (page - 1) * PER_PAGE
    # end = start + PER_PAGE
    # pagination = Pagination(page=page, total=total, record_name='questions')
    pagination = Question.query.order_by(Question.questionTime.desc()).paginate(page, per_page=5, error_out=False)
    questions = pagination.items

    context = {
        'pagination': pagination,
        'questions': questions  # Question.query.order_by(Question.questionTime.desc()).slice(start, end).all()
    }
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        user_name = form.user_name.data
        user_password = form.user_password.data
        user = User.query.filter(User.userName == user_name).first()
        if user and user.verify_password(user_password):
            session['user_name'] = user.userName
            # session.permanent = True

            g.user_name = user_name
            g.user_ip = request.remote_addr
            g.user_login_time = datetime.now()
            login_log()
            return redirect(url_for('index'))
        else:
            flash(u'登录失败，账号或者密码不正确！！！')
            return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    else:
        user_name = form.user_name.data
        user_password = form.user_password.data
        user_email = form.user_email.data
        user_nickname = form.user_nickname.data
        user_birth = form.user_birth.data
        register_time = datetime.now()
        user = User.query.filter(User.userName == user_name).first()
        if user:
            flash(u'账号已被注册！！！')
            return redirect(url_for('register'))
        else:
            user = User(user_name, user_password, user_email, user_nickname, register_time, user_birth)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token(secret_key=app.config['SECRET_KEY'])
            send_email(user_email, 'easyQAsystem User Register Confirm', 'notifymail', user=user, token=token)
            flash(u'账号确认邮件已发送到您的注册邮箱，请及时确认，否则无法发布新问题！！！')
            return redirect(url_for('login'))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender='yaoxing@fsc.cntaiping.com', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    user_name = session.get('user_name')
    user = User.query.filter(User.userName == user_name).first()
    if user and user.userConfirmed:
        return redirect(url_for('index'))
    if user.confirm(token, secret_key=app.config['SECRET_KEY']):
        flash(u'你的账号已经确认成功！！！')
        return redirect(url_for('index'))
    else:
        flash(u'账号确认链接已失效')
        return redirect(url_for('register'))


@app.route('/logout')
def logout():
    session.pop('user_name')
    session.clear
    return redirect(url_for('index'))


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


@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    form = QuestionForm()
    if request.method == 'GET':
        return render_template('post.html', form=form)
    else:
        question_topic = form.question_topic.data
        question_content = form.question_content.data
        my_question = Question(questionTopic=question_topic, questionContent=question_content,
                               questionTime=datetime.now())
        user_name = session.get('user_name')
        user = User.query.filter(User.userName == user_name).first()
        my_question.user = user
        db.session.add(my_question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    context = {
        'answers': Answer.query.filter_by(questionId=question_id).order_by(Answer.answerTime.desc()).all()
    }
    my_question = Question.query.filter(Question.questionId == question_id).first()
    my_question.questionView = my_question.questionView + 1
    db.session.add(my_question)
    db.session.commit()
    return render_template('detail.html', question=my_question, **context)


@app.route('/answer', methods=['POST'])
@login_required
def answer():
    answer_content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    current_user = User.query.filter(User.userName == session['user_name']).first()
    current_question = Question.query.filter(Question.questionId == question_id).first()
    my_answer = Answer(question_id=current_question.questionId, user_id=current_user.userId,
                       answer_content=answer_content,
                       answer_time=datetime.now())
    db.session.add(my_answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=current_question.questionId))


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter(User.userName == session['user_name']).first()
    # questions = user.questions
    # db.session.add(questions)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Question.query.filter(Question.userId == user.userId).order_by(
        Question.questionTime.desc()).paginate(page, per_page=5, error_out=False)
    questions = pagination.items

    context = {
        # 'pagination': pagination,
        'questions': questions,  # Question.query.order_by(Question.questionTime.desc()).slice(start, end).all()
        'answers': Answer.query.filter_by(userId=user.userId).order_by(Answer.answerTime.desc()).all()
    }
    return render_template('profile.html', **context)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
