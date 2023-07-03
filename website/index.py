from flask import Blueprint, render_template, request, redirect,session
import random

import os

path1 = 'website/books/french_recipes.txt'  # Path to the directory or file

# Check if the path exists
if os.path.exists(path1):
    # Get the file permissions
    permissions = os.stat(path1).st_mode

    # Check if the path is a directory or file
    if os.path.isdir(path1):
        print(f"{path1} is a directory.")
    elif os.path.isfile(path1):
        print(f"{path1} is a file.")

    # Check the file permissions
    if permissions & 0o400:
        print("Read permission is granted.")
    else:
        print("Read permission is not granted.")

    if permissions & 0o200:
        print("Write permission is granted.")
    else:
        print("Write permission is not granted.")

    if permissions & 0o100:
        print("Execute permission is granted.")
    else:
        print("Execute permission is not granted.")
else:
    print(f"{path1} does not exist.")





#functions

def ls(path_book):
    with open(path_book, 'r') as file:
        text = file.read()
    text_copy = text
    #lines of text in list
    lines = text_copy.split('\n')
    return lines

#importing text file
def starts(lines, keyword, one_two):
    indexes_recipes = []
    for i in range(len(lines)):
        if keyword in lines[i]:
            indexes_recipes.append(i-one_two)
    return indexes_recipes

def devide_resepies(indexes_recipes, lines):
    recipes = {}
    #indexes of lines with titles
    for first in range(len(indexes_recipes)):
        recipe = ''
        #amount of lines
        for second in range(len(lines)):
            if first < len(indexes_recipes)-1:
                #adds only tht lines that are betwwen titles
                if second < indexes_recipes[first+1] and second >= indexes_recipes[first]:
                    r = lines[second] + '\n'
                    recipe += r
        
        index_name = indexes_recipes[first]
        recipes[lines[index_name].replace('\x0c', '')] = recipe.replace('\x0c', '')
    return recipes
    
def finded_recepies(command, recipes):
    #unwanted characters
    chars = '/\\?|:;.^#~`&*-+_><'

    #ditionary with number-name of recipe pairs.
    number_name = {}

    count = 0
    for i in chars:
        if i in command:
            return 'Wrong form! Please retype it.'
    
    if ',' in command.lower():
        ingredients = command.lower().split(',')
    else:
        ingredients = command.lower().split()
    
    if command != 'all':
        #loops for every ingredient
        for i in ingredients:
            for k,v in recipes.items():
                if i in v and k.replace('\x0c', '') not in number_name.values():
                    number_name[count] = k.replace('\x0c', '')
                    count+=1
                    
        #checks that dict i not empty
        if count > 0:
            return number_name
        #if it empty
        else:
            return f'\n Sorry we couldn\'t find {command} \n'
    else:
        for k,v in recipes.items():
            number_name[count] = k.replace('\x0c', '')
            count+=1
        return number_name

#main dictionary
keyword_dict = {'french_recipes.txt':['Ingredients', 1], 'indian_recipes.txt':['Total Time', 1], 'famouse_recipes.txt':['Ingredients', 1], 'chinise_recipes.txt':['', 0], 'usa_recipes.txt':['Yield', 1]}

french_recipes = devide_resepies(starts(ls('website/books/french_recipes.txt'), keyword_dict['french_recipes.txt'][0], keyword_dict['french_recipes.txt'][1]), ls('website/books/french_recipes.txt')) 
indian_recipes = devide_resepies(starts(ls('website/books/indian_recipes.txt'), keyword_dict['indian_recipes.txt'][0], keyword_dict['indian_recipes.txt'][1]), ls('website/books/indian_recipes.txt'))
famouse_recipes = devide_resepies(starts(ls('website/books/famouse_recipes.txt'), keyword_dict['famouse_recipes.txt'][0], keyword_dict['famouse_recipes.txt'][1]), ls('website/books/famouse_recipes.txt')) 
chinise_recipes = devide_resepies(starts(ls('website/books/chinise_recipes.txt'), keyword_dict['chinise_recipes.txt'][0], keyword_dict['chinise_recipes.txt'][1]), ls('website/books/chinise_recipes.txt'))
usa_recipes = devide_resepies(starts(ls('website/books/usa_recipes.txt'), keyword_dict['usa_recipes.txt'][0], keyword_dict['usa_recipes.txt'][1]), ls('website/books/usa_recipes.txt'))

justNames = {'french_recipes.txt':french_recipes, 'indian_recipes.txt':indian_recipes, 'famouse_recipes.txt':famouse_recipes, 'chinise_recipes.txt':chinise_recipes, 'usa_recipes.txt': usa_recipes}

books = ['french_recipes.txt', 'indian_recipes.txt', 'famouse_recipes.txt', 'chinise_recipes.txt', 'usa_recipes.txt']
books_names = [
    "\"Classic French Recipes\" by Heviz",
    "\"Indian Slow Cooker Cookbook\" by Myra Gupta",
    "\"Famous Recipes Book\" by Victoria Love",
    "\"A Main Taste of China\" by Ken Hom",
    "\"Healthy Eating on a Budget\" by United States Department of Agriculture"
]

books_all = {}

for i in range(len(books)):
    books_all[books[i]] = books_names[i]

index = Blueprint('index', __name__)


@index.route('/', methods=['POST', 'GET'])
def home():
    selected_recipe = request.form.get('name')
    print(selected_recipe)
    return render_template('home.html', books=books_all)

selected_book = ''
ingredients = ''

@index.route('/book', methods=['GET', 'POST'])
def book_details():
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        global selected_book
        if request.form.get('name') is not None:
            selected_book = request.form.get('name')
        
        print(ingredients)
        print(selected_book)
    else:
        if session.get('selected_book') is not None:
            selected_book = session.get('selected_book')
    
    
    return render_template('book.html', book=books_all.get(selected_book))

@index.route('/recipes', methods=['POST', 'GET'])
def find_recipes(): 
    ingredients = request.form.get('ingredients')
    print(ingredients)
    recipes = justNames[selected_book]
    try:
        found = list(finded_recepies(ingredients, recipes).values())
    except:
        found = finded_recepies(ingredients, recipes)
    print(found)
    selected_recipe = request.form.get('name')
    print(selected_recipe)
    if isinstance(found, str):
        return render_template('recipes.html', ing = None, error = found)
    else:
        return render_template('recipes.html', ing = found, error = None)
    
    
@index.route('/recipe', methods = ['POST', 'GET'])
def chosen_recipe():
    name = request.form.get('name')
    if name == 'random':
        text = justNames[selected_book][random.choice(list(justNames[selected_book].keys()))].split('\n')
    else:
        text = justNames[selected_book][name].split('\n')
    print(text)
    return render_template('recipe.html', text = text)