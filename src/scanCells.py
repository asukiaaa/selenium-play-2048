import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from time import sleep

print(sys.argv)
# url = sys.argv[1] + '/wd/hub'
executor_url = 'http://localhost:4444/wd/hub'
# session_id = sys.argv[2]
session_id = sys.argv[1]

capabilities = webdriver.DesiredCapabilities.FIREFOX

# capabilities['sessionId'] = session_id
# https://selenium.dev/selenium/docs/api/rb/Selenium/WebDriver/Remote/Capabilities.html

print(capabilities)

# browser = webdriver.Remote(command_executor=url,desired_capabilities={})
browser = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
# browser = webdriver.Remote(command_executor=url, desired_capabilities=capabilities, sessionId=session_id)
# browser.get('https://www.quaxio.com/2048/')

# https://selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.desired_capabilities.html

# print('print executer url')
# print(browser.command_executor._url)
# print(browser.session_id)

browser.close()
browser.session_id = session_id
print(browser.session_id)

go_delay_second = 0.2

def go_right():
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()
    sleep(go_delay_second)

def go_left():
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_LEFT)
    actions.perform()
    sleep(go_delay_second)

def go_up():
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_UP)
    actions.perform()
    sleep(go_delay_second)

def go_down():
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_DOWN)
    actions.perform()
    sleep(go_delay_second)

def get_number_of_cell(x: int, y: int):
    cell_class = "tile-position-{}-{}".format(y+1, x+1)
    cell_elems = browser.find_elements_by_class_name(cell_class)
    elems_len = len(cell_elems)
    if elems_len is 0:
        return None
    elif elems_len is 1:
        text = cell_elems[0].find_element_by_class_name('tile-inner').text
        return int(text)
    else:
        # TODO
        text = cell_elems[elems_len -1].find_element_by_class_name('tile-inner').text
        return int(text)

def get_boad_cells():
    boad_cells = []
    for x in range(4):
        row_cells = []
        for y in range(4):
            row_cells.append(get_number_of_cell(x, y))
        boad_cells.append(row_cells)
    return boad_cells

def is_same_boad_cells(boad1, boad2):
    for x in range(4):
        for y in range(4):
            if (boad1[y][x] != boad2[y][x]):
                return False
    return True

# def should_joint_to_left_top(cells):
#     for x in range(3):
#         left = cells[0][x]
#         right = cells[0][x+1]
#         if left is None or right is None:
#             return False
#         if left == right or left > right:
#             return False
#     topLeft = cells[0][0]
#     if topLeft is not None and topLeft > 8:
#         return True

def top_right_is_filled(cells):
    for x in range(3):
        left = cells[0][x]
        right = cells[0][x+1]
        if left is not None and right is None:
            return False
    return True

def top_have_jointable_cells(cells):
    for x in range(3):
        left = cells[0][x]
        right = cells[0][x+1]
        if left is not None and left == right:
            return True
    return False

def top_has_none(cells):
    for x in range(4):
        if cells[0][x] is None:
            return True
    return False

def jointable_to_top(cells):
    for x in range(4):
        if (cells[0][x] == cells[1][x] and cells[0][x] is not None):
            return True
    return False

prev_boad_cells = None
same_state_count = 0

prev_else_action = None

while True:
    boad_cells = get_boad_cells() if prev_boad_cells is None else prev_boad_cells
    print(boad_cells)
    else_action = None
    if not top_right_is_filled(boad_cells):
        print('right because top is not filled')
        go_right()
    elif jointable_to_top(boad_cells) or top_has_none(boad_cells):
        print('up because jointable top or top has none')
        go_up()
    elif top_have_jointable_cells(boad_cells):
        print('right because top have jointable cells')
        go_right()
    # elif should_joint_to_left_top(boad_cells):
    #     print('left because should joint left top')
    #     go_left()
    else:
        if prev_else_action == 'right':
            print('up as else')
            else_action = 'up'
            go_up()
        else:
            print('right as else')
            else_action = 'right'
            go_right()
    prev_else_action = else_action
    boad_cells = get_boad_cells()
    if prev_boad_cells is not None:
        if is_same_boad_cells(prev_boad_cells, boad_cells):
            same_state_count += 1
        else:
            same_state_count = 0
        if same_state_count > 2:
            print('is same boards')
            go_left()
            boad_cells = get_boad_cells()
            if is_same_boad_cells(prev_boad_cells, boad_cells):
                print('still same boards')
                go_right()
            boad_cells = get_boad_cells()
            if is_same_boad_cells(prev_boad_cells, boad_cells):
                break
            boad_cells = get_boad_cells()

    prev_boad_cells = boad_cells
