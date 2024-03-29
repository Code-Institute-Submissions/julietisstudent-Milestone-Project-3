import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'Recipe_Cookbook'
app.config["MONGO_URI"] = 'mongodb+srv://Julietisstudent:Julietisstudent@recipecookbook-qpag8.mongodb.net/Recipe_Cookbook?retryWrites=true'

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.Recipes.find())
    
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
    RecipeCategories=mongo.db.RecipeCategories.find())
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.Recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    _recipe = mongo.db.Recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.RecipeCategories.find()
    return render_template('editrecipe.html', recipe =_recipe, RecipeCategories = all_categories)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.Recipes
    recipes.update( {"_id": ObjectId(recipe_id)},
    {
        'recipe_category':request.form.get('recipe_category'),
        'recipe_name':request.form.get('recipe_name'),
        'recipe_ingredients':request.form.get('recipe_ingredients'),
        'recipe_method':request.form.get('recipe_method'),
        'recipe_prep_and_cook_time':request.form.get('recipe_prep_and_cook_time'),
        'cuisine':request.form.get('cuisine'),
    })
    return redirect(url_for('get_recipes'))
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.Recipes.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))
    
@app.route('/get_categories')
def get_categories():
    _categories = mongo.db.RecipeCategories.find()
    category_list = [category for category in _categories]
    return render_template('categories.html', categories = category_list)
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.RecipeCategories.find_one({'_id': ObjectId(category_id)}))
    
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.RecipeCategories.update(
        {'_id': ObjectId(category_id)},
        {'recipe_category': request.form.get('recipe_category')})
    return redirect(url_for('get_categories'))
    
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.RecipeCategories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))
    
@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.RecipeCategories
    category_doc = {'recipe_category': request.form.get('recipe_category')}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    
@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)