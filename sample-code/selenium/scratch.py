from selenium import webdriver #non-optional

browser = webdriver.Chrome()
browser.get("https://automatetheboringstuff.com")
elem = browser.find_element_by_css_selector('body > div.main > ul:nth-child(16) > li:nth-child(2) > a')
elem.click()