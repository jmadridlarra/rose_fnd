import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

latitude = 34.023654445935286
longitude = -118.37377283773024
accuracy = 100

driver.maximize_window()
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    "latitude": latitude,
    "longitude": longitude,
    "accuracy": accuracy
     })

# driver = webdriver.Chrome("C:/Users/joaqu/Downloads/chromedriver_win32/chromedriver.exe")

# Target address
# 3535 S La Cienega Blvd, Los Angeles, CA 90016


def scrape_each_page(url_link):
    driver.get(url_link)
    print(driver.current_url)
    htmlXpath = "/html/body"
    html = driver.find_element(By.XPATH, htmlXpath)

    number_xpath = '//*[@id="pageBodyContainer"]/div[1]/div/div[13]/div/div[1]/div[2]/div/div[1]/h2'

    # top = driver.find_element_by_css_selector('div[class^=Heading__StyledHeading]')
    # driver.execute_script("arguments[0].scrollIntoView();", top)

    # top.location_once_scrolled_into_view

    # searchBarXpath = '//*[@id="search"]'
    # from selenium.common.exceptions import NoSuchElementException
    # def find_number_of_results():
    #     try:
    #         top = driver.find_element(By.XPATH, number_xpath)
            
    #     except NoSuchElementException:
    #         html.send_keys(Keys.PAGE_DOWN)
    #         wait = WebDriverWait(driver, 10)
    #         find_number_of_results()
    #     finally:
    #         html.send_keys(Keys.PAGE_DOWN)
    #         wait = WebDriverWait(driver, 10)
    # find_number_of_results()    
    from selenium.common.exceptions import TimeoutException
    def load_cards():
        try:
            wait = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class^=styles__StyledProductCardBody]')))
        except TimeoutException:
            html.send_keys(Keys.PAGE_DOWN)
            wait = WebDriverWait(driver, 10)
            load_cards()
    load_cards()
    wait = WebDriverWait(driver, 10)
    # # searching topic
    
    # topic = 'hair'

    # textbox = driver.find_element(By.XPATH, searchBarXpath)
    # textbox.click()
    # textbox.send_keys(topic)
    # textbox.send_keys(Keys.RETURN)
    # source = driver.page_source
    # print(driver.current_url)

    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


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
    def scrape_product_info(link):
        product_page_info = {}

        driver.execute_script('''window.open("''' + link + '''","_blank");''')
        window_name = driver.window_handles[-1]
        wait = WebDriverWait(driver, 30)
        driver.switch_to.window(window_name=window_name)
        wait = WebDriverWait(driver, 30)
        product_soup = bs(driver.page_source,"html.parser")
        
        wanted_info = {
            "wellness_badges": "styles__WellnessBadgeDescription",
            # "ingredients":"h-text-transform-caps",
            # "highlights":"styles__StyledRow",
            "description":"h-margin-v-default",
            "specifications": "styles__StyledCol"
        }
        # ingredients_scrape = []
        # print(product_soup.find_all(id='tabContent-tab-Labelinfo'))
        # for div in product_soup.find_all(id='tabContent-tab-Labelinfo'):
        #     print("empty div")
        #     ingredients_scrape.append(div)
        #     print(div.text)
        

        def general_scrape(div_class):
            # print(div_class)
            general_list = []
            for div in product_soup.select('div[class^='+div_class+']'):
                # print(div)
                # print(div.text)
                if not any(x in div.text for x in ["CleanYour", "FreeFormulated", "FreeA", "BrandTarget"]):
                    general_list.append(div.text)
            return general_list

        for key in wanted_info.keys():
            if key != "specifications":
                product_page_info[key] = general_scrape(wanted_info[key])
            else:
                scraped_list = general_scrape(wanted_info[key])
                product_page_info[key] = scraped_list[3:]
                import re
                price = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", scraped_list[1])[0]
                if price != str(5):
                    product_page_info["price"] = price
                else:
                    product_page_info["price"] = "not scraped"


        # product_page_info["highlights"] = driver.find_element("xpath", '//*[@id="tabContent-tab-Details"]/div/div/div/div[1]/div[2]/div/ul/div').text
        # print(driver.find_element("xpath", '//*[@id="tabContent-tab-Details"]/div/div/div/div[1]/div[2]/div/ul/div').text)

        from selenium.common.exceptions import NoSuchElementException
        try:
            driver.find_element("link text", "Label info").click()
            wait = WebDriverWait(driver, 30)
            product_page_info["ingredients"] = driver.find_element("xpath", '//*[@id="tabContent-tab-Labelinfo"]/div/div/div[1]/div').text 
        except NoSuchElementException:
            product_page_info["ingredients"] = "not available on Target website"

        driver.close()
        window_name = driver.window_handles[0]
        driver.switch_to.window(window_name=window_name)
        wait = WebDriverWait(driver, 30)
        return product_page_info


    full_product_list = {"Product Title":["Target 'badges'", "description", "specifications", "price", "ingredients", "Product Brand", "Target ratings"]}
    # soup = bs(driver.page_source,"html.parser")
    def create_list(soup):
        '''
        Loops through soup of each page and scrapes each product card.
        '''
        # print(soup.select('div[class^=styles__StyledProductCardBody]').__class__)
        info = []
        is_key = True
        cur_key = 'NULL'
        for div in soup.select('div[class^=styles__StyledProductCardBody]'):
            # loops through each product
            # print(div)
            for a in div.select('a[class^=Link__StyledLink]', href=True):
                # finds link for each product page
                if is_key:
                    # this is a new product
                    is_key = False
                    old_key = cur_key
                    cur_key = a.text
                    if cur_key not in full_product_list:
                        full_product_list[cur_key] = info
                        print("opening new tab")
                        if a.has_attr('href'):
                            print(a['href'])
                            for value in scrape_product_info(a["href"]).values():
                                info.append(value)
                    
                    
                elif a.text == 'Exclusions Apply.':
                    # signifies end of a product
                    is_key = True
                    info = []
                else:
                    # this is not a new product so we will just collect info
                    info.append(a.text)
        if cur_key not in full_product_list:
            # last product case
            # if old_key == "NULL":
            #     full_product_list[cur_key] = info
            full_product_list[cur_key] = info
            print("opening new tab")
            if a.has_attr('href'):
                print(a['href'])
                for value in scrape_product_info(a["href"]).values():
                    info.append(value)

    def scrape_page():
        count = 0
        old_list = {}
        while count < 10:
            print('scrolling')
            wait = WebDriverWait(driver, 50)
            soup = bs(driver.page_source,"html.parser")
            create_list(soup)
            if old_list == full_product_list:
                count += 1
                print('COUNTING')
            old_list = full_product_list
            html.send_keys(Keys.PAGE_DOWN)
            wait = WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class^=styles__StyledProductCardBody]')))
            wait = WebDriverWait(driver, 50)
            
            # print(full_product_list)
            print("exporting to excel")
            import pandas as pd
            df = pd.DataFrame.from_dict(full_product_list, orient='index')

            df = (df.T)

            print (df)

            df.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)

        for key in full_product_list.keys():
            print(key)

        print(len(full_product_list))
        return full_product_list
    # soup = bs(driver.page_source,"html.parser")

    return scrape_page()


    # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".h-sr-only")))
    # driver.find_element("link text", "Next page").click()
    # print(driver.current_url)
    # scrape_page()

    # https://www.target.com/c/textured-hair-care/-/N-4rsrfZvdjvcsibby6Zvdjvcsbepaw?Nao=24
    # for span in soup.select('span[class^=Pagination__StyledSpan]'):
    #     print(span.text)
    #     number = int(span.text[-1])
    #     print(number)
    # inc = 0
    # while inc < number:
    #     for button in soup.select('a[class^=h-sr-only]'):
    #         if button.text == 'Next Page':
    #             button.click()
    #     scrape_page()
    #     inc += 1

