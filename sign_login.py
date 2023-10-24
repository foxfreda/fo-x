#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
# import time
import os

class Xinuo():
    def __init__(self):
        self.ses = requests.session()
        self.host = os.environ.get('LIK_AI_HOST', '') or ''
        self.retData = {
            "success":False,
            "code":"-1",
            "message":"",
        }

    def sign_in(self):
        ''' 到 '''
        msg = ""
        token = os.environ.get('LIK_AI_TOKEN', '') or self.token
        num = os.environ.get('LIK_AI_NUM', '0') or '0'
        num = int(num)
        host_path = os.environ.get("LIK_AI_SIGN_IN_HOST") or "" 

        try:
            url = f"{self.host}/{host_path}"
            headers = {
              'Accept': 'application/json, text/plain, */*',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Authorization': 'Bearer {}'.format(token),
              'Referer': f'{self.host}/home',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
              'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
              'sec-ch-ua-platform': '"Linux"'
            }
            response = self.ses.get(url, headers=headers)
            """
            {
             "success": false,
             "code": 84,
             "message": "",
             "data": null
            }
            """
            if response.status_code == 200:
                res_json = response.json()
                
                if res_json.get("code") == 200:
                    score = res_json.get("data").get("score")
                    msg = f"lkai到成功获得分:{score}"
                    print(msg)
                else:
                    message = res_json.get("message")
                    msg = f"lkai到失败:{message}"
                    print("lkai到失败 req content: {}".format(response.text))
                self.retData = res_json
                self.retData["message"] = msg
            else:
                r_code = response.status_code
                msg = f"lkai到失败 response status_code:{r_code} {response.text}"
                print(msg)
                self.retData["message"] = msg

        except:
            msg = "lkai到失败 服务器内部错误"
            self.retData["message"] = msg

        return self.retData
    def login(self):
        ''' 录 '''
        host_path = os.environ.get("LIK_AI_LOGIN_HOST") or "" 
        url = f"{self.host}/{host_path}"
        username = os.environ.get('LIK_AI_USERNAME', '') or ''
        pwd = os.environ.get('LIK_AI_PWD', '') or ''
        payload = {
            "username":username,
            "password":pwd,
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': 'Bearer',
            'Referer': f'{self.host}/home',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
            'sec-ch-ua-platform': '"Linux"'
        }

        msg = ''
        response = self.ses.post( url, headers=headers, data=payload)
        if response.status_code == 200:
            res_json = response.json()
            self.retData = res_json

            if res_json.get("code") == 200:
                # score = res_json.get("data").get("score")
                msg = f"lkai录成功"
                print(msg)
                print('')
                # print('-res_json-',res_json)
                print('')
                # store.action.setToken(res.data.token);
                token = res_json.get("data").get("token")
                print('')
                print('-token-',token)
                print('')
                self.token = token
                # os.environ["LIK_AI_TOKEN"] = token
            else:
                message = res_json.get("message")
                msg = f"lkai录失败:{message}"
                self.retData["message"] = msg

                print("lkai录失败 req content: {}".format(response.text))
        else:
            r_code = response.status_code
            msg = f"lkai录失败 response status_code:{r_code}"
            self.retData["message"] = msg

            print(msg)
        return self.retData
    def get_cookie_dict(self):
        ''' 把自动保留的cookie转成dict格式 '''
        cookie = requests.utils.dict_from_cookiejar(self.ses.cookies)
        return cookie

    def lkai_balance(self):
        ''' 查询分 '''
        msg = ""
        token = os.environ.get('LIK_AI_TOKEN', '') or self.token
        host_path = os.environ.get("LIK_AI_BALANCE_HOST") or "" 

        try:
            url =  f"{self.host}/{host_path}"
            headers = {
              'Accept': 'application/json, text/plain, */*',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Authorization': 'Bearer {}'.format(token),
              'Host': 'chat.link-ai.tech',
              'Referer': f'{self.host}/console/account',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
              'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
              'sec-ch-ua-platform': '"Linux"'
            }
            response = self.ses.get(url, headers=headers)
            if response.status_code == 200:
                # 代码返回格式改变 会报错
                res_json = response.json()
                if res_json.get("code") == 200:
                    score = res_json.get("data").get("score")
                    msg = f"lkai总分:{score}"
                else:
                    message = res_json.get("message")
                    msg = f"lkai获取分失败:{message}"
            else:
                r_code = response.status_code
                msg = f"lkai获取分失败 response status_code:{r_code}"
                self.retData["message"] = msg

        except:
            msg = "lkai获取分失败 服务器内部错误"
            self.retData["message"] = msg
        return self.retData
def run():
    msg = xinuObj = Xinuo()

    msgLogin = xinuObj.login()
    print('')
    # print('-msgLogin-',msgLogin)
    if not msgLogin['success']:
        return msgLogin

    msgSign = xinuObj.sign_in()
    print('')
    print('')
    # print('-msgSign-',msgSign)
    print('')
    if not msgSign['success']:
        return msgSign
    msg = xinuObj.lkai_balance()
    print('')
    print('')
    print('-msg-',msg)
    print('')
    return msg


if __name__ == '__main__':
    # python sign_login.py
    ret = run()
    print('')
    print('--ret--',ret)



