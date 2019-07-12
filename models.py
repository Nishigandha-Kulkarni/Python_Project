from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scrapper import Players
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
print(db.Model.metadata.tables)
from flask import render_template


@app.route("/", methods=["GET" , "POST"])
def home():
    rows=db.session.query(Players).all()
    return render_template("home.html", players=rows[:50])
    


if __name__ == "__main__":
    app.run(debug=True)    