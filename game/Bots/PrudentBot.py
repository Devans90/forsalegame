from Bots.Super.PlayerSuper import Player


# During the bidding phase, it assesses the quality of the properties available. 
# If high-quality properties (above a certain threshold) are available, it's willing to bid up to 60% of its remaining money. For properties below this threshold, it only bids up to 40% of its remaining money.

# In the buying phase, it prefers to buy the property closest to the mean of the available properties it can afford.

# In the selling phase, it sells the property closest to the mean of its owned properties.

class PrudentBot(Player):
    def make_bid(self, properties, highest_bid, game):
        # If high quality properties are available, bid up to 60% of money
        # Otherwise, bid up to 40% of money
        quality_threshold = 15  # Adjust this threshold based on the game's property range
        if max(properties) > quality_threshold:
            max_bid = 0.6 * self.money
        else:
            max_bid = 0.4 * self.money

        if highest_bid + 1000 < max_bid:  # Check if they can afford to bid higher within their limit
            return highest_bid + 1000  # Bid the minimum amount necessary
        else:
            return None  # Can't bid higher within their limit, so pass

    def buy_property(self, game):
        affordable_properties = [p for p in game.current_properties if p <= self.money]
        if not affordable_properties:
            return None  # Can't afford to buy any property

        # Choose the property closest to the mean of affordable properties
        mean = sum(affordable_properties) / len(affordable_properties)
        chosen_property = min(affordable_properties, key=lambda x: abs(x - mean))
        self.money -= chosen_property
        self.properties.append(chosen_property)
        game.current_properties.remove(chosen_property)

    def sell_property(self, game):
        # Sell the property closest to the mean of owned properties
        if self.properties:
            mean = sum(self.properties) / len(self.properties)
            return min(self.properties, key=lambda x: abs(x - mean))
        else:
            return None
