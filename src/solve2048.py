import sys
import gc
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
    elif utils.handle_for_row(browser, boad, 3):
        # something if handled for 1
        print('handled for row 3')
    elif boad.is_movable_up():
        print('up as else')
        utils.go_up(browser)
    elif boad.is_movable_right():
        print('right as else')
        utils.go_right(browser)
    elif boad.is_movable_left():
        print('left as else')
        utils.go_left(browser)
    elif boad.is_movable_down():
        print('down up as else')
        utils.go_down(browser)
        utils.go_up(browser)
    else:
        print('cannot move cells so finish')
        break
    gc.collect()
