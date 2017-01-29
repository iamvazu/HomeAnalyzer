#-------------------------------------------------------------------------------
# Name:        schedules
# Purpose:  Grabs all data to be analyzed for LA, SC county
#
# Author:      Lord Azu
#
# Created:     22/01/2017
# Copyright:   (c) Lord Azu 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from schools import schoolinfo
from time import sleep
from crime import crimeinfo
from homes.zillow import *

def main():
    crimeinfo.grab_crime_data()
    sleep(6)
    schoolinfo.grab_school_data()# grab school
    sleep(6)
    zillow_la_santaclara.get_zillow_info()
    sleep(6)

if __name__ == '__main__':
    main()