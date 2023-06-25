from Bots.Super.PlayerSuper import Player


class AnalystBot(Player):
    def __init__(self, money):
        super().__init__(money)
        self.mean_property_value = 0
        self.sd_property_value = 0

    def update_statistics(self, properties):
        self.mean_property_value = sum(properties) / len(properties)
        self.sd_property_value = (sum((x-self.mean_property_value)**2 for x in properties) / len(properties))**0.5

    def make_bid(self, properties, highest_bid, game):
        self.update_statistics(properties)
        
        # Bid on properties that are above the mean
        # and not too far from 1 standard deviation
        if max(properties) > self.mean_property_value and max(properties) < self.mean_property_value + self.sd_property_value:
            bid = highest_bid + 1000
            if bid <= self.money:
                return bid
        return None

    def sell_property(self, game):
        # When selling, the bot uses a similar strategy.
        # It sells the properties that are close to the mean value
        if self.properties:
            self.update_statistics(self.properties)
            for prop in sorted(self.properties):
                if abs(prop - self.mean_property_value) <= self.sd_property_value:
                    return prop
        return None
