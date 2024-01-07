import random

#GLOBALLY  
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

class Card: 

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return self.rank + ' of ' + self.suit
    
class Deck: 

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit)) 
    
    def __str__(self): 
        deck_comp = ''
        for cards in self.deck:
            deck_comp += '\n' +  cards.__str__()
        return deck_comp

    def shuffle(self):
        random.shuffle(self.deck) 

    def deal(self):
        single_card = self.deck.pop() 
        return single_card
    
class Hand: 

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self,card): 
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1 

    def adjust_for_ace(self): 
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, total=100) -> None:
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:
        
        try:
            chips.bet = int(input("Enter the amount of chips you want to bet: "))
        except ValueError:
            print("Sorry, a bet must be an integer!")
        else:
            if chips.bet > chips.total:
                print("Your bet cannot exceed ", chips.total)
            elif chips.bet < 0:
                print("Bet should be a positive value!")
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):

    while True:

        x = input("Would you like to hit or stand, 's' for stand and 'h' for hit: ")

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("player stands, dealer is playing")
            playing = False
        else:
            print("sorry, try again")
            continue
        break

def show_some(player, dealer):
    print("\n Dealer's Hand: ")
    print("<card hidden>")
    print('', dealer.cards[1])
    print("\n player's Hand: ", *player.cards, sep='\n')


def show_all(player, dealer):
    print("\n Dealer's Hand: ", *dealer.cards, sep='\n')
    print("Dealer's Hand: ", dealer.value)
    print("\n player's Hand: ", *player.cards, sep='\n')
    print("player's Hand: ", player.value)


def player_win(chips, player, dealer):
    print("player wins!")
    chips.win_bet()

def player_busts(chips, player, dealer):
    print("player busts!")
    chips.lose_bet()

def dealer_win(chips, dealer, player):
    print("dealer wins!")
    chips.lose_bet()

def dealer_busts(chips, player, dealer):
    print("dealer busts!")
    chips.win_bet()

def push(player, dealer):
    print("Dealer and Player Tie! Its a Push")


#On to The Game!
if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    playing = True

    while playing:

        player_chips = Chips()
            
        take_bet(player_chips)

        show_some(player_hand, dealer_hand)

        hit_or_stand(deck, player_hand)

        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_chips, player_hand, dealer_hand)
            break

        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_chips, player_hand, dealer_hand)

            elif dealer_hand.value > player_hand.value:
                dealer_win(player_chips, dealer_hand, player_hand)

            elif dealer_hand.value < player_hand.value:
                player_win(player_chips, player_hand, dealer_hand)

            else:
                push(player_hand, dealer_hand)

        print("\nPlayer's Winnings at ",player_chips.total)

        playing = False

        new_game = input("Would You like to Play a new game?(type 'y' or 'n'):  ")

        if new_game.lower() == 'y':
            playing = True
        
        if new_game.lower() == 'n':
            print("Thanks for Playing! ")
            break
