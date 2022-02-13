from email import message
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask import Blueprint, send_file, send_from_directory, safe_join, abort
import os
from .models import Games, Flags, UserGameStatus
from flask_login import login_required, current_user
from . import db


main = Blueprint('main', __name__)

@main.route("/index")
@main.route("/")
def index():
    #test = Flags.query.filter_by(flag='Cardinalvvv').first()
    return render_template("index.html")

    
@main.route("/gameselect")
@login_required
def gameselect():
    
    started_games = UserGameStatus.query.with_entities(UserGameStatus.games_id).filter_by(user_id=current_user.id, status="Started")
    completed_games = UserGameStatus.query.with_entities(UserGameStatus.games_id).filter_by(user_id=current_user.id, status="Completed")
    
    show_started_games = Games.query.filter(Games.id.in_(started_games)).all()
    show_completed_games = Games.query.filter(Games.id.in_(completed_games)).all()
    not_started_games = Games.query.filter(Games.id.notin_(started_games or completed_games)).all()

    

    return render_template("gameselect.html", started_games=show_started_games, completed_games=show_completed_games, not_started_games=not_started_games)
    


@main.route("/gameselect/<path:path>", methods=['GET', 'POST'])
@login_required
def download(path):
    try:
        return send_from_directory("/mnt/c/Users/Calvin/devapp/CTFBuddy/static/ctfs", path, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, image=current_user.image)




