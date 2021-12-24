import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from dataclasses import dataclass
import unittest



# get surrounding tiles
def get_surrounding_tiles(grid, row, col):
    # check for edges
    # print(f'square: {row}_{col}')
    unopened = []
    bombs = []

    # top left
    if row - 1 >= 0 and col - 1 >= 0:
        if grid[row - 1][col - 1] == -1:
            unopened.append((row - 1, col - 1))
        elif grid[row - 1][col - 1] == -2:
            bombs.append((row - 1, col - 1))

    # top middle
    if row - 1 >= 0:
        if grid[row - 1][col] == -1:
            unopened.append((row - 1, col))
        elif grid[row - 1][col] == -2:
            bombs.append((row - 1, col))

    # top right
    if row - 1 >= 0 and col + 1 < len(grid[0]):
        if grid[row - 1][col + 1] == -1:
            unopened.append((row - 1, col + 1))
        elif grid[row - 1][col + 1] == -2:
            bombs.append((row - 1, col + 1))

    # middle left
    if col - 1 >= 0:
        if grid[row][col - 1] == -1:
            unopened.append((row, col - 1))
        elif grid[row][col - 1] == -2:
            bombs.append((row, col - 1))

    # middle right
    if col + 1 < len(grid[0]):
        if grid[row][col + 1] == -1:
            unopened.append((row, col + 1))
        elif grid[row][col + 1] == -2:
            bombs.append((row, col + 1))

    # lower left
    if row + 1 < len(grid) and col - 1 >= 0:
        if grid[row + 1][col - 1] == -1:
            unopened.append((row + 1, col - 1))
        elif grid[row + 1][col - 1] == -2:
            bombs.append((row + 1, col - 1))

    # lower middle
    if row + 1 < len(grid):
        if grid[row + 1][col] == -1:
            unopened.append((row + 1, col))
        elif grid[row + 1][col] == -2:
            bombs.append((row + 1, col))
    
    # lower right
    if row + 1 < len(grid) and col + 1 < len(grid[0]):
        if grid[row + 1][col + 1] == -1:
            unopened.append((row + 1, col + 1))
        elif grid[row + 1][col + 1] == -2:
            bombs.append((row + 1, col + 1))

    return unopened, bombs


# calculate chance of bomb for each square, higher number, higher chance of bomb
def calculate(driver, grid):
    finished  = True
    # inclusive
    for row in range(1, 16):
        for col in range(1, 30):
            # check each square
            square = driver.find_element(By.ID, f'{row}_{col}')
            class_type = square.get_attribute("class")
            unopened, bombs = get_surrounding_tiles(row, col, driver)

            # if there is at least one square still left to click
            if len(unopened) > 0:
                finished = False
            
            # number of bombs touching tile
            num_bombs = 1.0
            if class_type == "square open2":
                num_bombs = 2.0
            elif class_type == "square open3":
                num_bombs = 3.0
            elif class_type == "square open4":
                num_bombs = 4.0
            elif class_type == "square open5":
                num_bombs = 5.0
            elif class_type == "square open6":
                num_bombs = 6.0
            elif class_type == "square open7":
                num_bombs = 7.0
            elif class_type == "square open8":
                num_bombs = 8.0
            elif class_type == "square blank" and len(unopened) == 8:
                continue
            
            # calculate chance of bomb for each square c = [x,y]
            for c in unopened:
                # if edge square, skip
                if c[0] == 0 or c[1] == 0:
                    continue

                print('c[0]: {}'.format(c[0]))
                print('c[1]: {}'.format(c[1]))
                print('grid[c[0]][c[1]][0]: {}'.format(grid[c[0]][c[1]][0]))

                # how many squares have been factored into average already
                mult_factor = grid[c[0]][c[1]][0]
                # add one to amount of squares for calculating average
                grid[c[0]][c[1]][0] += 1
                # to find new average of square
                if len(bombs) == num_bombs:
                    grid[c[0]][c[1]][1] = 0
                elif grid[c[0]][c[1]][1] == float('-inf'):
                    grid[c[0]][c[1]][1] = 0
                    grid[c[0]][c[1]][1] = ((grid[c[0]][c[1]][1] * mult_factor) + (num_bombs / (len(unopened) - len(bombs)))) / grid[c[0]][c[1]][0]
                elif grid[c[0]][c[1]][1] != 0:
                    grid[c[0]][c[1]][1] = ((grid[c[0]][c[1]][1] * mult_factor) + (num_bombs / (len(unopened) - len(bombs)))) / grid[c[0]][c[1]][0]
    
    
    if finished == True:
        return finished
    return grid

def get_squares(driver):
    coords = []
    for i in range(9):
        boxes = driver.find_elements(By.CLASS_NAME, f'square.open{i}')
        temp = []
        for box in boxes:
            Id = box.get_attribute('id')
            Id = Id.split('_')
            square = (int(Id[0]) - 1, int(Id[1]) - 1)
            temp.append(square)
        coords.append(temp)
        
    return coords

def gimmes(board):
    to_flag = []
    to_click = []
    done = False
    while not done:
        restart = False
        for row in range(len(board)):
            if restart == True:
                break
            for col in range(len(board[row])):
                # still will call issue for edge squares
                if board[row][col] == -1 or board[row][col] == -2 or board[row][col] == 0:
                    continue
                unopened, bombs = get_surrounding_tiles(board, row, col)
                num = board[row][col] - len(bombs)
                
                # if all surrounding squares are bombs
                if num > 0 and num == len(unopened): 
                    for box in unopened:
                        board[box[0]][box[1]] = -2
                        to_flag.append((box[0] + 1, box[1] + 1))
                    restart = True
                    break
                if len(unopened) > 0 and num == 0:
                    for box in unopened:
                        board[box[0]][box[1]] = 0
                        to_click.append((box[0] + 1, box[1] + 1))
                    restart = True
                    break
        if restart == False:
            done = True
    # print(board)
    return to_click, to_flag

def get_flags(driver):
    coords = []
    boxes = driver.find_elements(By.CLASS_NAME, 'square.bombflagged')
    for box in boxes:
        Id = box.get_attribute('id')
        Id = Id.split('_')
        square = (int(Id[0]) - 1, int(Id[1]) - 1)
        coords.append(square)
        
    return coords



