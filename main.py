from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

ptasks = []

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        ptask = request.form['task']
        ptasks.append(ptask)

    return render_template('todo.html', title = "Get It Done!", tasks = ptasks)


app.run()