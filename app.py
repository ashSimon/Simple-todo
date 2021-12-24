from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    # show all todos
    return render_template('home.html')


@app.route('/todo')
def todo():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('Todos.html', todo_list=todo_list)


@app.route('/add', methods=['POST'])
def add():
    # add new item
    title = request.form.get('title')
    name = request.form.get('name')
    new_todo = Todo(title=title, name=name, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('todo'))


# update
@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('todo'))


# delete
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo_delete = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo_delete)
    db.session.commit()
    return redirect(url_for('todo'))


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()
