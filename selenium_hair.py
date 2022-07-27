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
# source = driver.page_source
print(driver.current_url)

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
htmlXpath = "/html/body"
html = driver.find_element(By.XPATH, htmlXpath)

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# html.send_keys(Keys.END)
wait = WebDriverWait(driver, 30)
# print("scrolled")
# wait = WebDriverWait(driver, 30)


# print(driver.execute_script("return window.pageYOffset"))
# print(driver.execute_script("return document.body.scrollHeight"))
# html.send_keys(Keys.PAGE_DOWN)
# print(driver.execute_script("return window.pageYOffset"))
# print(driver.execute_script("return document.body.scrollHeight"))

full_product_list = {}

def create_list():
    # print(soup.select('div[class^=styles__StyledProductCardBody]').__class__)
    info = []
    is_key = True
    cur_key = 'NULL'
    for div in soup.select('div[class^=styles__StyledProductCardBody]'):
        # print(div)
        for a in div.select('a[class^=Link__StyledLink]', href=True):
            if is_key:
                is_key = False
                old_key = cur_key
                cur_key = a.text
                if old_key not in full_product_list:
                    full_product_list[old_key] = info
                info = []
            elif a.text == 'Exclusions Apply.':
                is_key = True
            else:
                info.append(a.text)
    if old_key not in full_product_list:
        full_product_list[old_key] = info
count = 0
old_list = {}
while count < 10:
    print('scrolling')
    soup = bs(driver.page_source,"html.parser")
    create_list()
    if old_list == full_product_list:
        count += 1
        print('COUNTING')
    old_list = full_product_list
    html.send_keys(Keys.PAGE_DOWN)
    wait = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class^=styles__StyledProductCardBody]')))
    wait = WebDriverWait(driver, 10)
    
    print(full_product_list)

for key in full_product_list.keys():
    print(key)

print(len(full_product_list))
driver.quit()
