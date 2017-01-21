#-------------------------------------------------------------------------------
# Name:       rfcrawl
# Purpose:
#
# Author:      Lord Azu
#
# Created:     31/12/2016
# Copyright:   (c) Lord Azu 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
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

def valid_url(url):
    try:
        result = urlparse(url)
        return True if [result.scheme, result.netloc, result.path] else False
    except:
        return False

def save_urls(site_links, filename = "redfin-site-map.csv"):
    with open(filename,'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        for site in site_links:
            try:
                spamwriter.writerow([site])
            except Exception as e:
                print (e)

def crawl_page(url):

    options = webdriver.ChromeOptions()
    prefs = {"download.prompt_for_download": "false", "download.extensions_to_open": "", "download.directory_upgrade": "true"}
    options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options = options)
    queued_links = queue.Queue() # container to hold site
    queued_links.put(url)
    visited_links = set() # set contains visitied links. O(1) lookup
    #counter = 0
    while not queued_links.empty(): #loop until no links remain
        #if counter > 5:
        #    break
        next_link = queued_links.get() # get head of the queue
        if next_link in visited_links:
            continue # ignore if link visited
        try:
            browser.get(next_link)

            sleep(10)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            for a in soup.find_all('a', href = True):
                if 'http' in a['href'] or 'www' in a['href']: #skip external site links
                    continue
                temp = url + a['href']
                queued_links.put(temp)#add to list of pages to visit
            visited_links.add(next_link)
            #counter += 1
            try:
                elem = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "downloadLink")))#download link
                elem.click()
                sleep(7)
                print("successfully downloaded")
            except Exception as e:
                print("No link to download")
                print(e)
            print (visited_links)
        except Exception as e:
            print (e)

    browser.close()

    save_urls(visited_links)

def main():
    crawl_page('https://www.redfin.com')
    print ('finished')
    pass

if __name__ == '__main__':
    main()
