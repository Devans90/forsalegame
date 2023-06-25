import pandas as pd
import random
from Bots.Super.PlayerSuper import Player
sourcedata = pd.read_csv(r'C:\Users\devan\OneDrive\repostiories\forsalegame\game\Bots\HistoricalData.csv')

class HistorianBot(Player):
    def __init__(self, money):
        super().__init__(money)
        self.historical_data = sourcedata  # Load a pandas DataFrame with historical game data
        self.round_bids = self.get_average_bids_per_round()

    def get_average_bids_per_round(self):
        # Create a dictionary with rounds as keys and average successful bids as values
        successful_bids = self.historical_data[self.historical_data['winner'] == self.__class__.__name__]
        avg_bids = successful_bids.groupby('Round')['Money'].mean()
        return avg_bids.to_dict()

    def make_bid(self, properties, highest_bid, game):
        # Look up the average successful bid for this round in historical data
        average_bid = self.round_bids.get(game.round, 0)

        # If the highest bid is less than the average successful bid for this round, increase the bid
        if highest_bid < average_bid and highest_bid + 1000 <= self.money:
            return highest_bid + 1000

        # Otherwise, pass
        return None

    def sell_property(self, game):
        # Sell the lowest-valued property
        if self.properties:
            return min(self.properties)
        else:
            return None
