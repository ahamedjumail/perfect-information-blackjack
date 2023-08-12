import random 
import itertools
import sys
import copy

class Deck:
    """ Deck of playing cards """

    def __init__(self, number_of_decks=1):
        
        self.suits = ["spades", "clubs", "hearts", "diamonds"]
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.number_of_decks = number_of_decks
        self.deck = list(itertools.product(self.suits, self.ranks)) * self.number_of_decks
        random.shuffle(self.deck)
        self.deck_copy = self.deck[:]

    def deal(self, num=1):
        """ deal a card and remove that card from the deck, 
            this will also serve as a HIT function 
            num:    number of cards being drawn
        """
            
        if num == 1:
            dealt_card = self.deck.pop()
            try:
                self.deck_copy.remove(dealt_card)
            except ValueError:
                pass
            return dealt_card
        else:
            dealt_cards = [self.deck.pop() for _ in range(num)]
            self.deck_copy = [card for card in self.deck_copy if card not in dealt_cards]
            return dealt_cards

    def deal_copy(self, num=1):
        """ deal a card and remove that card from the deck, 
            this will also serve as a HIT function 
            num:    number of cards being drawn
        """
            
        if num == 1:
            return self.deck_copy.pop()

        else:
            return list( self.deck_copy.pop() for x in range(num) )

    def reset_copy(self):
        self.deck_copy = self.deck[:]
        
    def __str__(self):
        return "Deck of cards"
    
    
    def reset(self):
        """ restore the deck to its original state "52" cards """        
        
        self.deck = list(itertools.product(self.suits, self.ranks)) * self.number_of_decks
        random.shuffle(self.deck)

def get_hand_value(hand):
    
    """
    calculate the current hand value 
        # K,Q,J are worth 10 points each
        # A is worth either 1 or 11
        # 2-10 = face value
        # cards comming in format ('spades', 'K')
    """
    jdebug = 0
    if jdebug > 0:  print( "count_hand() called by: {}".format(sys._getframe(1).f_code.co_name) )
    
    # initialise
    status = "empty"            # if no cards in the hand
    val = 0                     # hand value
    aceCounter = 0              # number of aces
    aceCounterAddressed = 0     # number of aces addressed
    
    for card in hand:
        if jdebug > 0:  print("card={} card[1]={}".format(card, card[1]))
        
        # check to see if the card is numbered, 2-10
        try:
            val += int(card[1])
            if jdebug > 0:  print("Number detected, {}".format(card[1]))
            
        except ValueError:
            
            if jdebug > 0:  print("Letter detected, {}".format(card[1]))
            
            if card[1] in ["K", "Q", "J"]:
                val += 10
            
            else:
                if jdebug > 0:  print("'A' detected, {}".format(card[1]))
                
                if val+11 > 21:
                    val += 1
                else:
                    aceCounter += 1
                    val += 11
                
        if aceCounter > 0 and val > 21 and (aceCounterAddressed != aceCounter):
            aceCounterAddressed += 1
            val -= 10
        
        if val == 21:
            status = "BLACKJACK"
        elif val > 21:
            status = "BUST"
        else:
            status = "active"

    return val, status

def hint(player_hand,deck):
    
    
    p2 = copy.copy(player_hand)


    c1,s1 = get_hand_value(player_hand)
    c2,s2 = get_hand_value(p2)
    
    i = 0
    while c2<21:
        if i:
            for j in range(i):
                p2.append(deck.deal_copy())
        print("Copy while player hit:",deck.deck_copy)
        c2,s2 = get_hand_value(p2)
        print('\n',p2,'\n')
        if c2>21:
            deck.reset_copy()
            return "Can't win this round"
        house_hand = []
        print("Copy while house hits:",deck.deck_copy)
        for k in range(2):
            house_hand.append(deck.deck_copy.pop())

        cp,sp = get_hand_value(house_hand)
        while cp<17:
            house_hand.append(deck.deal_copy())
            cp,sp = get_hand_value(house_hand)
        print("final house hand:",house_hand)
        if cp>21 or c2>cp:
            deck.reset_copy()
            return i
        deck.reset_copy()
        p2 = copy.copy(player_hand)
        i+=1    
    return "Cannot win"