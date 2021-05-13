thetest = {
    'person_1': {
        'name': 'Zack',
        'favorite_foods': ['sushi', 'pizza', 'ice cream'],
        'friends': [
            {'Kot': {
                'age': 3,
                'color': 'grey',
                'height': 'like a foot',
                'favorite_foods': ['parmesian', 'avocados', 'cat food'],
            }},
            {'Jeff': {
                'last_name': 'Bezos',
                'color': 'white',
                'height': '5 10',
            }}
        ]
    },
}


# Your goal: Answer these questions

# What is Zack's 3rd favorite food?

zacks_3rd_favorite_food = thetest["person_1"]['favorite_foods'][2]

print(zacks_3rd_favorite_food)
# What is Zack's second friend's name?

zacks_2nd_frends_name = thetest["person_1"]['friends'][1]

# What is Zack's Kot's first favorite food?

kots_favorite_food = thetest["person_1"]['friends'][0]['Kot']['favorite_food'][0]

# Data Types
'strings'
1 # integer
1.0 # float
lists = []
dictionary = {'key': 'values'}
set = {'thing 1', 'thing 2', 'thing 3'}
tuple = ('thing 1', 'thing 2')
boolean = True # or False
None  # Nonetype
def func():
    print('hi')

type(func)  # Function
class MyClass:
    pass
type(MyClass) # Class