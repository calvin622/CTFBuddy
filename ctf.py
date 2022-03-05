from email import message
from .models import User, Flags, Games, UserGameStatus
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from . import db
from sqlalchemy import or_

ctf = Blueprint('ctf', __name__)


@ctf.route("/play/<string:games_name>", methods=["POST", "GET"])
@login_required
def play(games_name):
    self_redirect = "ctf.play"
    game = UserGameStatus.query.filter_by(
        games_name=games_name, user_id=current_user.id).first()

    games_saves = UserGameStatus.query.with_entities(UserGameStatus.flag1_status, UserGameStatus.flag2_status, UserGameStatus.flag3_status, UserGameStatus.flag4_status, UserGameStatus.flag5_status, UserGameStatus.flag6_status,
                                                     UserGameStatus.flag7_status, UserGameStatus.flag8_status, UserGameStatus.flag9_status, UserGameStatus.flag10_status).filter_by(user_id=current_user.id, games_name=games_name).first()

    if not game:
        session["message"] = "Welcome"
        new_save = UserGameStatus(
            status="Started", user_id=current_user.id, games_name=games_name)
        db.session.add(new_save)
        db.session.commit()
        return redirect(url_for(self_redirect, games_name=games_name))


    correct_flags = 0
    found_flag_strings = []
    not_found_flags = []

    if games_saves:
        for flags in games_saves:
            if flags != None:
                found_flag_strings.append(flags)
                correct_flags += 1
            
    flags = Flags.query.filter_by(games_name=games_name)
    if flags.count() == correct_flags:
        session["message"] = "You have found all the flags!"
        game.status = "Completed"
        db.session.commit()

    session.permanent = True
    if request.method == "POST":
        if request.form["btn_identifier"] == "flag_id_identifier":
            submitted_flag = request.form["flag"]
            correct_flag = Flags.query.filter_by(
                games_name=games_name, flag=submitted_flag).first()

            if submitted_flag in (found_flag_strings):
                session["message"] = "You have already submitted that flag!"
                return redirect(url_for(self_redirect, games_name=games_name))
            elif correct_flag:  # and not already in games saves
                session["message"] = "Correct!"
                # protoype code
                if game.flag1_status == None and correct_flag.flag_num == 0:
                    game.flag1_status = submitted_flag
                elif game.flag2_status == None and correct_flag.flag_num == 1:
                    game.flag2_status = submitted_flag
                elif game.flag3_status == None and correct_flag.flag_num == 2:
                    game.flag3_status = submitted_flag
                elif game.flag4_status == None and correct_flag.flag_num == 3:
                    game.flag4_status = submitted_flag
                elif game.flag5_status == None and correct_flag.flag_num == 4:
                    game.flag5_status = submitted_flag
                elif game.flag6_status == None and correct_flag.flag_num == 5:
                    game.flag6_status = submitted_flag
                elif game.flag7_status == None and correct_flag.flag_num == 6:
                    game.flag7_status = submitted_flag
                elif game.flag8_status == None and correct_flag.flag_num == 7:
                    game.flag8_status = submitted_flag
                elif game.flag9_status == None and correct_flag.flag_num == 8:
                    game.flag9_status = submitted_flag
                elif game.flag10_status == None and correct_flag.flag_num == 9:
                    game.flag10_status = submitted_flag
                #User.query.filter_by(id=current_user.id).update({User.points: + 10})
                current_user.points += correct_flag.points
                db.session.commit()
                return redirect(url_for(self_redirect, games_name=games_name))

            else:
                session["message"] = "incorrect flag!"
                return redirect(url_for(self_redirect, games_name=games_name))
        elif request.form["btn_identifier"] == "hint_id_identifier":
            session["message"] = session["hint"] = ""
            return redirect(url_for(self_redirect, games_name=games_name))

        elif request.form["btn_identifier"] == "reset_id_identifier":
            UserGameStatus.query.filter_by(
                games_name=games_name, user_id=current_user.id).delete()
            db.session.commit()
            return redirect(url_for(self_redirect, games_name=games_name))
        else:
            return redirect(url_for(self_redirect, games_name=games_name))

    return render_template("play.html", mess=session["message"], flags=correct_flags)
