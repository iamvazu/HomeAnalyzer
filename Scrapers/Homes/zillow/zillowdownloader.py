#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lord Azu
#
# Created:     11/01/2017
# Copyright:   (c) Lord Azu 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pdfkit
from bs4 import BeautifulSoup
import csv
import requests
import urllib
from time import sleep
import queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import urllib.request
import os

base_dir = r"C:\Users\Lord Azu\Desktop\pythonscripts\Scraping projects\Zillow-master\Zillow-master\ZillowHomes\\" #update this to change your directory
try:
    os.makedirs(base_dir)
except:
    pass

def createFolder(home):
    os.makedirs(base_dir  + home + '\\')
    return base_dir + home + '\\'

def loadAndSave(master_csv = "masterfile.csv"):
    browser = webdriver.Chrome()
    browser.maximize_window()
    with open(master_csv, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ',')
        for row in spamreader:
            if len(row) <1 :
                continue
            name = row[0]
            url = row[10]
            if name == "address" or name == "NA":
                continue
            try:

                created = createFolder(name)
                print (created)
                saveImages(url, created, browser)

            except Exception as e:
                print (e)


def saveImages(url, folder, browser):
    os.chdir(folder)

    browser.get(url)
    sleep(10)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    for a in soup.findAll('img', {"class": "hip-photo"}):
        try:
            if 'zillowstatic' in a['src']:
                URL = a['src']
                IMAGE = URL.rsplit('/',1)[1]
                urllib.request.urlretrieve(URL, IMAGE)
                sleep(5)
        except Exception as e:
            print (e)
            pass
    for script in soup(['script', 'style']):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # save housing info

    with open("Page.txt", 'w') as file:
        for line in text:
            if '<img' in line or '"targetDiv"' in line or 'targetDiv'  in line or 'iframe' in line:
                continue
            try:
                file.write(line)
            except Exception as e:
                print (e)

def main():
    loadAndSave()
    print ('finished')


if __name__ == '__main__':
    main()
