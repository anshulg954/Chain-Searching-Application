from bs4 import BeautifulSoup
import requests
import json
import re
import urllib.parse
from multiprocessing.dummy import Pool as ThreadPool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import re
import time
# from url_process import get_dynamic_url,insert_dynamic_url
import urllib.parse
import json
from database_mongo import *
import pprint


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--log-level=3")
options.add_argument("--no-sandbox")

# defining a global list for the data to be saved
info_lst = []

def extract_tags(page_count):
    link = "https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22parameters%22%3A%7B%22value%22%3A%22a%22%7D%2C%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22node_id%22%3A0%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22pager%22%3A%7B%22start%22%3A0%2C%22rows%22%3A100%7D%2C%22scoring_strategy%22%3A%22combined%22%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%7D%2C%22request_info%22%3A%7B%22src%22%3A%22ui%22%2C%22query_id%22%3A%220e78c1657e13337d974c3dcca4505e08%22%7D%7D"
    driver = webdriver.Chrome(
        executable_path='E:\Work\Miskaa\chromedriver', options=options)
    driver.get(link)
    datas = []
    print(page_count)
    for i in range(page_count):
        time.sleep(5)
        html = driver.page_source
        soup = bs(html, "lxml")
        data_entries = soup.find_all("table", class_="results-item-header")
        for data_e in data_entries:
            datas.append(data_e.tr.td.h3.a.text)
            # print(datas)
        time.sleep(2)
        driver.find_element_by_xpath(
            "//*[@id='app']/div[4]/div[2]/div[2]/div/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]").click()
    return datas


def get_data_for_tag(data):
    # print(data)
    time.sleep(5)
    global info_lst
    info_dic = {}
    link = "https://www.rcsb.org/fasta/entry/"+data+"/display"
    try:
        source = requests.get(link).text
        soup = BeautifulSoup(source, 'lxml')
        chain = soup.text
        info_dic['key'] = data
        info_dic['url'] = "https://www.rcsb.org/structure/"+data
        info_dic['chain'] = chain.split("\n")[1]
        info_lst.append(info_dic)
        print("Added data for "+data)
    except:
        print("Failed for "+data)


def check(search, filedata):
    ans = []
    for data in filedata:
        if search in data['chain']:
            ans.append(data['url'])
    return ans


if __name__ == "__main__":

    start = time.time()

# ------------------------------SCRAPPING THE TAGS FROM THE MAIN PAGE----------------------------------

    # getting the data from the site as the dataset withe the query of "a"
    datas = extract_tags(2)
    print(len(datas))
    print(datas)

    # # saving the data in the file
    # with open("tags.txt", "w") as tag:
    #     tag.write(str(datas))

    # # sample data extracted
    # # datas = ['5H7A', '167D', '1D6D', '1IKK', '6S47', '6T83', '6GQV', '6SV4', '6T4Q', '6SNT', '6T7I', '6HD7', '1EEG', '6QTZ', '6RI5', '6MEM', '6QT0', '6QIK', '6PY0', '6R86', '3A5C', '6RZZ', '1D49', '6TNU', '1FML', '1FMJ', '5NDG', '6YLG', '6S05', '1OZ8', '1AQB', '1CRB', '1D57', '1D56', '6I7O', '1KQW', '6R84', '6R87', '1HBP', '6YLH', '6Z6K', '1KT7', '1KT6', '1KT5', '1KT4', '1KT3', '1GX8', '6Z6J', '6QXE', '1KGL', '1MX8', '6YLY', '4QYN', '4QZT', '1EII', '5H8T', '5HBS', '5LJD', '5LJC', '5LJE', '5LJB', '2RCT', '6HHQ', '1IIU', '6T7T', '5GAK', '5OBM', '6Q8Y', '6GQB', '6QX3', '1JDG', '1GYT', '2ZNL', '6GQ1', '1BXH']

    # formartting and writing the data in file for future use:
    # with open("tags1.txt", "w") as tag:
    #     # print(tag.readlines()[0])
    #     for t in datas:
    #         temp = str(t)+","
    #         tag.write(temp)

