# selenium-play-2048

A project play [2048-undo](https://www.quaxio.com/2048/) with using selenium.

# Requirements

- selenium
- gekko

# Usage

Start web driver.
```
java -jar selenium-server-standalone-3.141.59.jar
```

Open session.
```
SESSION_ID=`python3 src/startSession.py`
```

Run job.
```
pytnon3 src/scanCells.py $SESSION_ID
```

# References

- [Remote WebDriver server](https://selenium.dev/documentation/en/remote_webdriver/remote_webdriver_server/)
- [Remote WebDriver client](https://selenium.dev/documentation/en/remote_webdriver/remote_webdriver_client/)
- [How to reuse existing Selenium browser session](https://qxf2.com/blog/reuse-existing-selenium-browser-session/)