from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE 
from flask import flash
import re
from flask_app.models import recipe_model


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod 
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print (results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes on users.id = recipes.user_id WHERE users.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        list_of_recipes=[]
        for row in results:
            recipe_data = {
                **row,
                'id':row['recipes.id'],
                'created_at':row['recipes.created_at'],
                'updated_at':row['recipes.updated_at']
            }
            this_party = recipe_model.Recipe(recipe_data)
            list_of_recipes.append(this_party)
        user.parties = list_of_recipes
        return user

    @classmethod
    def get_id_by_email(cls, data):
        query = "SELECT id FROM user WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_password_by_id(cls, data):
        query = "SELECT password FROM user WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate(user_data):
        is_valid = True
        if len(user_data['first_name']) <2:
            flash("First name must be at least 2 characters","reg")
            is_valid = False
        if len(user_data['last_name']) <2:
            flash("Last name must be at least 2 characters","reg")
            is_valid = False
        if len(user_data['email']) <1:
            flash("Please provide email","reg")
            is_valid = False
        if len(user_data['password']) <1:
            flash("Please provide password","reg")
            is_valid = False
        elif len(user_data['password']) < 8:
            flash("Password must be at least 8 characters", "reg")
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']):
            is_valid = False
            flash('invalid email', "reg")
        else:
            potential_user = User.get_by_email({'email': user_data['email']})
            if potential_user: #if we have a user, don't let them register with this email since they exist already
                is_valid = False
                flash("Email already registered", "reg")
        # if len(user_data['password']) < 8:
        #     flash("Password must be at least 8 characters", "reg")
        #     is_valiid = False
        if not user_data['password'] == user_data['confirm_password']:
            flash("Passwords don't match", 'reg')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user_data):
        is_valid = True
        id = User.get_id_by_email(data)
        print(id) #can check from terminal
        if len(id) == 0:
            flash("email or password do not match records")
            is_valid = False
        else:
            data = {
                "id": User.get_id_by_email(data)[0]
            }
            password = User.get_password(data['id'])
            if not bcrypt.check_password_hash(password[0]['password'], data['password']):
                flash("email or password do not match records")
                is_valid = False
        return is_valid
