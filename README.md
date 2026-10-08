The Xtreme Pizza Challenge!
The Big Picture 
Think of the project as 4 puzzle pieces that plug into each other:
Plaintext
[Person 1: Dough & Crust] ──┐
                            ├──> [Person 3: The Pizza Itself] ──> [Person 4: Price & Receipt]
[Person 2: The Toppings]  ──┘

Everyone can name their internal helper variables whatever feels natural, as long as the guidelines are respected:
snake_case for functions and variables.
PascalCase for classes.
UPPER_SNAKE_CASE for fixed constants (like base prices).
Add type hints (name: str, price: float).
Use your commit format (<ISSUE-ID> <type>: <description>).

Commits med ID: HU-85







Team Roles & Tasks
Person 1: Dough, Crust & Custom Errors
Issue ID: PZ-101 | Branch: PZ-101-crust-setup
What to build:
A Crust object: Represents the base of the pizza.
Needs a size (e.g., Small, Medium, Large).
Needs a crust style (e.g., Thin, Thick, Cheese-stuffed).
Custom error classes: Create a couple of clear exceptions your teammates can raise later:
One for when someone tries to add the exact same topping twice.
One for when someone tries to pile on too many toppings (e.g., more than 6).
Sample Commit: PZ-101 feat: add crust options and custom errors













Person 2: The Toppings
Issue ID: PZ-102 | Branch: PZ-102-toppings
What to build:
A Topping object: Represents an ingredient that goes on the pizza.
Needs a name (str, like "Mushrooms" or "Pepperoni").
Needs a group or category (e.g., Meat, Veggie, Cheese).
Needs an extra price (float, like 1.50).
Basic validation:
Prevent someone from setting a negative price (raise a ValueError if price < 0).
Sample Commit: PZ-102 feat: add topping model with price validation













Person 3: The Pizza Assembler
Issue ID: PZ-103 | Branch: PZ-103-pizza-class (Wait for Person 1 and 2 to finish, or agree on the names of their classes first)
What to build:
A Pizza object: Brings the crust and toppings together.
Needs a name (e.g., "Friday Special").
Takes in a Crust from Person 1.
Holds a list of Toppings from Person 2 (starts empty).
Methods to write:
An add_topping(...) method that appends an ingredient.
If that topping is already on the pizza, raise Person 1's duplicate error.
If the pizza already has too many toppings, raise Person 1's max-toppings error.
A helper method (like is_vegetarian()) that checks if any meat toppings were added.
Sample Commit: PZ-103 feat: assemble pizza and check for duplicates











Person 4: The Register (Pricing & Discounts)
Issue ID: PZ-104 | Branch: PZ-104-pricing (Needs Person 3's Pizza object)
What to build:
Base Prices: Set fixed prices at the top of your file for sizes (e.g., Small = $8, Medium = $10, Large = 12)andanyextrachargeforstuffedcrust(e.g.,+2).
A Total Calculator function: Takes a finished Pizza and returns the final cost.
Add the base price + crust extra + every topping's price.
Discount rule: If a pizza has 4 or more toppings, give a small discount (e.g., 10% off the toppings).
Sample Commit: PZ-104 feat: calculate pizza total with combo discount











Final 30 Minutes: Put It Together & Test
Once everyone merges their branch into main, test your code together using pytest:
Test the pizza building:
Can you add 3 different toppings without errors?
Does adding "Mushrooms" twice correctly trigger your duplicate error?
Test the math:
Does a Medium thin-crust cheese pizza cost exactly what you expect?
Does adding 4 toppings trigger the discount?

