import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from dataclasses import dataclass



# get surrounding tiles
def get_surrounding_tiles(row, col, driver):
    uncovered = []
    bombs = []

    # top left
    x = driver.find_element_by_id('{}_{}'.format(row - 1, col - 1))
    class_type = x.get_attribute("class")
    if class_type == "square blank":
        temp = (row - 1, col - 1)
        uncovered.append(temp)
    elif x.get_attribute("class") == "square bombflagged":
        temp = (row - 1, col - 1)
        bombs.append(temp)

    # top middle
    x = driver.find_element_by_id('{}_{}'.format(row - 1, col))
    class_type = x.get_attribute("class")
    if class_type == "square blank":
        temp = (row - 1, col)
        uncovered.append(temp)
    elif x.get_attribute("class") == "square bombflagged":
        temp = (row - 1, col)
        bombs.append(temp)

    # top right
    x = driver.find_element_by_id('{}_{}'.format(row - 1, col + 1))
    class_type = x.get_attribute("class")
    if class_type == "square blank":
        temp = (row - 1, col + 1)
        uncovered.append(temp)
    elif x.get_attribute("class") == "square bombflagged":
        temp = (row - 1, col + 1)
        bombs.append(temp)

    # middle left
    x = driver.find_element_by_id('{}_{}'.format(row, col - 1))
    class_type = x.get_attribute("class")
    if class_type == "square blank":
        temp = (row, col - 1)
        uncovered.append(temp)
    elif x.get_attribute("class") == "square bombflagged":
        temp = (row, col - 1)
        bombs.append(temp)

    # middle right
    x = driver.find_element_by_id('{}_{}'.format(row, col + 1))
    class_type = x.get_attribute("class")
    if class_type == "square blank":
        temp = (row, col + 1)
        uncovered.append(temp)
    elif x.get_attribute("class") == "square bombflagged":
        temp = (row, col + 1)
        bombs.append(temp)

    # lower left
    x = driver.find_element_by_id('{}_{}'.format(row + 1, col - 1))
    class_type = x.get_attribute("class")
    if class_type == "square blank":
        temp = (row + 1, col - 1)
        uncovered.append(temp)
    elif x.get_attribute("class") == "square bombflagged":
        temp = (row + 1, col - 1)
        bombs.append(temp)

    # lower middle
    x = driver.find_element_by_id('{}_{}'.format(row + 1, col))
    class_type = x.get_attribute("class")
    if class_type == "square blank":
        temp = (row + 1, col)
        uncovered.append(temp)
    elif x.get_attribute("class") == "square bombflagged":
        temp = (row + 1, col)
        bombs.append(temp)

    # lower right
    x = driver.find_element_by_id('{}_{}'.format(row + 1, col + 1))
    class_type = x.get_attribute("class")
    if class_type == "square blank":
        temp = (row + 1, col - 1)
        uncovered.append(temp)
    elif x.get_attribute("class") == "square bombflagged":
        temp = (row + 1, col - 1)
        bombs.append(temp)

    


    return uncovered, bombs


# calculate chance of bomb for each square, higher number, higher chance of bomb
def calculate(driver, grid):
    finished  = True
    # inclusive
    for row in range(1, 16):
        for col in range(1, 30):
            # check each square
            square = driver.find_element_by_id('{}_{}'.format(row, col))
            class_type = square.get_attribute("class")
            uncovered, bombs = get_surrounding_tiles(row, col, driver)

            # if there is at least one square still left to click
            if len(uncovered) > 0:
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
            elif class_type == "square blank" and len(uncovered) == 8:
                continue
            
            # calculate chance of bomb for each square c = [x,y]
            for c in uncovered:
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
                    grid[c[0]][c[1]][1] = ((grid[c[0]][c[1]][1] * mult_factor) + (num_bombs / (len(uncovered) - len(bombs)))) / grid[c[0]][c[1]][0]
                elif grid[c[0]][c[1]][1] != 0:
                    grid[c[0]][c[1]][1] = ((grid[c[0]][c[1]][1] * mult_factor) + (num_bombs / (len(uncovered) - len(bombs)))) / grid[c[0]][c[1]][0]
    
    
    if finished == True:
        return finished
    return grid

