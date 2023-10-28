from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


@app.route("/")
def home():
    return render_template("tasks.html")

# display categories
@app.route("/categories")
def categories():
    # convert cursor object returned by query into python list
    # NB each element of list represents a row of fields of model
    #row fields are accessed via dot notation
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
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>", methods=["GET"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))