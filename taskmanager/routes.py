from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    # convert cursor object returned by query into python list
    # NB each element of list represents a row of fields of model
    # row fields are accessed via dot notation
    tasks = list(Task.query.all())

    # categories argument in render_template() is variable name passed to 
    # template. It is assigned to value of categories as defined above
    return render_template("tasks.html", tasks=tasks)


# display categories
@app.route("/categories")
def categories():
    # convert cursor object returned by query into python list
    # NB each element of list represents a row of fields of model
    # row fields are accessed via dot notation
    categories = list(Category.query.all())

    # categories argument in render_template() is variable name passed to 
    # template. It is assigned to value of categories as defined above
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        # create new row in Category table
        category = Category()
        category.category_name = request.form.get("category_name")
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    print(request.method)
    if request.method=="POST":
        category.category_name=request.form.get("category_name")
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>", methods=["GET"]) # id passed in url
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))

@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    # get all categories to allow selection in new task form
    categories = list(Category.query.all())
    if request.method == "POST":
        # create new row in Task table
        task = Task()
        # assign values from form to fields in new Task row (see models.py)
        task.id = request.form.get("task_id")
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = True if (request.form.get("is_urgent")) else False
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        # commit new row to db
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
        # if GET. Return categories to template for dropdown
    return render_template("add_task.html", categories=categories)

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    # get all categories to allow selection in new task form
    categories = list(Category.query.all())
    task = Task.query.get_or_404(task_id)
    if request.method=="POST":
        task.task_name=request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.due_date = request.form.get("due_date")
        task.is_urgent = True if (request.form.get("is_urgent")) else False
        task.category_id = request.form.get("category_id")
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit_task.html", task=task, categories=categories)

# delete task. GET only; no template
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))