from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://naturporten.dk/temaer/danmarks-planter")
p_elements = driver.find_elements(By.TAG_NAME, 'a')

for i in p_elements:
    k = i.get_attribute('href')
    print(k)

print(p_element.text)


