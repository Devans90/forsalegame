import numpy as np
from Bots.Super.PlayerSuper import Player

# During the bidding phase, it takes into consideration the probability of getting a high-quality property (above a certain threshold) 
# based on the remaining properties. If the probability is high, it bids up to 70% of its remaining money. If the probability is low, 
# it only bids up to 30% of its remaining money.

# In the buying phase, it considers the expected value of the remaining properties in the deck and tries to buy the property closest to this expected value.

# In the selling phase, it sells the property that deviates the most from the expected value of the remaining checks in the game.

class AuctioneerBot(Player):
    def make_bid(self, properties, highest_bid):
        # If the probability of getting a high quality property is high, bid up to 70% of money
        # Otherwise, bid up to 30% of money
        quality_threshold = 15  # Adjust this threshold based on the game's property range
        high_quality_properties = [p for p in properties if p > quality_threshold]
        prob_high_quality = len(high_quality_properties) / len(properties)
        
        if prob_high_quality > 0.5:
            max_bid = 0.7 * self.money
        else:
            max_bid = 0.3 * self.money

        if highest_bid + 1000 < max_bid:  # Check if they can afford to bid higher within their limit
            return highest_bid + 1000  # Bid the minimum amount necessary
        else:
            return None  # Can't bid higher within their limit, so pass

    def buy_property(self, game):
        affordable_properties = [p for p in game.current_properties if p <= self.money]
        if not affordable_properties:
            return None  # Can't afford to buy any property

        # Choose the property closest to the expected value of remaining properties in the deck
        expected_value = np.mean(self.property_deck)
        chosen_property = min(affordable_properties, key=lambda x: abs(x - expected_value))
        self.money -= chosen_property
        self.properties.append(chosen_property)
        game.current_properties.remove(chosen_property)

    def sell_property(self, game):
        # Sell the property that deviates the most from the expected value of remaining checks in the game
        if self.properties:
            expected_value = np.mean(game.currency_deck)
            return max(self.properties, key=lambda x: abs(x - expected_value))
        else:
            return None
