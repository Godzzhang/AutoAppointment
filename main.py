import requests
import time
import datetime
import json

from datetime import datetime
from datetime import timedelta
from datetime import timezone

url = 'https://appointment-backend-cdn.dataesb.com/api/appointment/pub_add/?timestamp=1657683649024&callback=%23%2Findex%2F881%3Fcounter%3D1657670400000'

headers = {
"Connection": "keep-alive",
"Content-Length": "174",
"Accept": "application/json, text/plain, */*",
"unionid": "oF-BrwFcZMQ-ZVTm-Nz7HtfSpMQY",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6307001d)",
"Content-Type": "application/json;charset=UTF-8",
"Referer": "https://appointment-users.dataesb.com/?code=0711AIGa1XYivD0DofHa1Hg8z911AIGu&state=login",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

data = "{\"subLibId\":\"881\",\"scheduleId\":1412399,\"children\":0,\"card\":\"370321200502052416\",\"cardType\":\"IDCARD\",\"name\":\"张城玮\",\"phone\":\"13396432119\",\"childrenConfig\":false,\"code\":\"\"}"

n = 0

'2022-07-14-morning 1412399'
'date: year-month-day'
't: morning | afternoon'
def transform(date, t):
    start_time = '2022-07-14'
    end_time = date
    start = time.mktime(time.strptime(start_time, '%Y-%m-%d'))
    end = time.mktime(time.strptime(end_time, '%Y-%m-%d'))
    count_days = int((end-start) / (24*60*60))
    if t == 'morning':
        T = 0
    if t == 'afternoon':
        T = 1
    schedule_id = 1412399 + count_days * 2 + T
    return schedule_id
    
def make_appointment(date, t):
    global data, url, headers
    j = json.loads(data)
    sid = transform(date, t)
    j['scheduleId'] = sid
    data = json.dumps(j)
    responde = requests.post(url=url,data=data, headers=headers)
    return responde.text

   
#1. 获取北京时间
SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)
# 协调世界时
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
# 北京时间
beijing_now = utc_now.astimezone(SHA_TZ)
beijing_tomorrow = beijing_now + timedelta(days=1)

m = None
a = None

#等待开始
while True:
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_now = utc_now.astimezone(SHA_TZ)
    hours = int(beijing_now.strftime("%H"))
    minutes = int(beijing_now.strftime("%M"))
    seconds = int(beijing_now.strftime("%S"))
    
    if hours >= 16 and minutes >= 59 and seconds >= 30:
        break

print("开腔！")

#2. 开抢
while True:
    m = json.loads(make_appointment(beijing_tomorrow.strftime("%Y-%m-%d"), 'morning'))
    a = json.loads(make_appointment(beijing_tomorrow.strftime("%Y-%m-%d"), 'afternoon'))
    
    if m['msg'] == "成功" and a['msg'] == "成功":
        break
    
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    beijing_now = utc_now.astimezone(SHA_TZ)
    hours = int(beijing_now.strftime("%H"))
    minutes = int(beijing_now.strftime("%M"))
    seconds = int(beijing_now.strftime("%S"))

    time.sleep(1)

    if hours >= 17 and minutes >= 1:
        break
    
ret = "上午: " + m['msg'] + "\n" + "下午: " + a['msg']
print(ret)
#3. 微信提醒
d = {
"title": "图书馆预约通知",
"desp": ret
}
u = "https://sctapi.ftqq.com/SCT134112TkzWZq8fwSUdCphxSuSBvhbGW.send"
h = {
"Content-type": "application/x-www-form-urlencoded"
}

print(json.dumps(d))

res = requests.get(url=u, params=d)
print(res.text)


'''    
now = datetime.datetime.now()
now_date = now.strftime("%Y-%m-%d")
transform('2022-07-14', 'afternoon')
make_appointment('2022-07-14', 'afternoon')
'''
    
'''
while True:
    n += 1
    responde = requests.post(url=url,data=data2, headers=headers)
    print("Num: ", n, " ", responde.text)
    responde = requests.post(url=url,data=data, headers=headers)
    print("Num: ", n, " ", responde.text)
    time.sleep(1)
'''