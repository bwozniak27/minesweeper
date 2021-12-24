import helper_functions as helper


def test():
    # -1 is unopened, [] is not touching a bomb, -2 is flagged
    board = [[ 0,  1, -1, -1, -1],
             [ 1,  2,  2,  2, -1],
             [-1,  1,  1,  1, -1],
             [-1,  1,  1, -1, -1],
             [-1, -1, -1, -1, -1]]
    bombs = [[0,1], [0,4], [1,4], [4,0], [4,2]]
    probabilities = [[ [],  [],  [],  [],  []],
                     [ [],  [],  [],  [],  []],
                     [ [],  [],  [],  [],  []],
                     [ [],  [],  [],  [],  []],
                     [ [],  [],  [],  [],  []]]
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == -1 or board[row][col] == -2 or board[row][col] == 0:
                continue
            unopened, bombs = helper.get_surrounding_tiles(board, row, col)
            num = board[row][col] - len(bombs)
            
            # if all surrounding squares are bombs
            if num == len(unopened): 
                for box in unopened:
                    board[box[0]][box[1]] = -2
                print("board: ", board)
                continue
            for box in unopened:
                probabilities[box[0]][box[1]].append(float(num) / len(unopened))
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            if len(probabilities[row][col]) != 0:
                average = sum(probabilities[row][col]) / len(probabilities[row][col])
                probabilities[row][col] = round(average, 2)
            else:
                probabilities[row][col] = -1
    print(probabilities)

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
    selection = input("1: general\n2: gimmes\n")
    if selection == "1":
        test()
    elif selection == "2":
        test_gimmes()
    else:
        print("invalid selection")
        
if __name__ == "__main__":
    main()