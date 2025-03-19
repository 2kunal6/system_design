from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def process(self):
        pass

class A(Strategy):
    def process(self):
        print(1)

class B(Strategy):
    def process(self):
        print(2)

class Caller:
    def __init__(self, strategy):
        self.strategy = strategy

    def process(self):
        self.strategy.process()

ca = Caller(A())
ca.process()

cb = Caller(B())
cb.process()
