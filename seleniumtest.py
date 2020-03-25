from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('./chromedriver')

driver.get('https://docs.google.com/document/d/19LlNFgnT70gcOj4Jp-hTD4dRjMqU44cTVuwEIeD0RQo/edit?usp=sharing')
print(driver.title)