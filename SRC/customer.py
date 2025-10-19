import lib.observer as observer
import random

class Customer(observer.Subject, observer.Observer):
    def __init__(self, initial_balance):
        self.id = str(hash(random.randint(1000, 99999))) # Unique ID for the customer
        self.balance = initial_balance
        self.trade_history = []
        self.observers = []
        self.status = False

    def attach(self, observer: observer.Observer) -> None:
        print("Customer with Id: {}, Attached to subject {}".format(self.id, observer))
        self.observers.append(observer)

    def detach(self, observer: observer.Observer) -> None:
        print("Customer with Id: {}, Detached from subject {}".format(self.id, observer))
        self.observers.remove(observer)

    def update(self, subject: observer.Subject) -> None:
        print("Customer with Id: {}, Update observer {}".format(self.id, subject))

    def update_status(self):
        if self.status:
            self.status = False
        else:
            self.status = True
        self.notify_observers()

    def update_balance(self, amount):
        self.balance += amount

    def add_trade(self, trade):
        self.trade_history.append(trade)

class Bot:
    def update(self, customer):
        print(f"Bot notified: Customer balance is {customer.balance}, status is {customer.status}")