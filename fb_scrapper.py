import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import wget
import youtube_dl 
import os 

#downloads facebook videos and images

CSV_PATH = '' #fill in csv path
OUTPUT_PATH = '' #fill in output path (FOLDER)
df = pd.read_csv(CSV_PATH,encoding = 'ISO-8859-1')
counter = 1


for _, row in df.iterrows():
    counter +=1
    link = row['Link']
    if row['Type'] == 'Photo':
        driver= webdriver.Chrome()
        driver.get(link) 
        time.sleep(7)
        driver.find_element(By.XPATH,"//*[contains(text(), 'Decline optional cookies')]").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"[aria-label=Close]").click()
        time.sleep(2)
        img = driver.find_element(By.CSS_SELECTOR,"[data-visualcompletion=media-vc-image]")
        time.sleep(1)
        save_as = os.path.join(OUTPUT_PATH, str(counter) + '.jpg')
        print("Downloading........."+ row['Type'], counter ,":", link)  
        wget.download(img.get_attribute('src'), save_as)
        driver.close()
    elif row['Type'] != "Status": #videos

        options = {"format": "(mp4,webm)[height<=1080]",
                'outtmpl': OUTPUT_PATH +'/' + str(counter)  + '.%(ext)s'}
        try:
            with youtube_dl.YoutubeDL(options) as u: 
                    print("Downloading........."+ row['Type'], counter ,":", link) 
                    # download the video 
                    u.download([link])
        except Exception as e: 
            #if there is an error means that the link is not working/ video does not exist anymore
            print(e)
            pass
            