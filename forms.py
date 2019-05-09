# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    user_name = StringField(u'用户', validators=[DataRequired()])
    user_password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class RegisterForm(FlaskForm):
    user_name = StringField(u'用户', validators=[DataRequired()])
    user_password = PasswordField(u'密码', validators=[DataRequired()])
    user_email = StringField(u'邮件', validators=[Email()])
    user_nickname = StringField(u'昵称', validators=[DataRequired()])
    user_birth = StringField(u'生日')
    submit = SubmitField(u'提交')


class QuestionForm(FlaskForm):
    question_topic = StringField(u'标题', validators=[DataRequired()])
    question_content = TextAreaField(u'正文', validators=[DataRequired()])
    submit = SubmitField(u'发布')

# class AnswerForm(FlaskForm):
#     answer_content = TextAreaField('发布', validators=[DataRequired()])
#     submit = SubmitField('回答')
