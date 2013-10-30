from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", users = user_list)

@app.route("/allusers") 
#list of all the users
def see_all_users():
    user_list = model.session.query(model.User).all()
    return render_template("all_users.html", users=user_list)

@app.route("/user/<user_id>")
#click on user and see the list of movies they've rated as well as the ratings
def view_user(user_id):
    #the_user_id = model.session.query(model.User).get(user_id)
    movie_ratings = model.session.query(model.Ratings).all()



#get id out of users to apply to ratings to get ratings to apply to movies to get titles



"""
@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    user_id = model.get_user_by_name(username)
    posts = model.get_wall_posts(user_id)
    return render_template("wall.html", the_posts=posts, username=username)
"""
@app.route("/newrating") 
#should be able to when logged in, add or update personal rating for said movie  


@app.route("/register", methods = ["GET"])
def give_form():
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
