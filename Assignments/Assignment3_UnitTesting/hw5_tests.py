#########################################
##### Name: Haolin Li #####
##### Uniqname: haolinli#####
#########################################

import random
import unittest

import hw5_cards as HW_cards

class TestCard(unittest.TestCase):

    def test_construct_Card(self):
        c1 = HW_cards.Card(0, 2)
        c2 = HW_cards.Card(1, 1)

        self.assertEqual(c1.suit, 0)
        self.assertEqual(c1.suit_name, "Diamonds")
        self.assertEqual(c1.rank, 2)
        self.assertEqual(c1.rank_name, "2")

        self.assertIsInstance(c1.suit, int)
        self.assertIsInstance(c1.suit_name, str)
        self.assertIsInstance(c1.rank, int)
        self.assertIsInstance(c1.rank_name, str)

        self.assertEqual(c2.suit, 1)
        self.assertEqual(c2.suit_name, "Clubs")
        self.assertEqual(c2.rank, 1)
        self.assertEqual(c2.rank_name, "Ace")

    def test_q1(self):
        '''
        1. fill in your test method for question 1:
        Test that if you create a card with rank 12, its rank_name will be "Queen"

        2. remove the pass command

        3. uncomment the return command and
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''

        # Create a card
        c1 = HW_cards.Card(0, 12)
        self.assertEqual(c1.rank_name, "Queen")

        return c1.rank_name, "Queen"

    def test_q2(self):
        '''
        1. fill in your test method for question 1:
        Test that if you create a card instance with suit 1, its suit_name will be "Clubs"
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''

        c1 = HW_cards.Card(1, )
        self.assertEqual(c1.suit_name, 'Clubs')

        return c1.suit_name, "Clubs"

    def test_q3(self):
        '''
        1. fill in your test method for question 3:
        Test that if you invoke the __str__ method of a card instance that is created with suit=3, rank=13, it returns the string "King of Spades"

        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''

        c1 = HW_cards.Card(3, 13)
        self.assertEqual(c1.__str__(), "King of Spades")

        return c1.__str__(), "King of Spades"

    def test_q4(self):
        '''
        1. fill in your test method for question 4:
        Test that if you create a deck instance, it will have 52 cards in its cards instance variable
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''

        d1 = HW_cards.Deck()
        # whether the deck has 52 instances
        self.assertEqual(len(d1.cards), 52)
        # whether the items are in instance of cards
        # deal a random card
        # c1 = d1.deal_card(random.randint(0,51))
        # self.assertIsInstance(c1, HW_cards.Card)

        return len(d1.cards), 52
        # return len(d1.cards), 52, type(c1), HW_cards.Card

    def test_q5(self):
        '''
        1. fill in your test method for question 5:
        Test that if you invoke the deal_card method on a deck, it will return a card instance.
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''

        d1 = HW_cards.Deck()
        # deal a random card
        c1 = d1.deal_card(random.randint(0, 51))
        self.assertIsInstance(c1, HW_cards.Card)

        return c1, HW_cards.Card

    def test_q6(self):
        '''
        1. fill in your test method for question 6:
        
        Test that if you invoke the deal_card method on a deck, the deck has one fewer cards in it afterward.
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''

        d1 = HW_cards.Deck()
        ori_len = len(d1.cards)

        # deal a random card
        c1 = d1.deal_card(random.randint(0, 51))
        # record the number of cards afterward
        aft_len = len(d1.cards)
        # altering the line to fit the autograder
        self.assertEqual(aft_len, ori_len - 1)

        return aft_len, ori_len - 1

    def test_q7(self):
        '''
        1. fill in your test method for question 7:
        Test that if you invoke the replace_card method, the deck has one more card in it afterwards. (Please note that you want to use deal_card function first to remove a card from the deck and then add the same card back in)
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''

        # init deck
        d1 = HW_cards.Deck()
        # remove a card randomly
        c1 = d1.deal_card()
        # record the removed number
        ori_num = len(d1.cards)

        # replace the card
        d1.replace_card(c1)
        aft_num = len(d1.cards)

        # assertation
        expectedDiff = 1
        # self.assertEqual(aft_num - ori_num, expectedDiff)

        # altering the line to fit the autograder...
        self.assertEqual(ori_num + 1, aft_num)

        return ori_num + 1, aft_num

    def test_q8(self):
        '''
        1. fill in your test method for question 8:
        Test that if you invoke the replace_card method with a card that is already in the deck, the deck size is not affected.(The function must silently ignore it if you try to add a card that’s already in the deck)

        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''

        # init deck
        d1 = HW_cards.Deck()
        c1 = HW_cards.Card()

        # original size
        ori_num = len(d1.cards)

        # try inserting an existing card and catch errors
        try:
            d1.replace_card(c1)
        except:
            print("error trying inserting cards!")
        # afterward size
        aft_num = len(d1.cards)

        # assertation
        self.assertEqual(ori_num, aft_num)

        return ori_num, aft_num


if __name__ == "__main__":
    unittest.main()
