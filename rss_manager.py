import feedparser
from db_manager import (
    add_query,
    del_query,
    list_query,
    has_log,
    log_update,
)


def rss_list():
    lst_rss, msg = list_query()
    lst_res = []
    if any(lst_rss):
        for rss in lst_rss:
            lst_res.append(f'{rss[0]}\t|\t{rss[1]}\t|\t{rss[2]}')

    return lst_res, msg


def rss_add(name, url):
    res, msg = add_query(name, url)
    return res, msg


def rss_del(id):
    res, msg = del_query(id)
    return res, msg


def rss_update(id=None):
    """
    PyPI recent updates
    title = dgl-cu100 0.6a201220
    link = https://pypi.org/project/dgl-cu100/0.6a201220/
    description = Deep Graph Library
    pubDate = Sun, 20 Dec 2020 09:08:53 GMT

    """
    # 키에 대한 url을 찾거나 모든 피드 업데이트
    if id is None:
        rss_queue = []
        lst_rss, msg = list_query()
        for tp_rss in lst_rss:
            id = tp_rss[0]
            url = tp_rss[2]
            dic_rss = crawl_rss(url)
            if not has_log(id, dic_rss['post_title'], dic_rss['post_published']):
                rss_queue.append(dic_rss)
                log_update(id, dic_rss['post_title'], dic_rss['post_published'])

        return rss_queue
    else:
        lst_rss, msg = list_query()
        for tp_rss in lst_rss:
            if tp_rss[0] == id:
                url = tp_rss[2]
                dic_rss = crawl_rss(url)
                return [dic_rss, ]

        return None


def rss_scheduled():
    pass


def crawl_rss(url):
    rss = feedparser.parse(url)
    return {
        'rss_title': rss.feed['title'],
        'post_title': rss.entries[0].title,
        'post_link': rss.entries[0].link,
        'post_description': rss.entries[0].description,
        'post_published': rss.entries[0].published,
    }
