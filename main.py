from allrecipes import AllRecipes


"""
Outputs name, ingredients, directions, cooking time, ratings, and nutrients to file
"""


query_options = {
  "wt": "pork curry",         # Query keywords
  "ingIncl": "olives",        # 'Must be included' ingrdients (optional)
  "ingExcl": "onions salad",  # 'Must not be included' ingredients (optional)
  "sort": "re"                # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
}
query_result = AllRecipes.search(query_options)

#Just need to loop through the recipes and add them to a csv that downloads
#print(query_result[0:5])
main_recipe_url = query_result[18]['url']

hold = []
#print(query_result[0])
"""for i in range(len(query_result)):

    try:
        if query_result[i]['description']:
            hold.append(query_result[i])
    except:
        continue
print(len(query_result))
print(len(hold))"""



detailed_recipe = AllRecipes.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)
print(detailed_recipe['nutrients'])
# Display result :
"""print("%s" % detailed_recipe['name'])  # Name of the recipe
print(detailed_recipe['nutrients'])

for ingredient in detailed_recipe['ingredients']:  # List of ingredients
    #print("%s" % ingredient)
    pass

for step in detailed_recipe['steps']:  # List of cooking steps
    #print("%s" % step)
    pass"""

#print(detailed_recipe)  #need to send each recipe element to an interface such as ingredients and steps
