from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["FILE_UPLOADS"] = "/mnt/c/Users/Calvin/devapp/CTFBuddy/static/ctfs"
    app.config["FILE_DOWNLOADS"] = "/mnt/c/Users/Calvin/devapp/CTFBuddy/static/ctfs"
    app.config["ALLOWED_FILE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
    app.config['MAX_FILE_FILESIZE'] = 50 * 1024 * 10241

    db.init_app(app)
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Games, Flags, UserGameStatus
    
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for game
    from .ctf import ctf as ctf_blueprint
    app.register_blueprint(ctf_blueprint)

    # blueprint for game
    from .create import create as create
    app.register_blueprint(create)

    return app
