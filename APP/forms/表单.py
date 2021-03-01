from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo,ValidationError,Optional
from flask_ckeditor import CKEditorField

from flask_wtf.file import FileField,FileAllowed,FileRequired

from APP.数据库 import User,Category


class RegisterForm(FlaskForm):
    name = StringField('昵称',validators=[DataRequired(),Length(1,20)])
    username = StringField('用户名',validators=[DataRequired(),Length(1,30),
                                             Regexp('^[a-zA-Z0-9]*$',message='只允许输入字母与数字')])
    password = PasswordField('密码',validators=[DataRequired(),Length(1,128),EqualTo('password2')])
    password2 = PasswordField('确认密码',validators=[DataRequired()])
    submit = SubmitField('确认注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(1,30)])
    password = PasswordField('密码',validators=[DataRequired(),Length(1,128)])
    b = BooleanField('记住密码')
    SubmitField = SubmitField('登录')


class NoteForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(),Length(1,30)])
    photo = FileField('上传图片', validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png', 'gif']),Optional()])
    category = SelectField('类别',validators=[DataRequired(),Length(1,30)])
    body = CKEditorField('编辑文章',validators=[DataRequired(),Length(1,1000)])
    submit = SubmitField('发表')

    def __init__(self,*args,**kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class EditNoteForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(),Length(1,30)])
    category = SelectField('类别',validators=[DataRequired(),Length(1,30)])
    body = CKEditorField('编辑文章',validators=[DataRequired(),Length(1,1000)])
    submit = SubmitField('发表')

    def __init__(self,*args,**kwargs):
        super(EditNoteForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CommentForm(FlaskForm):
    body = TextAreaField('评论',validators=[DataRequired(),Length(1,200)])
    submit = SubmitField('发表评论')


class CategoryForm(FlaskForm):
    name = StringField('类名',validators=[DataRequired(),Length(1,30)])
    submit = SubmitField('创建分类')

    def validate_category(self,field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('此分类已存在')
