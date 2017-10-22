# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql

class BbsspiderPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host='192.168.199.248', port=3306, user='root', passwd='6121090q',db='spider',charset='utf8')
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        line = json.dumps(dict(item))+'\n'
        print(item.get("title"))
        print('查看输出：'+line)

        sql = "insert into bbs(create_time,update_time,umd5,url,replyNum,label1,label2,title,content) values ('%s','%s','%s','%s',%d,'%s','%s','%s','%s') " % (item.get("create_time"),item.get("update_time"),item.get("umd5"),item.get("url"),item.get("replyNum"),item.get("label1"),item.get("label2"),item.get("title"),item.get("content"))
        print("sql: ",sql)
        self.cur.execute(sql)
        self.db.commit()
