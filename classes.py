class InventoryItem:
    def __init__(self, name, value, quantity):
        self.name = name
        self.value = value
        self.quantity = quantity

    def increment_quantity(self, amount=1):
        self.quantity += amount


class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        for existing_item in self.items:
            if existing_item.name == item.name:
                existing_item.increment_quantity(item.quantity)
                break
        else:
            self.items.append(item)

    def get_total_value(self):
        return sum(item.value * item.quantity for item in self.items)
