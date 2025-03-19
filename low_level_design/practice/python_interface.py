from abc import ABC, abstractmethod

class Base(ABC):
    def non_abstract_method(self):
        print('hey')

    @abstractmethod
    def abstract_method(self):
        pass
class Inherited(Base):
    def abstract_method(self):
        print('abstract hey')
class Inherited_2(Base):
    def abstract_method(self):
        print('abstract hey 2')

class Caller():
    def __init__(self, use_abstract):
        self.use_abstract = use_abstract

    def test(self):
        self.use_abstract.abstract_method()


inherited = Inherited()
inherited.non_abstract_method()
inherited.abstract_method()

inherited_2 = Inherited_2()

print('-------------------------')
caller = Caller(inherited)
caller.test()

caller = Caller(inherited_2)
caller.test()