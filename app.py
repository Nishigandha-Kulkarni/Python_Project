from flask import Flask,send_file
from flask_sqlalchemy import SQLAlchemy
from model import Players
from flask import request
from flask import redirect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
print(db.Model.metadata.tables)
from flask import render_template
from io import  BytesIO
import json

@app.route("/", methods=["GET" , "POST"])
def home():
    name=request.form.get("name",None)
    height=request.form.get("height",None)
    weight=request.form.get("weight",None)
    if not name is None:
        value=request.form.get("search","")
        rows=list(db.session.query(Players).filter(Players.name.like("%"+value+"%")))
        print(rows)
        return render_template("home.html", players=rows[:50],search_term="name",search_value=name)

    elif not height is None:  
        print("heght")
        value=request.form.get("search",0)   
        rows=list(db.session.query(Players).filter(Players.height >=int(value)))
        
        return render_template("home.html", players=rows[:50],search_term="height",search_value=int(value))
    elif not weight is None:
        value=request.form.get("search",0)
        rows=list(db.session.query(Players).filter(Players.weight >=int(value)))
        return render_template("home.html", players=rows[:50],search_term="weight",search_value=int(value))
    else:
        rows=db.session.query(Players).all()
        return render_template("home.html",search_term="None",players=rows[:50])

@app.route("/update", methods=["GET", "POST"])
def update():
    print(request.method)
    if request.method=="GET":
        id = request.args.get("player_id")
        player = db.session.query(Players).filter_by(id=id).first()
        return render_template("update.html",player=player)
    elif request.method=="POST":
        id = request.form.get("player_id")    
        print(id)
        try:
            player = db.session.query(Players).filter_by(id=id).first()
            player.name=request.form.get("player_name")
            player.place=request.form.get("player_place")
            player.position=request.form.get("player_position")
            player.height=int(request.form.get("player_height"))
            player.weight=int(request.form.get("player_weight"))
            player.dob=request.form.get("player_dob")
            db.session.commit()
        except:
            pass
        return redirect("/")        
        
        
        


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("player_id")
    player = db.session.query(Players).filter_by(id=id).first()
    db.session.delete(player)
    db.session.commit()
    return redirect("/")    

@app.route("/more", methods=["GET"])
def more():
    id = request.args.get("player_id")
    player = db.session.query(Players).filter_by(id=id).first()
    return render_template("player.html",player=player)    

@app.route("/csv",methods=["POST"])
def download_csv():
    print("csv")
    value=None
    qtype=request.form.get("search_term",None)
    print(qtype)
    if not qtype is None: 
        value=request.form.get("search_value",0)
        if qtype=="name":
            rows=db.session.query(Players).filter(Players.name.like("%"+value+"%"))
        if qtype=="height":
            rows=list(db.session.query(Players).filter(Players.height >=int(value)))
                    
        if qtype=="weight":
            rows=list(db.session.query(Players).filter(Players.weight >=int(value)))
    else:
        rows=db.session.query(Players).all()        

    csv=[]
    for row in rows[:50]:
        csv.append(",".join(["\""+row.name+"\"","\""+row.dob+"\"",str(row.height),str(row.weight),"\""+str(row.position)+"\"","\""+str(row.place)+"\""]))
    csv="\n".join(csv)
    print(csv)
    with open(str(qtype)+str(value)+".csv","w",encoding="utf-8") as f:
        f.write(csv)
    output=BytesIO(csv.encode("utf-8"))
    
    return send_file(output,as_attachment=True,mimetype="text/plain",attachment_filename="players.csv")


@app.route("/json",methods=["POST"])
def download_json():
    print("json")
    
    value=None
    qtype=request.form.get("search_term",None)
    print(qtype)
    if not qtype is None: 
        value=request.form.get("search_value",0)
        if qtype=="name":
            rows=db.session.query(Players).filter(Players.name.like("%"+value+"%"))
        if qtype=="height":
            rows=list(db.session.query(Players).filter(Players.height >=int(value)))
                    
        if qtype=="weight":
            rows=list(db.session.query(Players).filter(Players.weight >=int(value)))
    else:
        rows=db.session.query(Players).all()        
    
    csv=[]
    for row in rows[:50]:
        csv.append(row.as_dict())
    csv=json.dumps(csv)
    with open(str(qtype)+str(value)+".json","w",encoding="utf-8") as f:
        f.write(csv)
    
    output=BytesIO(csv.encode("utf-8"))
    
    return send_file(output,as_attachment=True,mimetype="text/plain",attachment_filename="players.json")


if __name__ == "__main__":
    app.run(debug=True)    