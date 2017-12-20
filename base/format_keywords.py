# -*- coding: utf-8 -*-
'''
Created on 2017-10-24 15:52
---------
@summary: 统计线索信息
---------
@author: Boris
'''

import re

def get_info(content, regex):
    return re.compile(regex, re.S).findall(content)

def get_chinese_word(content):
    regex = '[\u4e00-\u9fa5]+'
    chinese_word = get_info(content, regex)
    return chinese_word

def replace_str(source_str, regex, replace_str = ''):
    '''
    @summary: 替换字符串
    ---------
    @param source_str: 原字符串
    @param regex: 正则
    @param replace_str: 用什么来替换 默认为''
    ---------
    @result: 返回替换后的字符串
    '''
    str_info = re.compile(regex)
    return str_info.sub(replace_str, source_str)

###########【拆分词组相关】################
def match_keys(keys_list):
    '''
    @summary: 解析乘积关系的词组
    ---------
    @param keys_list: 词组列表
    ---------
    @result:
    '''

    list_size = len(keys_list)

    if list_size < 2:
        # return ','.join(keys_list[0].split('|'))
        return keys_list[0].split('|')
    else:
        temp_keys_list = keys_list[:2] #截取前两个数组
        keys_list = keys_list[2:] #剩余的数组[[e|f]]

        keys=''
        for temp_keys1 in temp_keys_list[0].split('|'):
            for temp_keys2 in temp_keys_list[1].split('|'):
                keys += temp_keys1 + '&' + temp_keys2 + '|'

        keys = keys[:-1]
        if keys: keys_list.extend([keys])
        return match_keys(keys_list)

def match_keyword(keyword):
    '''
    @summary: 拆分乘积关系的keyword词组
    ---------
    @param keyword:关键词
    ---------
    @result:
    '''

    keywords = []
    temp_keywords = keyword.split(',')
    for keyword in temp_keywords:
        # keyword = keyword.replace('（',"(").replace('）',')')
        bracket_keys_list = get_info(keyword, '\((.*?)\)') # 括号中的词组
        # print(bracket_keys_list)
        if bracket_keys_list:
            keyword = match_keys(bracket_keys_list)
            keywords.extend(keyword)
        else:
            if keyword: keywords.append(keyword)

    return keywords

###############【处理中英文 格式化词组】####################
def format_keys(keywords):
    '''
    @summary: &表示与的关系 |表示或的关系，括号括起来表示一组
    ---------
    @param keywords:
    ---------
    @result:
    '''
    keywords = keywords.strip()
    keywords = keywords[:-1] if keywords.endswith(',') else keywords

    # keywords = keywords.replace('（','(')
    # keywords = keywords.replace('）',')')
    # keywords = keywords.replace(')(',')&(')
    # print(keywords)

    chinese_word = get_chinese_word(keywords)
    keywords = keywords.split(',')
    for i in range(len(keywords)):
        keywords[i] = keywords[i].strip()
        regex = '[a-zA-Z 0-9:]+'
        english_words = get_info(keywords[i], regex)
        while ' ' in english_words:
            english_words.remove(' ')

        for j in range(len(english_words)):
            english_words[j] = english_words[j].strip()
            if english_words[j]:
                keywords[i] = keywords[i].replace(english_words[j], '%s')

        keywords[i] = replace_str(keywords[i], ' +', '&')
        keywords[i] = keywords[i]%(tuple(english_words)) if '%s' in keywords[i] else keywords[i]

    keywords = ','.join(keywords)

    return keywords


def format_keywords(keywords):
    keywords = format_keys(keywords)
    keywords = match_keyword(keywords)

    return keywords


if __name__ == '__main__':
    keywords = '(3213)'
    print(format_keywords(keywords))

