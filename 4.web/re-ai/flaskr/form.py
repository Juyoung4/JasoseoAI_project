from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    passwd = PasswordField('passwd', validators = [DataRequired()])


class LoginForm(FlaskForm):
    """ 방법 1 바로 query
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
            
        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data
            
            usertable = User.query.filter_by(userid=userid).first()
            if usertable.password != password:
            	raise ValueError('비밀번호 틀림')
                
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])
    """
    
    """ 방법 2 : service에 보냄"""
    username = StringField('username', validators=[DataRequired()])
    passwd = PasswordField('passwd', validators=[DataRequired()])