def get_next_link(base_url, multiplier):
    num = str(24 * multiplier)
    return "https://www.target.com/c/textured-hair-care/-/N-4rsrfZvdjvcsibby6Zvdjvcsbepaw?Nao=" + num + "&moveTo=product-list-grid"

base_url = "https://www.target.com/c/textured-hair-care/-/N-4rsrfZvdjvcsibby6Zvdjvcsbepaw"

entire_product_list = scrape_each_page(base_url)
# entire_product_list = page_product_list


# import pandas as pd

# new_list = entire_product_list
# df = pd.DataFrame(new_list)
# writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
# df.to_excel(writer, sheet_name='welcome', index=False)
# writer.save()

# import pandas as pd
# df = pd.DataFrame(data=entire_product_list, index=[0])

# df = (df.T)

# print (df)

# df.to_excel('dict1.xlsx')
# data.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)

index = 1

while index < 7: 
    link = get_next_link(base_url, index)
    entire_product_list.update(scrape_each_page(link))
    index += 1

print("exporting to excel")
import pandas as pd
df = pd.DataFrame.from_dict(entire_product_list, orient='index')

df = (df.T)

print (df)

df.to_excel('rose_fnd_target_data-159.xlsx', sheet_name='sheet1', index=False)
# while index < 8:
#     link = get_next_link(base_url, index)
#     scrape_each_page(link)
#     index += 1

driver.quit()
