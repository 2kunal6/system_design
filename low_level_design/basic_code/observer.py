from abc import ABC, abstractmethod

class StateClass:
    def __init__(self):
        self.observer_list = {}

    def subscribe(self, observer):
        self.observer_list[observer] = 1

    def unsubscribe(self, observer):
        del(self.observer_list[observer])

    def notify(self):
        for k in self.observer_list:
            k.notify()

class Observer(ABC):
    @abstractmethod
    def notify(self):
        pass

class User_1(Observer):
    def notify(self):
        print('notify user_1')

class User_2(Observer):
    def notify(self):
        print('notify user_2')

user_1_obj = User_1()
user_2_obj = User_2()

state_obj = StateClass()
state_obj.subscribe(user_1_obj)
state_obj.subscribe(user_2_obj)
state_obj.notify()
state_obj.unsubscribe((user_1_obj))
state_obj.notify()