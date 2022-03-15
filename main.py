import json
import random
from itertools import cycle

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import lxml
from selenium.webdriver.common.by import By
import requests

from proxy import get_free_proxies

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.116 " \
             "YaBrowser/22.1.1.1544 Yowser/2.5 Safari/537.36 "
headers = {
    "user-agent": user_agent,
    "accept": "*/*"
}
list_proxy = get_free_proxies()
proxy_cycle = cycle(list_proxy)

# proxies = {
#     # 'http': f'http://{login}:{password}@{ip}:{port}'
#     'http': f'http://baygelov2001:oyEGpSMyII@185.230.88.22:59100',
#     'socks5': f'https://baygelov2001:oyEGpSMyII@185.230.88.22 :59101'
# }


# def get_html(url):
#     PATH = r"C:\Users\bayge\PycharmProjects\parsing-lessons\selenium_lesson1\chromedriver\chromedriver.exe"
#     s = Service(executable_path=PATH)
#
#     options = webdriver.ChromeOptions()
#     options.add_argument(user_agent)
#     options.add_argument("--disable-blink-features=AutomationControlled")
#
#     driver = webdriver.Chrome(service=s, options=options)
#
#     try:
#         driver.get(url=url)
#         driver.implicitly_wait(5)
#
#         with open("index.html", "w", encoding="utf-8") as file:
#             file.write(driver.page_source)
#         print("done")
#
#     except Exception as ex:
#         print(ex)
#
#     finally:
#         driver.close()
#         driver.quit()


def get_customer_data():
    with open("index.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    customers_cards = soup.find_all("div", class_="rxmfs")

    customer_list_result = []
    customer_urls = []
    timeout = random.randint(30, 60)

    for customer_url in random.sample(customers_cards, len(customers_cards)):
        proxy = proxy_cycle
        proxies = {
            "http": f"socks4://{proxy}",

        }
        customer_url = "https://prom.ua" + customer_url.find("a").get("href")
        customer_urls.append(customer_url)

        req = requests.get(url=customer_url, headers=headers, proxies=proxies, timeout=timeout)
        soup = BeautifulSoup(req.text, "lxml")
        print(req)

        customer_url_ua = "https://prom.ua" + soup.find("a", class_="J6BAS").get("href")

        req = requests.get(url=customer_url_ua, headers=headers, proxies=proxies, timeout=timeout)
        soup = BeautifulSoup(req.text, "lxml")

        customer_name = soup.find("span", class_="jSQa5").text
        customer_name = customer_name.replace("Продавець ", "")
        customer_location = soup.find("div", class_="og3Z2").find("span", class_="F5Vvy").text
        customer_location = customer_location.split(',')

        customer_list_result = [{
            "Customer_name": customer_name,
            "Customer_url": customer_url_ua,
            "Location": customer_location[0]
        }]

        print(customer_list_result)
    with open("customer_list_result.json", "w", encoding="utf-8") as file:
        json.dump(customer_list_result, file, indent=4, ensure_ascii=False)


def main():
    # get_html("https://prom.ua/Unty-uggi-snoubutsy;K")
    get_customer_data()


if __name__ == "__main__":
    main()
