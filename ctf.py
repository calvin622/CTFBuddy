from .models import User
from .models import flags
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from . import db

ctf = Blueprint('ctf', __name__)

@ctf.route("/play", methods=["POST", "GET"])
def play():
    self_redirect = "ctf.play"
    session.permanent = True
    if "points" and "hint" and "submitted_flags" and "amount_of_flags" in session:
        if request.method == "POST":
            if request.form["btn_identifier"] == "flag_id_identifier":
                submitted_flag = request.form["flag"]
                correct_flag = flags.query.filter_by(flag=submitted_flag).first()
                
                if correct_flag and submitted_flag not in session["submitted_flags"]:
                    session["hint"] = correct_flag.help
                    session["points"] += correct_flag.points
                    session["submitted_flags"].append(submitted_flag)
                    session["amount_of_flags"] += 1
                    session["message"] = "Well done, that's correct!"
                    return redirect(url_for(self_redirect))
                    
                elif submitted_flag in session["submitted_flags"]:
                    session["message"] = "You have already submitted that flag!"
                    return redirect(url_for(self_redirect))
        
                else:
                    session["message"] = "incorrect flag!"
                    return redirect(url_for(self_redirect))
            elif request.form["btn_identifier"] == "hint_id_identifier":
                    session["message"] = session["hint"]
                    return redirect(url_for(self_redirect))
                
                
            elif request.form["btn_identifier"] == "reset_id_identifier":
                session.pop("submitted_flags", None)
                session.pop("points", None)
                session.pop("hint", None)
                session.pop("amount_of_flags", None)
                session.pop("message", None)
                return redirect(url_for(self_redirect))
            else:
                return redirect(url_for(self_redirect))
    else:
        session["points"] = 0
        session["submitted_flags"] = []
        session["hint"] = "Hint for first flag"
        session["amount_of_flags"] = 0
        session["message"] = "Lets begin the CTF, you should start with a system scan. If you need help, just click the 'I need Help' button bellow."
    return render_template("play.html", points=session["points"], flags=session["amount_of_flags"], mess=session["message"])