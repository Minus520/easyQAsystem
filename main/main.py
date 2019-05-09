# coding: utf-8
from flask import render_template, session, request, redirect, url_for, jsonify
from flask_paginate import get_page_parameter
from models import Question, User, Answer, Like
from decorators import login_required
from forms import QuestionForm
from db import db
from datetime import datetime
from . import my_main


@my_main.route('/')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Question.query.order_by(Question.questionTime.desc()).paginate(page, per_page=5, error_out=False)
    questions = pagination.items
    context = {
        'pagination': pagination,
        'questions': questions
    }
    return render_template('index.html', **context)


@my_main.route('/question', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))


@my_main.route('/detail/<question_id>')
def detail(question_id):
    if session.get('user_name'):
        current_user = User.query.filter(User.userName == session.get('user_name')).first()
        user_id = current_user.userId
    else:
        user_id = 0
    my_like = Like.query.filter(Like.userId == user_id, Like.questionId == question_id).first()
    if my_like:
        isQuestionLike = 'color:red;'
    else:
        isQuestionLike = 'color:black;'
    context = {
        'answers': Answer.query.filter_by(questionId=question_id).order_by(Answer.answerTime.desc()).all(),
        'questionLike': Like.query.filter_by(questionId=question_id).all(),
        'isQuestionLike': isQuestionLike
    }
    my_question = Question.query.filter(Question.questionId == question_id).first()
    my_question.questionView = my_question.questionView + 1
    db.session.add(my_question)
    db.session.commit()
    return render_template('detail.html', question=my_question, **context)


@my_main.route('/answer', methods=['POST'])
@login_required
def answer():
    answer_content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    current_user = User.query.filter(User.userName == session.get('user_name')).first()
    current_question = Question.query.filter(Question.questionId == question_id).first()
    my_answer = Answer(question_id=current_question.questionId, user_id=current_user.userId,
                       answer_content=answer_content,
                       answer_time=datetime.now())
    db.session.add(my_answer)
    db.session.commit()
    return redirect(url_for('main.detail', question_id=current_question.questionId))


@my_main.route('/profile')
@login_required
def profile():
    user = User.query.filter(User.userName == session.get('user_name')).first()
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


@my_main.route('/like', methods=['GET', 'POST'])
def like():
    if request.method == 'GET':
        if session.get('user_name'):
            current_user = User.query.filter(User.userName == session.get('user_name')).first()
            user_id = current_user.userId
        else:
            user_id = 0
        question_id = request.args.get('questionId')
        accumulate = int(request.args.get('accumulation'))
        if user_id == 0:
            accumulate = 0
            status = 0
            errmsg = "请先登录再点赞！"
        else:
            if accumulate == 1:
                my_like = Like(user_id=user_id, questin_id=question_id, like_time=datetime.now())
                db.session.add(my_like)
                db.session.commit()
                accumulate = 1
                status = 1
                errmsg = "点赞成功！"
            else:
                my_like = Like.query.filter(Like.userId == user_id, Like.questionId == question_id).first()
                db.session.delete(my_like)
                db.session.commit()
                accumulate = -1
                status = 1
                errmsg = "取消点赞成功！"
        return jsonify({'status': status, 'errmsg': errmsg, 'accumulate': accumulate})
