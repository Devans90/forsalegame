import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from forsale import *

from Bots.GreedyBot import GreedyBot
from Bots.RandomBot import RandomBot
from Bots.CheapskateBot import CheapskateBot

winner, winnertype, final_scores, df = play_game({GreedyBot: 1, CheapskateBot:1, RandomBot: 2})



# Create a unique combination of 'Player' and 'Index'
df['PlayerIndex'] = df['Player'] + df['Player Index'].astype(str)

for player_index in df['PlayerIndex'].unique():
    subset = df[df['PlayerIndex'] == player_index]
    plt.plot(subset['Round'], subset['Money'], label=player_index)

plt.xlabel('Round')
plt.ylabel('Money')
plt.title('Money changes over Rounds by Player and Index')
plt.legend(loc='upper left')

plt.show()


pass