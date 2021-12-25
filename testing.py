import helper_functions as helper


def test_probability():
    # -1 is unopened, [] is not touching a bomb, -2 is flagged
    board = [[-1, -1, -1, -1, -1],
             [-1,  1,  1,  2, -1],
             [-1,  0,  0,  1, -1],
             [-1,  2,  1,  1, -1],
             [-1, -1, -1, -1, -1]]
    bombs = [(0,1), (0,4), (1,4), (4,0), (4,2)]
    square = helper.calculate(board)
    print("square: ", square)
    if square not in bombs:
        print("SUCCESS")
    else:
        print("FAIL")
    
    board = [[-1, -1, -1, -1, -1],
             [-1,  2,  1,  2, -1],
             [-1,  1,  0,  1, -1],
             [-1,  3,  3,  3, -1],
             [-1, -1, -1, -1, -1]]
    bombs = [(2,0), (2,4), (4,1), (4,3), (4,2), (0,2)]
    square = helper.calculate(board)
    print("square: ", square)
    if square not in bombs:
        print("SUCCESS")
    else:
        print("FAIL")

def test_gimmes():
    board = [[ 0,  1, -1, -1, -1],
             [ 1,  2,  2,  2, -1],
             [-1,  1,  1,  1, -1],
             [-1,  2,  1, -1, -1],
             [-1, -1, -1, -1, -1]]
    correct_click = [(4,1), (4,2), (4,3), (1,4), (2,4), (3,4), (3,0), (0,4)]
    print()
    correct_flag = [(0,2), (0,3), (3,3), (4,0), (2,0)]
    to_click, to_flag = helper.gimmes(board)
    a = set(correct_click)
    b = set(to_click)
    if a == b:
        print("Click test passed")
    else:
        if len(a) > len(b):
            print("correct_click has ", a - b)
        else:
            print("to_click has ", b - a)
    a = set(correct_flag)
    b = set(to_flag)
    if a == b:
        print("Click test passed")
    else:
        if len(a) > len(b):
            print("correct_flag has ", a - b)
        else:
            print("to_flag has ", b - a)


def main():
    print("select which test to run")
    selection = input("1: probability\n2: gimmes\n")
    if selection == "1":
        test_probability()
    elif selection == "2":
        test_gimmes()
    else:
        print("invalid selection")
        
if __name__ == "__main__":
    main()