from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

url = 'http://localhost:4444/wd/hub'
# print(url)
# print(webdriver.DesiredCapabilities.FIREFOX)

# browser = webdriver.Remote(command_executor=url,desired_capabilities={})
browser = webdriver.Remote(command_executor=url, desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)

# browser = webdriver.Firefox()

browser.get('https://www.quaxio.com/2048/')
print(browser.session_id)

