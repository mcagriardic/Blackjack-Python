import numpy as np

class Cards(object):

    def __init__(self,suit,rank,value):
        self.suit = suit
        self.rank = rank
        self.value = value

class Dealer(object):

    def __init__(self):
        self.dcards = []

class Player(object):

    def __init__(self,money):
        self.money = money
        self.bet = None
        self.pcards = []

    def check_bet_amount(self):
        if self.bet <= self.money:
            bet_control = True
        else:
            print("\nPlease bet less than what you currently have: %s\n" % self.money)
            bet_control = False

        return bet_control

    def win(self):
        self.money +=self.bet*2

    def lose(self):
        self.money -= self.bet*2

    def draw(self):
        self.money = self.money


class Deck(Cards, Dealer, Player):

    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
                  'Queen':10, 'King':10, 'Ace':11}

        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Cards(suit,rank,values[rank]))

    def shuffle_cards(self):
        np.random.shuffle(self.deck)

    def deal_cards(self):
        self.shuffle_cards()
        self.pcards = []
        self.dcards = []

        cards = 0
        while cards < 2:
            self.pcards.append(self.deck.pop(0))
            self.dcards.append(self.deck.pop(0))
            cards += 1

class BlackJack(Deck):

    def __init__(self):
        Dealer.__init__(self)
        Player.__init__(self, 500)
        Deck.__init__(self)

    def get_dealer_and_player_card(self):

        dealer_cards = [str(no+1) + "- " + vars(element)["rank"] + " of " +
                        vars(element)["suit"] for no, element in enumerate(self.__dict__["dcards"])]

        player_cards = [str(no+1) + "- " + vars(element)["rank"] + " of " +
                        vars(element)["suit"] for no, element in enumerate(self.__dict__["pcards"])]

        return dealer_cards, player_cards

    def get_total_value(self):

        total_value_player = [vars(element)["value"] for element in self.__dict__["pcards"]]
        total_value_dealer = [vars(element)["value"] for element in self.__dict__["dcards"]]
        return sum(total_value_player), sum(total_value_dealer)

    def get_bet(self):
        bet_control = False

        while bet_control is False:
            bet = input("\nHow much are you betting? - ")
            try:
                bet = int(bet)
                if bet > 0:
                    self.bet = bet
                    bet_control = self.check_bet_amount()
                else:
                    print(type(bet),bet)
                    print("\nPlease provide a positive value!\n")
            except ValueError:
                print("\nPlease provide a valid value!\n")

    def show_partial(self):

        dealer_cards, player_cards = self.get_dealer_and_player_card()
        total_value_player, total_value_dealer = self.get_total_value()

        print("------------------\n| Dealer's Cards |\n------------------")
        for no, card in enumerate(dealer_cards):
            if card == dealer_cards[0]:
                print(card)
            else:
                print(str(no+1) + "  <Card hidden>")

        print("\n------------------\n| Player's Cards |\n------------------")
        for card in player_cards:
            print(card)
            if player_cards[-1] == card:
                print("<Total points: {}>".format(total_value_player))

    def show_all(self):

        dealer_cards, player_cards = self.get_dealer_and_player_card()
        total_value_player, total_value_dealer = self.get_total_value()

        print("============================================================\n"+
              "\n------------------\n| Dealer's Cards |\n------------------")
        for no, card in enumerate(dealer_cards):
            print(card)
            if dealer_cards[-1] == card:
                print("<Total points: {}>".format(total_value_dealer))

        print("\n------------------\n| Player's Cards |\n------------------")
        for card in player_cards:
            print(card)
            if player_cards[-1] == card:
                print("<Total points: {}>".format(total_value_player))

    def hit_or_stand(self):
        hit_control = False
        player_hit = False

        while hit_control is False:
            hit_check = input("\nDo you wish to hit? Please enter 'Y' or 'N' - ").lower()
            if hit_check == "y":
                self.pcards.append(self.deck.pop(0))
                player_hit = True
                hit_control = True
            elif hit_check == "n":
                player_hit = False
                hit_control = True
            else:
                print("\nPlease provide a valid value!\n")

        self.check_if_ace_in_hand()

        if player_hit is True:
            self.dcards.append(self.deck.pop(0))

        return player_hit

    def check_if_ace_in_hand(self):

        player_cards = [vars(elements) for elements in self.__dict__["pcards"]]
        card_values = [card.values() for card in player_cards]
        ace_mask = ["Ace" in dict_values for dict_values in card_values]

        total_value_player, total_value_dealer = self.get_total_value()

        if any(ace_mask) and total_value_player > 21:
            print("\n>>>>>>>>Player's points exceed 21 - Ace counts as 1 point!!")
            card_no_ace = ace_mask.index(True)
            self.pcards[card_no_ace].value = 1

    def run_rules(self,player_hit):

        total_value_player, total_value_dealer = self.get_total_value()

        game_win = None
        continue_check = None
        if total_value_player > 21 or\
           total_value_dealer > 21 or\
           total_value_player == 21 or\
           total_value_dealer == 21:

            print("\n============================================================")
            if total_value_player > 21 and total_value_dealer > 21:
                print("Tie!")
            elif total_value_player > 21:
                game_win = False
                print("Dealer wins! Player goes bust!")
            elif total_value_dealer > 21:
                game_win = True
                print("Player wins! Dealer goes bust!")
            elif total_value_player == 21:
                if total_value_dealer == 21:
                    print("Tie!")
                else:
                    game_win = True
                    print("Player wins!")
            elif total_value_dealer == 21:
                if total_value_player == 21:
                    print("Tie!")
                else:
                    game_win = False
                    print("Dealer wins!")

            self.show_all()
            self.check_result(game_win)

        elif total_value_player < 21 and total_value_dealer < 21 and player_hit is False:

            print("\n============================================================")
            if total_value_player > total_value_dealer:
                game_win = True
                print("Player wins!")
            elif total_value_player < total_value_dealer:
                game_win = False
                print("Dealer wins!")
            elif total_value_player == total_value_dealer:
                print("Tie!")

            self.show_all()
            self.check_result(game_win)

        elif total_value_player < 21 and total_value_dealer < 21 and player_hit is True:
            continue_check = False
            self.show_partial()

        return game_win

    def check_result(self, game_win):

        if game_win:
            self.win()
        elif game_win is False:
            self.lose()
        else:
            self.draw()

        print("\nYour current outstanding stands at: %s \n" % self.money)

def start_game():
    continue_playing = True
    player = BlackJack()

    while continue_playing is True:
        player.deal_cards()
        player.show_partial()
        player.check_if_ace_in_hand()
        player.get_bet()

        player_hit = None
        game_win = player.run_rules(player_hit)
        total_value_player, total_value_dealer = player.get_total_value()

        while total_value_player < 21 and total_value_dealer < 21:
            player_hit = player.hit_or_stand()
            total_value_player, total_value_dealer = player.get_total_value()
            if player_hit is False:
                game_win = player.run_rules(player_hit)
                break
            else:
                game_win = player.run_rules(player_hit)

        continue_playing_control = False
        while continue_playing_control is False:
            continue_playing = input("Would you like to continue playing? Please enter 'Y' or 'N' -").lower()
            if continue_playing == 'y' or continue_playing == 'n':
                continue_playing_control = True
                if continue_playing == 'y':
                    continue_playing = True
                else:
                    continue_playing = False
            else:
                print("Please either provide 'y' or 'n'")

    #print("\nGame win= %s\n" % game_win)
    return player
