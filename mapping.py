# -*- coding: utf-8 -*-
'''
Created on 2017-01-03 11:05
---------
@summary: 提供一些操作数据库公用的方法
---------
@author: Boris
'''
import sys
sys.path.append('../../')
import init

import utils.tools as tools
from db.elastic_search import ES

es = ES()

def set_mapping():
    mapping = {
        "weibo_article":{
            "properties":{
                "comment_count":{
                    "type":"long"
                },
                "video_url":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "user_name":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "id":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "up_count":{
                    "type":"long"
                },
                "record_time":{
                    "type":"date",
                    "format":"yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                },
                "content":{
                    "type":"string",
                    "analyzer":"ik_max_word"
                },
                "url":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "release_time":{
                    "type":"date",
                    "format":"yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                },
                "transmit_count":{
                    "type":"long"
                }
            }
        }
    }


    es.set_mapping('weibo_article', mapping)


if __name__ == '__main__':
    set_mapping()