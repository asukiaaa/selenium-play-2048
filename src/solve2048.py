import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from typing import List
import utils

print(sys.argv)
executor_url = 'http://localhost:4444/wd/hub'
session_id = sys.argv[1]

capabilities = webdriver.DesiredCapabilities.FIREFOX

browser = webdriver.Remote(
    command_executor=executor_url, desired_capabilities=capabilities)

browser.close()
browser.session_id = session_id
print(browser.session_id)

prev_boad_cells = None
same_state_count = 0
prev_else_action = None
cells_on_down = None

while True:
    boad_cells = utils.get_boad_cells(browser) if prev_boad_cells is None else prev_boad_cells
    print(boad_cells)
    else_action = None
    if utils.handle_for_row(browser, boad_cells, 0):
        # something if handled for 0
        print('handled for row 0')
    elif utils.handle_for_row(browser, boad_cells, 1):
        # something if handled for 1
        print('handled for row 1')
    elif utils.handle_for_row(browser, boad_cells, 2):
        # something if handled for 1
        print('handled for row 2')
    else:
        if prev_else_action == 'right':
            print('up as else')
            else_action = 'up'
            utils.go_up(browser)
        else:
            print('right as else')
            else_action = 'right'
            utils.go_right(browser)
    prev_else_action = else_action
    boad_cells = utils.get_boad_cells(browser)
    if prev_boad_cells is not None:
        if utils.is_same_boad_cells(prev_boad_cells, boad_cells):
            same_state_count += 1
        else:
            same_state_count = 0
        if same_state_count > 2:
            print('is same boards')
            utils.go_left(browser)
            boad_cells = utils.get_boad_cells(browser)
            if utils.is_same_boad_cells(prev_boad_cells, boad_cells):
                print('still same boards')
                utils.go_right(browser)
            boad_cells = utils.get_boad_cells(browser)
            if utils.is_same_boad_cells(prev_boad_cells, boad_cells):
                if cells_on_down is None:
                    utils.go_down(browser)
                    utils.go_up(browser)
                    boad_cells = utils.get_boad_cells(browser)
                    cells_on_down = boad_cells
                elif not utils.is_same_boad_cells(boad_cells, cells_on_down):
                    boad_cells = utils.get_boad_cells(browser)
                    utils.go_down(browser)
                    utils.go_up(browser)
                else:
                    break
            boad_cells = utils.get_boad_cells(browser)

    prev_boad_cells = boad_cells
