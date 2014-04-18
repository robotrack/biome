from flask.ext.wtf import Form
from app.models import User

from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length
from flask.ext.babel import gettext

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False

        if self.nickname.data == self.original_nickname:
            return True

        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(gettext('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.'))
            return False

        user = User.query.filter_by(nickname = self.nickname.data).first()

        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
            
        return True

class PostForm(Form):
    post = TextField('post', validators = [Required()])

class PageForm(Form):
	page_title = TextField('page_title')
	page_content = TextAreaField('page_content')
