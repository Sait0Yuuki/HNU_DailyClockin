# coding=utf-8

import json
import requests
import logging
import os

from retry import retry

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

SECRET_ID = ''
SECRET_KEY = ''
ID = ''
PASSWORD= ''
BARK = ''

def fetch_verifyimage():
    # 获取验证码token
    url="https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode"
    result=requests.get(url)
    result_json=json.loads(result.text)
    
    token=result_json["data"]["Token"]
    return token

def fetch_code(token):
    try:
        cred = credential.Credential(SECRET_ID,SECRET_KEY) 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile) 

        req = models.GeneralAccurateOCRRequest()
        params = {
            "ImageUrl": 'https://fangkong.hnu.edu.cn/imagevcode?token='+token
        }
        req.from_json_string(json.dumps(params))

        resp = client.GeneralAccurateOCR(req) 
        res = json.loads(resp.to_json_string())
        print(res)
        return res['TextDetections'][0]['DetectedText']
    except TencentCloudSDKException as err: 
        print(err) 


def fetch_accesscookies(vercode, token):
    headers={
    'Host': 'fangkong.hnu.edu.cn',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64) AppleWebKit/537.36(KHTML,likeGecko) Chrome/86.0.4240.111 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://fangkong.hnu.edu.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://fangkong.hnu.edu.cn/app/',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
    }
    payload={"Code":ID,"Password":PASSWORD,"WechatUserinfoCode":"","VerCode":vercode,"Token":token}

    result=requests.post('https://fangkong.hnu.edu.cn/api/v1/account/login',json=payload,headers=headers)
    cookies=result.cookies
    return cookies


def clockin(access_cookies):
    url = 'https://fangkong.hnu.edu.cn/api/v1/clockinlog/add'
    headers = {
        'Host':'fangkong.hnu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Content-Type':'application/json;charset=UTF-8',
        'Referer': 'https://fangkong.hnu.edu.cn/app/'
    }
    para = {"Longitude":"","Latitude":"","RealProvince":"湖南省","RealCity":"长沙市","RealCounty":"岳麓区",
            "RealAddress":"湖南大学天马学生公寓","BackState":1,"MorningTemp":"36.5","NightTemp":"36.5","tripinfolist":[]}
    response = requests.post(url, headers=headers, json=para, cookies=access_cookies)
    print(response.text)
    result = json.loads(response.text)
    msg = result['msg']
    requests.post(url='https://api.day.app/'+ BARK + '/'+ msg)
    
@retry(delay=10,tries=10)
def main():
    global SECRET_ID, SECRET_KEY, ID, PASSWORD, BARK
    SECRET_ID = os.environ.get('SECRET_ID', None)
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    ID = os.environ.get('ID', None)
    PASSWORD = os.environ.get('PASSWORD', None)
    BARK = os.environ.get('BARK', None)

    token = fetch_verifyimage()
    vercode = fetch_code(token)
    access_cookies = fetch_accesscookies(vercode,token)
    clockin(access_cookies)

if __name__ == '__main__':
    logging.basicConfig()
    main()
