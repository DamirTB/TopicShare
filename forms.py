from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, validators, SearchField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, Email

class SeachPostForm(FlaskForm):
    title = SearchField("", validators=[DataRequired()], render_kw={'placeholder':'search', 'class':'form-control rounded'})

class RegisterForm(FlaskForm):
    username = StringField("", validators=[DataRequired()], render_kw={'placeholder': 'username', 'class' : 'form-control'})
    email = StringField('', validators=[DataRequired(), Email()], render_kw={'placeholder': 'email', 'class' : 'form-control'})
    gender = SelectField('', choices=[('female', 'Female'), ('male', "Male")], render_kw={'class' : 'form-control'})
    password = PasswordField("", validators=[DataRequired()], render_kw={'placeholder': 'password', 'class' : 'form-control'})
    password_repeat = PasswordField("", 
                                    validators=[DataRequired(), 
                                    validators.EqualTo('password', message='Password must match')], 
                                    render_kw={'placeholder': 'repeat password', 'class' : 'form-control'})
    submit = SubmitField("Enter", render_kw={'class' : 'btn btn-primary form-control '})

class LoginForm(FlaskForm):
    username = StringField("", validators=[DataRequired()], render_kw={'placeholder': 'username', 'class' : 'form-control'})
    password = PasswordField("", validators=[DataRequired()], render_kw={'placeholder' : 'password', 'class' : 'form-control'})
    submit = SubmitField("Enter", render_kw={'class' : 'btn btn-primary form-control '})

class NoteForm(FlaskForm):
    text = TextAreaField("Text", validators=[DataRequired()], render_kw={"rows": 4, "cols": 30, 'class' : 'form-control'})
    submit = SubmitField("Submit", render_kw={'class' : 'btn btn-primary'})

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()], render_kw={'class' : 'form-control'})
    text = TextAreaField("Text", validators=[DataRequired()], render_kw={"rows": 10, "cols": 30, 'class' : 'form-control'})
    submit = SubmitField("Submit", render_kw={'class' : 'btn btn-primary'})



