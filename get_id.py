import csv
import io
from selenium import webdriver
from selenium.common import exceptions
import sys
import time
from webdriver_manager.chrome import ChromeDriverManager
from requests_html import HTMLSession 
from selenium import webdriver 
import argparse
from bs4 import BeautifulSoup as bs # importing BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import sys
import io
import csv
import json
import pandas as pd
from os.path import exists

total_comments = 0

def addCounter():
     global total_comments
     total_comments = total_comments + 1
     return total_comments

def scrape(url, FILENAME):



    print("URL IS" , url)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome(ChromeDriverManager(version="87.0.4280.88").install())
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    try:
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
        driver.execute_script("arguments[0].scrollIntoView();", comment_section)
        time.sleep(7)
    except exceptions.NoSuchElementException:
    
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    # Scroll into view the comment section, then allow some time
    # for everything to be loaded as necessary.
   

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since Youtube dynamically loads them).
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down 'til "next load".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # One last scroll just in case.
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    try:
        # Extract the elements storing the usernames and comments.
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    with io.open( FILENAME, 'w', newline='', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
        writer.writerow(["Comment"])
        for comment in zip(username_elems, comment_elems):
            try:
                writer.writerow([comment.text])
                addCounter()
            except: 
                i =0
                for c in comment:
                    if i%2 ==1:
                        writer.writerow([c.text])
                        addCounter()
                    i = i +1

    driver.close()
    driver.quit()


def getID(data):
    id_list = []
    df = pd.read_csv(data)
    for id in df["ID"]:
        id_list.append(id)
    return id_list
rejected = 0
if __name__ == "__main__":
    df = pd.read_csv("data/youtube/videos_to_scrape.csv")
    # print(df)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    i = 0 
    for id in getID("data/youtube/videos_to_scrape.csv"): 
        if len(id) > 0:
            if not exists("data/youtube/comments/" + str(id)+ ".csv"):
                scrape( "https://www.youtube.com/watch?v=" + id, "data/youtube/comments/" + str(id)+ ".csv")
                time.sleep(2)
                print( total_comments)
                i+=1
            else:
                rejected +=1
                if (rejected % 100 == 0):
                    print("rejected: ", rejected)

    