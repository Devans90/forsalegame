import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import pandas as pd

from forsale import *

from Bots.GreedyBot import GreedyBot
from Bots.RandomBot import RandomBot
from Bots.CheapskateBot import CheapskateBot
from Bots.BigSpenderBot import BigSpenderBot
from Bots.SmartBot import SmartBot
from Bots.PrudentBot import PrudentBot
from Bots.AuctioneerBot import AuctioneerBot


def run_multiple_games(n_games, bots):

    all_game_data = []

    for i in range(n_games):
        n_players = random.randint(4, 6)
        bot_selections = random.choices(bots, k=n_players)

        player_setup = {}
        for bot in bot_selections:
            player_setup[bot] = player_setup.get(bot, 0) + 1

        winner, winnertype, final_scores, df = play_game(player_setup)
        df['GameNumber'] = i + 1
        df['winner'] = winnertype
        all_game_data.append(df)

    combined_df = pd.concat(all_game_data, ignore_index=True)
    return combined_df

combined_df = run_multiple_games(10000, bots = [GreedyBot, CheapskateBot, RandomBot, BigSpenderBot, SmartBot, PrudentBot, AuctioneerBot])



# Create a unique combination of 'Player' and 'Index'
combined_df['PlayerIndex'] = combined_df['Player'] + combined_df['Player Index'].astype(str)

final_round = combined_df['Round'].max()
final_money = combined_df[combined_df['Round'] == final_round]

plt.figure(figsize=(8,6))
sns.violinplot(data=final_money, x='Player', y='Money')
plt.title('Distribution of Final Money by Bot')
plt.show()

combined_df.to_csv('Data.csv')
pass