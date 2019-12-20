import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from time import sleep

executor_url = 'http://localhost:4444/wd/hub'
session_id = sys.argv[1]
capabilities = webdriver.DesiredCapabilities.FIREFOX

browser = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
browser.close()
browser.session_id = session_id

actions = ActionChains(browser)
actions.send_keys(Keys.ARROW_UP)
actions.send_keys(Keys.ARROW_RIGHT)
actions.perform()
