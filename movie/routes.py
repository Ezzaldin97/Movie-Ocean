from movie import app, db
from flask import render_template, flash, redirect, url_for, request
from movie.db_setup import User, Movies, Likes, Comments
from movie.forms import RegisterForm, LoginForm, FetchMovie, CommentOnMovie, LikeMovie
from flask_login import login_user, logout_user, login_required, current_user
import requests

@app.route('/')
@app.route('/home/')
def home_page():
    return render_template('home-page.html')

def api_response(title, genre):
    title=title.lower().replace(' ','+')
    url = "http://www.omdbapi.com/?t={}&type={}&apikey=2e12d3e3".format(title, genre)
    response = requests.get(url)
    if response.status_code==200:
        return True
    else: 
        return False

def find_json_data(title, genre):
    val=api_response(title, genre)
    if val:
        title=title.lower().replace(' ','+')
        url = "http://www.omdbapi.com/?t={}&type={}&apikey=2e12d3e3".format(title, genre)
        response = requests.get(url)
        json_data=response.json()
        return json_data
    else:
        return "Wrong"

def find_movie_in_db(movie_title):
    movie_to_find=Movies.query.filter_by(movie_title=movie_title).first()
    if movie_to_find:
        return True
    else:
        return False
    
@app.route('/movies/', methods=['GET', 'POST'])
@login_required
def movies_page():
    form=FetchMovie()
    if form.validate_on_submit():
        data=find_json_data(form.movie_title.data,
                            form.media_type.data)
        found=find_movie_in_db(form.movie_title.data)
        if not (found):
            if data!="Wrong":
                movie_to_create=Movies(movie_title=data['Title'],
                                       poster_link=data['Poster'],
                                       imdb_rating=data['Ratings'][0]['Value'],
                                       story=data['Plot'],
                                       actors=data['Actors'],
                                       director=data['Director'],
                                       awards=data['Awards'],
                                       genre=data['Genre'],
                                       post_creator=current_user.username)
                db.session.add(movie_to_create)
                db.session.commit()
                flash(f"{data['Title']} has been created", category='success')
                return redirect(url_for('movies_page')) 
            else:
                flash('Something went wrong!', category='danger')
        else:
            flash('Movie already existed, try to find it', category='danger')
    movies_data=Movies.query.all()
    return render_template('movies-page.html', form=form, movies=movies_data)

@app.route('/sign-up/', methods=['GET', 'POST'])
def sign_up_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password_1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('Your account created Successfully, and You logged in', category='success')
        return redirect(url_for('movies_page'))
    if form.errors!={}:
        for i in form.errors.values():
            flash(f'There was an error with creating a user: {i}', category='danger')
    return render_template('sign-up-form.html', form=form)

@app.route('/log-in/', methods=['GET', 'POST'])
def log_in_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('movies_page'))
        else:
            flash(r'Username or Password is not Correct', category='danger')
    return render_template('log-in-form.html', form=form)

@app.route('/log-out/')
def log_out():
    logout_user()
    flash('You have been logged out!', category='success')
    return redirect(url_for('home_page'))

@app.route('/<string:movie_title>/', methods=['GET', 'POST'])
@login_required
def movie_info_page(movie_title):
    movie_data=Movies.query.filter_by(movie_title=movie_title).one()
    movie_comments=Comments.query.filter_by(movies_id=movie_data.id).all()
    like_movie_data=Likes.query.filter_by(movies_id=movie_data.id).all()
    return render_template('movie-info-page.html', movie=movie_data, comments=movie_comments, user_db=User(), likes=like_movie_data)

@app.route('/<string:movie_title>-comment/', methods=['GET', 'POST'])
@login_required
def make_comment(movie_title):
    form=CommentOnMovie()
    movie_data=Movies.query.filter_by(movie_title=movie_title).one()
    user_id=current_user.id
    if form.validate_on_submit():
        user_comment= form.comment_area.data
        comment_to_create=Comments(comment=user_comment,
                                   user_id=user_id,
                                   movies_id=movie_data.id)
        db.session.add(comment_to_create)
        db.session.commit()
        return redirect(url_for('movie_info_page', movie_title=movie_title))
    return render_template('comment.html', form=form)

def like_dislike(movie_id, user_id):
    data=Likes.query.filter_by(user_id=user_id, movies_id=movie_id).first()
    if data:
        return True
    else:
        return False

@app.route('/<string:movie_title>-like/', methods=['GET', 'POST'])
@login_required
def give_like(movie_title):
    form=LikeMovie()
    movie_data=Movies.query.filter_by(movie_title=movie_title).one()
    if form.validate_on_submit():
        like_data=like_dislike(movie_data.id, current_user.id)
        if like_data:
            row=Likes.query.filter_by(user_id=current_user.id, movies_id=movie_data.id).first()
            db.session.delete(row)
            db.session.commit()
        else:
            like_to_create=Likes(user_id=current_user.id,
                                 movies_id=movie_data.id)
            db.session.add(like_to_create)
            db.session.commit()
        return redirect(url_for('movie_info_page', movie_title=movie_title))
    return render_template('likes.html', movie=movie_data, form=form) 