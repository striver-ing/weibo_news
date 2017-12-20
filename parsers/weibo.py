import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log
import datetime
import base.constance as Constance

SITE_ID = 1712140001
NAME = '微博'


def get_release_time(release_time):
    try:
        data = tools.time.time()
        ltime = tools.time.localtime(data)
        timeStr = tools.time.strftime("%Y-%m-%d", ltime)
        if tools.re.compile('今天').findall(release_time):
            release_time = release_time.replace('今天', '%s' % timeStr)
        elif tools.re.compile('刚刚').findall(release_time):
            release_time = tools.get_current_date()
        elif tools.re.compile('昨天').findall(release_time):
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            release_time = release_time.replace('昨天', '%s' % yesterday)
        elif '小时前' in release_time:
            nhours = tools.re.compile('(\d+)小时前').findall(release_time)
            hours_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(hours=int(nhours[0])))
            release_time = hours_ago.strftime("%Y-%m-%d %H:%M")
        elif tools.re.compile('分钟前').findall(release_time):
            nminutes = tools.re.compile('(\d+)分钟前').findall(release_time)
            minutes_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(minutes=int(nminutes[0])))
            release_time = minutes_ago.strftime("%Y-%m-%d %H:%M")
        else:
            if len(release_time) < 10:
                release_time = '%s-%s' % (timeStr[0:4], release_time)
    except:
        release_time = ''
    finally:
        return release_time


# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')

    table = 'WEIBO_site_info'
    url = 'https://m.weibo.cn'

    base_parser.add_website_info(table, site_id=SITE_ID, url=url, name=NAME)


# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(keywords):
    log.debug('''
        添加根url
        parser_params : %s
        ''' % str(keywords))
    # page_max_count = 236

    for keyword in keywords:
        next_keyword = False
        for page_num in range(1, 236):
            print(keyword)
            url = 'https://m.weibo.cn/api/container/getIndex?type=wb&queryVal=%s' % keyword + \
                  '&featurecode=20000320&luicode=10000011&lfid=100103type%3D1%26q%3D' + keyword \
                  + '&title=' + keyword + '&containerid=100103type%3D2%26q%3D' + keyword + '&page=%d' % page_num
            # base_parser.add_url('WEIBO_urls', SITE_ID, url)
            info_json = tools.get_json_by_requests(url)
            # log.debug(info_json)
            print(url)
            info_list = info_json['data']['cards']
            if info_list:
                info_list = info_list[0]['card_group']
            else:
                info_list = []
                next_keyword = True

            for weibo_info in info_list:
                content = weibo_info['mblog']['text']
                _id = weibo_info['mblog']['id']
                release_time = weibo_info['mblog']['created_at']
                release_time = get_release_time(release_time)
                current_time = tools.get_current_date('%Y-%m-%d')
                if current_time > release_time:
                    next_keyword = True
                    break
                url = 'https://m.weibo.cn/status/' + _id
                user_name = weibo_info['mblog']['user']['screen_name']
                video_url = tools.get_info(str(weibo_info), 'stream_url":"(.+?)"', fetch_one=True)
                reposts_count = weibo_info['mblog']['reposts_count']
                comments_count = weibo_info['mblog']['comments_count']
                attitudes_count = weibo_info['mblog']['attitudes_count']

                base_parser.save_weibo_info('WEIBO_info', site_id=SITE_ID, content=content, release_time=release_time,
                                            user_name=user_name, video_url=video_url, _id=_id, url=url,
                                            reposts_count=reposts_count, comments_count=comments_count,
                                            attitudes_count=attitudes_count)
            if next_keyword:
                break

            tools.delay_time(10)


# 必须定义 解析网址
def parser(url_info):
    pass
    # root_url = url_info['url']
    # info_json = tools.get_json_by_requests(root_url)
    # # log.debug(info_json)
    # info_list = info_json['data']['cards'][0]['card_group']
    # for weibo_info in info_list:
    #     content = weibo_info['mblog']['text']
    #     _id = weibo_info['mblog']['id']
    #     release_time = weibo_info['mblog']['created_at']
    #     release_time = get_release_time(release_time)
    #     url = 'https://m.weibo.cn/status/' + _id
    #     user_name = weibo_info['mblog']['user']['screen_name']
    #     video_url = tools.get_info(str(weibo_info), 'stream_url":"(.+?)"', fetch_one=True)
    #     reposts_count = weibo_info['mblog']['reposts_count']
    #     comments_count = weibo_info['mblog']['comments_count']
    #     attitudes_count = weibo_info['mblog']['attitudes_count']
    #
    #     base_parser.save_weibo_info('WEIBO_info', site_id=SITE_ID, content=content, release_time=release_time,
    #                                 user_name=user_name, video_url=video_url, _id=_id, url=url,
    #                                 reposts_count=reposts_count, comments_count=comments_count,
    #                                 attitudes_count=attitudes_count)
    #
    # base_parser.update_url('WEIBO_urls', url_info['url'], Constance.DONE)
