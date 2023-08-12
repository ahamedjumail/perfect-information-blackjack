'''Blackjack using dynamic programming'''
import random   #this is used for shuffling the cards 
import time 

class Player:
    '''Player class'''
    def __init__(self,cards=None,name=None):
        self.name = name #name of the player 
        self.cards = cards   #when cards is defined (when calculating max score in terms of values)
        if self.cards is None:
            self.cards = []   #but when cards is not defined (actual gameplay)
        self.total = 0   #total player sum 
        self.cash = 1000  #total amount of cash the player can bet 

    def deal(self,cards):
        '''This function is mostly used for obtaining the maximum score possible for the 
        player to score. It involves dealing the initial cards to the player.'''
        self.cards.extend(cards)
        self.total = sum(self.cards)

    def reset(self):
        '''Called when a fresh round has started'''
        self.cards = []
        self.total = 0 

    def make_bet(self,amount):
        '''Placing a bet'''
        if amount > self.cash:
            return 'low funds'
        
        else:
            self.cash = self.cash - amount 

    def show_cards(self):
        '''Printing the player's cards'''
        print(f"{self.name}'s CARDS: ")

        for card in self.cards:
            print('CARD: ',card,' ')

        print('SUM: ',self.total)
        #print('\n')

    def hit(self,card):
        '''Player chooses to take a card from the deck'''
        self.cards.append(card)
        self.total += card.value 
        
    def stand(self):
        '''Player chooses to stand'''
        if self.total < 17:
            return 'are you sure you want to stand?'
        
        else:
            return 'Player chooses to stand!'

class Dealer(Player):
    '''The dealer has the same functions as that of the player except with 
    some extra functionality, and therefore inherits from the Player class'''
      
    '''Dealer class'''
    def __init__(self,cards=None,name=None):
        super().__init__(cards,name)

    def reset(self):
        super().reset()

    def make_bet(self,amount):
        '''the dealer should make the same bet as the player'''
        if self.cash < amount:
            self.cash = 0
            return 'dealer is all in!'
        
        else:
            self.cash = self.cash - amount 

    def show_cards(self,show=False):
        '''Used for showing the dealer's cards'''
        print("DEALER'S CARDS: ")
        if show:   #show is true at the end of the round where all of the dealer's cards are displayed
            for i in range(0,len(self.cards)):
                card = self.cards[i]
                print('CARD: ',card.shape,' ',card.symbol,)
            print('SUM: ',self.total)
            

        else:
            print('unknown card')  #all but the first card of the dealer is displayed during gameplay
            for i in range(1,len(self.cards)):
                card = self.cards[i]
                print('CARD: ',card.shape,' ',card.symbol,)
            print('SUM: ',self.total - self.cards[0].value)


    def hit(self,card):
        '''Dealer taking a card'''

        if len(self.cards) < 2:
            self.cards.append(card)
            if len(self.cards) == 1:
                self.total += card.value 

            else:
                self.total += card.value 

        else:
            '''The dealer is supposed to keep taking cards if the 
            total is less than 17. Otherwise the dealer has to stand.'''
            if self.total < 17:
                self.cards.append(card)
                self.total += card.value 

            else:
                self.stand()

    def stand(self):
        '''Dealer is standing'''
        if self.total < 17:
            return 'not allowed to stand!'
        
        else:
            return 'dealer stands!'
        
class Cards:

    def __init__(self,symbol,shape):
        '''Class for defining the structure of the cards'''
        self.shape = shape   #diamond,spade,club
        self.symbol = symbol #ace, king, queen 
        self.value = 0       #the amount the card corresponds to in blackjack 

        if type(self.symbol) ==  int:
            self.value = self.symbol 

        elif self.symbol == 'J' or self.symbol == 'Q' or self.symbol == 'K':
            self.value = 10 

        else:
            self.value = 1  #in this blackjack implementation, the value of ace is 1


