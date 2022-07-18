import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome("C:/Users/joaqu/Downloads/chromedriver_win32/chromedriver.exe")
driver.get("https://www.target.com/s?searchTerm=hair")

wait = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class^=styles__StyledProductCardBody]')))
wait = WebDriverWait(driver, 10)
# searchBarXpath = '//*[@id="search"]'

       
# # searching topic
 
# topic = 'hair'

# textbox = driver.find_element(By.XPATH, searchBarXpath)
# textbox.click()
# textbox.send_keys(topic)
# textbox.send_keys(Keys.RETURN)
source = driver.page_source
print(driver.current_url)

# wait = WebDriverWait(driver, 30)
product_list = [] 
soup = bs(source,"html.parser")
# print(soup.select('div[class^=styles__StyledProductCardBody]').__class__)
for div in soup.select('div[class^=styles__StyledProductCardBody]'):
    # print(div)
    for a in div.select('a[class^=Link__StyledLink]', href=True):
        product_list.append(a.text)
        
print(product_list)