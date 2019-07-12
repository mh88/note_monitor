#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-07-11 16:15:36
# Project: test2

import base64
import json
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.base_url = 'url'
        self.page_num = 101
        self.total_num = 200
 
    @every(seconds=30)
    def on_start(self):
        
            if self.page_num > self.total_num:
                return
            
            url = self.base_url + '&page=' + str(self.page_num)
            print url
            data = {
                'pageNumber':self.page_num,
                'pageSize':100,
                'waittype':2,
                'num':0,
                'start_paix':'',
                'end_paix':'',
                'shoulbahzh':'',
                'xingm':'',
                'idcard':''
            }
            self.page_num += 1
            self.crawl(url, callback=self.index_page, method='POST', data=data)
    
    @config(age=10)    
    def index_page(self, response):
        
        print(response.json)
        #return response.json
        return {
            'result':
            [{
                "排位":x['PAIX'],
                "申请": x['XINGM'],
                "备案": x['SHOULHZH'],
                "身号": x['SFZH'],
                "入深": x['RUHSJ'],
                "SHOUCCBSJ": x['SHOUCCBSJ'],
                "社保": x['SHOUCCBSJ_AJ'],
                "SHOUCCBSJ_GZ": x['SHOUCCBSJ_GZ'],
                "LHMC_ID": x['LHMC_ID'],
                "SQB_ID": x['SQB_ID'],
                "LHCYXXB_ID": x['LHCYXXB_ID'],
                "RZQK": x['RZQK'],
                "RGQK": x['RGQK'],
                "REMARK": x['REMARK'],
        } for x in response.json['rows']]
        }

    @config(priority=2)
    def detail_page(self, response):
        print(response.json)
        #return response.json
        return [{
                "轮候排位":x['PAIX'],
                "申请人": x['XINGM'],
                "备案回执号": x['SHOULHZH'],
                "身份证号": x['SFZH'],
                "入深户时间": x['RUHSJ'],
                "SHOUCCBSJ": x['SHOUCCBSJ'],
                "社保累计缴费时间": x['SHOUCCBSJ_AJ'],
                "SHOUCCBSJ_GZ": x['SHOUCCBSJ_GZ'],
                "LHMC_ID": x['LHMC_ID'],
                "SQB_ID": x['SQB_ID'],
                "LHCYXXB_ID": x['LHCYXXB_ID'],
                "RZQK": x['RZQK'],
                "RGQK": x['RGQK'],
                "REMARK": x['REMARK'],
        } for x in response.json['rows']]



############################################################################

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-07-11 16:15:36
# Project: test2

import base64
import json
import sys
import time
from pyspider.libs.base_handler import *
reload(sys)
sys.setdefaultencoding('utf8')


class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.base_url = 'http://url/bzflh/lhmcAction.do?method=queryYgbLhmcList'
        self.page_num = 130
        self.total_num = 10000
 
    @every(seconds=30)
    def on_start(self):
        
            if self.page_num > self.total_num:
                exit()
            
            url = self.base_url + '&page=' + str(self.page_num)
            print url
            data = {
                'pageNumber':self.page_num,
                'pageSize':10,
                'waittype':2,
                'num':0,
                'start_paix':'',
                'end_paix':'',
                'shoulbahzh':'',
                'xingm':'',
                'idcard':''
            }
            self.page_num += 1
            self.crawl(url, callback=self.index_page, method='POST', data=data)
            
    
    @config(age=20)    
    def index_page(self, response):
        
        print(response.json)
        
        for x in response.json['rows']:

            self.crawl('http://url/lhmcAction.do?method=queryDetailLhc&lhmcId='+x['LHMC_ID']+'&waittype=2', callback=self.detail_page)
       
    @config(age=5)  
    def detail_page(self, response):
        
        parent = None
        r = []
        for each in response.doc('.leader_wrap1 > div.leader_intro1').filter(lambda i: i > 0).items():
            each('b').remove()
            x_map = each.text().split('\n')
            if parent is None:
                parent = x_map
                
            if parent is None and len(parent) < 2:
                parent = [' ',' ']
          
            if len(x_map) == 5:
                r.append( {
                        "姓名":x_map[0],
                        "身份证": x_map[1],
                        "户籍": '深圳',
                        "户籍区": x_map[2],
                        "入户时间": x_map[3],
                        "社保": x_map[4],
                        "配偶": '',
                        "fa": '',
                        "ma": '',
                        "join":''
                })
            if len(x_map) == 4:

                with_ = parent[1] if x_map[0] == '申请人配偶' else ''
                fa = parent[1] if x_map[0] == '申请人未成年子女' else ''
                ma = ''

                if len(fa) > 0 and parent[0][0] != x_map[1][0]:
                    ma = parent[1]
                    fa = ''
                r.append( {
                        "姓名":x_map[1],
                        "身份证": x_map[2],
                        "户籍": '深圳',
                        "户籍区": parent[2],
                        "入户时间": x_map[3],
                        "社保": '',
                        "配偶": with_,
                        "fa": fa,
                        "ma": ma,
                        "join": parent[0] + ':' + parent[1]
                })
        
        return {'result': r}



    
    
