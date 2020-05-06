#!/usr/bin/env python3
import feedparser
import json
import datetime as dt

def record_posttime(date):
    path = r"/home/ksmt/git/nnct-feed/posttime"
    with open(path, mode='r') as f:
        old_posttime = [s.strip() for s in f.readlines()]
        if old_posttime == []:
            old_posttime = date
    with open(path, mode='w') as f:
        #write new_posttime
        str_ = '\n'.join(date)
        f.write(str_)
    old_posttime = set(old_posttime)
    new_posttime = set(date)
    should_notify_news_post_time = new_posttime - old_posttime
    return should_notify_news_post_time

def extract_rss(news_dic):
    date = []
    for time in [entry.published for entry in news_dic.entries]:
        timedate = dt.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S +0000')
        timedate = timedate + dt.timedelta(hours=9)
        date.append(timedate.strftime('%Y/%m/%d %H:%M:%S'))

    title = [entry.title for entry in news_dic.entries]
    url = [entry.link for entry in news_dic.entries]

    return list(zip(date, title, url))


def get_post_lists(news_list, posttimes):
    timelist = [news_list[i][0] for i in range(len(news_list))]
    indexnumbers = [timelist.index(i) for i in posttimes]
    should_notify_news_list = [[news_list[n][i] for i in range(len(news_list[0]))]for n in indexnumbers]
    return should_notify_news_list

def convert_json(news_list):
    json_dat = ['\"' + str(i + 1) + '" : [' +'{' + '"date":' + ' \"' +  news_list[i][0] + '\", ' + '"title":' + ' \"' + news_list[i][1] + '\", ' + '"url":' + ' \"' + news_list[i][2] + '\"' + '}' + ']' + ',' for i in range(len(news_list))]
    json_dat.insert(0, '{')
    json_dat.append('}')

    json_str = ("".join(json_dat))
    json_str = json_str[::-1]
    json_str = json_str.replace(',', "", 1)
    return json.dumps(json.loads(json_str[::-1]), indent=2, ensure_ascii=False)


def main():
    url = r"http://www.nagaoka-ct.ac.jp/feed/"

    news_dic = feedparser.parse(url)
    news_list = extract_rss(news_dic)
    should_notify_news_post_time = record_posttime([news_list[i][0] for i in range(len(news_list))])
    should_notify_news_list = get_post_lists(news_list, should_notify_news_post_time)
    news_json = convert_json(should_notify_news_list)
    print(news_json)
if __name__ == '__main__':
    main()
