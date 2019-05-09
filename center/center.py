# coding: utf-8
from flask import render_template, session, request, redirect, flash, url_for, g
from flask_mail import Message
from datetime import datetime
from models import User
from forms import LoginForm, RegisterForm
from db import db
from utils import login_log
from threading import Thread
from decorators import login_required
from app import mail
import manage  # manage.app
from . import my_center
from config import Config


@my_center.route('/login', methods=['GET', 'POST'])
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
            # nginx 配置：proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
            # g.user_ip = request.headers['X-Forwarded-For']
            g.user_login_time = datetime.now()
            manage.app.logger.info(
                "login():current login user is " + g.user_name + " & login at " + str(
                    g.user_login_time) + " & user ip:" + g.user_ip)
            login_log()
            # 更新用户上次登录时间
            print(user)
            user.lastLoginTime=datetime.now()
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('main.index'))
        else:
            flash(u'登录失败，账号或者密码不正确！！！')
            return redirect(url_for('center.login'))


@my_center.route('/register', methods=['GET', 'POST'])
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
            token = user.generate_confirmation_token(secret_key=Config.SECRET_KEY)
            send_email(user_email, 'easyQAsystem User Register Confirm', 'notifymail', user=user, token=token)
            flash(u'账号确认邮件已发送到您的注册邮箱，请及时确认，否则无法发布新问题！！！')
            return redirect(url_for('center.login'))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender='yaoxing@fsc.cntaiping.com', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[manage.app, msg])
    thr.start()
    return thr


@my_center.route('/confirm/<token>')
@login_required
def confirm(token):
    user_name = session.get('user_name')
    user = User.query.filter(User.userName == user_name).first()
    if user and user.userConfirmed:
        return redirect(url_for('main.index'))
    if user.confirm(token, secret_key=manage.app.config['SECRET_KEY']):
        flash(u'你的账号已经确认成功！！！')
        return redirect(url_for('main.index'))
    else:
        flash(u'账号确认链接已失效')
        return redirect(url_for('center.register'))


@my_center.route('/logout')
def logout():
    session.pop('user_name')
    session.clear
    return redirect(url_for('main.index'))
