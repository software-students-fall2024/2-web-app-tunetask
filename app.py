from dotenv import load_dotenv
from flask import Flask, make_response, request, redirect, url_for, render_template
from flask_login import login_manager, login_user, UserMixin
import os
import pymongo

load_dotenv('./.env')
class User(UserMixin):
    pass

def create_app():
    app = Flask(__name__)
    connection = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = connection[os.getenv("MONGO_DBNAME")]

    @app.route('/')
    def show_home():
        
        connection = pymongo.MongoClient(os.getenv("MONGO_URI"))
        db = connection[os.getenv("MONGO_DBNAME")]

        try:
            connection.admin.command("ping")
            print("MongoDB connection successful")
        except Exception as e:
            print("MongoDB connection error:", e)

        return render_template('home.html')
    
    @app.route('/profile/<user>')
    def show_profile(user):
        tune_tasks = list(db.tune_tasks.find({"created_by":user}))
        return render_template('profile.html', user=user, collection=tune_tasks)
    
    @app.route('/profile/<user>/delete/<tunetask>', methods=["POST"])
    def delete_tunetask(user, tunetask):
        db.tune_tasks.delete_one({'title':"morning sun"})
        return redirect(url_for('show_profile', user=user))
    
    @app.route('/search')
    def show_search():
        return render_template('search.html')
    
    @app.route('/search', methods=["POST"])
    def post_search():
        user = request.form["user"]
        tune_tasks= list(db.tune_tasks.find({"created_by":user}))
        # return make_response("hello", 200)
        if len(tune_tasks) == 0:
            return make_response("user not found", 200)
        return render_template('profile.html', user=user, collection=tune_tasks)
    
    @app.route('/login', methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            
            # checking mongodb to find user
            user_data = db.users.find_one({"username": username})

            if user_data:
                # password is only plain text, not hashed so comparing as such
                if user_data["password"] == password:
                    return redirect(url_for('show_profile', user=username))
                else:
                    error = "Invalid password, please try again."
            else:
                error = "User not found"


        return render_template('login.html', error=error)
    
    @app.route('/register', methods=["GET", "POST"])
    def register():
        error = None
        if request.method == "POST":
            name = request.form["name"]
            username = request.form["username"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            if password != confirm_password:
                error = "Passwords do not match. Please try again."
            # check if the user already exists
            elif db.users.find_one({"username": username}):
                error = "Username already exists. Please choose a different one."
            else:
                # add new user into database
                db.users.insert_one({
                    "name": name,
                    "username": username,
                    "password": password
                })
                return redirect(url_for('login'))

        return render_template('register.html', error=error)

    
    return app


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "3000")
    app = create_app()
    app.run(port=FLASK_PORT)