# -*- coding: utf-8 -*-
'''
Created on 2017-12-11 17:23
---------
@summary: 关键词比对
---------
@author: Administrator
'''
import sys
sys.path.append('..')
import init

import utils.tools as tools
from utils.log import log
from db.oracledb import OracleDB
from base.format_keywords import format_keywords

class Keywords():
    def __init__(self):
        self._oracledb = OracleDB()
        self._clues = self.get_clues()

    def get_clues(self):
        sql = 'select t.id clues_id,to_char(t.keyword2),to_char(t.keyword3),t.zero_id, FIRST_ID, second_id  from TAB_IOPM_CLUES t where zero_id != 7' # 7 为传播途径
        clues = self._oracledb.find(sql)
        return clues

    def get_keywords(self):

        keywords = []

        for clue in self._clues:
            clue_id = clue[0]
            key2 = clue[1]
            key3 = clue[2]
            zero_id = clue[3]
            first_id = clue[4]
            second_id = clue[5]

            keys = format_keywords(key2) # 格式化线索词
            for key in keys: #['新闻节目', '总理&主席', 'the xi factor']
                unit_keys = key.replace('&', ' ') # [总理, 主席]
                keywords.append(unit_keys)

        return keywords

if __name__ == '__main__':
    compare_keywords = CompareKeywords()
    text = '聂辰席是中央宣传部的聂辰席&国家新闻出版广电总局'

    keywords = compare_keywords.get_keywords(text)
    for key in keywords:
        print(key)