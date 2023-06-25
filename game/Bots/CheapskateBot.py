from Bots.Super.PlayerSuper import Player
import random

# I wanna play, but i dont want to spend money....

class CheapskateBot(Player):
    def make_bid(self, properties, highest_bid):
        # Calculate maximum bid as 25% of remaining money or 2000, whichever is greater
        max_bid = max(0.25 * self.money, 2000)
        if highest_bid + 1000 < max_bid:  # Check if they can afford to bid higher within their limit
            return highest_bid + 1000  # Bid the minimum amount necessary
        else:
            return None  # Can't bid higher within their limit, so pass

    def buy_property(self, game):
        affordable_properties = [p for p in game.current_properties if p <= self.money]
        if not affordable_properties:
            return None  # Can't afford to buy any property
        chosen_property = min(affordable_properties)  # Choose the cheapest property
        self.money -= chosen_property
        self.properties.append(chosen_property)
        game.current_properties.remove(chosen_property)

    def sell_property(self):
        # Sell the lowest-valued property
        if self.properties:
            return min(self.properties)
        else:
            return None
