import json
import random
import string
import websocket
import ssl


class TradingViewWebsocket:
    def __init__(self):
        self.headers = json.dumps({
            'Origin': 'https://data.tradingview.com'
        })
        self.symbol = None
        self.ws = None
        self.session = None

    def generate_session(self):
        sl = 12
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(sl))
        return "qs_" + random_string

    def prepend_header(self, st):
        return "~m~" + str(len(st)) + "~m~" + st

    def construct_message(self, func, param_list):
        return json.dumps({
            'm': func,
            'p': param_list,
        }, separators=(',', ':'))

    def create_message(self, func, param_list):
        return self.prepend_header(self.construct_message(func, param_list))

    def send_message(self, func, args):
        self.ws.send(self.create_message(func, args))

    def get_kr_data(self, symbol: str):
        self.ws = websocket.create_connection('wss://data.tradingview.com/socket.io/websocket', sslopt={"cert_reqs": ssl.CERT_NONE}, headers=self.headers)
        self.session = self.generate_session()
        self.send_message('set_auth_token', ["unauthorized_user_token"])
        self.send_message('quote_create_session', [self.session])
        self.send_message('quote_add_symbols', [self.session, "KRX:" + symbol])

        data = {}
        idx = 0
        while idx != 1:
            result = self.ws.recv().split('~m~')
            for r in result:
                try:
                    r = json.loads(r)
                except json.JSONDecodeError:
                    continue
                if not isinstance(r, dict):
                    continue
                if 'm' in r and r['m'] == 'quote_completed':
                    idx += 1
                    break
                if 'm' in r and r['m'] == 'qsd':
                    dl = list(r['p'])[1]['v']
                    if 'dividends_yield_current' in dl:
                        data['배당수익률'] = dl['dividends_yield_current']
                    if 'float_shares_outstanding_current' in dl:
                        data['발행주식수'] = dl['float_shares_outstanding_current']
                    if 'net_income' in dl:
                        data['순이익'] = dl['net_income']
                    if 'total_revenue' in dl:
                        data['총수익'] = dl['total_revenue']
                    if 'sector' in dl:
                        data['섹터'] = dl['sector']
                    if 'industry' in dl:
                        data['산업'] = dl['industry']
                    if 'market_cap_basic' in dl:
                        data['시가총액'] = dl['market_cap_basic']
                    if 'web_site_url' in dl:
                        data['웹사이트'] = dl['web_site_url']
                    if 'location' in dl:
                        data['본사지역'] = dl['location']
                    if 'market-status' in dl:
                        data['마켓상태'] = dl['market-status']
                    if 'ch' in dl:
                        data['가격변화'] = dl['ch']
                    if 'chp' in dl:
                        data['가격변화율'] = dl['chp']

        '''
        for d in data:
            print("종목 : ", d)
            dl = data[d]
            for v in dl:
                if 'dividends_yield_current' in v:
                    print("배당수익률 :", v['dividends_yield_current'])
                if 'float_shares_outstanding_current' in v:
                    print('현재발행주식수 :', v['float_shares_outstanding_current'])
                if 'net_income' in v:
                    print('순이익 :', v['net_income'])
                if 'total_revenue' in v:
                    print('총수익 :', v['total_revenue'])
                if 'sector' in v:
                    print('섹터 :', v['sector'])
        '''
        return data


if __name__ == "__main__":
    TV_WS = TradingViewWebsocket()
    print(TV_WS.get_kr_data("005930"))