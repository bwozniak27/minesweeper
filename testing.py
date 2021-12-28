from helper_functions import Minesweeper

        
def gimme_printing(correct, output, test):
    a = set(correct)
    b = set(output)
    test_num = str(test).split('.')[0]
    test_type = str(test).split('.')[1]
    print(f'test {test_num}:')
    if a == b:
        print(f'{"click" if test_type == "1" else "flag"} test passed')
    else:
        if len(a) > len(b):
            print(f'correct {"click" if test_type == "1" else "flag"} has {a - b}')
        else:
            print(f'to {"click" if test_type == "1" else "flag"} has {b - a}')
    print("")

def test_gimmes():
    test = Minesweeper()
    # test 1
    board = [[ 0,  1, -1, -1, -1],
             [ 1,  2,  2,  2, -1],
             [-1,  1,  1,  1, -1],
             [-1,  2,  1, -1, -1],
             [-1, -1, -1, -1, -1]]
    correct_click = [(4,1), (4,2), (4,3), (1,4), (2,4), (3,4), (3,0), (0,4)]
    correct_flag = [(0,2), (0,3), (3,3), (4,0), (2,0)]
    test.set_board(board)
    to_click, to_flag = test.gimmes()
    gimme_printing(correct_click, to_click, 1.1)
    gimme_printing(correct_flag, to_flag, 1.2)
    
    # test 2
    board = [[-2, -1],
             [ 3, -1],
             [ 2, -1],
             [-2, -1]]
    correct_click = [(3,1)]
    correct_flag = [(0,1)]
    test.set_board(board)
    to_click, to_flag = test.gimmes()
    gimme_printing(correct_click, to_click, 2.1)
    gimme_printing(correct_flag, to_flag, 2.2)

    # test 3
    board = [[-2,  2,  1],
             [ 2, -1, -1],
             [ 2, -1, -1],
             [-2, -1, -1]]
    correct_click = [(3,1)]
    correct_flag = []
    test.set_board(board)
    to_click, to_flag = test.gimmes()
    gimme_printing(correct_click, to_click, 3.1)
    gimme_printing(correct_flag, to_flag, 3.2)
    
    # test 4
    board = [[-2, -2],
             [-1,  3],
             [-1,  2],
             [-1,  1]]
    correct_click = [(2,0)]
    correct_flag = [(1,0), (3,0)]
    test.set_board(board)
    to_click, to_flag = test.gimmes()
    gimme_printing(correct_click, to_click, 4.1)
    gimme_printing(correct_flag, to_flag, 4.2)
    
def main():
    test_gimmes()
        
if __name__ == "__main__":
    main()