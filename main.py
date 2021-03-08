from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from forms import LoginForm, RegisterForm
import requests
import os
from dotenv import load_dotenv
from config import SECRET_KEY

load_dotenv()

MOVIE_DB_API_KEY = os.getenv("MOVIE_DB_API_KEY")

MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_POPULAR = "https://api.themoviedb.org/3/movie/popular"
MOVIE_DB_LATEST = "https://api.themoviedb.org/3/movie/now_playing"
MOVIE_DB_RANKING = "https://api.themoviedb.org/3/movie/top_rated"

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CONFIGURE TABLE
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    user = relationship("Movie", back_populates="user")


db.create_all()


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="user")


db.create_all()


@ app.route('/')
def home():
    popular_response = requests.get(MOVIE_DB_POPULAR, params={
        "api_key": MOVIE_DB_API_KEY})
    popular_data = popular_response.json()["results"]

    ranking_response = requests.get(MOVIE_DB_RANKING, params={
                                    "api_key": MOVIE_DB_API_KEY})
    ranking_data = ranking_response.json()["results"]

    latest_response = requests.get(MOVIE_DB_LATEST, params={
                                   "api_key": MOVIE_DB_API_KEY})
    latest_data = latest_response.json()["results"][:5]

    return render_template('index.html', popular_options=popular_data, latest_options=latest_data, ranking_options=ranking_data, current_user=current_user)


@ app.route('/movie/<int:movie_id>, methods=["GET", "POST"]')
def get_movie(movie_id):
    movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_id}"
    response = requests.get(movie_api_url, params={
        "api_key": MOVIE_DB_API_KEY, "language": "en-US"})
    data = response.json()
    new_movie = Movie(
        id=data["id"],
        title=data["title"],
        year=data["release_date"].split("-")[0],
        img_url=data["backdrop_path"],
        description=data["overview"]
    )
    return render_template('movie.html', movie_id=new_movie.id, title=new_movie.title, img_url=new_movie.img_url, overview=new_movie.description)


@ app.route('/add/<int:movie_id>, methods=["GET", "POST"]')
def add_movie(movie_id):

    if not current_user.is_authenticated:
        flash("Please login.")
        return redirect(url_for('login'))

    movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_id}"
    response = requests.get(movie_api_url, params={
        "api_key": MOVIE_DB_API_KEY, "language": "en-US"})
    data = response.json()
    new_movie = Movie(
        id=data["id"],
        title=data["title"],
        year=data["release_date"],
        description=data["overview"],
        img_url=data['backdrop_path'],
        user=current_user
    )
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('all_fav'))


@ app.route('/fav', methods=["GET", "POST"])
def all_fav():
    if not current_user.is_authenticated:
        flash("Please login.")
        return redirect(url_for('login'))

    all_movies = Movie.query.filter_by(user=current_user).all()
    db.session.commit()
    return render_template('fav.html', movies=all_movies, current_user=current_user)


@ app.route('/delete')
def delete_movie():
    movie_id = request.args.get("movie_id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('all_fav'))


@ app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            flash("You've already signed up with that email, please log in.")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html', form=form)


@ app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('all_fav'))
    return render_template('login.html', form=form, current_user=current_user)


@ app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
