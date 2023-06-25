from Bots.Super.PlayerSuper import Player

## The greediest of bots.  HE WANTS EVERYTHING AND STOPS AT NOTHING.... WARNING. two of these faceing off gets hilarious.

class GreedyBot(Player):
    def make_bid(self, properties, highest_bid):
        if self.money > highest_bid:
            return highest_bid + 1000  # Always try to bid the minimum amount necessary
        else:
            return None  # Can't bid higher

    def buy_property(self, game):
        affordable_properties = [p for p in game.current_properties if p <= self.money]
        if not affordable_properties:
            return None
        chosen_property = min(affordable_properties)
        self.money -= chosen_property
        self.properties.append(chosen_property)
        game.current_properties.remove(chosen_property)

    def sell_property(self, game):
        # Sell the least valuable property first
        property_card = min(self.properties)
        return property_card
