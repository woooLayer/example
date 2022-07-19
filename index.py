from yiban import Yiban

import requests
import logging
import time
import random


def push_plus(token: str, title:str, content: str) -> dict:
    response = requests.post(
        url = "http://www.pushplus.plus/send",
        data={
            "token": token,
            "title": title,
            "content": content
        }
    ).json()
    if response['code'] == 200:
        print("推送成功")
    else:
        raise Exception("推送失败")

def submit(name: str, mobile: str, password: str, task_data: dict) -> str:
    msg = "健康提交"
    yb = Yiban(mobile=mobile, password=password)
    try:
        for i in range(0, 3):
            result = yb.submit_task(task_data=task_data)
            if result is True:
                msg = f"{name}: 打卡成功"
                return msg
            
            elif result is False: 
                msg = f"{name}: 未找到打卡任务"
                
            elif result is None:
                msg = f"{name}: 无未打卡任务"
                
        return msg
    except Exception as e:
        return str(f"{name}: {e}")

def main():
    # 修改处
    # FIX BEGIN

    user_list = [
        {"name": "xxx", "mobile": "xxx", "password": "xxx"},
    ]

    push_token = ""  # 推送密钥
    push_title = f'{time.strftime("%m-%d 易班打卡", time.localtime())}'  # 推送标题
    task_name = "每日健康打卡" # 任务名称 防止变更
    location  = ""     # 位置
    address   = location      # 定位位置
    longitude = 0  # 经度
    latitude  = 0  # 纬度
    temperature = round(random.uniform(36.0,37.0), 1) # 体温 36.0-37.0 随机
    
    # FIX END


    task_data = {
        "WFId": "",
        "Data": { 
            "9843754e97aad058523524bdb8991bcd": "否", 
            "72fe9c2c81a48fd0968edbbb3f2c1c42": temperature, 
            "769bbfbfb026629f1ddb0294a9c0d257": location, 
            "90b5b83950ae456fefebb0f751406e2d": [{ 
                "name": "348816E7-275F-42D8-9118-625FB45D8D48.png", 
                "type": "image/png", 
                "size ": 472092, 
                "status": "done", 
                "percent ": 100, 
                "fileName": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png ", 
                "path": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png "
            }], 
            "0242914b8746275c5073ccdb156f9d1d":[{ 
                "name": "86E7DCB9-7FEE-441F-B921-039302A1048B.png", 
                "type": "image/png", 
                "size": 179394, 
                "status": "done", 
                "percent": 100, 
                "fileName": "workflow/202110/23/30150ea922a720e7fb732eb7150cc532.png ", 
                "path": "workflow/202110/23/30150ea922a720e7fb732eb7150cc532.png "
            }],
            "1bac180dd37455f7c16a36336c0411a8":{
                "time":time.strftime("%y-%m-%d %H:%M:%S", time.localtime()),
                "longitude":longitude,
                "latitude":latitude,
                "address":address
            }
        },

        "Extend": { 
            "TaskId": "", 
            "title": "任务信息", 
            "content": [
                {"label": "任务名称", "value": task_name},
                {"label": "发布机构", "value": "学生处"},
                {"label": "发布人", "value": "邸灿"}
            ]
        }
    }
    msg = ""
    for i in user_list:
        result = submit(i["name"], i["mobile"], i["password"], task_data)
        msg = msg + result + "\n"
        print(result)
    

    push_plus(token=push_token, title=push_title, content=msg)

    return msg

if __name__ == '__main__':
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO) # DEBUG
    main()
