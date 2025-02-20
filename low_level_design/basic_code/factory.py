from abc import ABC, abstractmethod

#------------------------------------------------------------------------
class Shape:
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print('Drawing Circle')

class Triangle(Shape):
    def draw(self):
        print('Drawing Triangle')
#------------------------------------------------------------------------
class Factory:
    @abstractmethod
    def create_concrete_class(self):
        pass

class CircleFactory:
    def create_concrete_class(self):
        return Circle()


class TriangleFactory:
    def create_concrete_class(self):
        return Triangle()


circle_obj = CircleFactory().create_concrete_class()
triangle_obj = TriangleFactory().create_concrete_class()

circle_obj.draw()
triangle_obj.draw()