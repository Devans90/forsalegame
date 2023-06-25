import random
import pandas as pd


class ForSaleGame:
    def __init__(self, players):
        self.players = players
        self.property_deck = list(range(1, 31))
        self.currency_deck = [i for i in range(0, 15001, 1000) for _ in range(2)]
        self.currency_deck.remove(1000)
        self.currency_deck.remove(1000)
        random.shuffle(self.property_deck)
        random.shuffle(self.currency_deck)
        
        if len(players) in [3, 4]:
            for player in players:
                player.money = 2000 * 2 + 1000 * 14
        elif len(players) in [5, 6]:
            for player in players:
                player.money = 2000 * 2 + 1000 * 10

        if len(players) == 3:
            for _ in range(6):
                self.property_deck.pop()
                self.currency_deck.pop()
        elif len(players) == 4:
            for _ in range(2):
                self.property_deck.pop()
                self.currency_deck.pop()

        self.current_properties = []
        self.current_checks = []
        self.phase = "buying"
        self.round = 0
        self.history = {player: [] for player in self.players}

    def record_state(self):
        for player in self.players:
            player_index = self.players.index(player) + 1
            self.history[player].append((self.round, self.phase, player.money, list(player.properties), player_index))


    def setup_phase1(self):
        num_properties = len(self.players)
        self.current_properties = [self.property_deck.pop() for _ in range(num_properties)]
        self.current_properties.sort(reverse=True)

    def auction_phase1(self):
        
        active_bidders = list(self.players)
        bids = {player: 0 for player in self.players}
        current_player_index = 0  # Start with the player who lives in the largest house

        while len(active_bidders) > 1:
            current_player = active_bidders[current_player_index]
            print("Player:", type(current_player).__name__)
            print("Current Properties:", self.current_properties)

            bid = current_player.make_bid(self.current_properties, max(bids.values()), self)
            if bid is not None:
                if bid % 1000 != 0:
                    print("Invalid bid! Bids must be multiples of $1,000.")
                    continue
                bids[current_player] = bid
            else:  # Player has passed
                current_player.money += round(bids[current_player] // 2, -3)  # Get half of their bid back
                bids[current_player] = 0
                active_bidders.remove(current_player)
                lowest_property = min(self.current_properties)
                current_player.properties.append(lowest_property)
                self.current_properties.remove(lowest_property)

            current_player_index = (current_player_index + 1) % len(active_bidders)

        # Last remaining player gets the highest-valued property for their bid
        remaining_player = active_bidders[0]
        remaining_player.money -= bids[remaining_player]
        highest_property = max(self.current_properties)
        remaining_player.properties.append(highest_property)
        self.current_properties.remove(highest_property)
        self.round = self.round + 1
        self.record_state()

    def setup_phase2(self):
        random.shuffle(self.currency_deck)
        self.current_currency = []
        self.phase = 'selling'

    def selling_phase(self):
        # Turn up the number of Currency Cards equal to the number of players
        self.current_currency = self.currency_deck[:len(self.players)]
        self.currency_deck = self.currency_deck[len(self.players):]

        property_bids = []
        for player in self.players:
            property_card = player.sell_property(self)
            if property_card not in player.properties:
                raise ValueError("Player attempted to sell a property they do not own")
            property_bids.append((property_card, player))
        
        # Sort bids and currency in descending order
        property_bids.sort(reverse=True)
        self.current_currency.sort(reverse=True)

        # Players receive currency in order of their property value
        for i, (property_card, player) in enumerate(property_bids):
            player.money += self.current_currency[i]
            player.properties.remove(property_card)

        # Clear the current currency
        self.current_currency = []
        self.round = self.round + 1
        self.record_state()


def play_game(player_setup):

    total_players = sum(player_setup.values())
    if not 3 <= total_players <= 6:
        raise ValueError("Invalid number of players. The game requires between 3 and 6 players.")

    players = []
    for player_class, quantity in player_setup.items():
        players.extend([player_class(14000) for _ in range(quantity)])

    game = ForSaleGame(players)

    while game.property_deck:  # Play until the deck of properties runs out
        game.setup_phase1()
        print('Auction phase: ' + (str(game.round + 1)))
        game.auction_phase1()
    
    while game.currency_deck: # Play until the deck of checks runs out
        game.setup_phase2()
        print('Selling phase: ' + (str(game.round + 1)))
        game.selling_phase()


    # Initialize the winner and highest score
    winner = None
    highest_score = 0

    final_scores = {}
    for i, player in enumerate(game.players):
        final_scores[f"Player {i+1} ({player.__class__.__name__})"] = player.money
        print(f"Player {i+1} ({player.__class__.__name__}) ended with ${player.money} and properties {sorted(player.properties)}")
        if player.money > highest_score:
            highest_score = player.money
            winner = f"Player {i+1} ({player.__class__.__name__})"
            winnertype = player.__class__.__name__
    print('Winner was ' + winner)
    
    # Transform the history into a DataFrame
    rows = []
    for player, history in game.history.items():
        for round, phase, money, properties, player_index in history:
            rows.append({'Player': str(player.__class__.__name__), 'phase': str(phase), 'Round': round, 'Money': money, 'Properties': properties, 'Player Index': player_index, 'Num Players': total_players})
    df = pd.DataFrame(rows)

    return winner, winnertype, final_scores, df

