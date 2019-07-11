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

