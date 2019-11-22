import jqdatasdk as jq
import datetime as dt


def ma_func(pd, n):
    sum_c = 0
    pd_t = pd.tail(n)
    print(pd_t)
    for i in range(n):
        sum_c = sum_c + pd_t.iat[i]
    avg = round(sum_c / n, 2)
    return avg


if __name__ == '__main__':
    jq.auth("13811944446", "1qazxsw2")
    print(jq.get_query_count())
    res_sts = []
    stock_SH = jq.get_index_stocks('000001.XSHG')
    stock_SZ = jq.get_index_stocks('399001.XSHE')
    stock_cy = jq.get_index_stocks('399006.XSHE')
    stocks = stock_SZ + stock_SH + stock_cy
    stocks = list(set(stocks))
    # print(len(stocks))
    # stocks = ['003816.XSHE']

    # stocks.remove('300001.XSHE')
    # stocks.remove('688138.XSHG')

    today = dt.date.today()

    panel = jq.get_price(stocks, count=100, end_date=today, frequency='daily', fields=['close', 'volume'])
    df_close = panel['close']
    df_vol = panel['volume']
    for stock in stocks:
        dfc = df_close[stock]
        dfv = df_vol[stock]
        # print(stock)
        ma5 = ma_func(dfc, 5)
        ma10 = ma_func(dfc, 10)
        ma20 = ma_func(dfc, 20)
        # ma50 = ma_func(dfc, 50)
        # ma100 = ma_func(dfc, 100)
        min_c = dfc.min()
        max_c = dfc.max()

        v_max = dfv.tail(10).max()

        close = dfc.tail(1).iat[0]
        vol = dfv.tail(1).iat[0]
        # print(max_c)
        # print(close)
        # print(min_c)
        # print("-------------")

        if close > ma5 > ma10 > ma20 and \
                max_c * 0.9 > close > min_c * 1.1 and vol >= v_max:
            res_sts.append(stock)
            # print(close)
            # print(max_c)
            # print(stock)
    print(res_sts)