#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-07-15 14:53:02
# Project: www_ixigua_com
import re
from zlib import crc32
import random
from base64 import b64decode
import MySQLdb
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.url = 'https://www.ixigua.com/api/feedv2/feedById?_signature=0vBrMAAgEAHgIok-XKCvtNLwayAAI.k&channelId=61887739369&count=10&maxTime=1563145324'
        
        self.db = MySQLdb.connect("172.16.7.210", "root", "root", "pyspider_db_www_ixigua_com", charset='utf8' )


    @every(minutes=30)
    def on_start(self):
        
        self.crawl(self.url, callback=self.index_page)

    @config(age=15)
    def index_page(self, response):
        
        if response.json['code'] == 200:
            
            channelInfo = response.json['data']['channelInfo']
            channelFeed = response.json['data']['channelFeed']
            
            if channelFeed['HasMore'] != 'true':
                if hasattr(self, 'db'):
                    self.db.close()
                    print("close！")
                exit()
            
            for x in channelFeed['Data']:
                videoid = x['videoId']
                videoBigImage = x['videoBigImage']
                videoTitle = x['videoTitle']
                videoImage = x['videoImage']
                playNum = x['playNum']
                timeText = x['timeText']
                blackText = x['blackText']
                authorName = x['authorName']
                uid = x['uid']
                maxTime = x['maxTime']
                
                _url = 'https://www.ixigua.com/i'+videoid+'/'
                
                self.crawl(_url, callback=self.second_page,save={'obj': x})
    
    @config(age=8)
    def second_page(self, response):
        
        x = response.save['obj']     
        video_id = self.get_video_id(response)
        
        if video_id is not None:
            url = self.get_video_api(video_id)
            
            self.crawl(url, callback=self.detail_page,save={'obj': x})
            
    @config(age=6)
    def detail_page(self, response):
        
        x = response.save['obj']
        
        data = response.json
        
        if data['code'] == 0:
            video_1 = data['data']['video_list']['video_1']
            video_url = data['data']['video_list']['video_1']['main_url']
            video_url = b64decode(video_url.encode()).decode()
        
            videoid = x['videoId']
            videoBigImage = x['videoBigImage']
            videoTitle = x['videoTitle']
            videoImage = x['videoImage']
            playNum = x['playNum']
            timeText = x['timeText']
            blackText = x['blackText']
            authorName = x['authorName']
            uid = x['uid']
            maxTime = x['maxTime']
                
            return {
                "video_url": video_url,
                "video_id": data['data']['video_id'],
                "video_show_id":videoid,
                "videoBigImage":videoBigImage,
                "videoTitle":videoTitle,
                "videoImage":videoImage,
                "playNum":playNum,
                "timeText":timeText,
                "blackText":blackText,
                "authorName":authorName,
                "uid":uid,
                "maxTime":maxTime,
                "video_size":video_1['size'],
                "video_vwidth":video_1['vwidth'],
                "video_vheight":video_1['vheight'],
                "video_codec_type":video_1['codec_type'],
                "video_vtype":video_1['vtype'],
            }
        return {}
    
    def on_result(self, result):

        self.save_in_mysql(result)
        
    def get_video_id(self, response):
        
        result = re.search('"vid":"*?.*?"user_digg"', response.text)
        
        id = None
        if result is not None:
            id = result.group().replace('"vid":"','').replace('","user_digg"','')
        
        return id
        pass

    def get_video_api(self, videoid):
        
        r = str(random.random())[2:]
        url_part = '/video/urls/v/1/toutiao/mp4/{}?r={}'.format(videoid,r)
        print(url_part)
        s = crc32(url_part.encode())
        
        url = 'https://ib.365yg.com{}&s={}'.format(url_part,s)
        print(url)
        
        return url
    
    def save_in_mysql(self, item):
        try:
            sql = 'replace into video_0(uid,video_show_id,videoTitle,videoBigImage,videoImage,playNum,timeText,blackText,authorName,maxTime,video_id,video_url,video_size,video_vwidth,video_vheight,video_codec_type,video_vtype) \
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
          
            
            cursor = self.db.cursor()
            cursor.execute(sql,(item['uid'],item['video_show_id'],item['videoTitle'],item['videoBigImage'],item['videoImage'],item['playNum'],item['timeText'],item['blackText'],item['authorName'],item['maxTime'],item['video_id'],item['video_url'],item['video_size'],item['video_vwidth'],item['video_vheight'],item['video_codec_type'],item['video_vtype']))
        
            print(cursor.lastrowid)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

            
            
            
#######################################################


