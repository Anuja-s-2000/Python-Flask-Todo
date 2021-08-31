from flask import Flask,render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
global stodo

class Users(db.Model):
    __table_args__ = (db.UniqueConstraint('username'), )
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

@app.route("/", methods=['POST', 'GET'])
def home():
    """u = Users.query.all()
    for u1 in u:
        print(u1.username,u1.password)"""

    if request.method == 'POST':
        try:
            userName = request.form['signcontent']
            password = request.form['signpass']
            if len(userName)!=0 and len(password)!=0:
                new_User= Users(username=userName,password=password)
                try:
                    db.session.add(new_User)
                    db.session.commit()
                    return redirect('/'+str(new_User.id))
                except:
                    return 'There was an issue creating user, try another username'
        except:
            userName = request.form['content']
            passWord = request.form['pass']
            new_User= Users(username=userName,password=passWord)
            users = Users.query.filter_by(username=userName).first()
            if users is not None and users.password==passWord:
                return redirect('/'+str(users.id))
        return redirect('/')
    else:
        return render_template('login.html')


@app.route('/<string:id>', methods=['GET'])
def index(id):
    try:
        todo_list = Todo.query.filter_by(user_id=id).all()
        user= Users.query.filter_by(id=id).first()
        return render_template('todo.html', todo_list=todo_list, user_id=id,user_name=user.username)
    except:
        return redirect('/')   

@app.route("/search/<string:id>", methods=["POST"])
def search(id):
    try:
        user= Users.query.filter_by(id=id).first()
        title = request.form.get("title")
        stodo = Todo.query.filter_by(user_id=id).filter_by(title=title).first()
        print(stodo.id)
        return render_template("search-todo.html", stodo=stodo,user_id=id,user_name=user.username)
    except:
        return redirect('/'+str(id))   

@app.route("/add/<string:id>", methods=["POST"])
def add(id):
    
    title = request.form.get("title")
    if title:    
        new_todo = Todo(user_id=id,title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/'+str(id))
    else:
        return redirect('/'+str(id))    

@app.route("/update/<string:id>/<int:todo_id>")
def update(id,todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect('/'+str(id))

@app.route("/delete/<string:id>/<int:todo_id>")
def delete(id,todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/'+str(id))   

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)