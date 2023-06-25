from Bots.Super.PlayerSuper import Player

# During the bidding phase, it bids up to 50% of its remaining money if it can afford the next highest bid.
# In the buying phase, it buys the property closest to the median of the available properties it can afford.
# In the selling phase, it sells the property closest to the median of its owned properties.

class SmartBot(Player):
    def make_bid(self, properties, highest_bid, game):
        # Calculate maximum bid as 50% of remaining money
        max_bid = 0.5 * self.money
        if highest_bid + 1000 < max_bid:  # Check if they can afford to bid higher within their limit
            return highest_bid + 1000  # Bid the minimum amount necessary
        else:
            return None  # Can't bid higher within their limit, so pass

    def buy_property(self, game):
        affordable_properties = [p for p in game.current_properties if p <= self.money]
        if not affordable_properties:
            return None  # Can't afford to buy any property
        # Choose the property closest to the median of affordable properties
        median = sorted(affordable_properties)[len(affordable_properties) // 2]
        chosen_property = min(affordable_properties, key=lambda x: abs(x - median))
        self.money -= chosen_property
        self.properties.append(chosen_property)
        game.current_properties.remove(chosen_property)

    def sell_property(self, game):
        # Sell the property closest to the median of owned properties
        if self.properties:
            median = sorted(self.properties)[len(self.properties) // 2]
            return min(self.properties, key=lambda x: abs(x - median))
        else:
            return None
