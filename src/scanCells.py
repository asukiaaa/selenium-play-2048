import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

print(browser.command_executor._url)
print(browser.session_id)

browser.close()
browser.session_id = session_id
print(browser.session_id)

actions = ActionChains(browser)

actions.send_keys(Keys.ARROW_UP)
actions.send_keys(Keys.ARROW_RIGHT)
actions.perform()
