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

class Group:
    def __init__(self):
        self.users = []
        self.payments = []

    def add_user(self, user):
        self.users.append(user)

    def add_payment(self, payment):
        self.payments.append(payment)

    def show_all_payments(self):
        for payment in self.payments:
            print(payment)


user_1 = User(1)
user_2 = User(2)

group_1 = Group()
group_1.add_user(user_1)
group_1.add_user(user_2)
group_1.add_payment(Payment(user_1, user_2, 5, '20250101'))

group_1.show_all_payments()