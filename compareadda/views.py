from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
# from difflib import get_close_matches
# import webbrowser
from collections import defaultdict
import random
from selenium import webdriver
# p_element = driver.find_element_by_id(id_='intro-text')
# #print(p_element.text)
# from webdriver_manager.chrome import ChromeDriverManager
from . import proxy_gen

def home(request):
    return render(request, 'temp.html')

class Price_compare:

    def price_amzn(self,key):
        #print(key)

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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

        map = defaultdict(list)
        home = 'https://www.amazon.in'


        # proxies = {'http': "http://" + proxy_gen.generate_proxy()}  # }
        # source_code = requests.get(url_amzn, headers=headers, proxies=proxies)  # , headers = headers, proxies=proxies)
          
        # #print(source_code.text)
        proxy = "http://c52b5c62b02ad159e23c7c769e6290eac79f36f7:@proxy.zenrows.com:8001"
        proxies = {"http": proxy, "https": proxy}
        source_code = requests.get(url_amzn, proxies=proxies, verify=False)
        # print(response.text)
        plain_text = source_code.text
        # #print(plain_text)
        soup = BeautifulSoup(plain_text, "html.parser")
        # #print(self.soup)
        ind = 0
        # #print(plain_text)
        for html in soup.find_all('div', {'class': 'sg-col-inner'}):
            title, link, price = None, None, None
            reviews=None
            for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-price-whole'}):
                price = p.text.replace(',', "")
            for l in html.find_all('a', {
                'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}):
                link = home + l.get('href')
            #print(title, link, price)
            for review in html.find_all('span', {'class': 'a-icon-alt'}):
                reviews= review.text
            print(reviews)
            if title and link and ((str(title)).lower().find(str(key).lower())!=-1) and reviews:
                map[title] = [price, link, reviews]
          
        # user_input = self.var.get().title()
        # return
        # self.matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
        if not bool(map):
            map["Not available"] = ["price", "link", ""]
        result = []
        for title in map:
            #print(title)
            result.append([title, map[title][0], map[title][1],  map[title][2]])

        return result

    def price_amzn2(self, key):
        #print(key)
        url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)

        # Faking the visit from a browsercd .
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        map = defaultdict(list)
        home = 'https://www.amazon.in'
        # proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
        #                 "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
        #                 "134.213.29.202:4444"]
        # proxies = {'https': "https://" + random.choice(proxies_list)}
        source_code = requests.get(url_amzn, headers=headers)
        # #print(source_code.text)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        # #print(self.soup)
        ind = 0
        for html in soup.find_all('div', {'class': 'sg-col-inner'}):
            #print(html)
            #print()
            #print()
            title, link = None, None
            for heading in html.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'}):
                title = heading.text
            for p in html.find_all('span', {'class': 'a-price-whole'}):
                price = p.text.replace(',', "")
            for l in html.find_all('a', {'class': 'a-link-normal a-text-normal'}):
                link = home + l.get('href')
            # #print(title,link,price)
            if title and link:
                map[title] = [price, link]
        # user_input = self.var.get().title()
        # return
        # self.matches_amzn = get_close_matches(user_input, list(map.keys()), 20, 0.01)
        self.looktable = {}
        result = []
        for title in map:
            result.append([title, map[title][0], map[title][1]])

        return result

    def price_flipkart(self, key):
        url_flip = 'https://www.flipkart.com/search?q=' + str(
            key) + '&marketplace=FLIPKART&otracker=start&as-show=on&as=off'
        map = defaultdict(list)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        proxy = "http://c52b5c62b02ad159e23c7c769e6290eac79f36f7:@proxy.zenrows.com:8001"
        proxies = {"http": proxy, "https": proxy}
        source_code = requests.get(url_flip, proxies=proxies, headers=self.headers, verify=False)
        # source_code = requests.get(url_flip, headers=self.headers)
        soup = BeautifulSoup(source_code.text, "html.parser")
        # #print(source_code.text)
        home = 'https://www.flipkart.com'
        for block in soup.find_all('div', {'class': '_1AtVbE'}):
            title, price, link = None, 'Currently Unavailable', None
            #print(block.find('div', {'class': '_4rR01T'}))
            # #print()
            for heading in block.find_all('div', {'class': '_4rR01T'}):
                #print(heading)
                title = heading.text
            for p in block.find_all('div', {'class': '_30jeq3 _1_WHN1'}):
                price = p.text[1:].replace(",", "")
            for l in block.find_all('a', {'class': '_1fQZEK'}):
                link = home + l.get('href')

            #print(title)
            if title and ((str(title)).lower().find(str(key).lower())!=-1):
                #print(title,link,price)
                map[title] = [price, link]
            
        # return
        # user_input = self.var.get().title()
        result = []
        #print(map)
        for ele in map:
            result.append([ele, map[ele][0], map[ele][1]])
        return result

    def get_list_sc(self, key):
        url = "https://www.shopclues.com/search"
        source_code = requests.get(url,params={
            'q': key,
            'z': 0,
            'user_id': '',
            'user_segment': 'default',
            'rc':1
        })

        soup = BeautifulSoup(source_code.text, "html.parser")
        prices = {}
        elements = soup.find_all('div', {'class': 'search_blocks'})
        for element in elements:
            try:
                title= element.find('h2').get_text().lower()
                link = element.find('a')['href'][2:]

                price = int(element.find('div', {'class': 'ori_price'}).find('span',{'class':'p_price'}).get_text()[1:].replace(',',""))
                prices[title] = [price,"https://" +link]
            except Exception as e:
                #print(e)
                continue
        result = []
        for ele in prices.keys():
            result.append( [ele,prices[ele][0], prices[ele][1]]  )
        return result


    def price_croma(self,key):
        #print(key)

        # url_amzn = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + str(key)
        url_croma = 'https://www.croma.com/searchB?q=' + str(key)  + '%3Arelevance' 

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
        home = 'https://www.croma.com'


        # proxies = {'http': "http://" + proxy_gen.generate_proxy()}  # }
        # source_code = requests.get(url_amzn, headers=headers, proxies=proxies)  # , headers = headers, proxies=proxies)
        
        # #print(source_code.text)
        proxy = "http://ffffacf2d30d7a70707e0916f2888c00f09500ca:@proxy.zenrows.com:8001"
        proxies = {"http": proxy, "https": proxy}
        source_code = requests.get(url_croma, proxies=proxies, verify=False)
        # print(response.text)
        plain_text = source_code.text
        # #print(plain_text)
        soup = BeautifulSoup(plain_text, "html.parser")
        # #print(self.soup)
        ind = 0
        # #print(plain_text)
        for html in soup.find_all('div', {'class': 'product-item'}):
            title, link, price = None, None, None
            reviews=None
            for heading in html.find_all('h3', {'class': 'product-title plp-prod-title'}):
                title = heading.children.text
                print(title)
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
        if not bool(map):
            map["Not available"] = ["price", "link", ""]
        result = []
        for title in map:
            #print(title)
            result.append([title, map[title][0], map[title][1],  map[title][2]])

        return result
    


def search(request):
    key = request.POST.get("query")
    obj = Price_compare()
    amazon_price =  obj.price_amzn(key)
    count = 0
    while( len(amazon_price) == 0 and count < 10 ):
        amazon_price = obj.price_amzn(key)
        count+=1

    count = 0
    flipkart_price = obj.price_flipkart(key)
    while(len(flipkart_price) == 0 and count < 10):
        flipkart_price = obj.price_flipkart(key)
        # break
        count+=1
    sclues_price = obj.get_list_sc(key)
    # #print(amazon_price)
    return render(request, 'search.html', {'sclues_price' : sclues_price, 'amazon_price' : amazon_price, 'flipkart_price' : flipkart_price})
    # return render(request, 'search.html', {'amazon_price' : amazon_price})