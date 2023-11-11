#!/usr/sfw/bin/python
# -*- coding: utf-8 -*-
import glob, os, re, sys, time, requests, shutil
import codecs

"""
    Get pages by publication year from https://repertoiretheatreimprime.yale.edu
    Copyright (C) 2022 Philippe Gambette

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
"""

# pip3 install selenium
# install "geckodriver" from https://github.com/mozilla/geckodriver/releases
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Get the current folder
# The downloaded books will be placed in a folder named pages  inside this folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

driver = webdriver.Firefox()

# Specify a 15 second timeout to avoid getting stuck after each download
driver.set_page_load_timeout(15)

documentNb = 0
placeNameNb = 0
source = ""

old_file_names = []
new_file_names = []

for year in range(1600,1701):
   try:
      print("Downloading year " + str(year))
      driver.get("https://repertoiretheatreimprime.yale.edu/")
      time.sleep(2)
      # Set the dates
      date1 = driver.find_element_by_css_selector('#dateMin')      
      date1.send_keys(str(year))
      date2 = driver.find_element_by_css_selector('#dateMax')      
      date2.send_keys(str(year))
      findButton = driver.find_element_by_css_selector('input[type="submit"]')
      findButton.click()
      time.sleep(3)
      f = codecs.open(os.path.join(os.path.join(folder, "yearPages"), "page" + str(year) + ".html"), "w", "utf−8")
      h = driver.page_source
      f.write(h)
   except:
      time.sleep(1)