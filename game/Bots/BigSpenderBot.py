from Bots.Super.PlayerSuper import Player

# This bot behaves in an opposite manner to the CheapskateBot. It always tries to buy the most expensive property it can afford and sell the highest-valued property. 
# During bidding, it bids as high as it can (up to 75% of its remaining money) as long as it's above the highest current bid

class BigSpenderBot(Player):
    def make_bid(self, properties, highest_bid, game):
        # Calculate maximum bid as 75% of remaining money or 2000, whichever is greater
        max_bid = max(0.75 * self.money, 2000)
        if highest_bid + 1000 < max_bid:  # Check if they can afford to bid higher within their limit
            return highest_bid + 1000  # Bid the minimum amount necessary
        else:
            return None  # Can't bid higher within their limit, so pass

    def buy_property(self, game):
        affordable_properties = [p for p in game.current_properties if p <= self.money]
        if not affordable_properties:
            return None  # Can't afford to buy any property
        chosen_property = max(affordable_properties)  # Choose the most expensive property
        self.money -= chosen_property
        self.properties.append(chosen_property)
        game.current_properties.remove(chosen_property)

    def sell_property(self, game):
        # Sell the highest-valued property
        if self.properties:
            return max(self.properties)
        else:
            return None
