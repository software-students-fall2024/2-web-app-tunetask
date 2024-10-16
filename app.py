from dotenv import load_dotenv
from flask import Flask, make_response, request, redirect, url_for, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import os
import pymongo

load_dotenv('./.env')
class User(UserMixin):
    def __init__(self, username):
        self.id = username

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    connection = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = connection[os.getenv("MONGO_DBNAME")]

    @login_manager.user_loader
    def load_user(username):
        user_data = db.users.find_one({"username": username})
        if user_data:
            return User(username=user_data["username"])
        return None
    
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
    @login_required
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

            if user_data and user_data["password"] == password:
                user = User(username)
                login_user(user)
                return redirect(url_for('show_profile', user=username))
            else:
                error = "Invalid username or password."

        return render_template('login.html', error=error)



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
                return "User not found", 404


        return render_template('login.html')
    
    @app.route('/profile/<user>/new_task', methods = ["GET", "POST"])
    def new_task(user):
        if request.method == 'POST':
            # Get form data from the user
            title = request.form.get('title')
            description = request.form.get('description')
            task_list = [request.form.get('task_list')]
            play_list = [request.form.get('play_list')]

            if not task_name or not description:
                flash("Task name and description are required!")
                return redirect(url_for('new_task', user = user))

            task_data = {
                'username': user,
                'title': title,
                'description': description,
                'task_list': task_list,
                'play_list': play_list,
            }

            mongo.db.tune_tasks.insert_one(task_data)

            flash('New task added successfully!')
            return redirect(url_for('show_profile', user = user, collection = tune_tasks))
        return render_template('new_task.html')
    return app


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "3000")
    app = create_app()
    app.run(port=FLASK_PORT)