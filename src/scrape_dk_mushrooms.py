
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

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

base_url = "http://www.svampeguide.dk/"
main_url = f"{base_url}/alle-svampe"

driver.get(main_url)
hrefs = driver.find_elements(By.XPATH, "//div[@class='alfa']/div/a[@href]")
urls = [elem.get_attribute('href') for elem in hrefs]

da_names = []
lat_names = []

for url in urls:
    driver.get(url)
    da_name = driver.find_element(By.TAG_NAME, "h1").text
    lat_name = driver.find_element(By.CLASS_NAME, "latin").text
    da_names.append(da_name)
    lat_names.append(lat_name)
    time.sleep(3)

df = pd.DataFrame(list(zip(da_names, lat_names)),
               columns =['da_name', 'lat_name']) 
                         
df.to_csv("data/csv/danish_mushrooms.csv")


