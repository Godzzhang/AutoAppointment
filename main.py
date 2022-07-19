import time

import requests
import json
from datetime import timezone
from datetime import timedelta
from datetime import datetime

print("Start Program!")

#准备工作
SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)


def get_beijing_time():
    # 协调世界时
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    # 北京时间
    beijing_now = utc_now.astimezone(SHA_TZ)
    return beijing_now
    # beijing_tomorrow = beijing_now + timedelta(days=1)



unionid = 'oF-BrwFcZMQ-ZVTm-Nz7HtfSpMQY'

data = "{\"subLibId\":\"881\",\"scheduleId\":1412399,\"children\":0,\"card\":\"370321200502052416\",\"cardType\":\"IDCARD\",\"name\":\"张城玮\",\"phone\":\"13396432119\",\"childrenConfig\":false,\"code\":\"\"}"
data_json = json.loads(data)
data = data.encode('utf-8')

headers = {
    "Connection": "keep-alive",
    "Content-Length": str(len(data)),
    "Accept": "application/json, text/plain, */*",
    "unionid": unionid,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6307001d)",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://appointment-users.dataesb.com/?code=0711AIGa1XYivD0DofHa1Hg8z911AIGu&state=login",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

schedule_data = None

print("getting schedule")

#获取时间安排表
schedule_url = 'https://appointment-backend-cdn.dataesb.com/api/appointment/schedule/?subLibId=881&timestamp={}&callback=%23%2Findex%2F881%3Fcounter%3D1658102400000&subLibId=881'.format(
    int(get_beijing_time().timestamp()))
respond = requests.get(url=schedule_url, headers=headers, data=data)
schedule_json = json.loads(respond.text)
if schedule_json['code'] == 200 and schedule_json['msg'] == '成功':
    schedule_data = schedule_json['data']

print("preparing for appointment")

appointment_url = 'https://appointment-backend-cdn.dataesb.com/api/appointment/pub_add/?timestamp={}&callback=%23%2Findex%2F881%3Fcounter%3D1657670400000'.format(
    int(get_beijing_time().timestamp()))

beijing_now = get_beijing_time()
beijing_tomorrow = beijing_now + timedelta(days=1)

date = beijing_tomorrow.strftime("%Y-%m-%d")

ids = [0, 0]
startTime = ""
#获取预约id
for schedule in schedule_data:
    if date in schedule['startTime']:
        if ids[0] == 0:
            ids[0] = schedule['id']
        else:
            ids[1] = schedule['id']
        startTime = schedule['registerStart']

start_time = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
start_time_p10s = start_time - timedelta(seconds=10)
start_time_a10s = start_time + timedelta(seconds=10)
beijing_now = get_beijing_time()

print("now:", beijing_now)
print("start time:", start_time_p10s)

#等待开始
while True:
    beijing_now = get_beijing_time()
    print(beijing_now.timestamp(), start_time_p10s.timestamp())
    if beijing_now.timestamp() - start_time_p10s.timestamp() >= 0:
        break
    time.sleep(0.1)
    print("waiting")

#开枪
while True:
    data_json['scheduleId'] = ids[0]
    data = json.dumps(data_json).encode('utf-8')
    M = json.loads(requests.post(url=appointment_url, headers=headers, data=data).text)

    data_json['scheduleId'] = ids[1]
    data = json.dumps(data_json).encode('utf-8')
    A = json.loads(requests.post(url=appointment_url, headers=headers, data=data).text)

    if M['msg'] == "成功" and A['msg'] == "成功":
        break

    beijing_now = get_beijing_time()
    if beijing_now.timestamp() - start_time_a10s.timestamp() > 0:
        break
    print("makeing")

print(M)
print(A)

message = "上午: " + M['msg'] + "\n" + "下午: " + A['msg']

#微信提醒
d = {
"title": "图书馆预约通知",
"desp": message
}
u = "https://sctapi.ftqq.com/SCT134112TkzWZq8fwSUdCphxSuSBvhbGW.send"
h = {
"Content-type": "application/x-www-form-urlencoded"
}

print(json.dumps(d))

res = requests.get(url=u, params=d, headers=h)
print(res.text)
