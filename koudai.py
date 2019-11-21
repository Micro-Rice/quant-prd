import jqdatasdk as jq
import datetime as dt


def ma_func(pd, n):
    sum_c = 0
    pd_t = pd.tail(n)
    for i in range(n):
        sum_c = sum_c + pd_t.iat[i]
    avg = round(sum_c / n, 2)
    return avg


if __name__ == '__main__':
    jq.auth("13811944446", "1qazxsw2")
    print(jq.__version__)
    res_sts = []
    stocks = jq.get_industry_stocks('801080')
    # stocks = ['600000.XSHG', '000001.XSHE']

    stocks.remove('688368.XSHG')
    stocks.remove('688138.XSHG')

    now = dt.datetime.now()
    today = now.strftime('%Y-%m-%d')

    panel = jq.get_price(stocks, count=100, end_date=today, frequency='daily', fields=['close', 'volume'])
    df_close = panel['close']
    df_vol = panel['volume']
    for stock in stocks:
        dfc = df_close[stock]
        dfv = df_vol[stock]
        # print(df)
        ma10 = ma_func(dfc, 10)
        ma50 = ma_func(dfc, 50)
        ma100 = ma_func(dfc, 100)
        min_c = dfc.min()
        max_c = dfc.max()

        v_max = dfv.tail(10).max()

        close = dfc.tail(1).iat[0]
        vol = dfv.tail(1).iat[0]

        if close > ma10 and close > ma50 and close > ma100 and ma10 > ma50 > ma100 and \
                close > min_c * 1.3 and close > max_c * 0.9 and vol >= v_max:
            res_sts.append(stock)
    print(res_sts)
