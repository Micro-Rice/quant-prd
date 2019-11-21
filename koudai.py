

import jqdatasdk as jq
import datetime as dt


jq.auth("13811944446", "1qazxsw2")

print(jq.__version__)
if __name__ == '__main__':
stocks = ['600000.XSHG', '000001.XSHE']

stocks.remove('688368.XSHG')
stocks.remove('688138.XSHG')

now = dt.datetime.now()
today = now.strftime('%Y-%m-%d')

panel = jq.get_price(stocks, count=60, end_date=today, frequency='daily', fields=['close'])

