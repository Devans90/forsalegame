from Bots.Super.PlayerSuper import Player
import random

## What are the rules, what am i even doing here? i guess i bet this much?  

class RandomBot(Player):
    def make_bid(self, properties, highest_bid, game):
        # Calculate the number of increments of $1,000 the bot can afford
        max_increments = self.money // 1000
        min_increments = (highest_bid // 1000) + 1

        if max_increments > min_increments:
            bid_increments = random.randint(min_increments, max_increments)
            return bid_increments * 1000
        else:
            return None  # Can't bid higher

    def buy_property(self, game):
        affordable_properties = [p for p in game.current_properties if p <= self.money]
        if not affordable_properties:
            return None
        chosen_property = random.choice(affordable_properties)
        self.money -= chosen_property
        self.properties.append(chosen_property)
        game.current_properties.remove(chosen_property)

    def sell_property(self, game):
        # Choose a random property to sell
        property_card = random.choice(self.properties)
        return property_card
