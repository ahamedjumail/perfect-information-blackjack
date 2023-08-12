import unittest
import app


class TestApp(unittest.TestCase):
    """ 
    test suite for the game of blackjack
    """
    

    def test_card_names_conversion(self):
        """
        Tests for: 
            house's face-down cards
            card name conversion
            card numbers after conversion
        """
        
        faceDown_cards = app.convert_card_names([])  
        cards = app.convert_card_names( [('spades', 'Q'), ('hearts', '2'), ('diamonds', 'A')] ) 
        
        # check for two face-down cards being returned if no cards given
        self.assertEqual(faceDown_cards, ["back.png","back.png"], "incorrect cards returned" )
        self.assertEqual(len(faceDown_cards), 2, "incorrect number of cards returned" )
        self.assertNotEqual(len(faceDown_cards), 1, "incorrect cards returned" )
        # check for card names conversion
        self.assertEqual(len(cards), 3, "incorrect number of cards returned" )
        self.assertEqual(cards, ["Q_of_spades.png","2_of_hearts.png","A_of_diamonds.png"], "card names incorrectly converted" )


        
    def test_deck(self):
        """
        Tests for:
            correct number of cards per added deck - 52 cards for each deck
            cards being removed(popped) from the deck after being dealt
            cards being converted properly after being dealt - similar to "test_card_names_conversion"
            cards reset to the right number
        """
        # create decks
        deck1 = app.Deck()    # one deck - 52 cards
        deck2 = app.Deck(2)   # two decks - 104 cards
        deck3 = app.Deck(3)   # three decks - 156 cards
        deck4 = app.Deck(4)   # four decks - 208 cards
        deck5 = app.Deck(5)   # five decks - 260 cards
        
        # check for correct number of cards per added deck
        self.assertEqual(len(deck1.deck),  52, "incorrect number of cards in the deck" )
        self.assertEqual(len(deck2.deck), 104, "incorrect number of cards in the deck" )
        self.assertEqual(len(deck3.deck), 156, "incorrect number of cards in the deck" )
        self.assertEqual(len(deck4.deck), 208, "incorrect number of cards in the deck" )
        self.assertEqual(len(deck5.deck), 260, "incorrect number of cards in the deck" )
        
        card = deck2.deal(2) # deal 2 cards
        converted_card = app.convert_card_names( card ) # convert two cards
        self.assertEqual(len(deck2.deck ),  102, "cards not being popped after being dealt")
        self.assertNotIn(card,  deck2.deck, "cards shouldnt be still in the deck since it was dealt")
        self.assertEqual(len(converted_card), len(card), "same number of cards should presist after conversion")
        
        # all in one go
        converted_card = app.convert_card_names( [deck1.deal()] )  # deal one card and convert
        self.assertEqual(len(deck1.deck ),  51, "cards not being popped after being dealt")
        
        
        deck2.reset()   # reset deck2 - resorting to its original state of 104 cards
        self.assertEqual(len(deck2.deck ),  104, "deck not being reset to their default number of cards")
        
    
    
    def test_hand_value(self):
        """ Tests for:
                hand value
                the hand status: BUST, BLACKJACK or active
                aces addressed - crude analysis, if hand will go bust after card addition, consider the currently 
                held ace in hand as 1
        """
        
        hand_bust =      [("diaminds", "K"), ("clubs","Q"), ("hearts","6")] 
        hand_blackjack = [("diaminds", "9"),("diamonds","J"),("hearts", "2")]  
        hand_active =    [("hearts", "4"), ("clubs","10"), ("hearts","5")] 
        hand_aces1 =     [("clubs","A"), ("spades","9")] 
        hand_aces2 =     [("clubs","A"), ("spades","9"), ("diamonds","A")] 

        
        hand_val, hand_status = app.get_hand_value( hand_bust )
        self.assertGreater(hand_val,  21, "BUST miscalculation" )
        self.assertEqual(hand_status,  "BUST", "BUST status logic got it wrong" )       
        
        hand_val, hand_status = app.get_hand_value( hand_blackjack )
        self.assertEqual(hand_val,  21, "blackjack miscalculation" )
        self.assertEqual(hand_status,  "BLACKJACK", "BLACKJACK status logic got it wrong" )
        
        hand_val, hand_status = app.get_hand_value( hand_active )
        self.assertLess(hand_val,  21, "ACTIVE miscalculation" )
        self.assertEqual(hand_status,  "active", "ACTIVE status logic got it wrong" ) 
        
        hand_val, hand_status = app.get_hand_value( hand_aces1 )
        self.assertEqual(hand_val,  20, "ACE not being counted as 11" )
        self.assertEqual(hand_status,  "active", "ACTIVE status logic got it wrong" ) 
        
        hand_val, hand_status = app.get_hand_value( hand_aces2 )
        self.assertEqual(hand_val,  21, "existing ACE not being addressed" )
        self.assertEqual(hand_status,  "BLACKJACK", "BLACKJACK status logic got it wrong" )
 
 
    
    def test_get_verdict(self):
        """ tests to see if the program passes the right judgement """
        
        # Scenario 1 - verdict HOUSE: player goes BUST
        player_hand =   [("diaminds", "K"), ("clubs","Q"), ("hearts","6")] 
        house_hand =    [] 
        verdict = app.get_verdict(player_hand, house_hand)
        self.assertEqual(verdict,  "HOUSE", "verdict SHOULD have been HOUSE" )
        
        # Scenario 2 - verdict PUSH: player gets blackjack - house gets blackjack
        player_hand =   [("diaminds", "9"),("diamonds","J"),("hearts", "2")]  
        house_hand =    [("clubs","A"), ("spades","9"), ("diamonds","A")]  
        verdict = app.get_verdict(player_hand, house_hand)        
        self.assertEqual(verdict,  "PUSH", "verdict SHOULD have been PUSH" )
        
        # Scenario 3 - verdict PLAYER: player gets blackjack - house goes BUST
        player_hand =   [("diaminds", "9"),("diamonds","J"),("hearts", "2")]  
        house_hand =    [("diaminds", "K"), ("clubs","Q"), ("hearts","6")] 
        verdict = app.get_verdict(player_hand, house_hand)        
        self.assertEqual(verdict,  "PLAYER", "verdict SHOULD have been PLAYER" )

        # Scenario 4 - verdict PUSH: player has value equal to house value  
        player_hand =   [("clubs","A"), ("spades","9")]  
        house_hand =    [("diaminds", "K"), ("clubs","5"), ("hearts","5")] 
        verdict = app.get_verdict(player_hand, house_hand)        
        self.assertEqual(verdict,  "PUSH", "verdict SHOULD have been PUSH" )

        # Scenario 5 - verdict PLAYER: player has value greater than house value
        player_hand =   [("clubs","A"), ("spades","9")]  
        house_hand =    [("diaminds", "K"), ("clubs","5")] 
        verdict = app.get_verdict(player_hand, house_hand)        
        self.assertEqual(verdict,  "PLAYER", "verdict SHOULD have been PLAYER" )
        
        # Scenario 6 - verdict HOUSE: player has value less than house value
        player_hand =   [("diaminds", "K"), ("clubs","5")] 
        house_hand =    [("clubs","A"), ("spades","9")]  
        verdict = app.get_verdict(player_hand, house_hand)        
        self.assertEqual(verdict,  "HOUSE", "verdict SHOULD have been HOUSE" )
        
        # Scenario 7 - verdict HOUSE: player has value - house gets blackjack
        player_hand =   [("clubs","A"), ("spades","9")] 
        house_hand =    [("diaminds", "9"),("diamonds","J"),("hearts", "2")]   
        verdict = app.get_verdict(player_hand, house_hand)        
        self.assertEqual(verdict,  "HOUSE", "verdict SHOULD have been HOUSE" )
        
        # Scenario 8 - verdict PLAYER: player has value - house goes bust
        player_hand =   [("clubs","A"), ("spades","9")] 
        house_hand =    [("diaminds", "K"), ("clubs","Q"), ("hearts","6")]   
        verdict = app.get_verdict(player_hand, house_hand)        
        self.assertEqual(verdict,  "PLAYER", "verdict SHOULD have been PLAYER" )


    

        
        
    
if __name__ == "__main__":
    unittest.main()