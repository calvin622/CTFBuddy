from email import message
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask import Blueprint
from .models import flags
from flask_login import login_required, current_user


main = Blueprint('main', __name__)

@main.route("/index")
@main.route("/")
def index():
    return render_template("index.html")

    
@main.route("/gameselect")
@login_required
def gameselect():
    return render_template("gameselect.html")

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)




