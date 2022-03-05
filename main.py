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



@main.route('/profile')
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

    #categories_complete = [cracking, reverse] = 0, 1

    cat_dict = {
        "Reverse Engineering": 4,
        "Cryptography": 5,
        "Web": 3,
        "Linux": 4,
        "Windows": 5,
        "Forensics": 6,
    }


    for game in games:
        if game.games.category == "Reverse Engineering" and game.status == "Completed":
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
    
    return render_template('profile.html', name=current_user.name, image=current_user.image, points=current_user.points,reverse=cat_dict['Reverse Engineering'],crypto=cat_dict['Cryptography'],web=cat_dict['Web'],linux=cat_dict['Linux'],windows=cat_dict['Windows'], forensics=cat_dict['Forensics'], strongest=max(cat_dict, key=cat_dict.get), weakest=min(cat_dict, key=cat_dict.get),rank=leaderboard)


@main.route("/create")
@login_required
def create():

    return render_template("create.html")



