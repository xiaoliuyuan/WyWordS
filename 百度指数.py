# -*- coding: UTF-8 -*-
# Author :  LIUYUAN
# data : 2019/7/11
import datetime
import requests
import json
from urllib.parse import urlencode
from collections import defaultdict

Cookie = 'BAIDUID=DE88F3B21674F5D45B4B262658F037F4:FG=1; PSTM=1560219770; BIDUPSID=23B5326581ADEDB390439A19B16ABE63; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-257%3A; H_PS_PSSID=1461_21082_29523_29520_29238_28518_29099_28837_29221_29071; BDUSS=kx2SzAzV1RnWmV2LS15bVJ-c09TRn5LSE80bVF3QjhWTTBsQ0J5QnNVSFlkMDVkSVFBQUFBJCQAAAAAAAAAAAEAAADv~duUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANjqJl3Y6iZdS; CHKFORREG=c1f23bdb80de5f806773b68c380c679e; bdindexid=cadmfen9bse92g5opjsk98trg4; BDSFRCVID=H9ksJeCCxG3JggRw5wsZf9-_l8FOeQZRddMu3J; H_BDCLCKID_SF=tR30WJbHMTrDHJTg5DTjhPrMQxvAbMT-027OKKOF5b3CfIKwqfQUbj-j5tQlW-QIyHrb0p6athF0hDvYh4Oq2KCV-frb-C62aKDs04c1-hcqEpO9QTbkbP-w5Nof2RcZbeJC0ljIBb5GoxogbMchDUThDHR02t3-MPoa3RTeb6rjDnCry5rOKUI8LPbO05JZ5KvNLK55-Mctbj63h57PXPLuWR5bKUrtt2LE3-oJqC_5MCKx3J; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1562831406,1562833803,1562836400; delPer=0; PSINO=7; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1562837304'
headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Cookie': 'BAIDUID=DE88F3B21674F5D45B4B262658F037F4:FG=1; PSTM=1560219770; BIDUPSID=23B5326581ADEDB390439A19B16ABE63; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-257%3A; H_PS_PSSID=1461_21082_29523_29520_29238_28518_29099_28837_29221_29071; BDUSS=kx2SzAzV1RnWmV2LS15bVJ-c09TRn5LSE80bVF3QjhWTTBsQ0J5QnNVSFlkMDVkSVFBQUFBJCQAAAAAAAAAAAEAAADv~duUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANjqJl3Y6iZdS; CHKFORREG=c1f23bdb80de5f806773b68c380c679e; bdindexid=cadmfen9bse92g5opjsk98trg4; BDSFRCVID=H9ksJeCCxG3JggRw5wsZf9-_l8FOeQZRddMu3J; H_BDCLCKID_SF=tR30WJbHMTrDHJTg5DTjhPrMQxvAbMT-027OKKOF5b3CfIKwqfQUbj-j5tQlW-QIyHrb0p6athF0hDvYh4Oq2KCV-frb-C62aKDs04c1-hcqEpO9QTbkbP-w5Nof2RcZbeJC0ljIBb5GoxogbMchDUThDHR02t3-MPoa3RTeb6rjDnCry5rOKUI8LPbO05JZ5KvNLK55-Mctbj63h57PXPLuWR5bKUrtt2LE3-oJqC_5MCKx3J; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1562831406,1562833803,1562836400; delPer=0; PSINO=7; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1562837304'

}
class BaiduIndex:
    def __init__(self, keywords, start_date, end_date, area=0):
        self._keywords = keywords if isinstance(keywords, list) else keywords.split(',')
        self._time_range_list = self.get_time_range_list(start_date, end_date)
        self._all_kind = ['all', 'pc', 'wise']  # 选择终端接口
        self._area = area
        self.result = {keyword: defaultdict(list) for keyword in self._keywords}
        self.entry_function()
    # 入口函数
    def entry_function(self):
        for start_date, end_date in self._time_range_list:
            encrypt_datas, uniqid = self.get_encrypt_datas(start_date, end_date)
            key = self.get_key(uniqid)
            for encrypt_data in encrypt_datas:
                for kind in self._all_kind:
                    encrypt_data[kind]['data'] = self.decrypt_func(key, encrypt_data[kind]['data'])
                self.format_data(encrypt_data)

    def get_encrypt_datas(self, start_date, end_date):
        request_args = {
            'word': ','.join(self._keywords),
            'startDate': start_date,
            'endDate': end_date,
            'area': self._area,
        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        html = self.request_get(url)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def get_key(self, uniqid):
        url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self.request_get(url)
        datas = json.loads(html)
        key = datas['data']
        return key
    #
    def format_data(self, data):
        keyword = str(data['word'])
        time_len = len(data['all']['data'])
        start_date = data['all']['startDate']
        cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(time_len):
            for kind in self._all_kind:
                index_datas = data[kind]['data']
                index_data = index_datas[i] if len(index_datas) != 1 else index_datas[0]
                formated_data = {
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'index': index_data if index_data else '0'
                }
                self.result[keyword][kind].append(formated_data)
            cur_date += datetime.timedelta(days=1)

    @staticmethod
    def request_get(url):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    #
    @staticmethod
    def get_time_range_list(startdate, enddate):
        """
        max 6 months
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            tempdate = startdate + datetime.timedelta(days=300)
            if tempdate > enddate:
                all_days = (enddate-startdate).days
                date_range_list.append((startdate, enddate))
                return date_range_list
            date_range_list.append((startdate, tempdate))
            startdate = tempdate + datetime.timedelta(days=1)
    #
    @staticmethod
    def decrypt_func(key, data):
        """
        decrypt data
        """
        a = key
        i = data
        n = {}
        s = []
        for o in range(len(a)//2):
            n[a[o]] = a[len(a)//2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')

if __name__ == '__main__':
    baidu_index = BaiduIndex(keywords=['btc'], start_date='2019-01-01', end_date='2019-07-9')
    print(baidu_index.result['btc']['pc'])