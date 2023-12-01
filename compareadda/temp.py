from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from difflib import get_close_matches
import webbrowser
from collections import defaultdict
import random
from selenium import webdriver
# p_element = driver.find_element_by_id(id_='intro-text')
# print(p_element.text)
from webdriver_manager.chrome import ChromeDriverManager
import proxy_gen
def temp_func(key):
    # opening our output file in append mode

    # specifying user agent, You can use other user agents
    # available on the internet
    URL  = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)
    proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                    "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                    "134.213.29.202:4444"]

    proxies = {'http': "http://" + random.choice(proxies_list)}  # }
    HEADERS = ({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'})


    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS, proxies  = proxies)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
    print(webpage.content)
    # retrieving product title
    try:
        # Outer Tag Object
        title = soup.find("span",
                          attrs={"id": 'productTitle'})

        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip().replace(',', '')

    except AttributeError:
        title_string = "NA"
    print("product Title = ", title_string)

    # saving the title in the file

    # retrieving price
    try:
        price = soup.find(
            "span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
    # we are omitting unnecessary spaces
    # and commas form our string
    except AttributeError:
        price = "NA"
    print("Products price = ", price)


    # retrieving product rating
    # try:
    #     rating = soup.find("i", attrs={
    #         'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
    #
    # except AttributeError:
    #
    # try:
    #     rating = soup.find(
    #         "span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
    # except:
    #     rating = "NA"
    # print("Overall rating = ", rating)


    try:
        review_count = soup.find(
            "span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')

    except AttributeError:
        review_count = "NA"
    print("Total reviews = ", review_count)


def price_amzn( key):
    print(key)

    # url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)
    url_amzn = 'https://www.amazon.in/s?k='+str(key)+'&crid=3TDQWPKL8X426&sprefix=iph%2Caps%2C376&ref=nb_sb_noss_2'

    # Faking the visit from a browsercd .
    # headers = {
    #     'authority': 'www.amazon.com',
    #     'pragma': 'no-cache',
    #     'cache-control': 'no-cache',
    #     'dnt': '1',
    #     'upgrade-insecure-requests': '1',
    #     # 'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'sec-fetch-site': 'none',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-dest': 'document',
    #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # }

    headers = ({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'})

    map = defaultdict(list)
    home = 'https://www.amazon.in'
    proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                    "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                    "134.213.29.202:4444"]

    proxies = {'http': "http://" + proxy_gen.generate_proxy() } #}

    source_code = requests.get(url_amzn, headers = headers, proxies= proxies )#, headers = headers, proxies=proxies)
    # print(source_code.text)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    # print(self.soup)
    ind = 0
    # print(plain_text)
    for html in soup.find_all('div', {'class': 'sg-col-inner'}):
        title, link, price = None, None, None
        for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
            title = heading.text
        for p in html.find_all('span', {'class': 'a-price-whole'}):
            price = p.text.replace(',', "")
        for l in html.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
            link = home + l.get('href')
        print(title,link, price)
        if title and link:
            map[title] = [price, link]
    # user_input = self.var.get().title()
    # return
    # self.matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
    looktable = {}
    result = []
    for title in map:
        print(title)
        result.append([title, map[title][0], map[title][1]])

    return result


def price_amzn2(key):
        print(key)

        # url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)
        url_amzn = 'https://www.amazon.in/s?k=' + str(
            key) + '&crid=3TDQWPKL8X426&sprefix=iph%2Caps%2C376&ref=nb_sb_noss_2'

        # Faking the visit from a browsercd .
        # headers = {
        #     'authority': 'www.amazon.com',
        #     'pragma': 'no-cache',
        #     'cache-control': 'no-cache',
        #     'dnt': '1',
        #     'upgrade-insecure-requests': '1',
        #     # 'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'sec-fetch-site': 'none',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-dest': 'document',
        #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # }

        headers = ({
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Accept-Language': 'en-US, en;q=0.5'})

        map = defaultdict(list)
        home = 'https://www.amazon.in'
        proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                        "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                        "134.213.29.202:4444"]

        proxies = {'http': "http://" + proxy_gen.generate_proxy()}  # }

        source_code = requests.get(url_amzn, headers=headers, proxies=proxies)  # , headers = headers, proxies=proxies)
        # print(source_code.text)
        plain_text = source_code.text
        # print(plain_text)
        soup = BeautifulSoup(plain_text, "html.parser")
        print(soup)
        ind = 0
        # print(plain_text)
        for html in soup.find_all('div', {'class': 'sg-col-inner'}):
            title, link, price = None, None, None
            for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-price-whole'}):
                price = p.text.replace(',', "")
            for l in html.find_all('a', {
                'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
                link = home + l.get('href')
            print(title, link, price)
            if title and link:
                map[title] = [price, link]
        # user_input = self.var.get().title()
        # return
        # self.matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
        result = []
        for title in map:
            print(title)
            result.append([title, map[title][0], map[title][1]])

        return result





def price_croma(key):

        url_croma = 'https://www.croma.com/searchB?q=' + str(key)  + '%3Arelevance' +'&text=' + str(key) 


        headers = ({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

        map = defaultdict(list)
        home = 'https://www.croma.com'


        proxies = {'http': "http://" + proxy_gen.generate_proxy()}  # }
        source_code = requests.get(url_croma, headers=headers, proxies=proxies)  # , headers = headers, proxies=proxies)
        
        # #print(source_code.text)

        # proxy = "http://ffffacf2d30d7a70707e0916f2888c00f09500ca:@proxy.zenrows.com:8001"
        # proxies = {"http": proxy, "https": proxy}
        # source_code = requests.get(url_croma, proxies=proxies, verify=False)

        # print(response.text)
        plain_text = source_code.text
        #print(plain_text)
        soup = BeautifulSoup(plain_text, "html.parser")
        print(soup.prettify)
        for html in soup.find_all('div', {'class': 'cp-product typ-plp'}):
            print(html.text)
            title, link, price = None, None, None
            reviews=None
            # for heading in html.find_all('h3', {'class': 'product-title plp-prod-title'}):
            #     title = heading.text
            #     print(title)
            # for p in html.find_all('span', {'class': 'a-price-whole'}):
            #     price = p.text.replace(',', "")
            # for l in html.find_all('a', {
            #     'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
            #     link = home + l.get('href')
            #print(title, link, price)
            # for review in html.find_all('span', {'class': 'a-icon-alt'}):
            #     reviews= review.text
            # print(reviews)
            # if title and link and ((str(title)).lower().find(str(key).lower())!=-1) and reviews:
            #     map[title] = [price, link, reviews]
          
        # user_input = self.var.get().title()
        # return
        # self.matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
        # if not bool(map):
        #     map["Not available"] = ["price", "link", ""]
        # result = []
        # for title in map:
        #     #print(title)
        #     result.append([title, map[title][0], map[title][1],  map[title][2]])

        # return result
    



price_croma("iphone13") 




