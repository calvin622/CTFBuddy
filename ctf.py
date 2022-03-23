from email import message
from .models import User, Flags, Games, UserGameStatus
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from . import db
#from sqlalchemy import or_

ctf = Blueprint('ctf', __name__)


@ctf.route("/play/<string:games_name>", methods=["POST", "GET"])
@login_required
def play(games_name):
    self_redirect = "ctf.play"
    game_details = Games.query.filter_by(
        name=games_name, user_id=current_user.id).first()

    if not game_details: #check game exists
        return redirect(url_for("main.gameselect"))
    
    
    game_save = UserGameStatus.query.filter_by(
        games_name=games_name, user_id=current_user.id).first()

    games_save_flags = UserGameStatus.query.with_entities(UserGameStatus.flag1_status, UserGameStatus.flag2_status, UserGameStatus.flag3_status, UserGameStatus.flag4_status, UserGameStatus.flag5_status, UserGameStatus.flag6_status,
                                                     UserGameStatus.flag7_status, UserGameStatus.flag8_status, UserGameStatus.flag9_status, UserGameStatus.flag10_status).filter_by(user_id=current_user.id, games_name=games_name).first()
    
    used_hints = UserGameStatus.query.with_entities(UserGameStatus.hint1_status, UserGameStatus.hint2_status, UserGameStatus.hint3_status, UserGameStatus.hint4_status, UserGameStatus.hint5_status, UserGameStatus.hint6_status,
                                                     UserGameStatus.hint7_status, UserGameStatus.hint8_status, UserGameStatus.hint9_status, UserGameStatus.hint10_status).filter_by(user_id=current_user.id, games_name=games_name).first()

    if not game_save: #check if user has a valid game save
        session["message"] = game_details.description
        new_save = UserGameStatus(
            status="Started", user_id=current_user.id, games_name=games_name)
        db.session.add(new_save)
        db.session.commit()
        return redirect(url_for(self_redirect, games_name=games_name))

    correct_flags = 0
    found_flag_strings = []
    used_hints_strings = []
    flags = Flags.query.filter_by(games_name=games_name)

    if games_save_flags:
        for flag in games_save_flags:
            if flag != None:
                found_flag_strings.append(flag)
                correct_flags += 1
    else: #error
        return redirect(url_for("main.gameselect"))
    if used_hints:
        for hint in used_hints:
            if hint != None:
                used_hints_strings.append(hint)
    else: #error
        return redirect(url_for("main.gameselect"))

    if flags.count() == correct_flags:
        session["message"] = "You have found all the flags!"
        game_save.status = "Completed"
        db.session.commit()

    flagshints = Flags.query.filter(Flags.flag.notin_(
        found_flag_strings)).filter_by(games_name=games_name).first()
    if flagshints:
        hint_cost = flagshints.hint_cost
    else:
        hint_cost = 0

    if "current_game" in session:
        if session["current_game"] != games_name: #check if an old save has been loaded
            session["message"] = game_details.description #different game has been loaded
            session["current_game"] = games_name
            if "hint" in session:
                session.pop("hint", None)
            if "video" in session:
                session.pop("video", None)
            if game_save.video_status != None:
                    session["video"] = game_details.video_url
                
    else: # no session details, reload game message
        session["message"] = game_details.description
        session["current_game"] = games_name
        if "hint" in session:
                session.pop("hint", None)
        if "video" in session:
                session.pop("video", None)
        if game_save.video_status != None:
                    session["video"] = game_details.video_url

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
                if game_save.flag1_status == None and correct_flag.flag_num == 0:
                    game_save.flag1_status = submitted_flag
                elif game_save.flag2_status == None and correct_flag.flag_num == 1:
                    game_save.flag2_status = submitted_flag
                elif game_save.flag3_status == None and correct_flag.flag_num == 2:
                    game_save.flag3_status = submitted_flag
                elif game_save.flag4_status == None and correct_flag.flag_num == 3:
                    game_save.flag4_status = submitted_flag
                elif game_save.flag5_status == None and correct_flag.flag_num == 4:
                    game_save.flag5_status = submitted_flag
                elif game_save.flag6_status == None and correct_flag.flag_num == 5:
                    game_save.flag6_status = submitted_flag
                elif game_save.flag7_status == None and correct_flag.flag_num == 6:
                    game_save.flag7_status = submitted_flag
                elif game_save.flag8_status == None and correct_flag.flag_num == 7:
                    game_save.flag8_status = submitted_flag
                elif game_save.flag9_status == None and correct_flag.flag_num == 8:
                    game_save.flag9_status = submitted_flag
                elif game_save.flag10_status == None and correct_flag.flag_num == 9:
                    game_save.flag10_status = submitted_flag
                current_user.points += correct_flag.points
                db.session.commit()
                return redirect(url_for(self_redirect, games_name=games_name))

            else:
                session["message"] = "incorrect flag!"
                return redirect(url_for(self_redirect, games_name=games_name))
        elif request.form["btn_identifier"] == "hint_id_identifier":
            if flagshints:
                if "hint" not in session:
                    session["hint"] = ""
                if "hint" in session:
                    if session["hint"] != flagshints.hint:
                        if current_user.points >= flagshints.hint_cost:
                            current_user.points -= flagshints.hint_cost
                            session["message"] = session["hint"] = flagshints.hint
                            db.session.commit()
                        else:
                            session["message"] = "You dont have enough points!"
                    elif session["hint"] == flagshints.hint:
                        session["message"] = "You already have a hint: " + \
                            session["hint"]
                    else:
                        session["message"] = "Sorry, Theres no hint."
            return redirect(url_for(self_redirect, games_name=games_name))

        elif request.form["btn_identifier"] == "video_id_identifier":

            if "video" not in session:
                session["video"] = ""
            if "video" in session:
                if session["video"] != game_details.video_url and game_save.video_status == None:
                    if current_user.points >= game_details.video_cost:
                        current_user.points -= game_details.video_cost
                        session["video"] = game_details.video_url
                        game_save.video_status = game_details.video_url
                        db.session.commit()
                    else:
                        session["message"] = "You dont have enough points!"
                elif session["video"] == game_details.video_url or game_save.video_status != None:
                    session["video"] = game_details.video_url
                    session["message"] = "You already have a video: " + \
                        session["video"]
                else:
                    session["message"] = "Sorry, Theres no video."

            
            return redirect(url_for(self_redirect, games_name=games_name))

        elif request.form["btn_identifier"] == "reset_id_identifier":
            UserGameStatus.query.filter_by(
                games_name=games_name, user_id=current_user.id).delete()
            db.session.commit()
            session.pop("message", None)
            session.pop("video", None)
            session.pop("hint", None)
            return redirect(url_for(self_redirect, games_name=games_name))
        else:
            return redirect(url_for(self_redirect, games_name=games_name))
    
    if "video" in session:
        return render_template("play.html", mess=session["message"], flags=correct_flags, no_flags=flags.count(), hint_cost=hint_cost, download=game_details.url, video=session["video"])
    else:
        return render_template("play.html", mess=session["message"], flags=correct_flags, no_flags=flags.count(), hint_cost=hint_cost, download=game_details.url)
