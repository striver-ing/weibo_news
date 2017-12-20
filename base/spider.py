from db.mongodb import MongoDB
import utils.tools as tools
from base.parser_control import PaserControl
from base.collector import Collector
import threading


class Spider(threading.Thread):
    def __init__(self, tab_list, tab_unique_key_list, tab_ensure_index_list, parser_count=None,
                 site_parsers=None, parser_params={}, begin_callback=None, end_callback=None):
        '''
        @summary:
        ---------
        @param tab_urls: url表名
        @param tab_site: 网站表名
        @param parser_count: parser 的线程数，为空时以配置文件为准
        @param parser_params : 解析器所用的参数
        @param begin_callback:  爬虫开始的回调
        @param end_callback:    爬虫结束的回调
        ---------
        @result:
        '''
        super(Spider, self).__init__()

        self._tab_urls = tab_list[0]
        self._site_parsers = site_parsers

        self._db = MongoDB()
        for tab_index in range(len(tab_list)):
            self._db.set_unique_key(tab_list[tab_index], tab_unique_key_list[tab_index])
            # 设置索引 加快查询速度
            for ensure_index in tab_ensure_index_list[tab_index]:
                self._db.set_ensure_index(tab_list[tab_index], ensure_index)

        self._collector = Collector(self._tab_urls, self._site_parsers)
        self._parsers = []

        self._parser_params = parser_params

        self._begin_callback = begin_callback
        self._end_callabck = end_callback

        self._parser_count = int(
            tools.get_conf_value('config.conf', 'parser', 'parser_count')) if not parser_count else parser_count
        self._spider_site_name = tools.get_conf_value('config.conf', "spider_site", "spider_site_name").split(',')
        self._except_site_name = tools.get_conf_value('config.conf', "spider_site", "except_site_name").split(',')

    def add_parser(self, parser):
        if self._spider_site_name[0] == 'all':
            for except_site_name in self._except_site_name:
                if parser.NAME != except_site_name.strip():
                    self._parsers.append(parser)
        else:
            for spider_site_name in self._spider_site_name:
                if parser.NAME == spider_site_name.strip():
                    self._parsers.append(parser)

    def run(self):
        self.__start()

    def __start(self):
        if self._begin_callback:
            self._begin_callback()

        if not self._parsers:
            if self._end_callabck:
                self._end_callabck()
            return

        # 启动collector
        self._collector.add_finished_callback(self._end_callabck)
        self._collector.start()
        # 启动parser 的add site 和 add root
        # print(self._parser_params)
        for parser in self._parsers:
            threading.Thread(target=parser.add_site_info).start()
            threading.Thread(target=parser.add_root_url, args=(self._parser_params,)).start()
        # 启动parser control
        while self._parser_count:
            parser_control = PaserControl(self._collector, self._tab_urls)

            for parser in self._parsers:
                parser_control.add_parser(parser)

            parser_control.start()
            self._parser_count -= 1
