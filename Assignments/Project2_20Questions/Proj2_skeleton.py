#
# Name: Haolin Li
#

from Proj2_tree import printTree

#
# The following two trees are useful for testing.
#
smallTree = \
    ("Is it bigger than a breadbox?",
     ("an elephant", None, None),
     ("a mouse", None, None))
mediumTree = \
    ("Is it bigger than a breadbox?",
     ("Is it gray?",
      ("an elephant", None, None),
      ("a tiger", None, None)),
     ("a mouse", None, None))


def main():
    """DOCSTRING!"""
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.
    simplePlay(mediumTree)


def simplePlay(tree):
    """ Simple play with the tree inputed

    Parameters
    ----------
    tree: object
        the tree to play with

    Returns
    -------
    bool: whether the computer have guessed correctly
    """

    print("Think of an animal...\n")
    cur = tree
    while True:
        if cur[1] is None and cur[2] is None:
            while True:
                print(f"Is it {cur[0]}?")
                answer = input("(y/n) ")
                if answer == 'y':
                    print("I win!")
                    return True
                elif answer == 'n':
                    print("You win!")
                    return False
                else:
                    print("Please enter y or n.")
        answer = input(f"{cur[0]} (y/n) ")
        if answer == 'y':
            cur = cur[1]
        elif answer == 'n':
            cur = cur[2]
        else:
            print("Please enter y or n.")


def play(tree):
    """DOCSTRING!"""


#
# The following two-line "magic sequence" must be the last thing in
# your file.  After you write the main() function, this line it will
# cause the program to automatically play 20 Questions when you run
# it.
#
if __name__ == '__main__':
    main()
