class RestaurantMenu:
    def __init__(self):
        self.menu = {
            1: self.order_pizza,
            2: self.order_pasta,
            3: self.order_salad,
            4: self.order_burger,
            5: self.order_sandwich,
        }

    def show_menu(self):
        print("Menu:")
        print("1. Pizza")
        print("2. Pasta")
        print("3. Salad")
        print("4. Burger")
        print("5. Sandwich")

    def order_pizza(self):
        print("You ordered a pizza.")

    def order_pasta(self):
        print("You ordered pasta.")

    def order_salad(self):
        print("You ordered a salad.")

    def order_burger(self):
        print("You ordered a burger.")

    def order_sandwich(self):
        print("You ordered a sandwich.")

    def take_order(self):
        self.show_menu()
        choice = int(input("Enter your choice (1-5): "))
        func = self.menu.get(choice)
        if func:
            func()
        else:
            print("Invalid choice.")

restaurant = RestaurantMenu()
restaurant.take_order()