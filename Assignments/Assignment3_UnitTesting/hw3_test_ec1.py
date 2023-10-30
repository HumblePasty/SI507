#########################################
##### Name: Haolin Li #####
##### Uniqname: haolinli#####
#########################################

import random
import unittest

import hw3_cards_ec1 as HW_cards

class TestCard(unittest.TestCase):
    def testConstructHand(self):
        c1 = HW_cards.Card()
        c2 = HW_cards.Card(1,2)

        cardlist = [c1, c2]
        # create a hand
        h1 = HW_cards.Hand(cardlist)

        # test if card list is properly assigned
        self.assertEqual(h1.init_card, cardlist)
        # test if elements are instance of cards
        self.assertIsInstance(h1.init_card.pop(-1), HW_cards.Card)


    # testing the add and remove method
    def testAddAndRemove(self):
        c1 = HW_cards.Card()
        c2 = HW_cards.Card(1, 2)

        cardlist = [c1, c2]
        h1 = HW_cards.Hand(cardlist)

        # test the Add method
        # first test adding a card that already exists, the number of cards in hand before and after should be the same
        # and the function should execute quietly
        ori_num = len(h1.init_card)
        h1.add_card(c1)
        aft_num = len(h1.init_card)
        self.assertEqual(ori_num, aft_num)

        # then try adding a card that is not in hand
        ori_num = len(h1.init_card)
        h1.add_card(HW_cards.Card(3,12))
        aft_num = len(h1.init_card)
        self.assertEqual(ori_num + 1, aft_num)

        # test the remove method
        # try removing a card that does not exist, number of cards should stay the same
        ori_num = len(h1.init_card)
        h1.remove_card(HW_cards.Card(2,11))
        aft_num = len(h1.init_card)
        self.assertEqual(ori_num, aft_num)

        # try removing a card that does exist, number of cards should be reduced by 1
        ori_num = len(h1.init_card)
        h1.remove_card(c2)
        aft_num = len(h1.init_card)
        self.assertEqual(ori_num, aft_num + 1)


    def testDraw(self):
        c1 = HW_cards.Card()
        c2 = HW_cards.Card(1, 2)

        d1 = HW_cards.Deck()

        cardlist = [c1, c2]
        h1 = HW_cards.Hand(cardlist)

        # draw a card from d1
        h1_ori_num = len(h1.init_card)
        d1_ori_num = len(d1.cards)
        h1.draw(d1)
        h1_aft_num = len(h1.init_card)
        d1_aft_num = len(d1.cards)
        # testing the result
        # the number of cards in hand is increased by 1
        self.assertEqual(h1_ori_num + 1, h1_aft_num)
        # the number of cards in deck is reduced by 1
        self.assertEqual(d1_ori_num, d1_aft_num + 1)



if __name__ == "__main__":
    unittest.main()