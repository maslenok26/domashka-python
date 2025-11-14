class Product():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_info(self):
        return f'{self.name}: {self.price:.2f} руб.'
    
class Order():
    def __init__(self):
        self.items = []
        self.total_cost = 0

    def add_product(self, product):
        self.items.append(product)
        self.total_cost += product.price
    
    def remove_product(self, product_name):
        for product in self.items:
            if product.name == product_name:
                self.items.remove(product)
                self.total_cost -= product.price
                break
    
    def print_receipt(self):
        for product in self.items:
            print(product.get_info())
        print(f'Итог: {self.total_cost:.2f}')