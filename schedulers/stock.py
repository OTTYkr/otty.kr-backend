import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import pytz
from database import EngineConn
from models import Stock_Rank
from sqlalchemy.sql import *


class GetStockRankModule:
    def __init__(self):
        self.engine = EngineConn()
        self.session = self.engine.sessionmaker()

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        # 이미지 저장할 폴더가 없다면 생성
        if not os.path.isdir('./public/com_logo/'):
            os.mkdir('./public/com_logo/')

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'
        }
        self.country = {
            'USA': '미국', 'S. Arabia': '사우디아라비아', 'Taiwan': '대만', 'Denmark': '덴마크',
            'China': '중국', 'France': '프랑스', 'S. Korea': '대한민국', 'Switzerland': '스위스',
            'Netherlands': '네덜란드', 'Japan': '일본', 'UAE': '아랍에미리트',
            'UK': '영국', 'Ireland': '아일랜드', 'India': '인도',
            'Germany': '독일', 'Australia': '호주', 'Spain': '스페인', 'Belgium': '벨기에',
            'Canada': '캐나다', 'Argentina': '아르헨티나', 'Norway': '노르웨이',
            'Hong Kong': '홍콩', 'Brazil': '브라질'
        }

        self.dollar = 0
        self.urls = ['https://companiesmarketcap.com/', 'https://companiesmarketcap.com/page/2/']

    def start_module(self):
        self.upbit_get_usd_krw()
        data = self.get_stock_rank()

        now_date = datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y/%m/%d %H:%M:%S")

        # DB 세션 생성
        db = self.session()

        for d in data:
            if not os.path.isfile('./../public/com_logo/' + d[2] + '.webp'):
                try:
                    urllib.request.urlretrieve('https://companiesmarketcap.com/img/company-logos/64/' + d[2] + '.webp',
                                               "./../public/com_logo/" + d[2] + '.webp')
                except:
                    pass

            t = db.query(exists().where(Stock_Rank.code == d[2])).scalar()

            if t:  # DB에 있다면
                stock_data = db.query(Stock_Rank).where(Stock_Rank.code == d[2]).first()
                stock_data.market_cap = d[3]
                stock_data.price = d[4]
                stock_data.day_change = d[5]
                stock_data.date = now_date
                stock_data.dollar = self.dollar
            else:  # DB에 없다면
                stock_data = Stock_Rank(
                    name=d[1],
                    code=d[2],
                    market_cap=d[3],
                    price=d[4],
                    day_change=d[5],
                    country=d[6],
                    date=now_date,
                    dollar=self.dollar,
                )
                db.add(stock_data)

        db.commit()
        db.close()

    def upbit_get_usd_krw(self):
        url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
        exchange = requests.get(url, headers=self.headers).json()
        self.dollar = exchange[0]['basePrice']

    def get_stock_rank(self):
        data = []
        for url in self.urls:
            r = requests.get(url)
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')

            lists = soup.find('table', class_='dataTable').find('tbody')
            l = lists.find_all('td')

            row = []
            idx = 0
            for i in l:
                text = i.text
                if 'Close Ad' in text or len(text) == 0:
                    continue
                # 기업명 티커 분리
                if idx == 1:
                    if i.find('div', class_='name-div'):
                        row.append(i.find('div', class_='company-name').text)
                        row.append(i.find('div', class_='company-code').text)
                # 달러 단위 통일
                elif idx == 2 or idx == 3:
                    dollar = i.text.replace('$', '').replace(',', '')
                    if 'M' in dollar:
                        dollar = float(dollar.replace('M', '')) * 1000000
                    elif 'B' in dollar:
                        dollar = float(dollar.replace('B', '')) * 1000000000
                    elif 'T' in dollar:
                        dollar = float(dollar.replace('T', '')) * 1000000000000
                    else:
                        dollar = float(dollar)
                    row.append(dollar)
                # 등락 확인
                elif idx == 4:
                    if i.find('span', class_='percentage-red'):
                        row.append('⬇︎ ' + i.text)
                    else:
                        row.append('⬆︎ ' + i.text)
                # 국가명 번역
                elif idx == 5:
                    flag = False
                    for key in self.country:
                        if key in text:
                            row.append(self.country[key])
                            flag = True
                    if not flag:
                        row.append(text)
                else:
                    row.append(text)
                idx += 1
                if idx == 6:
                    data.append(row)
                    row = []
                    idx = 0
        return data
