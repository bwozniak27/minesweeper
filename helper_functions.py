# import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from itertools import combinations
from selenium.webdriver.chrome.options import Options

class Minesweeper:
    def __init__(self):
        self.driver = None
        self.board, self.completed = [], []
        self.open_squares = [[], [], [], [], [], [], [], [], []]
        for i in range(16):
            board_row, tracking_row = [], []
            for j in range(30):
                board_row.append(-1)
                tracking_row.append(False)
            self.board.append(board_row)
            self.completed.append(tracking_row)
            
    def run(self):
        path_to_adblock = '/Users/benwozniak/Desktop/4.41.0_0'
        chrome_options = Options()
        chrome_options.add_argument('load-extension=' + path_to_adblock)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.create_options()
        # open minesweeper.com
        self.driver.get('http://minesweeperonline.com/')
        self.driver.switch_to.window(self.driver.window_handles[0])
        # self.driver.find_element(By.ID, 'options-link').click()
        # self.driver.find_element(By.ID, 'custom').click()
        # h = self.driver.find_element(By.ID, 'custom_height')
        # h.clear()
        # h.send_keys('100')
        # w = self.driver.find_element(By.ID, 'custom_width')
        # w.clear()
        # w.send_keys('100')
        # b = self.driver.find_element(By.ID, 'custom_mines')
        # b.clear()
        # b.send_keys('1000')
        # self.driver.find_element(By.CLASS_NAME, 'dialogText').click()
        
        # initial filling. -1 for blank, -2 for bomb
        
        

        # Select id of square (gonna have to change boxes to select)
        square = (8, 15)
        id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')

        # click square
        id_box.click()
    
        done = False
        while not done:
            # each square type
            self.get_squares()
            # for i in range(len(coords)):
            #     for square in coords[i]:
            #         self.board[square[0]][square[1]] = i
            # flagged bombs
            # coords = self.get_flags()
            # for square in coords:
            #     self.board[square[0]][square[1]] = -2
            # print(grid)
            to_click, to_flag = self.gimmes()
            if len(to_click) == 0 and len(to_flag) == 0:
                print("ran out of moves")
                square = self.gamble()
                if square == None:
                    done = True
                else:
                    id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')
                    try:
                        id_box.click()
                    except Exception as e:
                        print(e.__class__.__name__)
                        print(square)
                # pause = input("press enter to continue")
            
            for square in to_click:
                id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')

                # click square
                try:
                    id_box.click()
                except Exception as e:
                    print(e.__class__.__name__)
                    print(square)
            # pause = input("press enter to continue")
        x = input("done: ")
        self.driver.quit()
    # get surrounding tiles
    def get_surrounding_tiles(self, row, col):
        # check for edges
        # print(f'square: {row}_{col}')
        unopened, bombs, other_squares = [], [], []
        pattern = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

        # top left
        for op in pattern:
            temp_row = row + op[0]
            temp_col = col + op[1]
            if temp_row >= 0 and temp_col >= 0 and temp_row < len(self.board) and temp_col < len(self.board[0]):
                if self.board[temp_row][temp_col] == -2:
                    bombs.append((temp_row, temp_col))
                elif self.board[temp_row][temp_col] == -1:
                    unopened.append((temp_row, temp_col))
                elif self.board[temp_row][temp_col] != 0 and not self.completed[temp_row][temp_col]:
                    other_squares.append((temp_row, temp_col))

        return unopened, bombs, other_squares

    def set_board(self, board):
        self.board = board
        self.completed, self.open_squares = [], [[], [], [], [], [], [], [], [], []]
        for i in range(len(board)):
            temp = []
            for _ in range(len(board[i])):
                temp.append(False)
            self.completed.append(temp)
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] != -1 and board[row][col] != -2:
                    self.open_squares[board[row][col]].append((row, col))
                    
    # improve gamble
    def gamble(self):
        square = None
        for row in range(len(self.board)):
            # for col in range(len(self.board[row])):
            #     if self.board[row][col] == -1:
            try:
                col = self.board[row].index(-1)
                return (row + 1, col + 1)
            except:
                continue
            

    def get_squares(self):
        # coords = []
        for i in range(9):
            boxes = self.driver.find_elements(By.CLASS_NAME, f'square.open{i}')
            temp = map(lambda x: (x.get_attribute('id')).split('_'), boxes)
            temp = list(map(lambda x: (int(x[0]) - 1, int(x[1]) - 1), temp))
            for x in range(len(temp)):
                self.board[temp[x][0]][temp[x][1]] = i
            completed_set = set([x for x in temp if not self.completed[x[0]][x[1]]])
            try:
                self.open_squares[i] = set(self.open_squares[i]).union(completed_set)
            except IndexError:
                print('')
                print("index error: ", i)
                print('')
            # coords.append(temp)
            
        # return coords
    
    def deducer(self, unopened, num_bombs, other_squares):
        decoding_dict = {}
        to_flag = []
        to_click = []
        restart = False
        for neighbor in other_squares:
            unopened2, bombs2, other_squares2 = self.get_surrounding_tiles(neighbor[0], neighbor[1])
            num_bombs2 = self.board[neighbor[0]][neighbor[1]] - len(bombs2)
            decoding_dict[neighbor] = [num_bombs2, unopened2]
        for square in decoding_dict:
            if decoding_dict[square][0] == 0:
                for box in decoding_dict[square][1]:
                    self.board[box[0]][box[1]] = 0
                    # TODO: change back to + 1
                    to_click.append((box[0] + 1, box[1] + 1))
                
                self.completed[square[0]][square[1]] = True
            elif decoding_dict[square][0] == len(decoding_dict[square][1]):
                for box in decoding_dict[square][1]:
                    self.board[box[0]][box[1]] = -2
                    # TODO: change back to + 1
                    to_flag.append((box[0] + 1, box[1] + 1))
                
                self.completed[square[0]][square[1]] = True
            else:
                # try all combos of bombs for current,
                # check if any work with neighbors
                # RULES:
                # 1) if theres a common element, must be bomb
                # 2) if all valid combos fulfill neighbor square, then all 
                # remaining tiles for neighbor are safe
                bomb_combos = list(combinations(unopened, num_bombs))
                remaining_tiles = []
                for combo in bomb_combos:
                    a = set(combo) # current square
                    b = set(decoding_dict[square][1]) # neighbor square
                    intersect = a.intersection(b)
                    if len(intersect) > decoding_dict[square][0]:
                        # invalid combo
                        bomb_combos.remove(combo)
                    if len(intersect) == decoding_dict[square][0]:
                        # valid combo
                        remaining = b - a
                        remaining_tiles.append(remaining)
                    
                # bomb_combos is only valid combos
                deduced_bombs = bomb_combos[0]
                for combo in bomb_combos:
                    deduced_bombs = list(set(deduced_bombs).intersection(combo))
                for box in deduced_bombs:
                    self.board[box[0]][box[1]] = -2
                    # TODO: change back to + 1
                    to_flag.append((box[0] + 1, box[1] + 1))
                
                # TODO: if elements are different, but length is same
                # could be false positive
                # need overlapping element to appear len(bomb combos) times
                if len(remaining_tiles) == len(bomb_combos):
                    deduced_clicks = remaining_tiles[0]
                    for tile in remaining_tiles:
                        deduced_clicks = list(set(deduced_clicks).intersection(tile))
                    for box in deduced_clicks:
                        self.board[box[0]][box[1]] = 0
                        # TODO: change back to + 1
                        to_click.append((box[0] + 1, box[1] + 1))
        if len(to_flag) > 0 or len(to_click) > 0:
            restart = True
        return restart, to_click, to_flag
                
    def gimmes(self):
        to_flag, to_click = [], []
        done = False
        while not done:
            restart = False
            for val in range(1, len(self.open_squares)):
                if restart == True:
                    break
                for square in self.open_squares[val]:
                    row = square[0]
                    col = square[1]
                    # still will call issue for edge squares
                    # unit = self.board[row][col]
                    # if unit == -1 or unit == -2 or unit == 0 or self.completed[row][col]:
                    #     continue
                    unopened, bombs, other_squares = self.get_surrounding_tiles(row, col)
                    num_bombs = self.board[row][col] - len(bombs)
                    
                    # if all surrounding squares are unclicked bombs
                    if num_bombs > 0 and num_bombs == len(unopened): 
                        for box in unopened:
                            self.board[box[0]][box[1]] = -2
                            # TODO: change back to + 1
                            to_flag.append((box[0] + 1, box[1] + 1))
                        restart = True
                        self.completed[row][col] = True
                        self.open_squares[val].remove(square)
                        break
                    # if all surrounding squares aren't bombs
                    if num_bombs == 0:
                        for box in unopened:
                            self.board[box[0]][box[1]] = 0
                            # TODO: change back to + 1
                            to_click.append((box[0] + 1, box[1] + 1))
                        restart = True
                        self.completed[row][col] = True
                        self.open_squares[val].remove(square)
                        break
                    # other
                    restart, to_click1, to_flag1 = self.deducer(unopened, num_bombs, other_squares)
                    to_click += to_click1
                    to_flag += to_flag1
                    if restart == True:
                        break
                    
            if restart == False:
                done = True
        # print(board)
        to_flag = list(set(to_flag))
        return to_click, to_flag




