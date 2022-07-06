

from flask import Flask, redirect , render_template, request 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import desc
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

class Todo(db.Model): #database model
    sno = db.Column(db.Integer,primary_key=True) #columns of database
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route('/', methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form["desc"]

        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template("home.html" , allTodo=allTodo)

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "this is page"

@app.route('/update/<int:sno>', methods=["GET","POST"])
def Update(sno):
    if request.method=='POST':
        title=request.form["title"]
        desc=request.form["desc"]
        todo= Todo.query.filter_by(sno=sno).first()
        todo.title= title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo= Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)   



@app.route('/delete/<int:sno>')
def Delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")






if __name__ == "__main__":
    app.run(debug=True)    
