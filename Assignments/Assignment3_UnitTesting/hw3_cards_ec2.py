import random

VERSION = 0.01


class Card:
    '''a standard playing card
    cards will have a suit and a rank
    Class Attributes
    ----------------
    suit_names: list
        the four suit names in order
        0:Diamonds, 1:Clubs, 2: Hearts, 3: Spades

    faces: dict
        maps face cards' rank name
        1:Ace, 11:Jack, 12:Queen,  13:King
    Instance Attributes
    -------------------
    suit: int
        the numerical index into the suit_names list
    suit_name: string
        the name of the card's suit
    rank: int
        the numerical rank of the card
    rank_name: string
        the name of the card's rank (e.g., "King" or "3")
    '''
    suit_names = ["Diamonds", "Clubs", "Hearts", "Spades"]
    faces = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.suit_name = Card.suit_names[self.suit]

        self.rank = rank
        if self.rank in Card.faces:
            self.rank_name = Card.faces[self.rank]
        else:
            self.rank_name = str(self.rank)

    def __str__(self):
        return f"{self.rank_name} of {self.suit_name}"


class Deck:
    '''a deck of Cards
    Instance Attributes
    -------------------
    cards: list
        the list of Cards currently in the Deck. Initialized to contain
        all 52 cards in a standard deck
    '''

    def __init__(self):

        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)  # appends in a sorted order

    def deal_card(self, i=-1):
        '''remove a card from the Deck
        Parameters
        -------------------
        i: int (optional)
            the index of the ard to remove. Default (-1) will remove the "top" card
        Returns
        -------
        Card
            the Card that was removed
        '''
        return self.cards.pop(i)

    def shuffle(self):
        '''shuffles (randomizes the order) of the Cards
        self.cards is modified in place
        Parameters
        ----------
        None
        Returns
        -------
        None
        '''
        random.shuffle(self.cards)

    def replace_card(self, card):
        card_strs = []  # forming an empty list
        for c in self.cards:  # each card in self.cards (the initial list)
            card_strs.append(c.__str__())  # appends the string that represents that card to the empty list
        if card.__str__() not in card_strs:  # if the string representing this card is not in the list already
            self.cards.append(card)  # append it to the list

    def sort_cards(self):
        '''returns the Deck to its original order

        Cards will be in the same order as when Deck was constructed.
        self.cards is modified in place.
        Parameters
        ----------
        None
        Returns
        -------
        None
        '''
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def deal_hand(self, hand_size):
        '''removes and returns hand_size cards from the Deck

        self.cards is modified in place. Deck size will be reduced
        by hand_size
        Parameters
        -------------------
        hand_size: int
            the number of cards to deal
        Returns
        -------
        list
            the top hand_size cards from the Deck
        '''
        hand_cards = []
        for i in range(hand_size):
            hand_cards.append(self.deal_card())
        return hand_cards

    def deal(self, numhand, handsize=-1):
        """
        deal the deck

        Parameters
        ------
        numhand: int
            the number of hands to be dealt
        handsize: int
            the handsize of the hands, -1 means

        Returns
        -------
        List
            a list of hands
        Boolean
            whether the deck is dealt evenly or not
        """

        # create a list of hands
        hands = [Hand() for _ in range(numhand)]
        # a flag that specify whether the deck is dealt evenly or not
        flag = False
        if handsize == -1:
            # if the handsize is set to -1, deal unevenly
            flag = False
            for i in range(len(self.cards) // numhand):
                for j in range(numhand):
                    hands[j].add_card(self.deal_card())
            # handle the rest of the cards
            for i in range(len(self.cards)):
                hands[i].add_card(self.deal_card())
        elif handsize * numhand <= len(self.cards):
            # else, deal evenly
            flag = True
            for i in range(len(self.cards) // numhand):
                for j in range(numhand):
                    currentHand = hands[j]
                    currentCard = self.deal_card()
                    currentHand.add_card(currentCard)
        else:
            print("Limit exceeded!")

        return hands, flag


def print_hand(hand):
    '''prints a hand in a compact form

    Parameters
    -------------------
    hand: list
        list of Cards to print
    Returns
    -------
    none
    '''
    hand_str = '/ '
    for c in hand:
        s = c.suit_name[0]
        r = c.rank_name[0]
        hand_str += r + "of" + s + ' / '
    print(hand_str)


# create the Hand with an initial set of cards
class Hand:
    '''a hand for playing card
    Class Attributes
    ----------------
    None
    Instance Attributes
    -------------------
    init_card: list
    a list of cards
    '''

    def __init__(self, init_cards=[]):
        self.init_card = init_cards

    def add_card(self, card):
        '''add a card
        add a card to the hand
        silently fails if the card is already in the hand
        Parameters
        -------------------
        card: instance
        a card to add
        Returns
        -------
        None
        '''
        card_strs = []  # forming an empty list
        for c in self.init_card:  # each card in self.cards (the initial list)
            card_strs.append(c.__str__())  # appends the string that represents that card to the empty list
        if card.__str__() not in card_strs:  # if the string representing this card is not in the list already
            self.init_card.append(card)  # append it to the list

    def remove_card(self, card):
        '''remove a card from the hand
        Parameters
        -------------------
        card: instance
            a card to remove
        Returns
        -------
        the card, or None if the card was not in the Hand
        '''
        cards_strs = []
        for c in self.init_card:
            cards_strs.append(c.__str__())
        if card.__str__() in cards_strs:
            # pop the card
            self.init_card.pop(cards_strs.index(card.__str__()))
            return card
        else:
            return None

    def draw(self, deck):
        '''draw a card
        draw a card from a deck and add it to the hand
        side effect: the deck will be depleted by one card
        Parameters
        -------------------
        deck: instance
        a deck from which to draw
        Returns
        -------
        None
        '''

        dw_card = deck.deal_card(random.randint(0, len(deck.cards)))
        self.init_card.append(dw_card)

    def remove_pairs(self):
        """
        remove all the pair from the current hand
        Returns
        -------
        list
            a list for all the cards (pairs) removed
        """
        pairs_removed = []
        # go through all the ranks to search for pairs
        for i in range(1, 14):
            # create a list for the cards with this rank
            cards_temp = [card for card in self.init_card if card.rank == i]
            if len(cards_temp) >= 2:
                # remove the cards, the first two
                pairs_removed.append(self.remove_card(cards_temp[0]))
                pairs_removed.append(self.remove_card(cards_temp[1]))
            else:
                continue

        return pairs_removed
