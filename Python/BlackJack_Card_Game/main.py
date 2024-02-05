import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    ranks = {"Ace": 1 or 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
             "Jack": 10, "Queen": 10, "King": 10}

    def __init__(self):
        self.cards = []

        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(f"{rank} of {suit}")

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, times):
        return [self.cards.pop() for _ in range(times) if len(self.cards) > times]


class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def show_card(self):
        return self.cards

    def calculate_value(self):
        self.value = 0
        for card in sorted(self.cards, key=lambda card: card.startswith('Ace')):
            card_suit = card.split()[0]
            card_value = Deck.ranks[card_suit]
            if card_suit == 'Ace':
                if self.value <= 10:
                    self.value += 11
                else:
                    self.value += 1
            else:
                self.value += card_value

    def get_value(self):
        self.calculate_value()
        if self.is_blackjack():
            print("BlackJack")
        return self.value

    def is_blackjack(self):
        self.calculate_value()
        return self.value == 21

    def display(self):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not self.is_blackjack():
                print('Hidden')
            else:
                print(card)
        if not self.dealer:
            print("Value:", self.get_value())
        print()


class Game:
    def play(self):
        game_number = 0
        games_to_play = self.get_number('How many times do you want to play? ')

        while game_number < games_to_play:
            game_number += 1
            print(f'\n\n{game_number} of {games_to_play}')

            deck = Deck()
            deck.shuffle()

            player = Hand()
            dealer = Hand(dealer=True)

            for _ in range(2):
                player.add_card(deck.deal(1))
                dealer.add_card(deck.deal(1))

            print('*' * 30)
            player.display()
            print()
            dealer.display()

            if self.check_win(player, dealer, game_number == games_to_play):
                continue

            choice = ''
            while player.get_value() < 21 and choice not in ['s', 'stand']:
                choice = input("'Hit' or 'Stand'? ").lower()
                while choice not in ['h', 'hit', 's', 'stand']:
                    choice = input("'Hit' or 'h' or 'Stand' or 's'? ").lower()
                if choice in ['h', 'hit']:
                    print()
                    player.add_card(deck.deal(1))
                    player.display()

            if self.check_win(player, dealer, game_number == games_to_play):
                continue

            player_value = player.get_value()
            dealer_value = dealer.get_value()

            while dealer_value < 17:
                dealer.add_card(deck.deal(1))
                dealer_value = dealer.get_value()

            dealer.display()

            if self.check_win(player, dealer, game_number == games_to_play):
                continue

            print("Final Results")
            print("Your hand:", player_value)
            print("Dealer's hand:", dealer_value)

            self.check_win(player, dealer, True)

        print("\nThanks for playing!")

    @staticmethod
    def check_win(player, dealer, game_over=False):
        if not game_over:
            if player.get_value() > 21:
                print("You lose! 😭")
                return True
            elif dealer.get_value() > 21:
                print("You win! 😀")
                return True
            elif player.is_blackjack() and dealer.is_blackjack():
                print("Both players have blackjack, it's a tie! 😑")
                return True
            elif player.is_blackjack():
                print("You have blackjack, You win! 😀")
                return True
            elif dealer.is_blackjack():
                print("Dealer has blackjack, You lose! 😭")
                return True
        else:
            if player.get_value() > dealer.get_value():
                print("You win! 😀")
            elif player.get_value() < dealer.get_value():
                print("Dealer wins. 😭")
            else:
                print("Tie! 😑")
            return True
        return False

    @staticmethod
    def get_number(ask=None):
        while True:
            try:
                return int(input(ask))
            except ValueError:
                print('Enter a number!')


game = Game()
game.play()
