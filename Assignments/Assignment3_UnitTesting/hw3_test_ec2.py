#########################################
##### Name: Haolin Li #####
##### Uniqname: haolinli#####
#########################################

import random
import unittest

import hw3_cards_ec2 as HW_cards

class TestCard(unittest.TestCase):

    def testRemovePairs(self):
        # initialize the deck and hand
        d1 = HW_cards.Deck()
        d1.shuffle()

        # deal the hand to h1 with tbe deal_hand method
        h1 = HW_cards.Hand(d1.deal_hand(12))
        for i in range(0, len(h1.init_card)):
            print(h1.init_card[i])

        # recording the initial status of h1
        ori_num = len(h1.init_card)
        print("before number:" + str(ori_num))

        # remove the pairs
        removedCards = h1.remove_pairs()

        # recording the afterward status of h1
        aft_num = len(h1.init_card)
        print("after number:" + str(aft_num))

        # testing
        self.assertEqual(ori_num, aft_num + len(removedCards))

    def testDeal(self):
        # initialize the deck
        d1 = HW_cards.Deck()
        d1.shuffle()

        # dealing evenly
        hands1, flag1 = d1.deal(4, 13)
        # dealing unevenly
        hands2, flag2 = d1.deal(5,-1)

        # testing
        self.assertEqual(len(hands1[0]), 52 / 4)



if __name__ == "__main__":
    unittest.main()