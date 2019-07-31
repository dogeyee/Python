import requests
import datetime
import time
import json
import random

# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup

standard = float(input("輸入匯率通知標準 ==> "))

start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
while 1 :
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    r = requests.get("https://ebank.megabank.com.tw/global2/fs/fs04/PFS40100.faces")
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        sections = soup.select("table.m-cardstyle-ratetable > tbody > tr")
        c = 0
        for i in sections :
            c += 1
            if c == 4 :
                money = i.find_all("td", "dollar")
                con = 0
                for m in money :
                    con += 1
                    if con == 2 :
                        current = m.contents[0].strip()
                        print("目前匯率為 :", current)
                        if float(current) <= standard :

                            #(For Slack)
                            WEB_HOOK_URL = "https://hooks.slack.com/services/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"
                            text_string = "🇯🇵 日幣 已經低於 " + str(standard) + "\n目前匯率為 : " + current
                            requests.post(WEB_HOOK_URL, data = json.dumps({
                                "text": "<@hoogle> " + text_string,
                                "username": "Page Parsing Python Bot",
                                "icon_emoji": ":currency_exchange:",
                            }))

                            #(For LINE)
                            WEB_HOOK_URL = "https://notify-api.line.me/api/notify"
                            token = "tVH3oNmrhZWCwDAu7c002scKhZf8DUn6jSzgnU9xaQs"
                            message = "🇯🇵 日幣 已經低於 " + str(standard) + "\n目前匯率為 : " + current
                            headers = {
                                "Authorization" : "Bearer " + token,
                                "Content-Type" : "application/x-www-form-urlencoded"
                            }
                            payload = {"message" : message}
                            requests.post(WEB_HOOK_URL, headers = headers, params = payload)
                            print(now_time + " (start from " + start_time + ")==> Send to LINE")
                            time.sleep(180)
                        else :
                            print("目前匯率未低於 %.5f"%standard)
                break

    t = random.randint(3,5)
    print("time sleep %d seconds"%t)
    time.sleep(t)
