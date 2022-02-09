from email import message
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask import Blueprint, send_file, send_from_directory, safe_join, abort
import os
from .models import Games, Flags
from flask_login import login_required, current_user
from . import db


main = Blueprint('main', __name__)

@main.route("/index")
@main.route("/")
def index():
    return render_template("index.html")

    
@main.route("/gameselect")
@login_required
def gameselect():
    return render_template("gameselect.html", games=flags.query.all())


@main.route("/gameselect/<path:ctf_name>", methods=['GET', 'POST'])
@login_required
def download(ctf_name):
    try:
        return send_from_directory("/mnt/c/Users/Calvin/CTFBuddy/static/ctfs", filename=ctf_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)




