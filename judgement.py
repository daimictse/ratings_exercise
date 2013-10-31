from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    return render_template("user_list.html")

@app.route("/", methods=["POST"])
def process_login():
    emailAddr = request.form.get("emailaddress")
    password = request.form.get("password")

    user = model.session.query(model.User).filter(model.User.email==emailAddr).filter(model.User.password==password).first()
    if (user):
        flash("User authenticated!")
        session['userId'] = user.id
    else:
        flash("Login information is incorrect.")
        return redirect(url_for("index"))
    
    return redirect("/user/%s"%user.id)

@app.route("/allusers") 
#list of all the users
def see_all_users():
    user_list = model.session.query(model.User).all()
    return render_template("all_users.html", users=user_list)

@app.route("/user/<user_id>")
#click on user and see the list of movies they've rated as well as the ratings
def view_user(user_id):
    #the_user_id = model.session.query(model.User).get(user_id)
    # movie_ratings = model.session.query(model.Ratings).all()
    user = model.session.query(model.User).get(user_id)
    rating_list = model.session.query(model.Ratings).all()
    return render_template("user_profile.html", user=user, ratings=rating_list)

@app.route("/search", methods=["GET"])
def display_search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form['query']
    movies = model.session.query(model.Movies).\
            filter(model.Movies.name.ilike("%" + query + "%")).\
            limit(20).all()

    return render_template("results.html", movies=movies)

@app.route("/movie/<movie_id>")
#click on user and see the list of movies they've rated as well as the ratings
def movie_list(movie_id):
    movie = model.session.query(model.Movies).get(movie_id)
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    for r in ratings:
        if r.user_id == session['userId']:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums)) / len(rating_nums)

    # Prediction code: only predict if the user hasn't reated it
    user = model.session.query(model.User).get(session['userId'])
    prediction = None
    
    if not user_rating:
        prediction = user.predict_rating(movie)
        effective_rating = prediction
    else:
        effective_rating = user_rating.rating

    the_eye = model.session.query(model.User).filter_by(email="theeye@ofjudgement.com").one()
    eye_rating = model.session.query(model.Ratings).filter_by(user_id=the_eye.id, movie_id=movie.id).first()

    if not eye_rating:
        eye_rating = the_eye.predict_rating(movie)
    else:
        eye_rating = eye_rating.rating

    difference = abs(eye_rating - effective_rating)

    # End prediction
    return render_template("movie.html", movie=movie, average=avg_rating, rating=user_rating, prediction=prediction)
    # userId = session.get("userId")
    # user = model.session.query(model.User).get(userId)
    # rating = model.session.query(model.Ratings).filter_by(movie_id=movie.id, user_id=userId).one()
    # print rating.rating
    # # rating = model.session.query(model.Ratings).filter(movie.name).all()
    # return render_template("movie.html", movie=movie,user_email=user.email, rating=rating.rating)


@app.route("/movie/<movie_id>", methods=['POST'])
#click on user and see the list of movies they've rated as well as the ratings
def rate_movie(movie_id):
    movie = model.session.query(model.Movies).get(movie_id)
    userId = session.get("userId")
    # user = model.session.query(model.User).get(userId)
    rating = model.session.query(model.Ratings).filter_by(movie_id=movie.id, user_id=userId).one()
    rating.rating = request.form['rating']
    model.session.commit()
    return render_template("movie.html", movie=movie, average=None, rating=rating.rating, prediction=None)

@app.route("/movie_ratings/<movie_id>", methods=['POST'])
#click on user and see the list of movies they've rated as well as the ratings
def movie_ratings(movie_id):
    movie = model.session.query(model.Movies).get(movie_id)
    ratings = model.session.query(model.Ratings).filter_by(movie_id=movie_id).all()
    return render_template("movie_ratings.html", movieName=movie.name, ratings=ratings)

#get id out of users to apply to ratings to get ratings to apply to movies to get titles


@app.route("/register", methods = ["GET"])
def register():
    return render_template("register.html")

@app.route("/register", methods = ["POST"])
def create_user():
    email = request.form.get("emailaddress")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    user = model.User(email=email, password=password, age=age, zipcode=zipcode)
    model.session.add(user)
    model.session.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)
