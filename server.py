from flask_app import app
from flask_app.controllers import recipes_controller, users_controller
#change import file name when reusing this file


if __name__ == "__main__":
    app.run(debug=True)
    #add in a custom port if defult port = 5000 doesn't work
    