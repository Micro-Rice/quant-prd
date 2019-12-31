import jqdatasdk as jq
import datetime as dt
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def ma_func(pd, n):
    sum_c = 0
    pd_t = pd.tail(n)
    print(pd_t)
    for i in range(n):
        sum_c = sum_c + pd_t.iat[i]
    avg = round(sum_c / n, 2)
    return avg


def mail_func(info):
    # 第三方 SMTP 服务
    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "zhengy19881123"  # 用户名
    mail_pass = "19881123"  # 口令

    sender = 'zhengy19881123@126.com'
    receivers = ['635435791@qq.com']

    mail_msg = info
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header(receivers, 'utf-8')

    subject = '生成的股票列表'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


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
    res = ",".join(res_sts)
    print(res)
    mail_func(res)

