from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:launchcodelc101@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = "k3nje9J3saY"

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, name, owner):
        self.name = name
        self.completed = False
        self.owner = owner

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))

    tasks =  db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        user = User.query.filter_by(email=user_email).first()

        if not user_email.strip():
            flash('Username cannot be empty', category='error_email')
            return redirect('/')

        elif not user_password.strip():
            flash('Password cannot be empty', category='error_password')
            return redirect('/')

        elif not user:
            flash('User does not exits. Please check the user name or regiter new.', category='error_email')
            return redirect('/')

        elif user.password != user_password:
            flash('Password is incorrect.', category='error_password')
            return redirect('/')

        else:
            session['email'] = user_email
            flash('Logging successful.', category='success')
            return redirect('/')

    return render_template("login.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']
        user_verify_pwd = request.form['verify']

        existing_user = User.query.filter_by(email=user_email).first()

        if not user_email.strip():
            flash("Email cannot be empty", category='email_error')
            redirect("/register")
        elif not user_password.strip():
            flash("password cannot be empty", category="password_error")
            redirect("/register")

        elif user_password.isspace():
            flash("Password cannot have space", category='password_error')
            redirect("/register")

        elif user_password != user_verify_pwd:
            flash("Passwords don't match.", category='verify_password_error')
            redirect("/register")

        elif not existing_user:
            new_user = User(user_email, user_password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = user_email

            return redirect("/")

        else:
            flash("Duplicate User.", category="email_error")

    return render_template("register.html")

@app.route('/', methods=['POST', 'GET'])
def index():
    this_owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        task_name = request.form['task']
        if task_name.strip():
            new_task = Task(task_name, this_owner)
            db.session.add(new_task)
            db.session.commit()

    pcompleted = Task.query.filter_by(completed = True, owner=this_owner).all()
    ptasks = Task.query.filter_by(completed=False, owner=this_owner).all()

    return render_template('todo.html', title = "Get It Done!", tasks = ptasks, completed_task = pcompleted)

@app.route('/delete-task', methods=['POST'])
def delete_task():
    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)

    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

@app.route('/add-back', methods=['POST'])
def add_back_task():
    task_id = int(request.form['add-back-task'])
    task = Task.query.get(task_id)

    task.completed = False
    db.session.add(task)
    db.session.commit()

    return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    del session['email']
    return redirect('/')

if __name__ == '__main__':
    app.run()   