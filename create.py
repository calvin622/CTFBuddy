from flask import redirect, url_for, request, flash, Blueprint, current_app
import os
from .models import Games, Flags
from flask_login import login_required, current_user
from . import db
from werkzeug.utils import secure_filename


create = Blueprint('create', __name__)

def allowed_file(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in current_app.config["ALLOWED_FILE_EXTENSIONS"]:
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

@create.route('/create', methods=['POST'])
@login_required
def create_post():
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
    
    if not name or not description or not category or not difficulty:
        flash('Not enough general information provided.')
        return redirect(url_for('main.create'))

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
        elif (flag_hint or flag_points) and not flag:
            flash('Missing flags, try again.')
            return redirect(url_for('main.create'))

        else:
            flag_num += 1
    
    if request.files:
        filename = upload_file()
        if not filename:
            flash('Error with upload.')
            return redirect(url_for('main.create'))

    new_game = Games(name=name, category=category,
                     difficulty=difficulty, url=filename, user_id=current_user.id)
    
    file = request.files["file"]
    file.save(os.path.join(current_app.config["FILE_UPLOADS"], filename))
    
    # add the new game and flags to db
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('main.create'))