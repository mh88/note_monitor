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

            
###########################################################


#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-07-15 14:53:02
# Project: www_kuishow_com
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
        self.url = 'http://101.251.217.210/rest/n/feed/list?app=0&country_code=CN&ver=4.55&c=HUAWEI_KWAI&mod=HUAWEI(BKL-AL00)&oc=UNKNOWN&appver=4.55.5.4284&language=zh-cn&sys=ANDROID_9&net=WIFI&did=ANDROID_fdde31ab5ee08806&ud=0'
        
        self.db = MySQLdb.connect("172.16.7.210", "root", "root", "pyspider_db_www_kuishou_com", charset='utf8' )


    @every(seconds=60 * 1)
    def on_start(self):
        data = {
            'type':7,
            'page':3,
            'count':20,
            'pv':'false',
            'id':13,
            'pcursor':1,
            'sig':'ecfca06e784c3371056cbb93c4c4ad03',
            'client_key':'3c2cd3f3',
            'os':'android',
        }
        url = self.url
        
        #self.save_in_log(self.channelId, tick, url)
        
        self.crawl(url, callback=self.detail_page, method='POST', data=data)

    @config(age=55 * 1)
    def index_page(self, response):
        pass

            
    @config(age=5)
    def detail_page(self, response):
        
        data = response.json
        
        if data['result'] == 1:
            feeds = data['feeds']

            reg = re.compile(u"[\u4e00-\u9fa5]+")
            r = []
            try:
                for x in feeds:
                    title = x['caption'].replace('\n','')
                    name = ' '.join(reg.findall(title))
                    r.append({
                        "video_url": x['main_mv_urls'][0]['url'],
                        "video_url_api": '',
                        "video_id": x['photo_id'],
                        "video_show_id":x['photo_id'],
                        "videoBigImage":x['cover_thumbnail_urls'][0]['url'],
                        "videoTitle":name,
                        "videoImage":x['cover_thumbnail_urls'][0]['url'],
                        "playNum":x['view_count'],
                        "timeText":x['time'],
                        "blackText":x['duration'],
                        "authorName":' '.join(reg.findall(x['user_name'])),
                        "uid":x['photo_id'],
                        "maxTime":x['timestamp'],
                        "video_size":x['ext_params']['video'],
                        "video_vwidth":x['ext_params']['w'],
                        "video_vheight":x['ext_params']['h'],
                        "video_codec_type":'',
                        "video_vtype":x['ext_params']['mtype'],
                    })
            except Exception as e:
                print(e)
                pass
        return r
    
    def on_result(self, result):
        print(result)
        self.save_in_mysql(result)
        pass

    def save_in_mysql(self, items):
        try:
            sql = 'replace into video_kuishou_1(uid,video_show_id,videoTitle,videoBigImage,videoImage,playNum,timeText,blackText,authorName,maxTime,video_id,video_url,video_url_api,video_size,video_vwidth,video_vheight,video_codec_type,video_vtype) \
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
          
            sql_all = []
            for item in items:
                sql_all.append( (item['uid'],item['video_show_id'],item['videoTitle'],item['videoBigImage'],item['videoImage'],item['playNum'],item['timeText'],item['blackText'],item['authorName'],item['maxTime'],item['video_id'],item['video_url'],item['video_url_api'],item['video_size'],item['video_vwidth'],item['video_vheight'],item['video_codec_type'],item['video_vtype']))
                
            cursor = self.db.cursor()
            cursor.executemany(sql,sql_all)
        
            print(cursor.lastrowid)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
            
    def save_in_log(self, channelId, tick, url):
        try:
            sql = 'replace into spider_log_kuishou(channelId, tick, url) \
          VALUES (%s,%s,%s);'
          
            cursor = self.db.cursor()
            cursor.execute(sql,(channelId, tick, url))
        
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
            
            
#########################################################

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-07-15 14:53:02
# Project: www_huoshan_com
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
        self.url = 'https://api-a.huoshan.com//hotsoon/feed/?type=video'
        
        self.db = MySQLdb.connect("172.16.7.210", "root", "root", "pyspider_db_www_huoshan_com", charset='utf8' )


    @every(seconds=60 * 1)
    def on_start(self):
        
        url = self.url
        
        #self.save_in_log(self.channelId, tick, url)
        
        self.crawl(url, callback=self.detail_page)

    @config(age=55 * 1)
    def index_page(self, response):
        pass

            
    @config(age=5)
    def detail_page(self, response):
        
        data = response.json
        
        if data['status_code'] == 0:
            feeds = data['data']

            reg = re.compile(u"[\u4e00-\u9fa5]+")
            r = []
            try:
                for _x in feeds:
                    if _x['type'] != 3:
                        continue
                        
                    x = _x['data']
                    video = x['video']
                    
                    title = x['title'].replace('\n','')
                    #name = ''.join(reg.findall(title))
                    title = title if len(title) > 0 else x['share_title'].replace('\n','')
                    r.append({
                        "video_url": video['url_list'][0],
                        "video_url_api": '',
                        "video_id": video['video_id'],
                        "video_show_id":video['video_id'],
                        "videoBigImage":video['cover']['url_list'][0],
                        "videoGifImage":video['gif_url_list'][0],
                        "videoTitle":title,
                        "videoImage":video['cover_thumb']['url_list'][0],
                        "playNum":x['stats']['play_count'],
                        "timeText":video['duration'],
                        "blackText":video['duration'],
                        "authorName":''.join(reg.findall(x['author']['nickname'])),
                        "uid":x['id'],
                        "maxTime":x['create_time'],
                        "video_size":str(video['width']) + 'x' + str(video['height']),
                        "video_duration":video['duration'],
                        "video_vwidth":video['width'],
                        "video_vheight":video['height'],
                        "video_codec_type":'',
                        "video_vtype":x['media_type'],
                    })
            except Exception as e:
                print(e)
                pass
        return r
    
    def on_result(self, result):
        print(result)
        self.save_in_mysql(result)
        pass

    def save_in_mysql(self, items):
        try:
            sql = 'replace into video_1(uid,video_show_id,videoTitle,videoBigImage,videoGifImage,videoImage,playNum,timeText,blackText,authorName,maxTime,video_id,video_url,video_url_api,video_size,video_duration,video_vwidth,video_vheight,video_codec_type,video_vtype) \
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
          
            sql_all = []
            for item in items:
                sql_all.append( (item['uid'],item['video_show_id'],item['videoTitle'],item['videoBigImage'],item['videoGifImage'],item['videoImage'],item['playNum'],item['timeText'],item['blackText'],item['authorName'],item['maxTime'],item['video_id'],item['video_url'],item['video_url_api'],item['video_size'],item['video_duration'],item['video_vwidth'],item['video_vheight'],item['video_codec_type'],item['video_vtype']))
                
            cursor = self.db.cursor()
            cursor.executemany(sql,sql_all)
        
            print(cursor.lastrowid)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
            
    def save_in_log(self, channelId, tick, url):
        try:
            sql = 'replace into spider_log_kuishou(channelId, tick, url) \
          VALUES (%s,%s,%s);'
          
            cursor = self.db.cursor()
            cursor.execute(sql,(channelId, tick, url))
        
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

