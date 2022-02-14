from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time

import json

#lokasi chrome driver
chromedriver = './chromedriver.exe'
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.set_window_size(1920,1080)

#Url produk
#driver.get("https://www.tokopedia.com/edisoncomp/mifi-modem-wifi-4g-huawei-e5577-unlock-all-operator-best-seller-hitam")
driver.get("https://www.tokopedia.com/uniqcom/modem-huawei-e3372-4g-lte-fdd-900-1800-150mbps-huawei-hilink")

#driver.execute_script("window.alert = function() {};")

#file simpan
store_name = "mifi"

wait = WebDriverWait(driver, 20)
SCROLL_PAUSE_TIME = 0.5
driver.execute_script("window.scrollTo(0, 300)")
time.sleep(10)

# Ganti mode review
driver.find_element_by_xpath("/html//div[@id='zeus-root']//div[@class='css-1jdotmr']/div[@class='css-lxq5l3']/div[@class='css-7j0kii-unf-tab e1yhziio2']/div[2]/p[@class='css-u5a5vt-unf-heading e1qvo2ff8']").click()
time.sleep(3)

# url = driver.command_executor._url
# session_id = driver.session_id
#
# print(url)
# print(session_id)

# Mendapatkan ukuran ketinggian scroll
# last_height = driver.execute_script("return document.body.scrollHeight")
# print(last_height)

# Counter
for j in range(205):
    print('Page : ',j + 1)
    k = 0
    div = 5
    for n in range(10):

        #path username
        username_pth = ("/html//div[@id='zeus-root']//div[@class='css-1jdotmr']/div[5]/div["+str(div)+"]/div[@class='css-drikti e1ufc1ph1']/div[@class='css-1hkkpmr e1ufc1ph0']/div[@class='css-drikti e1ufc1ph1']//a[@data-testid='txtCustFullNameFilter"+ str(k)+"']")
        try:
            #username
            username = driver.find_element_by_xpath(username_pth).text
        except NoSuchElementException as exception:
            username_pth = ("/html//div[@id='zeus-root']//div[@class='css-1jdotmr']/div[5]/div["+str(div)+"]/div[@class='css-drikti e1ufc1ph1']/div[@class='css-1hkkpmr e1ufc1ph0']/div[@class='css-drikti e1ufc1ph1']//p[@data-testid='txtCustFullNameFilter" + str(k) + "']")
            username = driver.find_element_by_xpath(username_pth).text

        #counter review
        print("review ke: ",k)

        print(username)

        #path view
        review_path = ("/html//div[@id='zeus-root']//div[@class='css-1jdotmr']/div[5]/div["+str(div)+"]/div[@class='css-drikti e1ufc1ph1']/div[@class='css-s5g83y e1ufc1ph0']/p[@class='css-1np3d84-unf-heading e1qvo2ff8'][@data-testid='txtReviewFilter"+ str(k) +"']/span")

        try:
            #review
            review = driver.find_element_by_xpath(review_path).text
        except NoSuchElementException as exception:
            print("Error. Review not found")
            break

        print(review)

        with open('debug/'+store_name+'_review.csv',"a") as output_file:
            json.dump(review,output_file)
            output_file.write("\n")

            print("Save:", username)
            print("\n")

        k = k + 1
        div = div + 1

    driver.execute_script("window.scrollTo(0, 3300)")

    driver.set_page_load_timeout(10)
    element = driver.find_element_by_class_name('css-98hn3t')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(3)

