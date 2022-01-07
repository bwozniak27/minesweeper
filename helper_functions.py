import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import itertools
from selenium.webdriver.chrome.options import Options
class Minesweeper:
    def __init__(self):
        self.driver = None
        self.board, self.completed = [], [] 
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
        self.driver.get('http://minesweeperonline.com/')
        self.driver.switch_to.window(self.driver.window_handles[0])
        square = (8, 8)
        id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')
        id_box.click()
        coords = []
        done = False
        while not done:
            try:
                self.get_squares()
                to_click, to_flag = self.gimmes()
                if len(to_click) == 0 and len(to_flag) == 0:
                    print("ran out of moves")
                    x = input("continue?: ")
                    square = self.gamble()
                    if square == None:
                        done = True
                    else:
                        id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')
                        id_box.click()
                for square in to_click:
                    id_box = self.driver.find_element(By.ID, f'{square[0]}_{square[1]}')
                    try:
                        id_box.click()
                    except Exception as e:
                        print(e)
                        print(square)
                if self.done():
                    x = input("should be done: ")
            except Exception as e:
                x = input("done: ")
                obj = self.driver.switch_to.alert
                obj.send_keys("BenWozniak")
                obj.accept()
                self.driver.quit()
    def get_surrounding_tiles(self, row, col):
        unopened, bombs, other_squares = [], [], []
        pattern = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
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
        for row in range(len(self.board)):
            try:
                col = self.board[row].index(-1)
                return (row + 1, col + 1)
            except Exception as e:
                continue
    def done(self):
        for row in range(len(self.board)):
            try:
                col = self.board[row].index(-1)
                return False
            except Exception as e:
                continue
        return True
    def get_squares(self):
        coords = []
        for i in range(9):
            boxes = self.driver.find_elements(By.CLASS_NAME, f'square.open{i}')
            temp = map(lambda x: (x.get_attribute('id')).split('_'), boxes)
            temp = list(map(lambda x: (int(x[0]) - 1, int(x[1]) - 1), temp))
            for x in range(len(temp)):
                self.board[temp[x][0]][temp[x][1]] = i
        return coords
    def deducer(self, unopened, num_bombs, other_squares):
        to_flag = []
        to_click = []
        restart = False
        for neighbor in other_squares:
            unopened2, bombs2, other_squares2 = self.get_surrounding_tiles(neighbor[0], neighbor[1])
            num_bombs2 = self.board[neighbor[0]][neighbor[1]] - len(bombs2)
            if num_bombs2 == 0:
                for box in unopened2:
                    self.board[box[0]][box[1]] = 0
                    to_click.append((box[0] + 1, box[1] + 1))
                self.completed[neighbor[0]][neighbor[1]] = True
            elif num_bombs2 == len(unopened2):
                for box in unopened2:
                    self.board[box[0]][box[1]] = -2
                    to_flag.append((box[0] + 1, box[1] + 1))
                self.completed[neighbor[0]][neighbor[1]] = True
            else:
                bomb_combos = list(itertools.combinations(unopened, num_bombs))
                remaining_tiles = []
                for combo in bomb_combos:
                    a = set(combo)
                    b = set(unopened2)
                    intersect = a.intersection(b)
                    if len(intersect) > num_bombs2:
                        bomb_combos.remove(combo)
                    if len(intersect) == num_bombs2:
                        remaining = b - a
                        remaining_tiles.append(remaining)
                deduced_bombs = bomb_combos[0]
                for combo in bomb_combos:
                    deduced_bombs = list(set(deduced_bombs).intersection(combo))
                for box in deduced_bombs:
                    self.board[box[0]][box[1]] = -2
                    to_flag.append((box[0] + 1, box[1] + 1))
                if len(remaining_tiles) == len(bomb_combos):
                    deduced_clicks = remaining_tiles[0]
                    for tile in remaining_tiles:
                        deduced_clicks = list(set(deduced_clicks).intersection(tile))
                    for box in deduced_clicks:
                        self.board[box[0]][box[1]] = 0
                        to_click.append((box[0] + 1, box[1] + 1))
            if len(to_flag) > 0 or len(to_click) > 0:
                restart = True
        return restart, to_click, to_flag
    def gimmes(self):
        to_flag, to_click = [], []
        done = False
        while not done:
            restart = False
            for row in range(len(self.board)):
                if restart == True:
                    break
                for col in range(len(self.board[row])):
                    unit = self.board[row][col]
                    if unit == -1 or unit == -2 or unit == 0 or self.completed[row][col]:
                        continue
                    unopened, bombs, other_squares = self.get_surrounding_tiles(row, col)
                    num_bombs = self.board[row][col] - len(bombs)
                    if num_bombs == 0:
                        self.completed[row][col] = True
                    if num_bombs > 0 and num_bombs == len(unopened): 
                        for box in unopened:
                            self.board[box[0]][box[1]] = -2
                            to_flag.append((box[0] + 1, box[1] + 1))
                        restart = True
                        self.completed[row][col] = True
                        break
                    if len(unopened) > 0 and num_bombs == 0:
                        for box in unopened:
                            self.board[box[0]][box[1]] = 0
                            to_click.append((box[0] + 1, box[1] + 1))
                        restart = True
                        self.completed[row][col] = True
                        break
                    restart, to_click1, to_flag1 = self.deducer(unopened, num_bombs, other_squares)
                    to_click += to_click1
                    to_flag += to_flag1
                    if restart == True:
                        break
            if restart == False:
                done = True
        to_flag = list(set(to_flag))
        return to_click, to_flag




