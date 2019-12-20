from selenium import webdriver

url = 'https://www.quaxio.com/2048/'
executor_url = 'http://localhost:4444/wd/hub'
capabilities = webdriver.DesiredCapabilities.FIREFOX

browser = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
browser.get(url)

print(browser.session_id)
