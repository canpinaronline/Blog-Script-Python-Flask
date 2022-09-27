from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import Length,DataRequired,EqualTo,ValidationError,Email
from flaskblog.models import User,Post
from flask_login import current_user




class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı adı', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-Posta', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    confirm_password = PasswordField('Şifre (Tekrar)', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Kayıt ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı ismi alınmış, lütfen başka bir kullanıcı adı seçin.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu E-Posta adresi mevcut, lütfen başka bir kullanıcı adı seçin.')



class LoginForm(FlaskForm):
    email = StringField('E-Posta',validators=[DataRequired(),Email()])        
    password = PasswordField('Şifre',validators=[DataRequired()])                             
    submit = SubmitField("Giriş yap")


class PostForm(FlaskForm):
    title = StringField('Başlık',
                        validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Yazı ekle')



class AccountForm(FlaskForm):
    username = StringField('Kullanıcı adı',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-posta',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Güncelle')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı ismi alınmış, lütfen başka bir kullanıcı adı seçin.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu E-Posta adresi mevcut, lütfen başka bir kullanıcı adı seçin.')