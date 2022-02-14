from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
import time

from optparse import OptionParser
from matplotlib.cbook import dedent
from requests_testadapter import Resp
import requests
import os
import re
import json
import pickle
from lxml import html

import codecs
import csv

#lokasi chrome driver
chromedriver = './chromedriver.exe'
options = webdriver.ChromeOptions()

#options.add_argument('headless')

options.add_argument('window-size=1200x600') # optional
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

#get url
driver.get("https://play.google.com/store/apps/details?id=com.ruangguru.livestudents&hl=id&showAllReviews=true")

#json file save
appname= "ruangguru" # The name of the app- the json files will be named as per this field

wait = WebDriverWait(driver, 20)
SCROLL_PAUSE_TIME = 0.5

# Ganti mode review
driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div/div").click()
time.sleep(3)

# Pilih review terbaru
driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[2]/div[1]").click()
time.sleep(1)

# url = driver.command_executor._url
# session_id = driver.session_id
#
# print(url)
# print(session_id)

# Mendapatkan ukuran ketinggian scroll
last_height = driver.execute_script("return document.body.scrollHeight")

# Counter
k = 0

for i in range(6):

    print("i:", i)

    #scroll jika keluar 'tampilkan lebih banyak'
    for j in range(20):
        print('in inner loop')
        print("j:",j)
        for n in range(20):

            #path username
            username_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k+1) + "]/div/div[2]/div[1]/div[1]/span")

            try:
                #username
                username =  driver.find_element_by_xpath(username_pth).text
            except NoSuchElementException as exception:
                print("error. Username not found")
                break
            else:
                k = k + 1
                #counter nomor review
                print("review number: ",k)


            print(username)

            ##Rating dan Tanggal
            #rating_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[1]/div[1]/div/span[1]/div/div")
            #rating = driver.find_element_by_xpath(rating_pth).get_attribute("aria-label")
            #date_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[1]/div[1]/div/span[2]")
            #date = driver.find_element_by_xpath(date_pth).text

            #Klik Full Review jika review lengkap
            try:
                fullRev_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div["+ str(k) +"]/div/div[2]/div[2]/span[1]/div/button")
                fullRev = driver.find_element_by_xpath(fullRev_pth)
            except NoSuchElementException as exception:
                print("Short Review.")
                review_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[2]/span[1]")
                review = driver.find_element_by_xpath(review_pth).text
            else:
                print("Long review")
                try:
                    fullRev.click()
                except (ElementNotVisibleException, ElementClickInterceptedException) as exception:
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
                    print("Element not clickable. scrolling up")
                    time.sleep(2)
                    fullRev.click()
                #time.sleep(1)

                #Review Path
                review_pth = ("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[" + str(k) +"]/div/div[2]/div[2]/span[2]")
                review = driver.find_element_by_xpath(review_pth).text

            #with open('debug/'+appname+'_username.csv',"a") as output_file:
            #    json.dump({"username": username},output_file)
            #with open('debug/'+appname+'_rating.csv',"a") as output_file:
            #    json.dump({"dump_rating": rating},output_file)
            #with open('debug/'+appname+'_date.csv',"a") as output_file:
            #    json.dump({"date": date},output_file)


            with open('debug/'+appname+'_review.csv',"a") as output_file:
                json.dump(review,output_file)
                output_file.write("\n")

            #tmp = [appname, username, rating, review, date]

            #with open(appname+'.csv',"a") as output_file:
                #fieldnames = ['app_name', 'username', 'rating','review', 'date']
                #output_file.write(str(tmp) + '\n')
                #writer = csv.DictWriter(output_file, delimiter=',',fieldnames=fieldnames)
                #writer.writerow({'app_name':appname,'username':username,'rating':rating,'review':review, 'date':date})


            #with open(appname+'.json',"a") as output_file:
                #json.dump(tmp,output_file)

            print("saved data for:", username)
            print("\n")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    try:
        time.sleep(5)

        #Bug
        #Klik Manual 'Tampilkan Lebih Banyak'
        #element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div").click();
        #element = driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span").click();
        time.sleep(5)
    except NoSuchElementException as exception:
        print("'Show More' not found. Continuing to scroll.")
        continue

