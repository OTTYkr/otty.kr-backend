import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time
from sqlalchemy.sql import *
import FinanceDataReader as fdr


class YahooScreener:
    def __init__(self):
        self.session = None
        self.crumb = None
        self.currency = None
        # 상장 종목 목록 가져오기
        self.krx = fdr.StockListing('KRX')
        self.krx_code = {}
        for d in self.krx.itertuples():
            self.krx_code[d.Code] = d.Name

    def start_module(self):
        # 쿠키 및 세션 설정
        self.session = requests.Session()
        self.get_cookie_crumb()
        # 환율 가져오기
        self.get_upbit_currency()

        self.get_screener()

    def get_cookie_crumb(self):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # 창 숨기는 옵션 추가
        options.add_argument("headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://finance.yahoo.com/")
        driver.get("https://query2.finance.yahoo.com/v1/test/getcrumb")

        # crumb 값 설정
        self.crumb = driver.find_element(By.XPATH, "/html/body").text
        # cookie 값 설정
        cookies = driver.get_cookies()
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        driver.quit()

    def get_upbit_currency(self):
        url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
        }
        self.currency = requests.get(url, headers=headers).json()[0]['basePrice']

    def get_screener(self):
        screener_url = ("https://query2.finance.yahoo.com/v1/finance/screener"
                        "?crumb=%s&lang=en-US&region=US&formatted=true&corsDomain=finance.yahoo.com") % self.crumb

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'
        }
        post_body = {
            "size":200,
            "offset":0,
            "sortField":"intradaymarketcap",
            "sortType":"DESC",
            "quoteType":"EQUITY",
            "topOperator":"AND",
            "query":{
                "operator":"AND",
                "operands":[{
                    "operator":"or",
                    "operands":[{
                        "operator":"EQ",
                        "operands":["region","kr"]}
                    ]}
                ]},
            "userId":"",
            "userIdType":"guid"
        }

        r = self.session.post(screener_url, data=json.dumps(post_body), headers=headers)
        data = json.loads(r.text)

        symbol_list = data['finance']['result'][0]['quotes']


        for i in symbol_list:
            try:
                kr_name = self.krx_code[i['symbol'].split('.')[0]]
            except:
                kr_name = i['longName']
            market_cap = float(i['sharesOutstanding']['raw']) * float(i['regularMarketPrice']['raw'])
            print("-" * 30)
            print("거래소 :", i['fullExchangeName'])
            print("티커 :", i['symbol'])
            print("회사명 :", i['longName'])
            print("현재가 :", i['regularMarketPrice']['raw'])
            print("전일대비 :", i['regularMarketChange']['raw'])
            print("전일대비 (퍼센트) :", i['regularMarketChangePercent']['raw'])
            print("주식발행수 :", i['sharesOutstanding']['raw'])
            print("시가총액 :", i['marketCap']['raw'])
            #print("화폐단위 :", i['currency'])
            print("시장화폐단위 :", i['financialCurrency'])
            print("현재환율 :", self.currency)


if __name__ == "__main__":
    screener = YahooScreener()
    screener.get_screener()