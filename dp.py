from testt_dpp import Deck,Player 

def calculate_max_score(deck, start,scores):
    '''function for calculating the score '''
    player = Player(deck.deal(start,1))
    dealer = Player(deck.deal(start + 1, 1))
    player.deal(deck.deal(start+2,1))
    dealer.deal(deck.deal(start+3,1))
    results = []  #used for storing all possible scores of the player from the given deck of cards 
    action_player = []
    for i in range(49 - start):  #iterating through all the remaining undealt cards
        count = start + 4
        #gives the amount of cards that have already been dealt
        if count>52 or player.total>21:
            break
        for hits in range(i):
            player.deal(deck.deal(count, 1))  #equivalent to the hit function 
            count += 1

            if count>52 or player.total>21:
                break

            if dealer.total < 17:
                dealer.deal(deck.deal(count,1))
                count+=1
        
        if player.total > 21:
                '''player gets busted and since this is undesirable, backtracking occures and the 
                solution is broken'''
                results.append((-1, count,i))

            
        while dealer.total < 17 and count < 52:
                dealer.deal(deck.deal(count, 1))
                count += 1
        if dealer.total > 21:
                results.append((1, count,i))
                action_player.append(i)
        else:
            if player.total > dealer.total:
                results.append((1,count,i))  #1st element - decides if the player won or lost 
                    #2nd element - gives the card index at which the game reached the end 
                action_player.append(i)
                    
                
            elif player.total < dealer.total:
                results.append((-1,count,i))
                 

            else:
                results.append((0,count,i))
    options = []
    #it stores all the scores possible for the player to get 
    for score, next_start,hits in results:
        #score gives the cost of the winnings in the current round 
        #and the score that the player gets in the next game 

        #this is assuming that for each round won - +1
        options.append((score +
                       scores[next_start][0] if next_start <= 48 else score,hits))
        
        #if the card index is 49 or 50, it indicates the end of the game, the 
        #score is simply the result of the current game 


    #the best score is considered
    scores[start] = options[0]
    for i in options:
        if scores[start][0]<i[0]:
            scores[start] = i

def get_score(starti,deck,seed=None):
    
    scores = [0 for _ in range(52)]  #keeps in track of all the scores the player can achieve
    #with the given starting index 
    f= {}
    for start in range(48, -1, -1):
        #backward iteration is used as it follows a bottom up dynamic programming approach
        f[start]=(calculate_max_score(deck, start,scores))

    return scores[starti]


def simulate(start,w,h):
    for i in range(w):
        if start>48:
            break
        s, h = get_score(start,deck)
        player = Player(deck.deal(start,1))
        player.name = 'player'
        
        dealer = Player(deck.deal(start + 1, 1),'dealer')

        player.deal(deck.deal(start+2,1))
        dealer.deal(deck.deal(start+3,1))
        start+=4
        if h == 0 :
            while dealer.total<17:
                dealer.deal(deck.deal(start,1))
                start+=1
        for i in range(h):
            player.deal(deck.deal(start,1))
            start+=1
            if start>52:
                break
            if dealer.total < 17 and start<52:
                        dealer.deal(deck.deal(start,1))
                        start+=1
                
        player.show_cards()
        dealer.show_cards()
        win = 0
        los = 0
        if (player.total>dealer.total and player.total<22) or (dealer.total>21 and player.total<=21):
            print("Win")
            win = win+1
        elif (dealer.total>player.total and dealer.total<22) or (player.total>21 and dealer.total<=21):
            print("Lost")
            los = los+1
        else:print("Draw")
        print()
    return


#simulation
if __name__=="__main__":
    deck = Deck()

    start = 0
    w,h = get_score(start,deck)

    simulate(12,w,h)
