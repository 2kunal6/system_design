from abc import ABC, abstractmethod

class StateClass:
    def __init__(self):
        self.state = 0
        self.observer_list = {}

    def subscribe(self, observer):
        self.observer_list[observer] = 1

    def unsubscribe(self, observer):
        del(self.observer_list[observer])

    def notify(self):
        for k in self.observer_list:
            k.notify(self.state)

    def set_state(self, new_state):
        if(self.state == new_state):
            return
        self.state = new_state
        self.notify()

class Observer(ABC):
    @abstractmethod
    def notify(self, new_state):
        pass

class User_1(Observer):
    def notify(self, new_state):
        print(f'notify user_1 {new_state}')

class User_2(Observer):
    def notify(self, new_state):
        print(f'notify user_2 {new_state}')

user_1_obj = User_1()
user_2_obj = User_2()

state_obj = StateClass()
state_obj.subscribe(user_1_obj)
state_obj.subscribe(user_2_obj)
state_obj.set_state(1)
state_obj.set_state(1)
state_obj.unsubscribe((user_1_obj))
state_obj.set_state(2)