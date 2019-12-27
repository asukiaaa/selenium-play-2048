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

boad = None

while True:
    if boad is None:
        boad = utils.read_to_create_boad(browser)
    print(boad.cells)
    next_actions = None
    if next_actions is None:
        next_actions = utils.get_actions_for_row(boad, 0)
        if next_actions is not None:
            print('got actions for row 0')
    if next_actions is None:
        next_actions = utils.get_actions_for_row(boad, 1)
        if next_actions is not None:
            print('got actions for row 1')
    if next_actions is None:
        next_actions = utils.get_actions_for_row(boad, 2)
        if next_actions is not None:
            print('got actions for row 2')
    if next_actions is None:
        next_actions = utils.get_actions_for_row(boad, 3)
        if next_actions is not None:
            print('got actions for row 3')
    if next_actions is None:
        if boad.is_movable_up():
            print('up as else')
            next_actions = ['up']
        elif boad.is_movable_right():
            print('right as else')
            next_actions = ['right']
        elif boad.is_movable_left():
            print('left as else')
            next_actions = ['left']
        elif boad.is_movable_down():
            print('down up as else')
            next_actions = ['down', 'up']
    if next_actions is None:
        print('cannot move cells so finish')
        break
    boad = boad.create_next_by_actions(browser, next_actions)
    gc.collect()
