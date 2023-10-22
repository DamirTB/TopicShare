from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
from flask_mail import Mail, Message
from forms import *
import os

load_dotenv()
app = Flask(__name__)

app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"), 
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_USE_SSL=os.getenv("MAIL_USE_SSL"),
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
)

mail = Mail(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

from models import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
admin.add_view(Anypageview(name="Pages of the website"))

def send_mail(Message, UserMail, Body):
    msg = mail.send_message(
        Message,
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[UserMail],
        body=Body
    )

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
    return render_template('dashboard.html', form=form, list=list_posts)

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
            new_user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(new_user)
            try:
                db.session.commit()
                login_user(new_user)
                send_mail(Message="You successfully registered!", UserMail=new_user.email, Body="You're a new user! Try out the features of the application, and contact me if you have some suggestions")
                return redirect(url_for('profile'))
            except:
                db.session.rollback()
        else:
            flash('Such username already exists')
            return redirect(url_for("register"))
    return render_template("register.html", form=form)

@app.route('/Forum', methods=["GET", "POST"])
def forum():
    form = SeachPostForm()
    user = current_user
    if form.validate_on_submit():
        query = form.title.data
        post_list = Post.query.filter(Post.title.like("%"+query+"%")).all()
        return render_template("Forum.html", list=post_list, form=form)
    post_list = Post.query.all()
    post_list.sort(key=lambda x : x.timestamp, reverse=True)
    return render_template("Forum.html", list=post_list, form=form)

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

if __name__=="__main__":
    app.run(host="0.0.0.0", port=80)