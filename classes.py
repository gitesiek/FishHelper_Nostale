class InventoryItem:
    def __init__(self, name, value, quantity, exp_profession):
        self.name = name
        self.quantity = quantity
        self.value = value
        self.exp_profession = exp_profession

    def get_item_info(self):
        return {
            'Name': self.name,
            'Quantity': self.quantity,
            'Value': self.value,
            'Profession': self.exp_profession,
            }

    def change_value(self, new_value):
        self.value = new_value

    def increment_quantity(self, amount=1):
        self.quantity += amount


class Inventory:
    def __init__(self):
        self.items = []

    def get_items(self):
        items_info = []
        for item in self.items:
            items_info.append(item.get_item_info())
        return items_info

    def add_item(self, item):
        for existing_item in self.items:
            if existing_item.name == item.name:
                existing_item.increment_quantity(item.quantity)
                break
        else:
            self.items.append(item)

    def get_total_value(self):
        total_value = 0
        for item in self.items:
            total_value += int(item.value) * item.quantity
        return total_value

    def get_total_exp_profession(self):
        total_exp = 0
        for item in self.items:
            total_exp += int(item.exp_profession) * item.quantity
        return total_exp
