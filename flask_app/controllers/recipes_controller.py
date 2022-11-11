from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


@app.route('/recipes/new')
def new_recipe_form():
    if not 'user_id' in session:
        return redirect("/")
    user = User.get_by_id({"id": session['user_id']})
    return render_template('recipe_new.html', user=user)

@app.route("/recipes/create", methods=['POST'])
def create_recipe():
    if not 'user_id' in session:
        return redirect("/")
    if not Recipe.validator(request.form):
        return redirect("/recipes/new")
    print(request.form)
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create(data)
    return redirect("/welcome")

@app.route('/recipes/<int:id>/edit')
def edit_recipe_form(id):
    if not 'user_id' in session:
        return redirect("/")
    recipe = Recipe.get_by_id({"id": id})
    return render_template('recipe_edit.html', recipe = recipe)

@app.route("/recipes/<int:id>/update", methods=['POST'])
def update_recipe(id):
    if not 'user_id' in session:
        return redirect("/")
    if not Recipe.validator(request.form):
        return redirect(f"/recipes/{id}/edit")
    data = {
        **request.form,
        'id': id
    }
    Recipe.update(data)
    return redirect("/welcome")

@app.route("/recipes/<id>/delete")
def delete_recipe(id):
    if not "user_id" in session:
        return redirect(("/"))
    data = {
        "id": id
    }
    to_be_deleted = Recipe.get_by_id(data)
    #not on exam but good to know
    if not session['user_id'] == to_be_deleted.user_id:
        flash("Quit Trying to delete other people's stuff")
        return redirect('/')
    Recipe.delete(data)
    return redirect('/welcome')

@app.route("/recipes/<int:id>")
def show_one_recipe(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    recipe = Recipe.get_by_id(data)
    return render_template("recipe_one.html", recipe=recipe)