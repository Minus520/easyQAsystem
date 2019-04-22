from db import db
from datetime import datetime


class User(db.Model):
    userId = db.Column('userId', db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column('userName', db.String(16), nullable=False)
    userPassword = db.Column('userPassword', db.String(12), nullable=False)
    userEmail = db.Column('userEmail', db.String(30), nullable=True)
    userNickname = db.Column('userNickname', db.String(20), nullable=True)
    registerTime = db.Column('registerTime', db.DateTime, default=datetime.now())
    userBirth = db.Column('userBirth', db.String(20))
    __tablename__ = 't_user'

    def __repr__(self):
        return '<User %r>' % self.userId

    def __init__(self, user_name=None, user_password=None, user_email=None, user_nickname=None, register_time=None,
                 user_birth=None):
        self.userName = user_name
        self.userPassword = user_password
        self.userEmail = user_email
        self.userNickname = user_nickname
        self.registerTime = register_time
        self.userBirth = user_birth


class Question(db.Model):
    questionId = db.Column('questionId', db.Integer, primary_key=True, autoincrement=True)
    # userId = db.Column('userId', db.Integer, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('t_user.userId'))
    user = db.relationship('User', backref=db.backref('questions'))
    questionTopic = db.Column('questionTopic', db.String(100), nullable=False)
    questionContent = db.Column('questionContent', db.String(2000), nullable=False)
    questionTime = db.Column('questionTime', db.DateTime, default=datetime.now())
    questionView = db.Column('questionView', db.Integer, default=0)
    __tablename__ = 't_question'

    def __repr__(self):
        return '<Question %r>' % self.questionId


class Answer(db.Model):
    answerId = db.Column('answerId', db.Integer, primary_key=True, autoincrement=True)
    # foreign key userId
    userId = db.Column(db.Integer, db.ForeignKey('t_user.userId'))
    user = db.relationship('User', backref=db.backref('answers'))
    # foreign key postId
    questionId = db.Column(db.Integer, db.ForeignKey('t_question.questionId'))
    question = db.relationship('Question', backref=db.backref('answers'))

    answerContent = db.Column('answerContent', db.String(500), nullable=False)
    answerTime = db.Column('answerTime', db.DateTime, default=datetime.now())
    __tablename__ = 't_answer'

    def __repr__(self):
        return '<Answer %r>' % self.answerId

    def __init__(self, question_id=None, user_id=None, answer_content=None, answer_time=None):
        self.questionId = question_id
        self.userId = user_id
        self.answerContent = answer_content
        self.answerTime = answer_time
