from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField,IntegerField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    user_name = StringField('用户', validators=[DataRequired()])
    user_password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('提交')


class RegisterForm(FlaskForm):
    user_name = StringField('用户', validators=[DataRequired()])
    user_password = PasswordField('密码', validators=[DataRequired()])
    user_email = StringField('邮件', validators=[Email()])
    user_nickname = StringField('昵称', validators=[DataRequired()])
    user_birth = StringField('生日')
    submit = SubmitField('提交')


class QuestionForm(FlaskForm):
    question_topic = StringField('标题', validators=[DataRequired()])
    question_content = TextAreaField('正文', validators=[DataRequired()])
    submit = SubmitField('发布')


# class AnswerForm(FlaskForm):
#     answer_content = TextAreaField('发布', validators=[DataRequired()])
#     submit = SubmitField('回答')
