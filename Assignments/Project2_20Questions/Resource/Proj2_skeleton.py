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
    """
    printTree(tree)
    pass


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
