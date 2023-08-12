import sys 


def convert_card_names(cards):
    
    """ 
    Convert the name of the cards in the deck to match the names of 
    the individual PNGs.
    format of card names in deck =  ('spades', 'Q') 
                   target format =  Q_of_spades.png
    """
    jdebug = 0
    if jdebug > 0:  print( "convert_card_names() called by: {}".format(sys._getframe(1).f_code.co_name) )
    
    if jdebug > 0:  print("cards = ", cards)
    
    if cards:
        conversions = list(card[1] + "_of_" + card[0] + ".png" for card in cards)
    else:
        # if the cards is empty return 2 face down cards - used for the house before its turn
        conversions = ["back.png","back.png"]
    
    if jdebug > 0:  print("convert_card_names():    conversions = ", conversions)
    
    return conversions
    


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



def get_verdict(player_hand, house_hand):
    """ 
    Passes a verdict based on the hand values of 
    both player and house.
    
    player ->  get_hand_value(player_hand) ->  player_hand_val, player_stat
    house  ->  get_hand_value(house_hand)  ->  house_val, house_stat
    if house_hand empty -> get_hand_value(player_hand) - > 0, 'undecided'
    
    where player_hand_val/house_val is numerical values of the hand and -
    player_stat/house_stat is the status of the hand "BUST, BLACKJACK ..."
    if no verdict were passed then return "undecided"

    """
    jdebug = 0
    if jdebug > 0:  print( "get_verdict() called by: {}".format(sys._getframe(1).f_code.co_name) )
    
    # initialise verdict
    verdict = "undecided"
    
    # fetching house/player data from session
    player_hand_val , player_status = get_hand_value( player_hand )
    house_hand_val , house_status = get_hand_value( house_hand )
    
    if jdebug > 0:
        print("get_verdict():   player_hand_val = ", player_hand_val)
        print("get_verdict():   house_hand_val  = ", house_hand_val)
        print("get_verdict():   player_status   = ", player_status)
        print("get_verdict():   house_status    = ", house_status)
    
    # player stands and no bust/blackjack occurs
    if player_status == "active" and house_status == "active":
        
        # house matches the player hand
        if player_hand_val == house_hand_val:
            verdict = "push"
            
        # player ends up with a higher hand value
        elif player_hand_val > house_hand_val:
            verdict = "player"
        
        # house ends up with a higher hand value
        elif player_hand_val < house_hand_val:
            verdict = "house"
        
        else:
            assert False

    else:

        if player_status != "BUST" and house_status == "empty":
            # at this point house hasnt played its turn yet
            # if player goes BUST, house wins, period!
            verdict = "undecided" 
            
        # if player goes bust or house gets blackjack declare house as winner
        elif player_status == "BUST":
            verdict = "house"
            
        elif house_status == "BUST":
            verdict = "player"
            
        # if both player and house get black jack then PUSH
        elif player_status == "BLACKJACK" and house_status == "BLACKJACK":
            verdict = "push"
            
        # if house goes bust or player gets blackjack declare player as winner
        elif player_status == "BLACKJACK":
            
            verdict = "player" 
            
        # if house goes bust or player gets blackjack declare player as winner
        elif house_status == "BLACKJACK":
            verdict = "house"

        else:
            assert False
    
    if jdebug > 0:  print("get_verdict():   verdict.upper() = ", verdict.upper())
    
    return verdict.upper()
    


def house_plays(deck, player_hand, house_hand):
    
    """ 
        Simulate house playing its turn
        the house will stop pulling cards if one of the 
        conditions given below is met:
        
        - house BUST
        - house gets BLACKJACK
        - house_hand_val is greater than player_hand_value
        - house_hand_val is greater than 18 and player_hand_val is less than 18
        
        house is smart enough to stop pulling when it gets a value higher than what the player 
        has achieved, However, if the player somehow ends up with a higher value than the house, 
        knowing that it has already lost the game, it will risk going bust in efforts of beating the player.
        lets assume the player ends up with "20" and the house with a high "18", now since the house
        has already lost the game, it will pull another card just for the sake of beating the player, 
        in the hopes of pulling a BLACKJACK or PUSH.
    """
    jdebug = 0
    if jdebug > 0:  print( "house_plays() called by: {}".format(sys._getframe(1).f_code.co_name) )
    
    # fetch player hand value out to compare with house's
    player_hand_val , _ = get_hand_value( player_hand )

    while True:
        
        # fetch house data everytime a card is pulled - the first time it gets here, there are 
        # already two cards in house's deck
        house_hand_val , house_game_outcome = get_hand_value( house_hand)
        if jdebug > 0:  print("house_plays(): house_hand = {}, player_hand={}, house_game_outcome= {} ".format(house_hand_val, player_hand_val, house_game_outcome) )
        
        # break out of loop if the ny of these conditions are met
        if (house_game_outcome == "BUST" or 
            house_game_outcome == "BLACKJACK" or 
            house_hand_val >= player_hand_val or 
            (house_hand_val > 16) ):
                        
            if jdebug > 0:  print("house_plays(): outcome = ", house_hand_val, house_game_outcome)
            
            break
        
        house_hand.append(deck.deal())  
        
    return house_hand  



def pick_winner(scores,r):
    """ at the end of the final rounds, pick the winner.
        if noone scores any points, house wins
        if a player scores the highest point, player wins
        if several players score the same highest point, no-one wins """

    # get maximum score attained by the players
    maxScore = max( scores.values()  )     
    winner = ""
    
    # noone has won a single game - declare house as the winner
    if maxScore<(r+1)//2:       
        winner = "house"
    
    # check to see if there is anybody else with the same max score
    else:   # only one person scored the max score!
        winner = max(scores, key= lambda x: scores[x]) # get the player with the highest score
        
    return winner