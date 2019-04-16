from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:launchcodelc101@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False


##ptasks = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        if task_name.strip():
            new_task = Task(task_name)
            db.session.add(new_task)
            db.session.commit()

    pcompleted = Task.query.filter_by(completed = True).all()
    ptasks = Task.query.filter_by(completed=False).all()

    return render_template('todo.html', title = "Get It Done!", tasks = ptasks, completed_task = pcompleted)

@app.route('/delete-task', methods=['POST'])
def delete_task():
    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)

    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()   