class Blackjack:
    '''Game implementation of blackjack'''

    def __init__(self,player,dealer,deck):
        self.player = player 
        self.dealer = dealer 
        self.player_points = 0  #keeps in track of player points 
        self.dealer_points = 0  #keeps in track of dealer points 
        self.current_deck = deck  #the deck which deals the cards 
        self.new_deck = deck      #when the current deck gets completely exhausted, it is replenished



    def gameplay(self,amount,seed=None):
        '''Starting the game!!!'''

        random.seed(seed)
        random.shuffle(self.current_deck)
        '''seed - seed is a function that is used to shuffle the cards in a particular way 
        such that everytime the same number is given as seed, the cards get shuffled in the 
        exact same order. This will help in testing the working of the dp as well as correlate 
        the dynamic programming part of the program and the gaming part '''

        new_start = 52 - len(self.current_deck)  #gives the index of the starting card 

        print('MAXIMUM SCORE POSSIBLE FOR THE PLAYER WITH REMAINING DECK: ',get_score(new_start,seed))
        time.sleep(1)

        '''Bets have been made! Now it is time to deal'''
        for i in range(4):
            '''2 cards are dealt in random'''
            card = self.current_deck.pop()
            if i < 2:
                self.player.hit(card) 

            else:
                self.dealer.hit(card)

        '''The cards have been dealt. Now to display them'''
        self.player.show_cards()
        self.dealer.show_cards()

        '''after dealing, it is the player's turn'''

        player_move = self.player_turn()   #keeps in track of the player's every move 
        dealer_move = self.dealer_turn()   #keeps in track of every dealer's move 

        if player_move == 'OVER' or dealer_move == 'OVER':
            pass 

        else:

            '''The player/dealer keeps hitting and standing till blackjack or bust or both choose to stand'''
            while (player_move != 'Stand' and dealer_move != 'Stand') or player_move != 'OVER' or dealer_move != 'OVER':
                print('\nPLAYER TURN\n')
                player_move = self.player_turn()
                if player_move == 'OVER':
                    break 
                self.player.show_cards()
                print("\n DEALER'S TURN, PLEASE WAIT...\n")
                dealer_move = self.dealer_turn()
                if dealer_move == 'OVER':
                    break
                self.dealer.show_cards()

        print('\nROUND OVER: NOW THE CARDS ARE TO BE REVEALED......\n')
        time.sleep(1)

        self.player.show_cards()
        print()
        self.dealer.show_cards(True)
        print()

        '''Different conditional statements are specified to declare the winner'''

        if self.player.total < 21 and self.player.total > self.dealer.total:
            print('PLAYER WON THIS ROUND! ')
            self.player_points += 1 
            self.player.cash += (2*amount)

        elif self.player.total > 21 and self.dealer.total <= 21:
            print('PLAYER BUSTED!!!')
            self.dealer_points += 1 
            self.dealer.cash += (2*amount)

        elif self.player.total == 21 and (self.dealer.total != 21):
            print('BLACKJACK! PLAYER WON!!')
            self.player_points += 1 
            self.player.cash += (2*amount)

        elif self.dealer.total == 21 and self.player.total != 21:
            print('BLACKJACK! DEALER WON!')
            self.dealer_points += 1 
            self.dealer.cash += (2*amount)

        elif self.player.total < 21 and self.dealer.total > 21:
            print('DEALER BUSTED!')
            self.player_points += 1 
            self.player.cash += (2*amount)

        elif self.dealer.total < 21 and self.player.total < self.dealer.total:
            print('DEALER WON THIS ROUND!')
            self.dealer_points += 1 
            self.dealer.cash += (2*amount)

        print('\n CURRENT SCOREBOARD:  ')
        print('PLAYER POINTS: ',self.player_points)
        print('DEALER POINTS: ',self.dealer_points)
        print()

        print('\n CASH LEFT: ')
        print('PLAYER CASH: ',self.player.cash)
        print('DEALER CASH: ',self.dealer.cash)



        if self.player.cash == 0:
            print('GAME OVER!!! DEALER HAS WON!')

        elif self.dealer.cash == 0:
            print('GAME OVER!! PLAYER HAS WON!')

        else:

            if len(self.current_deck) < 6:
                self.current_deck = self.new_deck  #the deck is replenished 
            play_more = input('Do you want to continue playing? ')
            seed = random.randint(1,200)  #seed for shuffling the deck 
            if play_more == 'yes':
                self.player.reset()  #the player and dealer's cards are reset 
                self.dealer.reset()
                amount = int(input('place your bets: '))
                new_play = self.gameplay(amount,seed)  #the next round begins!
                
                while new_play == 'Low funds':
                      print('CASH LEFT: ',self.player.cash)
                      print('You have insufficient funds. Please place a lower bet\n')

                      amount = int(input('Enter amount: '))
                      new_play = self.gameplay(amount,seed) 

            else:
                if self.player_points > self.dealer_points:
                    print('PLAYER WON!! CONGRATULATIONS!')

                elif self.player_points < self.dealer_points:
                    print('DEALER WON! BETTER LUCK NEXT TIME!') 

        

    def player_turn(self):
        '''Player's turn '''
        if self.player.total >= 21:
            return 'OVER'
        
        
        ask = input('Press H to hit and S to stand')
        if ask == 'H' or ask == 'h':
            '''player chooses to hit'''
            card = self.current_deck.pop()
            self.player.hit(card)

        elif ask == 'S' or ask == 's':
            return 'Stand'

    def dealer_turn(self):

        if self.dealer.total >= 21:
            return 'OVER'
        
        if self.dealer.total < 17:
            card = self.current_deck.pop()
            self.dealer.hit(card)

        else:
            return 'Stand'
            
