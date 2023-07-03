with open('website/books/french_recipes.txt', 'r') as file:
    text = file.readlines()
    print(text[:10])