import jqdatasdk as jq
import datetime as dt


def ma_func(pd, n):
    sum_c = 0
    pd_t = pd.tail(n)
    # print(pd_t)
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
    print(len(stocks))
    # stocks = ['003816.XSHE']
    today = dt.date.today()
    k = 60
    panel = jq.get_price(stocks, count=k, end_date=today, frequency='daily', fields=['close', 'volume'])
    df_close = panel['close']
    df_vol = panel['volume']
    for stock in stocks:
        dfc = df_close[stock]
        ratio = round((dfc.iat[k - 1] - dfc.iat[k - 2]) / dfc.iat[k - 2], 4)
        print(ratio)
        max_c = dfc.head(30).max()
        print(max_c)
        min_c = dfc.tail(30).min()
        print(min_c)
        ratio2 = round((max_c - min_c) / min_c, 4)
        close = dfc.tail(1).iat[0]
        ratio3 = round((close - min_c) / min_c, 4)
        dfv = df_vol[stock]
        max_v = dfv.tail(11).max()
        print(max_v)
        vol = dfv.tail(1).iat[0]

        if ratio >= 0.035 and ratio2 > 0.02 and ratio3 > 0.01 and vol >= max_v:
            res_sts.append(stock)

    print(res_sts)
