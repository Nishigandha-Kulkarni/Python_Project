import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "playerdatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class player(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def __repr__(self):
        return "<Name: {}>".format(self.name)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        player = player(name=request.form.get("name"))
        db.session.add(player)
        db.session.commit()
    players = player.query.all()
    return render_template("home.html", players=players)


@app.route("/update", methods=["GET", "POST"])
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    player = player.query.filter_by(name=oldname).first()
    player.name = newname
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    player = player.query.filter_by(name=name).first()
    db.session.delete(player)
    db.session.commit()
    return redirect("/")