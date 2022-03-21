from audioop import reverse
from email import message
from fileinput import filename
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask import Blueprint, send_file, send_from_directory, safe_join, abort, current_app
import os
from .models import Games, Flags, UserGameStatus, User
from flask_login import login_required, current_user
from . import db
from werkzeug.utils import secure_filename


main = Blueprint('main', __name__)


@main.route("/index")
@main.route("/")
def index():
    return render_template("index.html")

@main.route("/guide")
def guide():
    return render_template("guide.html")



@main.route("/gameselect")
@login_required
def gameselect():

    started_games = UserGameStatus.query.filter_by(user_id=current_user.id, status="Started")
    completed_games = UserGameStatus.query.filter_by(user_id=current_user.id, status="Completed")
    all_games = Games.query.all()

    return render_template("gameselect.html", started_games=started_games, completed_games=completed_games, all_games=all_games)


@main.route("/gameselect/<path:path>", methods=['GET', 'POST'])
@login_required
def download(path):
    try:
        return send_from_directory(current_app.config["FILE_DOWNLOADS"], path, as_attachment=True)
    except FileNotFoundError:
        abort(404)

def allowed_file(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_file_filesize(filesize):

    if int(filesize) <= current_app.config["MAX_FILE_FILESIZE"]:
        return True
    else:
        return False


def upload_file():

    if request.files:

        if "filesize" in request.cookies:

            if not allowed_file_filesize(request.cookies["filesize"]):
                print("Filesize exceeded maximum limit")
                return False

            file = request.files["file"]

            if file.filename == "":
                print("No filename")
                return False

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                return filename

            else:
                print("That file extension is not allowed")
                return False
    else:
        return False



@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    users = User.query.order_by(User.points.desc())
    leaderboard = 1
    for user in users:
        if user.name == current_user.name:
            break
        else:
            leaderboard +=1

    games = UserGameStatus.query.filter_by(user_id=current_user.id)
    num_complete = UserGameStatus.query.filter_by(user_id=current_user.id, status="Completed")
    user = User.query.filter_by(id=current_user.id).first()

    #categories_complete = [cracking, reverse] = 0, 1

    cat_dict = {
        "CTFs": 0,
        "Reverse Engineering": 0,
        "Cryptography": 0,
        "Web": 0,
        "Linux": 0,
        "Windows": 0,
        "Forensics": 0,
    }


    for game in games:
        if game.games.category == "CTFs" and game.status == "Completed":
            cat_dict['CTFs'] += 1
        elif game.games.category == "Reverse Engineering" and game.status == "Completed":
            cat_dict['Reverse Engineering'] += 1

        elif game.games.category == "Cryptography" and game.status == "Completed":
            cat_dict['Cryptography'] += 1

        elif game.games.category == "Web" and game.status == "Completed":
            cat_dict['Web'] += 1

        elif game.games.category == "Linux" and game.status == "Completed":
            cat_dict['Linux'] += 1

        elif game.games.category == "Windows" and game.status == "Completed":
            cat_dict['Windows'] += 1

        elif game.games.category == "Forensics" and game.status == "Completed":
            cat_dict['Forensics'] += 1
    
    
    if request.files and request.method == 'POST':
        filename = upload_file()
        if not filename:
            flash('Error with upload.')
            return redirect(url_for('main.profile'))
        file = request.files["file"]
        #path = os.path.join(current_app.config["IMG_UPLOADS"], filename)
        file.save(os.path.join(current_app.config["IMG_UPLOADS"], filename))
        user.image = filename
        db.session.commit()

        return redirect(url_for('main.profile'))
    
    
    
    return render_template('profile.html', name=current_user.name, image=current_user.image, points=current_user.points,ctfs=cat_dict['CTFs'],reverse=cat_dict['Reverse Engineering'],crypto=cat_dict['Cryptography'],web=cat_dict['Web'],linux=cat_dict['Linux'],windows=cat_dict['Windows'], forensics=cat_dict['Forensics'], strongest=max(cat_dict, key=cat_dict.get), weakest=min(cat_dict, key=cat_dict.get),rank=leaderboard, num_games=num_complete.count())


@main.route("/create")
@login_required
def create():

    return render_template("create.html")



