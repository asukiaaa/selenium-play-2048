import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

print(sys.argv)
# url = sys.argv[1] + '/wd/hub'
url = 'http://localhost:4444/wd/hub'
# print(url)
# session_id = sys.argv[2]
session_id = sys.argv[1]

capabilities = webdriver.DesiredCapabilities.FIREFOX

# capabilities['sessionId'] = session_id
# https://selenium.dev/selenium/docs/api/rb/Selenium/WebDriver/Remote/Capabilities.html

print(capabilities)

# browser = webdriver.Remote(command_executor=url,desired_capabilities={})
browser = webdriver.Remote(command_executor=url, desired_capabilities=capabilities)
# browser = webdriver.Remote(command_executor=url, desired_capabilities=capabilities, sessionId=session_id)
# browser.get('https://www.quaxio.com/2048/')

# https://selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.desired_capabilities.html

# print('print executer url')
# print(browser.command_executor._url)
# print(browser.session_id)

browser.close()
browser.session_id = session_id
print(browser.session_id)

def go_up_right():
    actions = ActionChains(browser)
    actions.send_keys(Keys.ARROW_UP)
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()

def get_number_from_elem(elem: WebElement) -> int:
    value = elem.find_element_by_class_name('tile-inner').text
    return int(value)

def get_boad_cells():
    boad_cells = []
    for x in range(4):
        row_cells = []
        for y in range(4):
            cell_class = "tile-position-{}-{}".format(y+1, x+1)
            try:
                cell = browser.find_element_by_class_name(cell_class)
                # print(cell)
                row_cells.append(get_number_from_elem(cell))
            except Exception as e:
                # print('cannot find', cell_class, e)
                row_cells.append(None)
        boad_cells.append(row_cells)
    return boad_cells

go_up_right()
boad_cells = get_boad_cells()
print(boad_cells)
