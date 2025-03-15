class User:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return str(self.id)

class Payment:
    def __init__(self, payer, payee, amount, timestamp):
        self.payer = payer
        self.payee = payee
        self.amount = amount
        self.timestamp = timestamp

    def __str__(self):
        return f'{self.timestamp} {self.payer} {self.payee} {self.amount}'

from abc import ABC, abstractmethod

class IPayment:
    @abstractmethod
    def pay(self, amount):
        pass

class gpay(IPayment):
    def pay(self, amount):
        print('paying using gpay')

class phonepay(IPayment):
    def pay(self, amount):
        print('paying using phonepay')

class Group:
    def __init__(self):
        self.users = set()
        self.payments = set()

    def add_user(self, user):
        self.users.add(user)

    def add_payment(self, payment):
        self.payments.add(payment)

    def show_all_payments(self):
        for payment in self.payments:
            print(payment)

    def pay(self, payer, payee, payment_method, pay_amount, paytime):
        payment_method.pay(pay_amount)
        self.payments.add(Payment(payer, payee, pay_amount, paytime))


user_1 = User(1)
user_2 = User(2)

group_1 = Group()
group_1.add_user(user_1)
group_1.add_user(user_2)
group_1.add_payment(Payment(user_1, user_2, 5, '20250101'))

group_1.show_all_payments()

group_1.pay(user_2, user_1, gpay(), 5, '20250201')
group_1.show_all_payments()