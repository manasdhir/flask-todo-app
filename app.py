from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    #return 'Hello, World!'
    if(request.method=="POST"):
        #print(request.form['title'])
        tit=request.form['title']
        des=request.form['desc']
        TODO=Todo(title=tit,desc=des)
        db.session.add(TODO)
        db.session.commit()
    all=Todo.query.all()
    return render_template('index.html',alltodo=all)
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        tit=request.form['title']
        des=request.form['desc']
        TODO=Todo.query.filter_by(sno=sno).first()
        TODO.title=tit
        TODO.desc=des
        db.session.add(TODO)
        db.session.commit()
        return redirect("/")
        


    updtodo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=updtodo)
@app.route('/delete/<int:sno>')
def dele(sno):
    print(sno)
    deltodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(deltodo)
    db.session.commit()
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True,port=8000)