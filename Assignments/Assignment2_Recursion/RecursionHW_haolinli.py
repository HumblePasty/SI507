# import packages
from math import *

# Version 1: return only the minimum amount of coins
def change(amount, coins):
    """

    Parameters
    ----------
    amount: int
        the amount of change to be made
    coins: list
        a list of coin values

    Returns
    -------
    int
        the minimum number of coins required to make up the given amount

    """

    # base case 1:
    # if the amount is 0, then obviously the number is 0
    if amount == 0:
        return 0
    # base case 2:
    # if the amount is not zero, but the length of the current coins system is 1
    # that means there is only one way to make change (base case)
    elif len(coins) == 1:
        if amount % coins[0] == 0:
            # if the only way left to change is valid, then return the number
            return amount // coins[0]
        else:
            # if not valid, return inf
            return inf
    else:
        return min(
            # the return value is the minimum result of the two possible calculating method:
            # the changing method that make sure to use the maxmum denomination of the current coin system
            amount // coins[-1] + change(amount % coins[-1], coins[0:-1]),
            # the changing method using all the denominations apart from the maximum one (recursion appear)
            change(amount, coins[0:-1])
        )


# Version 2: return both the number of coins and the coin list
def giveChange(amount, coins):
    """

    Parameters
    ----------
    amount: int
        the amount of change to be made
    coins: list
        a list of coin values

    Returns
    -------
    list
        int
            the minimum number of coins required to make up the given amount
        list
            a list of the coins in that optimal solution

    """

    if amount == 0:
        return [0, []]
    elif len(coins) == 1:
        if amount % coins[0] == 0:
            return [amount // coins[0], [coins[0]] * (amount // coins[0])]
        else:
            return [inf, []]
    else:
        changeCount1 = amount // coins[-1] + giveChange(amount % coins[-1], coins[0:-1])[0]
        changeCount2 = giveChange(amount, coins[0:-1])[0]
        if changeCount1 >= changeCount2:
            return giveChange(amount, coins[0:-1])
        elif changeCount1 < changeCount2:
            return [
                # the number count part of the return
                changeCount1,
                # the list part of the return
                # the added element
                [coins[-1]] * (amount // coins[-1]) +
                # the recursive element
                giveChange(amount % coins[-1], coins[0:-1])[1]
            ]


# main program
coins = [1, 5, 10, 25, 50, 100]
amount = 169

# change function test
print(change(amount, coins))
# giveChange function test
print(giveChange(amount, coins))
