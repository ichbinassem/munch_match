from app.extensions import db
from app.models.type import Type
from app.models.meal import Meal
from uuid import uuid4
import random
import requests
import urllib.parse


# Creating a function that will add types for food if it's empty
def add_types():
    if not Type.query.first():
        italian = Type(uuid=str(uuid4()), name="Italian")
        db.session.add(italian)
        chinese = Type(uuid=str(uuid4()), name="Chinese")
        db.session.add(chinese)
        mexican = Type(uuid=str(uuid4()), name="Mexican")
        db.session.add(mexican)
        japanese = Type(uuid=str(uuid4()), name="Japanese")
        db.session.add(japanese)
        indian = Type(uuid=str(uuid4()), name="Indian")
        db.session.add(indian)
        american = Type(uuid=str(uuid4()), name="American")
        db.session.add(american)
        french = Type(uuid=str(uuid4()), name="French")
        db.session.add(french)
        thai = Type(uuid=str(uuid4()), name="Thai")
        db.session.add(thai)
        spanish = Type(uuid=str(uuid4()), name="Spanish")
        db.session.add(spanish)
        greek = Type(uuid=str(uuid4()), name="Greek")
        db.session.add(greek)
        korean = Type(uuid=str(uuid4()), name="Korean")
        db.session.add(korean)
        turkish = Type(uuid=str(uuid4()), name="Turkish")
        db.session.add(turkish)
        brazilian = Type(uuid=str(uuid4()), name="Brazilian")
        db.session.add(brazilian)
        other = Type(uuid=str(uuid4()), name="Other")
        db.session.add(other)
        db.session.commit()


dish_names = [
    "Spaghetti Carbonara",
    "Chicken Tikka Masala",
    "Pad Thai",
    "Sushi Rolls",
    "Hamburger",
    "Caesar Salad",
    "Pizza Margherita",
    "Beef Stroganoff",
    "Fish and Chips",
    "Taco Salad",
    "Miso Soup",
    "Pesto Pasta",
    "Beef and Broccoli Stir-Fry",
    "Grilled Cheese Sandwich",
    "Fried Rice",
    "Mac and Cheese",
    "Veggie Burger",
    "Chicken Caesar Wrap",
    "Meatball Sub",
    "Philly Cheesesteak",
]


def generate_dish():
    dish = {}
    dish["uuid"] = str(uuid4())
    dish["name"] = random.choice(dish_names)
    dish["price"] = random.randint(5, 30)
    # Get a random image from Unsplash
    query = urllib.parse.quote(dish["name"])
    response = requests.get(f"https://source.unsplash.com/random/800x600/?food,{query}")
    dish["picture"] = response.url
    dish["location"] = ""
    return dish


def generateInitialMeals(number_of_meals):
    if not Meal.query.first():
        for _ in range(number_of_meals):
            dish = generate_dish()
            meal = Meal(**dish)
            db.session.add(meal)
            db.session.commit()


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    add_types()
    generateInitialMeals()
