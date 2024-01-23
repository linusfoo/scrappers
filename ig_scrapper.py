import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import wget

#Downloads instagram images

CSV_PATH = '' #fill in csv path
OUTPUT_PATH = '' #fill in output path (FOLDER)
df = pd.read_csv(CSV_PATH,encoding = 'ISO-8859-1')


links = df['Link']  
counter = 2
for link in links:
    driver= webdriver.Chrome()
    driver.get(link) 
    time.sleep(8)
    driver.find_element(By.XPATH,"//*[contains(text(), 'Decline optional cookies')]").click()
    time.sleep(2)
    img = driver.find_element(By.CSS_SELECTOR, "._aagv img")
    save_as = os.path.join(OUTPUT_PATH, str(counter) + '.jpg')
    wget.download(img.get_attribute('src'), save_as)
    counter += 1
    driver.close()
        