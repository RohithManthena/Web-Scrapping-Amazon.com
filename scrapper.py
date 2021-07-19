
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import requests
import json
import time
import pandas as pd


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.amazon.com/gp/bestsellers/?ref_=nav_cs_bestsellers_8a080d3d7b55497ea1bdd97b7cff8b7b') 
    
html_list = driver.find_element_by_id("zg_browseRoot")
items = html_list.find_elements_by_tag_name("li")
item_names = []
for item in items:
    item_names.append(item.text)

item_names.remove('Any Department')

data = []
for item_name in item_names:
    try:
        driver.find_element_by_link_text(item_name).click()
        driver.implicitly_wait(5)
        root = driver.find_element_by_id("zg-ordered-list")
        itemss=root.find_elements_by_tag_name("li")

        data_dict = {}
        for item in itemss:
            print(item, type(item))
            product = item.text.split('\n')
            if len(product) == 3:
                data_dict['Name'] = product[1]
                data_dict['Reviews'] = None
                data_dict['Price'] = product[2]
                data_dict['Department'] = item_name
                data.append(data_dict)
                data_dict = {}

            elif len(product) == 4:


                print(product)
                data_dict['Name'] = product[1]
                data_dict['Reviews'] = product[2]
                data_dict['Price'] = product[3]
                data_dict['Department'] = item_name
                data.append(data_dict)
                data_dict = {}

        driver.back()
    except NoSuchElementException:
        driver.back()

df = pd.DataFrame(data)
print(df)
df.to_csv("results.csv")