#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-07-15 14:53:02
# Project: www_ixigua_com
import re
from zlib import crc32
import random
from base64 import b64decode
import MySQLdb
import time
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.channelId = '61887739369'
        self.url = 'https://www.ixigua.com/api/feedv2/feedById?_signature=0vBrMAAgEAHgIok-XKCvtNLwayAAI.k&channelId={1}&count=50&maxTime={0}'
        
        self.db = MySQLdb.connect("172.16.7.210", "root", "root", "pyspider_db_www_ixigua_com", charset='utf8' )


    @every(seconds=60 * 2)
    def on_start(self):
        tick = round(time.time())
        url = self.url.format(tick, self.channelId)
        
        self.save_in_log(self.channelId, tick, url)
        
        self.crawl(url, callback=self.index_page)

    @config(age=55 * 2)
    def index_page(self, response):
        
        if response.json['code'] == 200:
            
            channelInfo = response.json['data']['channelInfo']
            channelFeed = response.json['data']['channelFeed']
            
            if channelFeed['HasMore'] != True:
                if hasattr(self, 'db'):
                    self.db.close()
                    print("close！")
                exit()
            
            for x in channelFeed['Data']:
                videoid = x['videoId']
                videoBigImage = x['videoBigImage']
                videoTitle = x['videoTitle']
                videoImage = x['videoImage']
                playNum = x['playNum']
                timeText = x['timeText']
                blackText = x['blackText']
                authorName = x['authorName']
                uid = x['uid']
                maxTime = x['maxTime']
                
                _url = 'https://www.ixigua.com/i'+videoid+'/'
                
                self.crawl(_url, callback=self.second_page,save={'obj': x})
    
    @config(age=5)
    def second_page(self, response):
        
        x = response.save['obj']     
        video_id = self.get_video_id(response)
        
        if video_id is not None:
            url = self.get_video_api(video_id)
            
            self.crawl(url, callback=self.detail_page,save={'obj': x})
            
    @config(age=5)
    def detail_page(self, response):
        
        x = response.save['obj']
        
        data = response.json
        
        if data['code'] == 0:
            video_1 = data['data']['video_list']['video_1']
            video_url = data['data']['video_list']['video_1']['main_url']
            video_url = b64decode(video_url.encode()).decode()
        
            videoid = x['videoId']
            videoBigImage = x['videoBigImage']
            videoTitle = x['videoTitle']
            videoImage = x['videoImage']
            playNum = x['playNum']
            timeText = x['timeText']
            blackText = x['blackText']
            authorName = x['authorName']
            uid = x['uid']
            maxTime = x['maxTime']
                
            return {
                "video_url": video_url,
                "video_url_api": response.url,
                "video_id": data['data']['video_id'],
                "video_show_id":videoid,
                "videoBigImage":videoBigImage,
                "videoTitle":videoTitle,
                "videoImage":videoImage,
                "playNum":playNum,
                "timeText":timeText,
                "blackText":blackText,
                "authorName":authorName,
                "uid":uid,
                "maxTime":maxTime,
                "video_size":video_1['size'],
                "video_vwidth":video_1['vwidth'],
                "video_vheight":video_1['vheight'],
                "video_codec_type":video_1['codec_type'],
                "video_vtype":video_1['vtype'],
            }
        return {}
    
    def on_result(self, result):

        self.save_in_mysql(result)
        pass
        
    def get_video_id(self, response):
        
        result = re.search('"vid":"*?.*?"user_digg"', response.text)
        
        id = None
        if result is not None:
            id = result.group().replace('"vid":"','').replace('","user_digg"','')
        
        return id
        pass

    def get_video_api(self, videoid):
        
        r = str(random.random())[2:]
        url_part = '/video/urls/v/1/toutiao/mp4/{}?r={}'.format(videoid,r)
        print(url_part)
        s = crc32(url_part.encode())
        
        url = 'https://ib.365yg.com{}&s={}'.format(url_part,s)
        print(url)
        
        return url
    
    def save_in_mysql(self, item):
        try:
            sql = 'replace into video_1(uid,video_show_id,videoTitle,videoBigImage,videoImage,playNum,timeText,blackText,authorName,maxTime,video_id,video_url,video_url_api,video_size,video_vwidth,video_vheight,video_codec_type,video_vtype) \
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
          
            
            cursor = self.db.cursor()
            cursor.execute(sql,(item['uid'],item['video_show_id'],item['videoTitle'],item['videoBigImage'],item['videoImage'],item['playNum'],item['timeText'],item['blackText'],item['authorName'],item['maxTime'],item['video_id'],item['video_url'],item['video_url_api'],item['video_size'],item['video_vwidth'],item['video_vheight'],item['video_codec_type'],item['video_vtype']))
        
            print(cursor.lastrowid)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
            
    def save_in_log(self, channelId, tick, url):
        try:
            sql = 'replace into spider_log(channelId, tick, url) \
          VALUES (%s,%s,%s);'
          
            cursor = self.db.cursor()
            cursor.execute(sql,(channelId, tick, url))
        
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
