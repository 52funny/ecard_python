import json
import re
import datetime
from io import BytesIO
from logging import debug
from typing import Any, Tuple
from urllib.parse import urljoin

import pytesseract
import requests
from bs4 import BeautifulSoup
from PIL import Image

from utils import encryptString

UserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'


class Ecard:
    def __init__(self, username, password, url, debug=False) -> None:
        self.debug = debug
        self.session = requests.Session()
        # update user-agent
        self.session.headers.update({'User-Agent': UserAgent})
        self.username = username
        self.password = password
        self.url = url

    def Login(self) -> Any:
        """登陆函数"""
        state = ''
        while state != '3':
            url = urljoin(self.url, '/easytong_portal/login')
            exponent, modulus = self.getkeyMap()
            username = encryptString(exponent, modulus, self.username)
            password = encryptString(exponent, modulus, self.password)
            code = self.getCodeImg()
            data = {'username': username,
                    'password': password, 'jcaptchacode': code}
            r = self.session.post(url, data=data, headers={
                                  'X-Requested-With': 'XMLHttpRequest'})
            obj = json.loads(r.content)
            if self.debug:
                print(obj)
            state = obj['ajaxState']
            if (state != '3') and state != '0' and (obj['msg'] == '账号不存在' or obj['msg'] == '用户或密码错误'):
                break

    def getkeyMap(self) -> Tuple:
        """获取Rsa公钥"""
        url = urljoin(self.url, '/easytong_portal/publiccombo/keyPair')
        r = self.session.post(url)
        keyObj = json.loads(r.content)
        exponent = keyObj['publicKeyMap']['exponent']
        modulus = keyObj['publicKeyMap']['modulus']
        # return exponent, modulus
        return (exponent, modulus)

    def getCodeImg(self):
        """获取验证码"""
        url = urljoin(self.url, '/easytong_portal/jcaptcha.jpg')
        content = self.session.get(url).content
        byteIO = BytesIO(content)
        image = Image.open(byteIO)
        # with open('code.png', 'wb') as f:
        #     f.write(content)
        code = pytesseract.image_to_string(image, lang='eng')
        return code.strip()

    def isCookieOverDue(self):
        """判断Cookie是否过期"""
        url = urljoin(self.url, '/easytong_portal')
        r = self.session.get(url)
        reg = re.compile(r'<title>(.*)</title>')
        ans = reg.search(r.text).group(1)
        if ans.find('登录') != -1:
            return True
        return False

    def ObtainBalance(self):
        """获取饭卡余额"""
        url = urljoin(self.url, '/easytong_portal')
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        money = soup.select('p.money')
        return money[0].contents[0].strip()

    def ObtainDormitoryElectricity(self, areaNo: str, buildingNo: str, roomNo: str):
        """获取宿舍电费"""
        url = urljoin(self.url, '/easytong_portal/payFee/getBalance')
        data = {"itemNum": 1, "areano": areaNo,
                "buildingno": buildingNo, 'roomno': roomNo}
        header = {"X-Requested-With": "XMLHttpRequest"}
        data = json.dumps(data).replace(" ", "")
        r = self.session.post(
            url, data={"data": data}, headers=header)
        obj = json.loads(r.text)
        if self.debug:
            print(obj)
        return obj['feeDate']['balance']

    def ObtainIntervalBill(self, typeFlag: str, size: str, startTime: str, endTime: str):
        """
        ObtainIntervalBill 获取时间区间的账单信息
        typeFlag 1 消费 2 充值 3 补助 4 互转
        size 页面大小
        startTime 开始时间
        endTime 结束时间
        时间格式应为 2006-01-02类型
        返回一个List
        """
        url = urljoin(self.url, '/easytong_portal/bill')
        data = {"typeFlag": typeFlag, "startdealTime": startTime,
                "enddealTime": endTime, "start": "1", "end": size, "size": size}
        r = self.session.post(url, data=data)
        soup = BeautifulSoup(r.content, 'lxml')
        list = soup.select('.row tbody > tr')
        bill = []
        for it in list:
            bill.append({
                "Time": it.select('.text-muted')[0].text,
                "Content": it.select('.time + td')[0].text,
                "Merchant": it.select('td:nth-child(4)')[0].text,
                "Location": it.select('td:nth-child(5)')[0].text,
                "Money": it.select('td:nth-child(6)')[0].text
            })
        return bill
