import requests
from bs4 import BeautifulSoup
import twstock
import requests
import schedule
import time
import re
import time
from interval import Interval
data = requests.get("https://tw.stock.yahoo.com/rank/volume")
soup = BeautifulSoup(data.text, "html.parser")


b_tag = soup.find_all(class_="Fz(14px) C(#979ba7) Ell")
list_b_tag = list(b_tag)
max_idx = 0
now = 0
outside = 0
category_name = []
stock_num = 15

def get_two_float(f_str, n):
    a, b, c = f_str.partition('.')
    c = c[:n]
    return ".".join([a, c])
# 把回傳數字保留小數後兩位的function

def containEnglish(str0):
    return bool(re.search('[A-Z]',str0))



for i in range(stock_num):
    list_b_tag1 = str(list_b_tag[i])
    after_sp = list_b_tag1.split('">')[-1].split('.TW')[0] #去切文字，利用符號切其中-1是後面數回來的位置
    category_name.append(after_sp) #將中文目錄丟入list中
    # print(after_sp)

# stock2330 = twstock.realtime.get('8478')


# stock = twstock.realtime.get('2330')

old_stock_id = 0
now_localtime_set_hstart = 9
now_localtime_set_hstop = 13
now_localtime_set_mstart1 = 0
now_localtime_set_mstop1 = 3
now_localtime_set_mstart2 = 30
now_localtime_set_mstop2 = 33


while True:
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    if int(now_localtime.split(":")[0]) >= now_localtime_set_hstart and int(now_localtime.split(":")[0]) <= now_localtime_set_hstop : #切字元
        if int(now_localtime.split(":")[1]) >= now_localtime_set_mstart1 and int(now_localtime.split(":")[1]) < now_localtime_set_mstop1 \
                or int(now_localtime.split(":")[1]) >= now_localtime_set_mstart2 and int(now_localtime.split(":")[1]) < now_localtime_set_mstop2:

            for i in range(len(category_name)):
                if containEnglish(str(category_name[i])) != True and len(str(category_name[i])) < 5:
                    try:

                        stock = twstock.realtime.get(str(category_name[i]))

                        stock1 = twstock.Stock(str(category_name[i]))
                        b = twstock.BestFourPoint(stock1)

                        #buy = b.best_four_point_to_buy()  # 買點分析
                        #sell = b.best_four_point_to_sell()  # 賣點分析
                        mix = b.best_four_point()  # 綜合分析 建議直接用這個 會比較快
                        mix_show = ""
                        if mix[0] == True:
                            mix_show = "經AI評估，可放做多清單"
                        else:
                            mix_show = "經AI評估，可放做空清單"

                        average_5_days = stock1.moving_average(stock1.price, 5)[-1]
                        #average_10_days = stock1.moving_average(stock1.price, 10)[-1]
                        #average_30_days = stock1.moving_average(stock1.price, 30)[-1]
                        #average_3_capacity = int((stock1.moving_average(stock1.capacity, 3)[-1])/3000)
                        average_1_capacity = int((stock1.moving_average(stock1.capacity, 1)[-1]) / 1000)


                        num = stock['info']['code']
                        name = stock['info']['name']
                        low2330 = stock['realtime']['low']
                        high2330 = stock['realtime']['high']
                        ltr2330 = stock['realtime']['latest_trade_price']
                        open_stock = stock1.open[-1] #開盤價




                        if get_two_float(ltr2330, 2) != "-.":

                            # 乖離值 Y值（乖離率）＝（當日收盤價－N日內移動平均收市價）/N日內移動平均收盤價×100％
                            bias_val = int((float(get_two_float(ltr2330, 2)) - average_5_days) / 5 * 100)
                            predict_val = int(((float(get_two_float(high2330, 2)) - float(open_stock)) / (
                                        float(get_two_float(high2330, 2)) - float(get_two_float(low2330, 2)))) * 100)

                            msg2330 = (
                                f' \n >[參考交易，盈虧自負]< \n [成交量排行] : {get_two_float(num, 2)} {get_two_float(name, 2)}\n 高點價格 : {get_two_float(high2330, 2)} '
                                f'\t 最低價格 : {get_two_float(low2330, 2)} \n 現價 : {get_two_float(ltr2330, 2)} \t 開盤價 : {open_stock}\n 5T: {average_5_days} \t bias_val : {bias_val}%\n 今日成量 : {average_1_capacity}'
                                f'\n 綜合分析(買/賣) : {mix_show} ')
    #綜合分析理由(買/賣) : {mix[1]}

                            ###############################################
                            url = "https://notify-api.line.me/api/notify"
                            payload = {'message': {msg2330}}
                            headers = {'Authorization': 'Bearer ' + 'JBQGWjqhZkSOMv55IEhWR4P9OSHQyjNZtiOGF13Thuj'}
                            print(msg2330)
                            # response = requests.request("POST", url, headers=headers, data=payload)

                        time.sleep(7)
                    except:
                            time.sleep(5)
                            print("ERROR")


