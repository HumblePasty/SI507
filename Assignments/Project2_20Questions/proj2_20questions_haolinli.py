#
# Name: Haolin Li (haolinli@umich.edu)
# Date: 11/29/2023
#

#
# Support functions for the 20 Questions problem
#
def printTree(tree, prefix='', bend='', answer=''):
    """Recursively print a 20 Questions tree in a human-friendly form.
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch."""
    text, left, right = tree
    if left is None and right is None:
        print(f'{prefix}{bend}{answer}It is {text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "Yes: ")
        printTree(right, prefix, '`-', "No:  ")

#
# The following two trees are useful for testing.
#


def main():
    """
    The main function for the program.
    """
    # Write the "main" function for 20 Questions here.  Although
    # main() is traditionally placed at the top of a file, it is the
    # last function you will write.

    smallTree = \
        ("Is it bigger than a breadbox?",
         ("an elephant", None, None),
         ("a mouse", None, None)
         )
    mediumTree = \
        ("Is it bigger than a breadbox?",
         ("Is it gray?",
          ("an elephant", None, None),
          ("a tiger", None, None)),
         ("a mouse", None, None))

    saveTree(mediumTree, "proj2_tree.txt")

    # 1. Simple play with the small tree
    print("----------1. Simple play with the small tree----------")
    simple_result = simplePlay(smallTree)
    print(f"simplePlay result: {simple_result}\n")

    # 2. Advanced play with the medium tree
    print("----------2. Advanced play with the medium tree----------")
    newMediumTree = play(mediumTree)
    # print the new tree
    print("----------The new tree----------")
    printTree(newMediumTree)

    # 3. Play with the tree loaded from file
    print("----------3. Play with the tree loaded from file----------")
    newTree = playFromFile()
    # print the new tree
    print("----------The new tree----------")
    printTree(newTree)


def simplePlay(tree):
    """ Simple play with the tree inputed

    Parameters
    ----------
    tree: object
        the tree to play with

    Returns
    -------
    object: a new tree that is the result of playing the game
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
    """ Simple play with the tree inputed

    Parameters
    ----------
    tree: object
        the tree to play with

    Returns
    -------
    bool: whether the computer have guessed correctly
    """

    def update_tree(cur, path, new_question, newObject, yes_for_newObject):
        """ Update the tree
        Parameters
        ----------
        cur: object
            the current node
        path: list
            the path to the current node
        new_question: str
            the new question
        newObject: str
            the new object
        yes_for_newObject: bool
            whether the answer for the new object is yes

        Returns
        -------
        object: a new tree that is the result of playing the game
        """
        if path:
            direction = path.pop(0)
            if direction == 'y':
                updated_subtree = update_tree(cur[1], path, new_question, newObject, yes_for_newObject)
                return (cur[0], updated_subtree, cur[2])
            else:
                updated_subtree = update_tree(cur[2], path, new_question, newObject, yes_for_newObject)
                return (cur[0], cur[1], updated_subtree)
        else:
            if yes_for_newObject:
                return (new_question, (newObject, None, None), cur)
            else:
                return (new_question, cur, (newObject, None, None))

    print("Think of an object...\n")
    cur = tree
    path = []  # the path to the current node
    while True:
        if cur[1] is None and cur[2] is None:
            while True:
                print(f"Is it {cur[0]}?")
                answer = input("(y/n) ")
                if answer == 'y':
                    print("I got it!")
                    return tree
                elif answer == 'n':
                    print("You win!")
                    print("What animal were you thinking of?")
                    newObject = input("Enter the name of the object: ")
                    print(f"What is the question that would distinguish between {newObject} and {cur[0]}?")
                    newQuestion = input("Enter the question: ")
                    while True:
                        print(f"What is the answer for {newObject}?")
                        answer = input("(y/n) ")
                        if answer == 'y':
                            # adjust the tree
                            return update_tree(tree, path, newQuestion, newObject, True)
                        elif answer == 'n':
                            return update_tree(tree, path, newQuestion, newObject, False)
                else:
                    print("Please enter y or n.")
        answer = input(f"{cur[0]} (y/n) ")
        if answer == 'y':
            path.append('y')
            cur = cur[1]
        elif answer == 'n':
            path.append('n')
            cur = cur[2]
        else:
            print("Please enter y or n.")


def playFromFile(filename="proj2_tree.txt"):
    """ Simple play with the tree loaded from a file and save it back

    Parameters
    ----------
    filename: str
        The name of the file to load and save the tree.
    """
    # Load the tree from file
    tree = loadTree(filename)

    def update_tree(cur, path, new_question, newObject, yes_for_newObject):
        """ Update the tree
        Parameters
        ----------
        cur: object
            the current node
        path: list
            the path to the current node
        new_question: str
            the new question
        newObject: str
            the new object
        yes_for_newObject: bool
            whether the answer for the new object is yes

        Returns
        -------
        object: a new tree that is the result of playing the game
        """
        if path:
            direction = path.pop(0)
            if direction == 'y':
                updated_subtree = update_tree(cur[1], path, new_question, newObject, yes_for_newObject)
                return (cur[0], updated_subtree, cur[2])
            else:
                updated_subtree = update_tree(cur[2], path, new_question, newObject, yes_for_newObject)
                return (cur[0], cur[1], updated_subtree)
        else:
            if yes_for_newObject:
                return (new_question, (newObject, None, None), cur)
            else:
                return (new_question, cur, (newObject, None, None))

    print("Think of an object...\n")
    cur = tree
    path = []  # the path to the current node
    while True:
        if cur[1] is None and cur[2] is None:
            while True:
                print(f"Is it {cur[0]}?")
                answer = input("(y/n) ")
                if answer == 'y':
                    print("I got it!")
                    return tree
                elif answer == 'n':
                    print("You win!")
                    print("What animal were you thinking of?")
                    newObject = input("Enter the name of the object: ")
                    print(f"What is the question that would distinguish between {newObject} and {cur[0]}?")
                    newQuestion = input("Enter the question: ")
                    while True:
                        print(f"What is the answer for {newObject}?")
                        answer = input("(y/n) ")
                        if answer == 'y':
                            # adjust the tree
                            updated_tree = update_tree(tree, path, newQuestion, newObject, True)
                            print("saving new tree...")
                            saveTree(updated_tree, filename)
                            return updated_tree
                        elif answer == 'n':
                            updated_tree = update_tree(tree, path, newQuestion, newObject, False)
                            print("saving new tree...")
                            saveTree(updated_tree, filename)
                            return updated_tree
                else:
                    print("Please enter y or n.")
        answer = input(f"{cur[0]} (y/n) ")
        if answer == 'y':
            path.append('y')
            cur = cur[1]
        elif answer == 'n':
            path.append('n')
            cur = cur[2]
        else:
            print("Please enter y or n.")


def saveTree(tree, filename):
    """ Save the tree structure to a file.

    Parameters
    ----------
    tree: tuple
        The tree to save.
    filename: str
        The name of the file to save the tree to.
    """

    def saveNode(node, file, indent=""):
        if node[1] is None and node[2] is None:  # Leaf node
            file.write(f"{indent}Leaf\n{indent}{node[0]}\n")
        else:
            file.write(f"{indent}Internal node\n{indent}{node[0]}\n")
            saveNode(node[1], file, indent + "    ")
            saveNode(node[2], file, indent + "    ")

    with open(filename, 'w') as file:
        saveNode(tree, file)


def loadTree(filename):
    """ Load a tree structure from a file.

    Parameters
    ----------
    filename: str
        The name of the file to load the tree from.

    Returns
    -------
    tuple: The loaded tree structure.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    def parseNode(lines):
        """ Parse a node from the lines read from file

        Parameters
        ----------
        lines: list
            the lines read from file

        Returns
        -------
        tuple:
            the node parsed as tree structure

        """

        if not lines:
            # return None if there is no line
            return None, []

        line = lines.pop(0).strip() # strp to remove the spaces and \n
        if line == "Leaf":
            # if it is a leaf node, return the object
            return (lines.pop(0).strip(), None, None), lines
        elif line == "Internal node":
            # if it is an internal node, parse recursively
            question = lines.pop(0).strip()
            yes_node, lines = parseNode(lines)
            no_node, lines = parseNode(lines)
            return (question, yes_node, no_node), lines

    tree, _ = parseNode(lines)
    return tree


#
# The following two-line "magic sequence" must be the last thing in
# your file.  After you write the main() function, this line it will
# cause the program to automatically play 20 Questions when you run
# it.
#
if __name__ == '__main__':
    main()
