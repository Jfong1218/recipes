from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE 
from flask import flash
from flask_app.models import user_model

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.time = data['time']
        self.instructions = data['instructions']
        self.date = data['date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (title, description, time, instructions, date, user_id) VALUES (%(title)s, %(description)s, %(time)s, %(instructions)s, %(date)s,%(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET title = %(title)s, description = %(description)s, time = %(time)s, instructions = %(instructions)s, date = %(date)s WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod #might need explination
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users on users.id = recipes.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_recipes = []
            for row in results:
                this_recipe = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.planner = this_user
                all_recipes.append(this_recipe)
            return all_recipes
        return results

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users on users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        row = results[0]
        this_recipe = cls(row)
        user_data = {
            **row,
            'id': row['users.id'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }   
        planner = user_model.User(user_data)
        this_recipe.planner = planner
        return this_recipe

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['title']) <1:
            flash("Title requeired")
            is_valid = False
        if len(form_data['description']) <1:
            flash("Description required")
            is_valid = False
        if len(form_data['instructions']) <1:
            flash("Instructions required")
            is_valid = False
        if "date" not in form_data:
            flash("Date required")
            is_valid = False
        if "time" not in form_data:
            flash("Please select if Recipe can be done in less than 30 minutes")
            is_valid = False
        return is_valid

