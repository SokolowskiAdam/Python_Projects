from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Date
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField, BooleanField
from wtforms.validators import DataRequired, URL
import os


# Flask config
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Task Table Configuration
class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(250), nullable=False)
    deadline: Mapped[str] = mapped_column(String(250))


with app.app_context():
    db.create_all()


# Flask form - add task
class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    status = SelectField(
        label="Status",
        choices=["New", "In Progress", "Done"],
        validators=[DataRequired()],
    )
    deadline = StringField("Deadline - format date YYYY-MM-DD")
    submit = SubmitField("Submit")


# -------- Flask Routes --------
@app.route("/")
def home():
    result = db.session.execute(db.select(Task).order_by(Task.status.desc()))
    all_tasks_db = result.scalars().all()

    return render_template("index.html", tasks=all_tasks_db)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        print("Success")
        new_task = Task(
            task=form.task.data,
            status=form.status.data,
            deadline=form.deadline.data,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html", form=form)


@app.route("/delete", methods=["GET"])
def delete_task():
    with app.app_context():
        task_id = request.args.get("id")

        # Delete record by ID
        movie_to_delete = db.get_or_404(Task, task_id)
        db.session.delete(movie_to_delete)
        db.session.commit()

    return redirect(url_for("home"))


@app.route("/finish", methods=["GET", "POST"])
def finish_task():
    task_id = request.args.get("id")
    task = db.get_or_404(Task, task_id)

    task.status = "Done"
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit-post/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    edit_form = TaskForm(
        task=task.task,
        status=task.status,
        deadline=task.deadline,
    )

    if edit_form.validate_on_submit():
        task.task = edit_form.task.data
        task.status = edit_form.status.data
        task.deadline = edit_form.deadline.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html", form=edit_form, is_edit=True)


if __name__ == "__main__":
    app.run(debug=True)
