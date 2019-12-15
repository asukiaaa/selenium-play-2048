from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Firefox()
browser.get('https://www.quaxio.com/2048/')
# browser.find_element_by_id("lst-ib").send_keys("Python")
# browser.find_element_by_name("btnK").click()

actions = ActionChains(browser)
while (True):
  input("press enter to continue")
  for _ in range(10):
    actions.send_keys(Keys.ARROW_UP)
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()

# element = browser.switch_to_active_element
# element.send_keys(Keys.ARROW_UP)
# element.send_keys(Keys.ARROW_RIGHT)
