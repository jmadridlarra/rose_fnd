import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome("C:/Users/joaqu/Downloads/chromedriver_win32/chromedriver.exe")
driver.get("https://www.target.com/")

wait = WebDriverWait(driver, 30)

searchBarXpath = '//*[@id="search"]'

       
# searching topic
 
topic = 'hair'

textbox = driver.find_element(By.XPATH, searchBarXpath)
textbox.click()
textbox.send_keys(topic)
textbox.send_keys(Keys.RETURN)
source = driver.page_source
print(driver.current_url)

product_list = [] 
soup = bs(source,"html.parser")
print(soup.findAll('div', class_="styles__StyledCol-sc-ct8kx6-0").__class__)

# wait = WebDriverWait(driver, 100)

for div in soup.findAll('div', class_="styles__StyledCol-sc-ct8kx6-0"):
     # print(div)
     for a in div.findAll("a",href=True):
            product_list.append(a.text)
        
print(product_list)