# ------------------------------------GETTING THE FINAL DATA----------------------------------------

    # # # we need to have some time as after making a large number of requests at the same time we will not be getting the data back

    # reading from the file to get the tags
    # with open("tags1.txt", "r") as tag:
    #     datas = (tag.read().split(",")[:-1])

    # # print(datas[:50])

    # # Make the Pool of workers
    # pool = ThreadPool(20)

    # # getting the data for each of the tag which we had stored

    # pool.map(get_data_for_tag, datas[11000:])

    # # Close the pool and wait for the work to finish
    # pool.close()
    # pool.join()

    # # checking the data
    # # print(info_lst)
    # print(len(info_lst))

    # # saving the final dataset

    # with open("temp.json", "w") as inp:
    #     inp.write(str(info_lst))
    # print("Data has been inserted.")

# -------------------------------------INSERTING IN THE DATABSE------------------------------

    # # inserting the data in the database
    # json_get()    # till here for the app

# ------------------------------------------SEARCHING----------------------------------------

    # query part searching
    # search = str(input("Enter the chain you wanna search: "))
    # search = search.upper()

    # # searching using regex
    # ans = search_chains(search)

    # # checking the length of the data recived by us and printing the data
    # pprint.pprint(ans)
    # print(len(ans))


# --------------------------------------------------------------------------------------------

    end = time.time()
    print(end-start)

# --------------------------------------------------------------------------------------------

    # the checking of strings start from here

    # print(link)
    # source = requests.get(link).text
    # soup = BeautifulSoup(source, 'lxml')
    # # print(soup)
    # data_entries = soup.find_all("table", class_="results-item-header")
    # print(data_entries)
    # for data_e in data_entries:
    #     print(data_e.text)

    # print(urllib.parse.parse_qs(link))
    # query = str({"query": {"parameters": {"value": "a"}, "service": "text", "type": "terminal", "node_id": 0}, "return_type": "entry", "request_options": {"scoring_strategy": "combined", "sort": [
    #             {"sort_by": "score", "direction": "desc"}], "pager": {"start": 0, "rows": 100}}, "request_info": {"src": "ui", "query_id": "81b2a20834e1c9279b0aaa234d8f3fe6"}})
    # print("https://www.rcsb.org/search?request="+urllib.parse.quote(query).replace("%27","%22"))


# https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22parameters%22%3A%7B%22value%22%3A%22a%22%7D%2C%22service%22%3A%22text%22%2C%22type%22%3A%22terminal%22%2C%22node_id%22%3A0%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22pager%22%3A%7B%22start%22%3A100%2C%22rows%22%3A100%7D%2C%22scoring_strategy%22%3A%22combined%22%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%7D%2C%22request_info%22%3A%7B%22src%22%3A%22ui%22%2C%22query_id%22%3A%2281b2a20834e1c9279b0aaa234d8f3fe6%22%7D%7D
# https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22parameters%22%3A%7B%22value%22%3A%22a%22%7D%2C%22service%22%3A%22text%22%2C%22type%22%3A%22terminal%22%2C%22node_id%22%3A0%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22scoring_strategy%22%3A%22combined%22%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%2C%22pager%22%3A%7B%22start%22%3A0%2C%22rows%22%3A100%7D%7D%2C%22request_info%22%3A%7B%22src%22%3A%22ui%22%2C%22query_id%22%3A%2281b2a20834e1c9279b0aaa234d8f3fe6%22%7D%7D

# https://www.rcsb.org/search?request={"query":{"parameters":{"value":"a"},"service":"text","type":"terminal","node_id":0},"return_type":"entry","request_options":{"scoring_strategy":"combined","sort":[{"sort_by":"score","direction":"desc"}],"pager":{"start":0,"rows":100}},"request_info":{"src":"ui","query_id":"81b2a20834e1c9279b0aaa234d8f3fe6"}}
'''
{
    "query": {
        "parameters": {
            "value": "a"
        },
        "service": "text",
        "type": "terminal",
        "node_id": 0
    },
    "return_type": "entry",
    "request_options": {
        "scoring_strategy": "combined",
        "sort": [
            {
                "sort_by": "score",
                "direction": "desc"
            }
        ],
        "pager": {
            "start": 0,
            "rows": 100
        }
    },
    "request_info": {
        "src": "ui",
        "query_id": "81b2a20834e1c9279b0aaa234d8f3fe6"
    }
}
'''
