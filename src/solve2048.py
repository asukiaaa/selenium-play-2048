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

prev_boad = None
same_state_count = 0
prev_else_action = None
boad_on_down = None

while True:
    boad = utils.read_to_create_boad(browser)
    print(boad.cells)
    else_action = None
    if utils.handle_for_row(browser, boad, 0):
        # something if handled for 0
        print('handled for row 0')
    elif utils.handle_for_row(browser, boad, 1):
        # something if handled for 1
        print('handled for row 1')
    elif utils.handle_for_row(browser, boad, 2):
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
    boad = utils.read_to_create_boad(browser)
    if prev_boad is not None:
        if boad.is_same(prev_boad):
            same_state_count += 1
        else:
            same_state_count = 0
        if same_state_count > 2:
            print('is same boards')
            utils.go_left(browser)
            boad = utils.read_to_create_boad(browser)
            if boad.is_same(prev_boad):
                print('still same boards')
                utils.go_right(browser)
            boad = utils.read_to_create_boad(browser)
            if boad.is_same(prev_boad):
                print('same board so up down or finish')
                print(boad.cells)
                print(prev_boad)
                if boad_on_down is None:
                    utils.go_down(browser)
                    utils.go_up(browser)
                    boad = utils.read_to_create_boad(browser)
                    boad_on_down = boad
                elif not boad.is_same(prev_boad):
                    boad = utils.read_to_create_boad(browser)
                    utils.go_down(browser)
                    utils.go_up(browser)
                else:
                    break
            boad = utils.read_to_create_boad(browser)
    prev_boad = boad
