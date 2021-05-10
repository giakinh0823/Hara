# -*- coding: utf-8 -*-
# import build-in packages
import io
import time
import os
from decimal import Decimal
from urllib.parse import urlparse
from urllib.parse import urlparse
import urllib.request as urllib2
from django.core.files import File
from django.core.files.base import ContentFile

import pip
import warnings
from datetime import datetime

from .models import Product, Category

import random

# ignore future warnings
warnings.filterwarnings("ignore")


# call for pip command
def install(package):
    pip.main(['install', package])


# pandas, bs4, selenium, webdriver-manager, ftfy packages
def requirements_check(package):
    try:
        __import__("pandas")
        __import__("bs4")
        __import__("selenium")
        __import__("webdriver_manager")
        __import__("ftfy")
        __import__("numpy")
    except:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pandas"])
        __import__("pandas")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "bs4"])
        __import__("bs4")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "selenium"])
        __import__("selenium")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "webdriver-manager"])
        __import__("webdriver_manager")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "ftfy"])
        __import__("ftfy")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', "numpy"])


requirements_check("pandas")
requirements_check("bs4")
requirements_check("selenium")
requirements_check("webdriver_manager")
requirements_check("ftfy")
requirements_check("numpy")

# Import packages
import pandas as pd
from selenium import webdriver
from bs4 import SoupStrainer
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ftfy import fix_encoding
import numpy as np


def data_scrap(request):
    link = 'https://www.indiegogo.com/explore/all?project_type=campaign&project_timing=all&sort=trending'
    # Empty lists for storing information
    list_of_title = []
    list_of_caption = []
    list_of_price = []
    list_of_image = []
    list_of_percent = []
    list_of_category = []

    # Driver
    global driver
    browser = ""
    while browser != "exit":
        browser = input("Enter number of your browser: "
                        "\n1. Chrome"
                        "\n2. Edge"
                        "\n3. Firefox"
                        "\nYour choice: ")
        if browser == "1":
            driver = webdriver.Chrome(ChromeDriverManager().install())
            break
        elif browser == "2":
            driver = webdriver.Edge(EdgeChromiumDriverManager().install())
            break
        elif browser == "3":
            driver = webdriver.Firefox(GeckoDriverManager().install())
            break
        else:
            print("Valid value only in range 1->3")
    driver.get(str(link))
    time.sleep(1)

    time.sleep(6)
    accept_cookie = driver.find_element_by_xpath('//a[@id="CybotCookiebotDialogBodyButtonAccept"]')
    accept_cookie.click()
    time.sleep(6)

    # Locating the Show more button
    show_more_button = driver.find_element_by_xpath('//a[@gogo-test="show_more"]')
    print(show_more_button)

    count = 0

    while show_more_button.is_enabled() is not False and count < 30:
        show_more_button.click()
        count += 1
        time.sleep(3)
    print("Begin")

    # Get product title, category, price, image, caption, percent
    htmlSource = driver.page_source
    only_class = SoupStrainer("div", {"class": "exploreDetail-campaigns row"})
    print(only_class)
    list_product = BeautifulSoup(htmlSource, "html.parser", parse_only=only_class)
    print(list_product)
    for item in list_product.findAll("discoverable-card", {"class": "ng-scope ng-isolate-scope"}):
        for title in item.findAll("div", {"class": "discoverableCard-title ng-binding discoverableCard-lineClamp2"}):
            list_of_title.append(str(title.text))
        for caption in item.findAll("div",
                                    {"class": "discoverableCard-description ng-binding discoverableCard-lineClamp3"}):
            list_of_caption.append(str(caption.text))
        for category in item.findAll("div", {"class": "discoverableCard-category ng-binding"}):
            list_of_category.append(str(category.text))
        for price in item.findAll("div", {"class": "discoverableCard-balance ng-binding ng-scope"}):
            priceText = str(price.text)
            priceText.replace("£", "")
            priceText.replace("€", "")
            priceText.replace("$", "")
            list_of_price.append(priceText)
        for percent in item.findAll("div", {"class": "discoverableCard-percent"}):
            percent_text = str(percent.text).replace("%", "")
            percent_text = percent_text.replace(" ", "")
            percent_text = percent_text.strip()
            list_of_percent.append(percent_text.replace("%", ""))
        for image in item.findAll("div", {"class": "discoverableCard-image lazyloaded"}):
            img = image.find("source", attrs={"data-srcset": True})
            list_of_image.append(str(img.get('data-srcset')))

    # Set rational sleep time
    time.sleep(2)

    # Get everything u need
    driver.close()
    # Get product title, category, price, image, caption, percent
    for i in range(len(list_of_title)):
        try:
            category = Category.objects.get(name=list_of_category[i])
        except:
            category = Category.objects.create(name=list_of_category[i])
            category.save()
        price = list_of_price[i].strip()
        price = price[1:]
        text_price = str(price).replace(',', '.')
        if len(text_price) >= 8:
            text_price = text_price.replace('.', '', 1)

        try:
            decimal = float(text_price)
        except:
            decimal = float(10)
        print(text_price)

        try:
            image = list_of_image[i]
        except:
            image = None

        percent = str(list_of_percent[i]).replace(',','.')
        print(percent)
        product = Product.objects.create(
            user=request.user,
            title=str(list_of_title[i]),
            category=category,
            price=decimal,
            caption=str(list_of_caption[i]),
            like=random.randint(50,1000),
            percent=float(percent),
            img=image,
        )
        img_url = list_of_image[i]
        name_image = urlparse(img_url).path.split('/')[-1]
        content = io.BytesIO(urllib2.urlopen(img_url).read())
        product.img.save(name_image, content, save=True)
        product.save()

    print(list_of_title, list_of_caption, list_of_price, list_of_category, list_of_percent, list_of_image, )

    # Create dataframe
    df = pd.DataFrame(
        list(zip(list_of_title, list_of_caption, list_of_price, list_of_category, list_of_percent, list_of_image)),
        columns=['title', 'caption', 'price', 'category', 'percent', 'image'])

    # Fix unicode errors
    df['title'] = df['title'].map(lambda x: fix_encoding(x))
    df['caption'] = df['caption'].map(lambda x: fix_encoding(x))
    df['category'] = df['category'].map(lambda x: fix_encoding(x))
    df['price'] = df['price'].map(lambda x: fix_encoding(x))
    df['percent'] = df['percent'].map(lambda x: fix_encoding(x))
    # df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Output
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    fileData = "data_" + current_time + ".csv"
    df.to_csv(fileData, index=False)
    file_name = "products_indiegogo_" + current_time + ".csv"
    df.to_csv(file_name, index=False)
    print("-----------------------------------------------")
    print("Your file is ready! Check " + str(file_name))
    print("-----------------------------------------------")
    print("PROCESS ENDED.")
    input("Press Enter to continue...")


# value = ""

# while value != "exit":
#     value = input("------------------------------------------------"
#                   "\nEnter one of the following values:"
#                   "\n0. Build data"
#                   "\n1. Quit"
#                   "\n-----------------------------------------------"
#                   "\nYour value: ")
#     if value == '0':
#         link = input("Enter the link link: ")
#         while link == "":
#             link = input("This field must not be empty: ")
#         data_scrap(link)
#     elif value == '1':
#         exit()
#     else:
#         print("Valid values are in range (0) only!")
#         print()
