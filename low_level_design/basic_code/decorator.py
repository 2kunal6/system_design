from abc import ABC, abstractmethod

#----------------------------------------------------
class BaseCoffee(ABC):
    @abstractmethod
    def get_ingredients(self):
        pass
    @abstractmethod
    def get_cost(self):
        pass

class FilterCoffee(BaseCoffee):
    def get_ingredients(self):
        print('Filter Coffee')
    def get_cost(self):
        return 1.0

class BlackCoffee(BaseCoffee):
    def get_ingredients(self):
        print('Black added')
    def get_cost(self):
        return 2.0
#----------------------------------------------------------
class CoffeeDecorator(BaseCoffee):
    def __init__(self, coffee):
        self.coffee = coffee
    def get_ingredients(self):
        pass
    def get_cost(self):
        pass

class MilkDecorator(CoffeeDecorator):
    def get_ingredients(self):
        self.coffee.get_ingredients()
        print('Milk added')
    def get_cost(self):
        return self.coffee.get_cost() + 0.5


class Flavour_a_Decorator(CoffeeDecorator):
    def get_ingredients(self):
        self.coffee.get_ingredients()
        print('Flavour a added')
    def get_cost(self):
        return self.coffee.get_cost() + 0.2

#-----------------------------------------------------------
new_coffee = MilkDecorator(BlackCoffee())
new_coffee.get_ingredients()
new_coffee.get_cost()

flavour_coffee = Flavour_a_Decorator(new_coffee)
flavour_coffee.get_ingredients()
flavour_coffee.get_cost()