'''used for getting all 52 cards as a list for the gameplay'''

shapes = ['Diamond','Spade','Club','Heart']
symbols = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']  #the game is played with a deck of cards - 52 in total. 

cards = []   #stores all the cards 


for symbol in symbols:
    for shape in shapes:
        card = Cards(symbol,shape)
        cards.append(card)


'''the functions and classes defined after this use dynamic programming to calculate 
the maximum score that is possible for the user to obtain with the deck given '''
class Deck:
    ''''''

    def __init__(self,seed=None,card = None):
        self.cards = [i for i in range(1,11)]  #only the card values are considered 
        self.cards.extend([10,10,10])
        self.cards = self.cards * 4
        if card is not None:
            self.cards = card

        random.seed(seed)    #also shuffled according to the seed.
        #the seed of these value cards and the gameplay cards is the same to ensure 
        #that the maximum score is being calculated accurately according to the deck 
        random.shuffle(self.cards)

    def deal(self,start,no_of_cards):
        '''dealing the cards. the start refers to the starting index and no_of_cards 
        refers to the number of cards that is dealt'''
        return self.cards[start:start+no_of_cards]

def calculate_max_score(deck, start, scores):
    '''function for calculating the score '''
    player = Player(deck.deal(start, 2))
    dealer = Player(deck.deal(start + 2, 2))
    results = []  #used for storing all possible scores of the player from the given deck of cards 

    for i in range(49 - start):  #iterating through all the remaining undealt cards 
        count = start + 4    #gives the amount of cards that have already been dealt
        player.deal(deck.deal(count, i))  #equivalent to the hit function 
        count += i

        if player.total > 21:
            '''player gets busted and since this is undesirable, backtracking occures and the 
            solution is broken'''
            results.append((-1, count))
            break

        while dealer.total < 17 and count < 52:
            dealer.deal(deck.deal(count, 1))
            count += 1
        if dealer.total > 21:
            results.append((1, count))
        else:
            if player.total > dealer.total:
                results.append((1,count))  #1st element - decides if the player won or lost 
                #2nd element - gives the card index at which the game reached the end 

            elif player.total < dealer.total:
                results.append((-1,count))
                break 

            else:
                results.append((0,count))

    options = []
    #it stores all the scores possible for the player to get 
    for score, next_start in results:
        #score gives the cost of the winnings in the current round 
        #and the score that the player gets in the next game 

        #this is assuming that for each round won - +1
        options.append(score +
                       scores[next_start] if next_start <= 48 else score)
        
        #if the card index is 49 or 50, it indicates the end of the game, the 
        #score is simply the result of the current game 

    scores[start] = max(options)  #the best score is considered 


def get_score(start,seed=None):
    deck = Deck(seed)
    scores = [0 for _ in range(52)]  #keeps in track of all the scores the player can achieve
    #with the given starting index 

    for start in range(48, -1, -1):
        #backward iteration is used as it follows a bottom up dynamic programming approach
        calculate_max_score(deck, start, scores)

    return scores[0]


if __name__ == '__main__':
    seed = random.randint(1,200)

    name = input('Enter your name: ')
    amount = int(input('Enter amount you want to bet: '))
    player1 = Player(name=name)
    dealer = Dealer()
    
    game = Blackjack(player1,dealer,cards)
    game.gameplay(amount,seed)