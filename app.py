from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db" 
# I decided to switch to postgresql database system here insteda of using sqlite
<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jmypwdhfrsidru:1893a34fea121ff8a0f2beb4212b3974a6390cc827fda96d9d90ab86cb6d981f@ec2-3-208-74-199.compute-1.amazonaws.com:5432/dckrqrttcqnt7g'
=======
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:63626167@localhost/mydb'

#Here I changed my SQLALCHEMY_database_uri to another database for deploying my app on heroku
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ojeallicxnrgys:8592a4eea0e786a48a10b9d31acafd697e266f87800a48ab19ec12d42ca1bf98@ec2-3-233-174-23.compute-1.amazonaws.com:5432/df5aoalf88a4s6'

>>>>>>> 1449c967231d09dbccdda9f9888020b13c83ec3b
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "12345678"

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class RegisterForm(FlaskForm):
    username = StringField("", validators=[DataRequired()], render_kw={'placeholder': 'username', 'class' : 'form-control'})
    password = PasswordField("", validators=[DataRequired()], render_kw={'placeholder': 'password', 'class' : 'form-control'})
    password_repeat = PasswordField("", 
                                    validators=[DataRequired(), 
                                    validators.EqualTo('password', message='Password must match')], 
                                    render_kw={'placeholder': 'password', 'class' : 'form-control'})
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

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return f"{self.text}"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    text = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    def showtime(self):
        formatted_timestamp = self.timestamp.strftime("%d %B %Y")
        return f"{formatted_timestamp}"
    def __repr__(self):
        user = User.query.get(self.user_id)
        formatted_timestamp = self.timestamp.strftime("%d %B %Y")
        return f"by {user.username} ({formatted_timestamp})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post')
    def __repr__(self):
        user = User.query.get(self.user_id)
        return f"Made by {user.username}"
    def showtime(self):
        formatted_timestamp = self.timestamp.strftime("%d %B %Y")
        return f"{formatted_timestamp}"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    note = db.relationship('Note', backref='user') # One to many
    comments = db.relationship('Comment', backref='user')
    posts = db.relationship('Post', backref='user') 
    def __repr__(self):
        return f"<{self.username}>"

class Anypageview(BaseView):
    @expose('/')
    def anypage(self):
        return self.render('admin/anypage/index.html')

class Dashboardview(AdminIndexView):
    @expose('/')
    @login_required
    def add_data_db(self):
        return self.render('admin/dashboard_admin.html') 

admin = Admin(app, template_mode='bootstrap4', index_view=Dashboardview())
admin.add_view(ModelView(User, db.session, name="Users"))
admin.add_view(ModelView(Post, db.session, name="Posts"))
admin.add_view(ModelView(Comment, db.session, name="Comments"))
admin.add_view(Anypageview(name="Something else"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index(): 
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(503)
def server_overloaded(e):
    return "Server is down"

@app.errorhandler(429)
def too_many_request(e):
    return "Too many request"

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit('100 per hour')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            if check_password_hash(existing_user.password, form.password.data):
                login_user(existing_user)
                flash('Logged in successfully!')
                return redirect(url_for('profile'))
            else: 
                flash('Incorrect password')
                return redirect(url_for('login'))
        else: flash('There is no such user')
        return redirect(url_for('login'))
    return render_template("login.html", form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = PostForm()
    list_posts = current_user.posts
    if form.validate_on_submit():
        newPost = Post(text=form.text.data, title=form.title.data, user_id=current_user.id, author=current_user.username)
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('blog', ID_POST=newPost.id))
    return render_template('dashboard.html', tempuser=current_user, form=form, list=list_posts)

""" @app.route('/dashboard')
@login_required 
def dashboard():
    return render_template("dashboard.html") """

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            new_user = User(username=form.username.data, password=generate_password_hash(form.password.data))
            db.session.add(new_user)
            try:
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('profile'))
            except:
                db.session.rollback()
        else:
            flash('Such username already exists')
            return redirect(url_for("register"))
    return render_template("register.html", form=form)

@app.route('/Forum')
def forum():
    user = current_user
    post_list = Post.query.all()
    post_list.sort(key=lambda x : x.timestamp, reverse=True)
    return render_template("Forum.html", list=post_list, user=user)

@app.route('/Forum/<ID_POST>', methods=["GET", "POST"])
def blog(ID_POST):
    comment_form = NoteForm()
    current_post = Post.query.filter_by(id=ID_POST).first()
    comment_list = current_post.comments
    if request.method == 'POST':
        if current_user.is_authenticated:
            if comment_form.validate_on_submit():
                new_comment = Comment(text=comment_form.text.data, user_id=current_user.id, post_id=ID_POST)
                db.session.add(new_comment)
                db.session.commit()
                return redirect(url_for('blog', ID_POST=ID_POST))
        else:
            return redirect(url_for('register'))
    return render_template("topic.html", current_post=current_post, form=comment_form, comment_list=comment_list)

@app.route('/delete_blog/<ID_POST>')
@login_required
def delete_blog(ID_POST):
    current_post = Post.query.get(ID_POST)
    if current_post and current_post.user_id == current_user.id:
        db.session.delete(current_post)
        db.session.commit()
    return redirect(url_for('forum'))

@app.route('/update_blog/<ID_POST>', methods=["GET", "POST"])
@login_required
def update_blog(ID_POST):
    current_post = Post.query.get(ID_POST)
    form = PostForm()
    if current_post and current_post.user_id == current_user.id: 
        if form.validate_on_submit():
            current_post.text = form.text.data
            current_post.title = form.title.data
            db.session.commit()
            return redirect(url_for('blog', ID_POST=ID_POST))
    form.title.data = current_post.title
    form.text.data = current_post.text
    return render_template('edit_post.html', form=form)