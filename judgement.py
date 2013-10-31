from flask import Flask, render_template, redirect, request, url_for, flash, session
import model

app = Flask(__name__)
app.secret_key = "shhhthisisasecret"

@app.route("/")
def index():
    if session.get("id"):
        user = model.get_user_by_id(session["id"])
        return redirect(url_for("profile", user_id =user.id))
    else:
        return render_template("index.html", user_id=None)

@app.route("/", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_id = model.authenticate(email, password)
    if user_id == None:
        flash("User does not exist")
        return redirect(url_for("index"))
    else:
        session['id'] = user_id
        return redirect(url_for("profile", user_id =user_id))


@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for ("index"))

@app.route("/profile/<user_id>")
def profile(user_id):
    profile_link = my_profile_link()
    user = model.get_user_by_id(user_id)
    movie_ratings = model.view_movie_list(user_id)
    if session.get('id'):
        if session['id'] == int(user_id):
            return render_template("profile.html", user_id=user_id, email = user.email,
                                    movie_ratings=movie_ratings, profile_link=profile_link)
        else:
            return render_template("user_profile.html", user_id=user_id, email = user.email,
                        movie_ratings=movie_ratings, profile_link=profile_link)
    else:
        return render_template("user_profile.html", user_id=user_id, email = user.email,
                        movie_ratings=movie_ratings, profile_link=profile_link)

        

@app.route("/profile/<user_id>", methods=["POST"])
def add_rating(user_id):
    movie_name = request.form.get("movie_name")
    rating = request.form.get("rating")
    if model.movie_does_not_exist(movie_name):
        flash("Movie not in database")
        return redirect(url_for("profile", user_id=user_id))
    else:
        movie_id = model.view_movieid_by_name(movie_name)
        if model.user_rated_movie(movie_id, user_id):
            model.update_rating(user_id, movie_id, rating)
        elif movie_name == "":
            flash("Please enter a movie name...")
        elif rating == None:
            flash("...Rating?")
        else:
            model.create_rating(user_id, movie_id, rating)
        return redirect(url_for("profile", user_id=user_id))

def my_profile_link():
    if session.get('id'):
        profile_link = session['id']
    else:
        profile_link = None
    return profile_link

@app.route("/display_users/")
@app.route("/display_users/<int:page_id>")
def display_users(user_id, page_id=0):
    profile_link = my_profile_link()
    user_list = model.session.query(model.User).filter(model.User.id > page_id).limit(50).all()
    return render_template("user_list.html", users=user_list, page_id=page_id, profile_link = profile_link)

@app.route("/movie_results", methods = ["POST"])
def show_search_results():
    movie_title = request.form.get("movie_title")
    movie_exist = model.movie_does_not_exist(movie_title)
    if not movie_exist:
        return redirect(url_for("movie_profile", movie_name= movie_title))
    else:
        flash ("There isn't a movie by that name. Make sure to capitalize!")
        return redirect(url_for("movies"))


@app.route("/movies/")
@app.route("/movies/<int:page_id>")
def display_movies(page_id=0):
    profile_link = my_profile_link()
    movie_list = model.session.query(model.Movie).filter(model.Movie.id > page_id).limit(50).all()
    return render_template("movie_list.html", movies=movie_list, page_id=page_id, profile_link = profile_link)

@app.route("/movie_title/<movie_name>")
def movie_profile(movie_name):
    profile_link = my_profile_link()
    user_ratings = model.view_users_ratings(movie_name)
    if session.get('id'):
        id = session['id']
    else:
        id = None
    avg_rating, rating, prediction, beratement = model.get_movie_prediction(id, movie_name)
    return render_template("movie_profile.html", profile_link=profile_link, user_ratings=user_ratings,
                            movie_name=movie_name, average=avg_rating, rating=rating, prediction=prediction,
                            beratement = beratement)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def create_user():
    email = request.form.get("email")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    password = request.form.get("password")
    verify_password = request.form.get("password_verify")
    
    if password != verify_password:
        flash("Passwords do not match")
        return redirect(url_for("register"))
    if model.user_exists(email):
        flash("Account already exists for user email")
        return redirect(url_for("register"))

    model.create_user(email, password, age, zipcode)
    flash("You've successfully made an account!")
    return redirect(url_for("index"))



if __name__=="__main__":
    app.run(debug = True)


