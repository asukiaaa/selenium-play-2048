# import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# print(sys.argv)
url = 'http://localhost:4444/wd/hub'
print(url)
print(webdriver.DesiredCapabilities.FIREFOX)

# browser = webdriver.Remote(command_executor=url,desired_capabilities={})
browser = webdriver.Remote(command_executor=url, desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)

# browser = webdriver.Firefox()

browser.get('https://www.quaxio.com/2048/')

print(browser.command_executor._url)
print(browser.command_executor)
print(browser.session_id)

actions = ActionChains(browser)

actions.send_keys(Keys.ARROW_UP)
actions.send_keys(Keys.ARROW_RIGHT)
actions.perform()

while (True):
  input("press enter to continue")
  for _ in range(10):
    actions.send_keys(Keys.ARROW_UP)
    actions.send_keys(Keys.ARROW_RIGHT)
    actions.perform()

# element = browser.switch_to_active_element
# element.send_keys(Keys.ARROW_UP)
# element.send_keys(Keys.ARROW_RIGHT)
