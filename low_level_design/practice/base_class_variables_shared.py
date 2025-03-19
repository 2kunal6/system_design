class Base:
    type = 'base variable'

    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)

class Inherited(Base):
    def __init__(self, name, occu):
        super().__init__(name)
        self.occu = occu

inh = Inherited(1, 2)
print(inh.name)
print(inh.occu)
inh.print_name()
print(inh.type)