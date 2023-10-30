# from math import *
# coins = [1, 3, 16, 30, 50]
# amount = 116
# def change(amount, coins):
#     """
#
#     Parameters
#     ----------
#     amount: int
#         the amount of change to be made
#     coins: list
#         a list of coin values
#
#     Returns
#     -------
#     int
#         the minimum number of coins required to make up the given amount
#
#     """
#
#     # if the amount is 0, then obviously the number is 0
#     if amount == 0:
#         return 0
#     # if the amount is not zero, but the length of the current coins system is 1
#     # that means there is only one way to make change (base case)
#     elif len(coins) == 1:
#         if amount % coins[0] == 0:
#             # if the only way left to change is valid, then return the number
#             return amount / coins[0]
#         else:
#             # if not valid, return inf
#             return inf
#     else:
#         return min(  # the return value is the minimum of the two possible method:
#             # the changing method that make sure to use the maxmum denomination of the current coin system
#             amount // coins[-1] + change(amount % coins[-1], coins[0:-1]),
#             # the changing method using all the denominations apart from the maximum one (recursion appear)
#             change(amount, coins[0:-1])
#         )
#
# testlist = [0,[0]]
# print(testlist[1])
# # print(change(amount, coins))

seq = [0,[0]]
print(seq[0])