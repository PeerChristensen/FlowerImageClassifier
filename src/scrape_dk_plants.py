from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import pandas as pd

#driver = webdriver.Chrome()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# PLANTS
driver.get("https://naturporten.dk/temaer/danmarks-planter")
a_tags = driver.find_elements(By.TAG_NAME, 'a')

urls = []
for tag in a_tags:
    url = tag.get_attribute('href')
    if "item" in url:
        urls.append(url)
        
da_names = []
indices_to_pop = []

for ind, url in enumerate(urls):
    driver.get(url)
    da_name = driver.find_element(By.TAG_NAME, 'h1') # or class name = 'pos-title' (requires try-catch)
    if da_name.text in ['404', '500']:
        indices_to_pop.append(ind)
    da_names.append(da_name.text)
    time.sleep(1)

urls = [ele for idx, ele in enumerate(urls) if idx not in indices_to_pop]
da_names = [ele for idx, ele in enumerate(da_names) if idx not in indices_to_pop]

lat_names = []
eng_names = []
group_names = []
class_names = []
order_names = []
family_names = []
texts = []

for url in urls:
    
    print(url)
    
    try:
        driver.get(url)
        div_element = driver.find_element(By.XPATH, "//div[@class='leksikon_venstre']/div") 
        div_text = div_element.text
        
        lat_name = re.search(r'Latinsk navn: (.*?)\n', div_text).group(1)
        eng_name = re.search(r'Engelsk navn: (.*?)\n', div_text).group(1)
        group_name = re.search(r'Gruppe: (.*?)\n', div_text).group(1)
        class_name = re.search(r'Klasse: (.*?)\n', div_text).group(1)
        order_name = re.search(r'Orden: (.*?)\n', div_text).group(1)
        family_name = re.search(r'Familie: (.*?)\n', div_text).group(1)
        text = div_text.partition("Familie")[2].partition("\n")[2].replace("\n", " ")
    
    except Exception as e: 
        print(e)
        
    if lat_name:
        lat_names.append(lat_name)
    else:
        lat_names.append(None)
        
    if eng_name:
        eng_names.append(eng_name)
    else:
        eng_names.append(None)
        
    if group_name:
        group_names.append(group_name)
    else:
        group_names.append(None)
        
    if class_name:
        class_names.append(class_name)
    else:
        class_names.append(None)
    
    if order_name:
        order_names.append(order_name)
    else:
        order_names.append(None)
        
    if family_name:
        family_names.append(family_name)
    else:
        family_names.append(None)

    if text:
        texts.append(text)
    else:
        texts.append(None)

    time.sleep(3)


df = pd.DataFrame(list(zip(da_names, lat_names, eng_names, group_names, class_names, order_names, family_names, texts)),
               columns =['da_name', 'lat_name', 'eng_name', 'group_name', 'class_name', 'order_name', 'family_name', 'text'])  
    

df.to_csv("danish_plants.csv")


'''for ind, name in enumerate(da_names):
    if name in ['404', '500']:
        indices_to_pop.append(ind)'''

'''indices_to_pop = []
for ind, name in enumerate(eng_names):
    if ind % 2 == 0:
        indices_to_pop.append(ind)
        
eng_names = [j for i,j in enumerate(eng_names) if not i in indices_to_pop]
'''

