toppings = ["Salami", "Mushrooms", "Ham", "Mozzarella", "Pineapple"]

class Topping:
    def __init__(self, item_name, item_category, item_price):
        self.name = item_name
        self.category = item_category
        self.price = item_price

    def getPrice(self):
        name: str = self.name
        match name:
            case "Salami":
                result = "12kr"
                self.setCategory("Meat")

            case "Mushrooms":
                result = "8kr"
                self.setCategory("Veggie")

            case "Ham":
                result = "14kr"
                self.setCategory("Meat")

            case "Mozzarella":
                result = "3kr"
                self.setCategory("Cheese")

            case "Pinapple":
                result = "10kr"

        return result

    def setCategory(self):
        name: str = self.name
        match name:
            case "Salami":
                self.setCategory("Meat")
    
            case "Mushrooms":
                self.setCategory("Veggie")

            case "Ham":
                self.setCategory("Meat")

            case "Mozzarella":
                self.setCategory("Cheese")

            case "Pinapple":
                self.setCategory("Veggie")
        
salami = Topping("Salami")
value = salami.getPrice()
print(f"Värdet är: {value}")
