#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lord Azu
#
# Created:     18/01/2017
# Copyright:   (c) Lord Azu 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import csv
import requests
import urllib
from time import sleep
import queue
from urllib.parse import urlparse
import urllib.request
import os
import time

base_url = 'http://www.city-data.com/crime/'


def get_state_links(s):
    """grabs all relavent state links embedded in the web page
    \
    s: requests session object"""
    page_source = (s.get(base_url)).content
    #grab all links
    state_links = set()# change to ordered set
    soup = BeautifulSoup(page_source, "html.parser")
    for a in soup.find_all('a', href = True): #find all links
        link = a['href']
        if base_url in link and link != base_url: #check links to other states
            state_links.add(link)

    return sorted(state_links)

def process_states(s, state_links, fileout):
    """ grabs all counties per state
    \
    s: requests session obj, state_links: set obj"""
    #s = requests.session()

    for state in state_links:
        print ("Now looking at %s" % state)
        try:
            page_source = (s.get(state)).content
            county_links = set() #individual county links
            soup = BeautifulSoup(page_source, "html.parser")
            for a in soup.find_all('a', href = True): #find all links
                link = a['href']
                print ( "checking href: %s" % link)
                if 'crime' in  link : #check links to other states
                    county_links.add(base_url + link)
            for city in county_links:

                process_city(s, city, fileout)
                sleep(4)
        except Exception as e:
            print (e)
        sleep(4)


def process_city(s, url, fileout):
    """ Grabs all relavent data from url representing county
    \
    s: request Session obj, url: str url"""
    city_data = {}


    print ("working: %s " % url)
    try:
        response = (s.get(url)).content
        soup = BeautifulSoup(response, "html.parser")
        graphs = soup.find_all('div', {"class" : "hgraph"}) # look for all horizontal bar charts
        crime_tables = []
        for ele in graphs: # loop through all charts and search for crime charts
            try:
                text = ele.text
                if 'crime' in text:
                    crime_tables.append(ele.text)
            except Exception as e:
                print (e)

        city = crime_tables[0].split(",")[0] # get the current city and state. combine these 2 lines...but lazy
        state = crime_tables[0].split(",")[1]
        state = state[:3]

        city = city.replace("See how dangerous ", "")# live dangerously
        #print (city)
        violent_crimes = []# separate violent and property crimes
        propery_crimes = []
        use_violent = False
        for item in crime_tables[1:]: #loop past first index
            data = item.split(city)
            #print(data)
            if "Violent" in data[0]: # decide which list to populate
                year = data[0].replace("Violent crime rate in ", "")
                use_violent = True
            else:
                year = data[0].replace("Property crime rate in", "")
                use_violent = False
            rates = data[1].split("U.S. Average:")
            city_rate = rates[0].replace(":","")
            avg_rate = rates[1]
            if use_violent: # append to proper positions
                violent_crimes.append((year, city_rate))
            else:
                propery_crimes.append((year, city_rate))

        city_data["Violent"] = violent_crimes
        city_data["Property"] = propery_crimes
        if  city != None and city != "":
            write_city(city, state, city_data, fileout)
    except Exception as e:
        print (e)

def create_file(file_out = time.strftime("%Y%m%d-%H%M%S") + "-Crimedata.csv"):
    """Create a timestamped csvfile"""
    with open(file_out,'w+', newline = '') as csvfile:
        spamwriter = csv.writer(csvfile)
        headers = ['city', 'state']
        for i in range(2014, 2001, -1):
            headers.append("%d Violent rate" % i)
        for i in range(2014, 2001, -1):
            headers.append("%d Property rate" % i)
        spamwriter.writerow(headers)
    return file_out


def write_city(city, state, city_table, fileout):
    """Writes property and crime rates to fileout
    \
    city: str, state: str, city_table: dict containing keys of crimetype. Each key maps to a list of tuples indicating year/rate, fileout: outfile"""
    with open(fileout,'a') as csvfile:
        spamwriter = csv.writer(csvfile)
        violent_rates = city_table["Violent"]
        property_rates = city_table["Property"]
        row = [city, state]
        row += [i[1] for i in violent_rates]
        row += [i[1] for i in property_rates]
        try:
            spamwriter.writerow(row)
        except Exception as e:
            print (e)

def main():
    s = requests.session()
    state_links = get_state_links(s)
    fileout = create_file()
    process_states(s, state_links, fileout)
    s.close()

    print ('finished')

if __name__ == '__main__':
    main()
