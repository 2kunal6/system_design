from abc import ABC, abstractmethod

class Pay(ABC):
    @abstractmethod
    def pay(self):
        pass

class Gpay(Pay):
    def pay(self):
        print('Paying using Gpay')

class PhonePay(Pay):
    def pay(self):
        print('Paying using PhonePay')


class Order:
    def __init__(self, payment_method):
        self.payment_method = payment_method

    def place_order(self):
        self.payment_method.pay()
        print('order placed')


gpay_order = Order(Gpay())
gpay_order.place_order()

phonepay_order = Order(PhonePay())
phonepay_order.place_order()