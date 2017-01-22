#-------------------------------------------------------------------------------
# Name:        school_info
# Purpose: Retrieves school rankings. Gathers, district, statewide ranking,
# grade type, address, phone, student population
# Author:      Lord Azu
#
# Created:     22/01/2017
# Copyright:   (c) Lord Azu 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from bs4 import BeautifulSoup
import csv
import requests
import urllib
from time import sleep
from urllib.parse import urlparse
import urllib.request
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


base_url = "https://www.schooldigger.com/go/CA/zip/%s/search.aspx"
rankings_page = '?t=tbRankings'

def get_zips_from_file(filename):
    zips = []
    with open(filename, 'r') as f:
        for line in f:
            zips.append(line.strip())
    return zips


def process_zipcode(browser, zipcode, filename):
    """Retrieves information of schools within zipcode
    \
    browser: selenium browser, zipcode: str, filename: strout"""
    print ("Working on schools in %s" % zipcode)
    curr_url = base_url % zipcode
    browser.get(curr_url)
    sleep(5)
    school_links = set()
    try:
        soup = BeautifulSoup(browser.page_source, "html.parser")
        schools = soup.find_all('h3',class_='panel-title')
        for item in schools:
            try:
                current_school = item.find('a')['href']
                school_links.add(current_school)

            except Exception as e:
                print (e)
    except Exception as e:
        print (e)
    for school in school_links:
        process_school(browser, school, filename)

def process_school(browser, school_url, filename):
    """Parses and retrieves information from school url
    \
    browser: selenium browser, school_url:explanatory"""
    browser.get(school_url + rankings_page)
    sleep(4)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    school_name = ""
    address = ""
    city = ""
    state = ""
    zipcode = ""
    phone = ""
    district = ""
    ratio = ""

    try: # name
        school_name = ((soup.find('span', {"itemprop" : "name"})).text).strip()
    except Exception as e:
        print (e)
    try: # address
        address = ((soup.find('span', {"itemprop" : "streetAddress"})).text).strip()
    except Exception as e:
        print (e)
    try:#city
        city = ((soup.find('span', {"itemprop" : "addressLocality"})).text).strip()
    except Exception as e:
        print (e)
    try: #state
        state = ((soup.find('span', {"itemprop" : "addressRegion"})).text).strip()
    except Exception as e:
        print (e)
    try: # zip
        zipcode = ((soup.find('span', {"itemprop" : "postalCode"})).text).strip()
    except Exception as e:
        print (e)
    try: # district
        district = ((soup.find('div', {"id" : "ctl00_ContentPlaceHolder1_scTabRankings_divLeaRank"})).find('h4').text).strip()
        if ':' in district:
            district = district.replace(':',"")
    except Exception as e:
        print (e)
    try: # phone
        phone = ((soup.find('span', {"itemprop" : "telephone"})).text).strip()
    except Exception as e:
        print (e)
    try: # ratio
        ratio = ((soup.find_all('span', {"class" : "bigOrange"})[1]).text).strip()
    except Exception as e:
        print (e)
    #rankings dictionary. use a dictionary to look up year and input the appropriate item for writing. key:year
    rankings = {}
    #rankings value: (tuple) 1 = ranking, 2 = total schools, 3 = percentile
    table = soup.find('div', {"id" : "tableWrapper"})
    table_row = table.find_all('tr')
    for row in table_row[1:]:
        try:
            table_entries = row.find_all('td')
            rankings[table_entries[0].text] = (table_entries[2].text, table_entries[3].text, table_entries[4].text)

        except Exception as e:
            print (e)

    row_data = [school_name, address, city, state, zipcode, district, ratio] # prepare data for writing
    for i in range(2016, 2003, -1): # get yearly data
        key = str(i)
        if key in rankings: # check if it exists in dictionary
            current_row = rankings[key] # add data
            row_data += [current_row[0], current_row[1], current_row[2]]
        else: # else add non existent
            row_data += ["N/A" for x in range(3)]

    write_school(filename, row_data) # save the data

def create_file(file_out = time.strftime("%Y%m%d-%H%M%S") + "schools.csv"):
    """Create the initial file for storing csv data. Default output is timestamped"""
    with open(file_out,'w+', newline = '') as csvfile:
        spamwriter = csv.writer(csvfile)
        headers = ['School', 'Address', 'City', 'State', 'Zip', 'District', 'S/T ratio']
        for i in range(2016, 2003, -1):
            headers.append("%d Ranking" % i)
            headers.append("%d Ranked Schools" % i)
            headers.append("%d Percentile" % i)
        spamwriter.writerow(headers)
    return file_out

def write_school(file_out, row):
    """writes row of data to file_out"""
    with open(file_out, 'a') as csvfile:
        spamwriter = csv.writer(csvfile)
        try:
            spamwriter.writerow(row)
        except Exception as e:
            print (e)


def main():
    browser = webdriver.Chrome()
    browser.implicitly_wait(30)

    zipcodes = get_zips_from_file('resources\LosAngelesZips.txt')
    zipcodes += get_zips_from_file('resources\SantaClaraZips.txt')
    filename = create_file()
    for zipcode in zipcodes:
        process_zipcode(browser, zipcode, filename)

    browser.close()


if __name__ == '__main__':
    main()
