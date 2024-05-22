from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__) #pass the Flask library to our variable 'app'

app.config["SQLALCHEMY_DATABASE_URI"] =  'sqlite:///recipes.db' #where the database is stored
db = SQLAlchemy(app) #call SQLAlchemy - link the application and database together
migrate = Migrate(app, db) #use migration to implement changes in SQLAlchemy model to the actual database

# Create some manual data instead of linking to an actual database
all_recipes = [
    {"title": "Recipe 1", "description": "Some ingredients for 1 recipe", "author": "Joey"}, 
    {"title": "Recipe 2", "description": "Some ingredients for 2 recipe", "author": ""}
]

@app.route("/recipes/")
def recipes():
    return render_template("recipes.html", recipes=all_recipes)

# Instead of using manual recipe data, we're going to define a model
# that describes the structures of recipe data in our database 'db'
# We'll inherit our model from db.Model
class Recipe(db.Model): 
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False, unique=True) 
    description = db.Column(db.Text, nullable=False) 
    author = db.Column(db.String(50)) 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Recipe" + str(self.id)

# Define a basic app decorator for the homepage
#@app.route("/")
#def hello():
#    return "Hello, world!"

# Define a personalised, dynamic app decorator
#@app.route("/home/<string:name>/") 
#def hello(name):
#    return f"Hello, {name}!"

# Define an app decorator that renders and displays an html template
@app.route("/home/") 
def home():
    return render_template("index.html")

# Run the app (using debugger mode)
if __name__ == "__main__":
    app.run(debug=True)