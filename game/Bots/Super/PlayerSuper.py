class Player:
    def __init__(self, starting_money):
        self.money = starting_money
        self.properties = []

    def make_bid(self, properties, highest_bid):
        pass  # To be implemented in subclasses

    def buy_property(self, game):
        pass  # To be implemented in subclasses

    def sell_property(self, game):
        pass  # To be implemented in subclasses
