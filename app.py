from email import message
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.permanent_session_lifetime

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))

    def __init__(self, name, email):
        self.name = name
        self.email = email


class flags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(200))
    help = db.Column(db.String(200))
    points = db.Column(db.Integer)

    def __init__(self, flag, help, points):
        self.flag = flag
        self.help = help
        self.points = points


@app.route("/index")
@app.route("/")
def home():
    return render_template("index.html")

    
@app.route("/play-menu")
@app.route("/play-menu.html")
def base():
    return render_template("play-menu.html")


@app.route("/play", methods=["POST", "GET"])
def play():
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
                    return redirect(url_for("play"))
                    
                elif submitted_flag in session["submitted_flags"]:
                    session["message"] = "You have already submitted that flag!"
                    return redirect(url_for("play"))
        
                else:
                    session["message"] = "incorrect flag!"
                    return redirect(url_for("play"))
            elif request.form["btn_identifier"] == "hint_id_identifier":
                    session["message"] = session["hint"]
                    return redirect(url_for("play"))
                
                
            elif request.form["btn_identifier"] == "reset_id_identifier":
                session.pop("submitted_flags", None)
                session.pop("points", None)
                session.pop("hint", None)
                session.pop("amount_of_flags", None)
                session.pop("message", None)
                return redirect(url_for("play"))
            else:
                return redirect(url_for("play"))
    else:
        session["points"] = 0
        session["submitted_flags"] = []
        session["hint"] = "Hint for first flag"
        session["amount_of_flags"] = 0
        session["message"] = "Lets begin the CTF, you should start with a system scan. If you need help, just click the 'I need Help' button bellow."
    return render_template("play.html", points=session["points"], flags=session["amount_of_flags"], mess=session["message"])


@app.route("/view")
def view():
    return render_template("view.html", values=flags.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()  # or .all()
        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("login success")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("already logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("you are not logged in!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("you have been logged out")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
