while True:
    # prompting and inputing
    move_input = input("" + "'s move: ")
    # validating
    if len(move_input) != 1 or ord(move_input) > 57 or ord(move_input) < 49:
        print("Please input a VALID number from 1-9")
    # elif ~board[int(move_input)]:
    #     print("This cell is already occupied!")
    else:
        print(int(move_input))
        break