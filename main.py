from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__) #pass the Flask library to our variable 'app'

# Linking to an actual database
app.config["SQLALCHEMY_DATABASE_URI"] =  'sqlite:///recipes.db' #where the database is stored
db = SQLAlchemy(app) #call SQLAlchemy - link the application and database together
migrate = Migrate(app, db) #use migration to implement changes in SQLAlchemy model to the actual database

# Create some manual data instead of linking to an actual database
#all_recipes = [
#    {"title": "Recipe 1", "description": "Some ingredients for 1 recipe", "author": "Joey"}, 
#    {"title": "Recipe 2", "description": "Some ingredients for 2 recipe", "author": ""}
#]

@app.route("/recipes/", methods=["GET","POST"])
def recipes():
    # Implement functionality to receive information from website user
    if request.method == "POST": # if someone has added a new recipe
        recipe_title=request.form["title"]
        recipe_description=request.form["description"]
        new_recipe = Recipe(title=recipe_title,description=recipe_description,author="Joey")
        db.session.add(new_recipe)
        db.session.commit()
        return redirect("/recipes/") # refresh the page
    else: # request is GET
        all_recipes = Recipe.query.all() # print a list of all recipes
        return render_template("recipes.html", recipes=all_recipes)
    
# Define a new route for deleting recipes
@app.route("/recipes/delete/<int:id>/")
def delete(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect("/recipes/")

# Define a new route for editing recipes
@app.route("/recipes/edit/<int:id>/", methods=["GET","POST"])
def edit(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == "POST": # if someone is editing the recipe
        recipe.title=request.form["title"] # overwrite
        recipe.description=request.form["description"] # overwrite
        db.session.commit()
        return redirect("/recipes") # refresh the page
    else: # What happens when you click on the EDIT button
        return render_template("edit.html", recipe=recipe)

# Instead of using manual recipe data, we're going to define a model
# that describes the structures of recipe data in our database 'db'
# We'll inherit our model from db.Model
class Recipe(db.Model): 
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False, unique=True) 
    description = db.Column(db.Text, nullable=False) 
    author = db.Column(db.String(50), nullable=False) 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #automatically adds the date

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