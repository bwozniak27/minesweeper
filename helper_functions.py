import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from dataclasses import dataclass
import itertools


class Minesweeper:
    def __init__(self):
        self.driver = None
        self.board = []
        self.completed = [] # used to track which squares don't need to be checked
        for i in range(16):
            board_row = []
            tracking_row = []
            for j in range(30):
                board_row.append(-1)
                tracking_row.append(False)
            self.board.append(board_row)
            self.completed.append(tracking_row)
            
    def run(self):
        self.driver = webdriver.Chrome()
        # open minesweeper.com
        self.driver.get('http://minesweeperonline.com/')
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
        
        coords = []
    
        done = False
        while not done:
            # each square type
            coords = self.get_squares()
            for i in range(len(coords)):
                for square in coords[i]:
                    self.board[square[0]][square[1]] = i
            # flagged bombs
            coords = self.get_flags()
            for square in coords:
                self.board[square[0]][square[1]] = -2
            # print(grid)
            to_click, to_flag = self.gimmes()
            if len(to_click) == 0 and len(to_flag) == 0:
                print("run out of moves")
                break
                # based on probability of bombs
                # square = self.calculate_maxes()
                # print("calculate: ", square)
                # if square == None:
                #     done = True
                # else:
                #     id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')
                #     id_box.click()
            action = ActionChains(self.driver)
            for square in to_flag:
                id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')
                action.context_click(id_box).perform()
            for square in to_click:
                id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')

                # click square
                try:
                    id_box.click()
                except Exception as e:
                    print(e)
                    print(square)
        x = input("done: ")
        self.driver.quit()
    # get surrounding tiles
    def get_surrounding_tiles(self, row, col):
        # check for edges
        # print(f'square: {row}_{col}')
        unopened = []
        bombs = []
        other_squares = []
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
        self.completed = []
        for i in range(len(board)):
            temp = []
            for _ in range(len(board[i])):
                temp.append(False)
            self.completed.append(temp)
    def gamble(self):
        boxes = self.driver.find_elements(By.CLASS_NAME, 'square.open1')
        for box in boxes:
            Id = box.get_attribute('id')
            Id = Id.split('_')
            square = (int(Id[0]) - 1, int(Id[1]) - 1)
            unopened, bombs = self.get_surrounding_tiles(square[0], square[1])
            num_bombs = self.board[square[0]][square[1]] - len(bombs)
            return (unopened[0][0] + 1, unopened[0][1] + 1)
            
    # calculate chance of bomb for each square, higher number, higher chance of bomb
    def calculate_averages(self):
        probabilities = []
        for row in range(len(self.board)):
            temp =[]
            for col in range(len(self.board[row])):
                temp.append([])
            probabilities.append(temp)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                unit = self.board[row][col]
                if unit == -1 or unit == -2 or unit == 0 or self.completed[row][col]:
                    continue
                unopened, bombs, other_squares = self.get_surrounding_tiles(row, col)
                if len(unopened) > 6:
                    continue
                num_bombs = self.board[row][col] - len(bombs)
                for box in unopened:
                    probabilities[box[0]][box[1]].append(round(float(num_bombs) / len(unopened), 2))
        
        for row in range(len(probabilities)):
            for col in range(len(probabilities[row])):
                if len(probabilities[row][col]) != 0:
                    average = sum(probabilities[row][col]) / len(probabilities[row][col])
                    probabilities[row][col] = round(average, 2)
                else:
                    probabilities[row][col] = 2
        min_val = min(min(row) for row in probabilities)
        square = []
        for i, row in enumerate(probabilities):
            if min_val in row:
                square = (i, row.index(min_val))
                break
        return (square[0] + 1, square[1] + 1)
    
    def calculate_maxes(self):
        probabilities = []
        for row in range(len(self.board)):
            temp = []
            for col in range(len(self.board[row])):
                temp.append(2)
            probabilities.append(temp)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                unit = self.board[row][col]
                if unit == -1 or unit == -2 or unit == 0:
                    continue
                if self.completed[row][col]:
                    # print(f'completed: ({row}, {col})')
                    continue
                unopened, bombs, other_squares = self.get_surrounding_tiles(row, col)
                if len(unopened) > 6:
                    continue
                num_bombs = self.board[row][col] - len(bombs)
                for box in unopened:
                    if probabilities[box[0]][box[1]] == 2:
                        probabilities[box[0]][box[1]] = round(float(num_bombs) / len(unopened), 2)
                    else:
                        probabilities[box[0]][box[1]] = max(probabilities[box[0]][box[1]], round(float(num_bombs) / len(unopened), 2))
        
        # for row in range(len(probabilities)):
        #     for col in range(len(probabilities[row])):
        #         if len(probabilities[row][col]) != 0:
        #             average = sum(probabilities[row][col]) / len(probabilities[row][col])
        #             probabilities[row][col] = round(average, 2)
        #         else:
        #             probabilities[row][col] = 2
        min_val = min(min(row) for row in probabilities)
        square = []
        for i, row in enumerate(probabilities):
            if min_val in row:
                square = (i, row.index(min_val))
                break
        return (square[0] + 1, square[1] + 1)

    def get_squares(self):
        coords = []
        for i in range(9):
            boxes = self.driver.find_elements(By.CLASS_NAME, f'square.open{i}')
            temp = []
            for box in boxes:
                Id = box.get_attribute('id')
                Id = Id.split('_')
                square = (int(Id[0]) - 1, int(Id[1]) - 1)
                temp.append(square)
            coords.append(temp)
            
        return coords
    
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
                bomb_combos = list(itertools.combinations(unopened, num_bombs))
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
                # need orlapping element to appear len(bomb combos) times
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
        to_flag = []
        to_click = []
        done = False
        while not done:
            restart = False
            for row in range(len(self.board)):
                if restart == True:
                    break
                for col in range(len(self.board[row])):
                    # still will call issue for edge squares
                    unit = self.board[row][col]
                    if unit == -1 or unit == -2 or unit == 0 or self.completed[row][col]:
                        continue
                    unopened, bombs, other_squares = self.get_surrounding_tiles(row, col)
                    num_bombs = self.board[row][col] - len(bombs)
                    
                    if num_bombs == 0:
                        self.completed[row][col] = True
                    # if all surrounding squares are unclicked bombs
                    if num_bombs > 0 and num_bombs == len(unopened): 
                        for box in unopened:
                            self.board[box[0]][box[1]] = -2
                            # TODO: change back to + 1
                            to_flag.append((box[0] + 1, box[1] + 1))
                        restart = True
                        self.completed[row][col] = True
                        break
                    # if all surrounding squares aren't bombs
                    if len(unopened) > 0 and num_bombs == 0:
                        for box in unopened:
                            self.board[box[0]][box[1]] = 0
                            # TODO: change back to + 1
                            to_click.append((box[0] + 1, box[1] + 1))
                        restart = True
                        self.completed[row][col] = True
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
        return to_click, to_flag

    def get_flags(self):
        coords = []
        boxes = self.driver.find_elements(By.CLASS_NAME, 'square.bombflagged')
        for box in boxes:
            Id = box.get_attribute('id')
            Id = Id.split('_')
            square = (int(Id[0]) - 1, int(Id[1]) - 1)
            coords.append(square)
            
        return coords



