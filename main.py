from email import message
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask import Blueprint, send_file, send_from_directory, safe_join, abort, current_app
import os
from .models import Games, Flags, UserGameStatus
from flask_login import login_required, current_user
from . import db
from werkzeug.utils import secure_filename


main = Blueprint('main', __name__)


@main.route("/index")
@main.route("/")
def index():
    #test = Flags.query.filter_by(flag='Cardinalvvv').first()
    return render_template("index.html")


@main.route("/gameselect")
@login_required
def gameselect():

    started_games = UserGameStatus.query.with_entities(
        UserGameStatus.games_id).filter_by(user_id=current_user.id, status="Started")
    completed_games = UserGameStatus.query.with_entities(
        UserGameStatus.games_id).filter_by(user_id=current_user.id, status="Completed")

    show_started_games = Games.query.filter(Games.id.in_(started_games)).all()
    show_completed_games = Games.query.filter(
        Games.id.in_(completed_games)).all()
    not_started_games = Games.query.filter(
        Games.id.notin_(started_games or completed_games)).all()

    return render_template("gameselect.html", started_games=show_started_games, completed_games=show_completed_games, not_started_games=not_started_games)


@main.route("/gameselect/<path:path>", methods=['GET', 'POST'])
@login_required
def download(path):
    try:
        return send_from_directory("/mnt/c/Users/Calvin/devapp/CTFBuddy/static/ctfs", path, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@main.route("/create")
@login_required
def create():

    return render_template("create.html")


@main.route('/create', methods=['POST'])
@login_required
def create_post():
    # code to validate and add user to database goes here
    name = request.form.get('name')

    description = request.form.get('description')
    category = request.form.get('category')
    difficulty = request.form.get('difficulty')

    flagstrings = ['flag1', 'flag2', 'flag3', 'flag4',
                   'flag5', 'flag6', 'flag7', 'flag8', 'flag9', 'flag10']
    flag_hint_strings = ['flag1_hint', 'flag2_hint', 'flag3_hint', 'flag4_hint',
                         'flag5_hint', 'flag6_hint', 'flag7_hint', 'flag8_hint', 'flag9_hint', 'flag10_hint']
    flag_point_strings = ['points1', 'points2', 'points3', 'points4',
                         'points5', 'points6', 'points7', 'points8', 'points9', 'points10']

    game = Games.query.filter_by(name=name).first()

    if game:
        flash('Game name already exists.')
        return redirect(url_for('main.create'))

    flag_num = 0
    while flag_num < 10:
        flag = request.form.get(flagstrings[flag_num])
        flag_hint = request.form.get(flag_hint_strings[flag_num])
        flag_points = request.form.get(flag_point_strings[flag_num])
        if flag:
            if not flag_hint:
                flash('Hint required.')
                return redirect(url_for('main.create'))
            if not flag_points:
                flash('Points required.')
                return redirect(url_for('main.create'))
            new_flag = Flags(flag=flag, hint=flag_hint,
                             points=flag_points, games_name=name)
            db.session.add(new_flag)
            flag_num += 1
        elif flag_hint and not flag:
            flash('Flag required for hint.')
            return redirect(url_for('main.create'))
        elif flag_points and not flag:
            flash('Flag required for hint.')
            return redirect(url_for('main.create'))

        else:
            flag_num += 1

    new_game = Games(name=name, category=category,
                     difficulty=difficulty, url="/url", user_id=current_user.id)
    #new_flag = Flags(flag=flag1, hint=flag2, points=10)

    # add the new user to the database
    db.session.add(new_game)
    # db.session.add(new_flag)
    db.session.commit()

    return redirect(url_for('main.create'))


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, image=current_user.image)


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= current_app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@main.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)

                    image.save(os.path.join(
                        current_app.config["IMAGE_UPLOADS"], filename))

                    print("Image saved")

                    return redirect(request.url)

                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

    return render_template("upload.html")
