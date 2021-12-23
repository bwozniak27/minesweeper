import selenium
import helper_functions as helper
from selenium import webdriver
from selenium.webdriver import ActionChains
from dataclasses import dataclass


import time

def algorithm():
    # using chrome to access web
    driver = webdriver.Chrome()
    

    # open minesweeper.com
    driver.get('http://minesweeperonline.com/')
    

    # Select id of square (gonna have to change boxes to select)
    square = (9, 15)
    id_box = driver.find_element_by_id('{}_{}'.format(square[0], square[1]))

    # click square
    id_box.click()

    #time.sleep(3)

    empty_squares = driver.find_elements_by_class_name("square.blank")
    while empty_squares:

        # holds list for each type of square
        one_squares = driver.find_elements_by_class_name("square.open1")
        print('length of one_squares: {}'.format(len(one_squares)))
        two_squares = driver.find_elements_by_class_name("square.open2")
        three_squares = driver.find_elements_by_class_name("square.open3")
        four_squares = driver.find_elements_by_class_name("square.open4")
        five_squares = driver.find_elements_by_class_name("square.open5")
        six_squares = driver.find_elements_by_class_name("square.open6")
        seven_squares = driver.find_elements_by_class_name("square.open7")
        eight_squares = driver.find_elements_by_class_name("square.open8")

        # one squares
        for i in range(2):
            print('start')
            for square in one_squares:
                id = square.get_attribute("id")
                row_col = id.split("_")
                row = int(row_col[0])
                col = int(row_col[1])
                uncovered, bombs = helper.get_surrounding_tiles(row, col, driver)
                #print('uncovered size: {}'.format(len(uncovered)))

                # if already touching a bomb, click rest
                if len(bombs) == 1:
                    for x in uncovered:
                        id_box = driver.find_element_by_id('{}_{}'.format(x[0], x[1]))
                        id_box.click()
                # only one uncovered square flag bomb
                elif len(uncovered) == 1:
                    for x in uncovered:
                        id_box = driver.find_element_by_id('{}_{}'.format(x[0], x[1]))
                        action = ActionChains(driver)
                        action.context_click(id_box).perform()

        # two squares
        for i in range(2):
            print('start')
            for square in two_squares:
                id = square.get_attribute("id")
                row_col = id.split("_")
                row = int(row_col[0])
                col = int(row_col[1])
                uncovered, bombs = helper.get_surrounding_tiles(row, col, driver)
                #print('uncovered size: {}'.format(len(uncovered)))

                # if already touching 2 bombs, click rest
                if len(bombs) == 2:
                    for x in uncovered:
                        id_box = driver.find_element_by_id('{}_{}'.format(x[0], x[1]))
                        id_box.click()
                elif len(bombs) == 1 and len(uncovered) == 1:
                    for x in uncovered:
                        id_box = driver.find_element_by_id('{}_{}'.format(x[0], x[1]))
                        action = ActionChains(driver)
                        action.context_click(id_box).perform()
                # only one uncovered square flag bomb
                elif len(uncovered) == 2:
                    for x in uncovered:
                        id_box = driver.find_element_by_id('{}_{}'.format(x[0], x[1]))
                        action = ActionChains(driver)
                        action.context_click(id_box).perform()

        word = input('press k to kill, else to continue: ')
        # use different thread to kill
        if word == 'k':
            break


        empty_squares = driver.find_elements_by_class_name("square.blank")



def main():
    algorithm()
    

if __name__ == "__main__":
    main()