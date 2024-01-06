import requests
from bs4 import BeautifulSoup
import FinanceDataReader as fdr
import os
from database import EngineConn
from models import KrStocks
from sqlalchemy.sql import *


class TradingViewScraper:
    def __init__(self):
        self.engine = EngineConn()
        self.session = self.engine.sessionmaker()

        # 이미지 저장할 폴더가 없다면 생성
        #if not os.path.isdir('./public/kr_stocks/'):
            #os.mkdir('./public/kr_stocks/')

        # 상장 종목 목록 가져오기
        self.krx = fdr.StockListing('KRX')
        self.krx_code = {}
        for d in self.krx.itertuples():
            self.krx_code[d.Code] = d.Name

        self.url = 'https://www.tradingview.com/markets/stocks-korea/market-movers-large-cap/'

    def get_data(self):
        r = requests.get(self.url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        l = soup.find(attrs={'tabindex': 100}).find_all('tr')

        # DB 세션 생성
        db = self.session()
        for tr in l:
            tds = tr.find_all('td')

            symbol = tds[0].find('a').text
            name = self.krx_code[symbol]
            market_cap = tds[1].text.split(' ')[0]
            if 'T' in market_cap:
                market_cap = market_cap.replace("T", "")
                market_cap = int(float(market_cap) * 1000000000000)
            elif 'B' in market_cap:
                market_cap = market_cap.replace("B", "")
                market_cap = int(float(market_cap) * 1000000000)
            elif 'M' in market_cap:
                market_cap = market_cap.replace("M", "")
                market_cap = int(float(market_cap) * 1000000)
            regular_price = int(tds[2].text.split(' ')[0])
            change_per = float(tds[3].text.replace("%", "").replace("−", "-"))
            print(symbol)
            print(name)
            print(market_cap)
            print(regular_price)
            print(change_per)

            t = db.query(exists().where(KrStocks.symbol == symbol)).scalar()
            if t:  # DB에 있다면
                stock_data = db.query(KrStocks).where(KrStocks.symbol == symbol).first()
                stock_data.market_cap = market_cap
                stock_data.regular_price = regular_price
                stock_data.change_per = change_per
            else:  # DB에 없다면
                stock_data = KrStocks(
                    symbol=symbol,
                    name=name,
                    regular_price=regular_price,
                    change_per=change_per,
                    market_cap=market_cap,
                )
                db.add(stock_data)

            # 로고 이미지 다운로드
            try:
                logo_url = tds[0].find('img')['src']
            except TypeError:
                continue
            logo_path = './../public/kr_stocks/' + symbol + '.svg'
            if not os.path.isfile(logo_path):
                svg = requests.get(logo_url).text
                with open(logo_path, 'w') as file:
                    file.write(svg)

        db.commit()
        db.close()


if __name__ == "__main__":
    #t = TradingViewScraper()
    #t.get_data()
    krx = fdr.StockListing('KRX')
    krx_code = {}
    for d in krx.itertuples():
        print(d)