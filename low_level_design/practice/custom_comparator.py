class Person:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def __eq__(self, other):
        return self.id == other.id

p1 = Person(1, 1)
p2 = Person(1, 2)
p3 = Person(2, 1)

print(p1 == p2)
print(p1 == p3)