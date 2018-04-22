import urllib.request
import urllib.parse
import urllib.error
import json
import heapq
import http.cookiejar
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
import os
import datetime

import sqllite




url='http://www.bitkan.com/price/w_price'

data = {'categoryId': 'btc'}

postdata=bytes(json.dumps(data),'utf8') #urllib.parse.urlencode(data).encode('utf8')

header={
    'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    ,'Content-Type':'application/json'
}

# #使用http.cookiejar.CookieJar()创建CookieJar对象
# cjar=http.cookiejar.CookieJar()
# #使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
# cookie=urllib.request.HTTPCookieProcessor(cjar)
# opener=urllib.request.build_opener(cookie)
#将opener安装为全局





def getPriceData():
    with urllib.request.urlopen(url,postdata) as f:
        # print('Data:', f.read().decode('utf-8'))
        jsonData = json.loads(f.read().decode('utf-8'))
        reponseData = jsonData['data']['marketCoins']

        tradDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cheap = heapq.nsmallest(4, reponseData, key=lambda s: s['price'][1][4])
        expensive = heapq.nlargest(3, reponseData, key=lambda s: s['price'][1][4])
        for c in expensive:
            sqllite.insertData(c['title'],c['price'][1][4],c['price'][0][4],"expensive",tradDate)
            # print('expensive----',c['title'],c['price'][1][4])

        for c in cheap:
            # print('cheap-----',c['title'],c['price'][1][4])
            sqllite.insertData(c['title'],c['price'][1][4],c['price'][0][4],"cheap",tradDate)


        # print("cheap",cheap[0]['title'],cheap[0]['price'][1][4])
        # print("expensive", expensive[0]['title'],expensive[0]['price'][1][4])
        # print(expensive[0]['price'][1][4]-cheap[0]['price'][1][4])

        # print("cheap",cheap[1]['title'],cheap[1]['price'][1][4])
        # print("expensive", expensive[1]['title'],expensive[1]['price'][1][4])
        #     sqllite.insertData("chae",expensive[1]['price'][1][4]-cheap[1]['price'][1][4],expensive[1]['price'][0][4]-cheap[1]['price'][0][4],"chae",tradDate)



if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(getPriceData, 'cron', second='*/30', hour='*')
    print(    'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except SystemExit:
        scheduler.shutdown()

    getPriceData()
