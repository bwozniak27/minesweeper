import selenium
from helper_functions import Minesweeper
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By




def main():
    solver = Minesweeper()
    solver.run()

if __name__ == "__main__":
    main()