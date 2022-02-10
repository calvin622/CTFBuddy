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
    games = Games.query.all()

    test = UserGameStatus.query.filter_by(user_id=current_user.id)

    return render_template("gameselect.html", games=games, test=test)


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




