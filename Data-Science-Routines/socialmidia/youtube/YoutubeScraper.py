from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Firefox()

browser.get('https://www.climatempo.com.br/')

cidade = WebDriverWait(browser, 10).until(browser.find_element_by_id('momento-localidade'))  # Find the localidade
temperatura = browser.find_element_by_id('momento-temperatura')  # Find temperatura

print (cidade.text + ", " + temperatura.text)

browser.quit()