#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import time


from const import header


def get_bangumi():
    url = 'https://bangumi.bilibili.com/web_api/season/index_global?page=1&page_size=2963&version=0&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0&area=0&quarter=0'
    html = requests.get(url=url, headers=header, timeout=30)
    content = html.content
    return content


def get_info(url):
    html = requests.get(url=url, headers=header, timeout=30)
    soup = BeautifulSoup(html.content, 'html.parser')
    info = soup.find('div', {'class': 'bangumi-info-r'})
    title = info.find('div', {'class': 'b-head'}).find('h1').text
    titles = info.find('div', {'class': 'b-head'}).findAll('span')
    spans = []
    for each in titles:
        spans.append(each.text)
    span = '+'.join(spans)
    plays = info.find('div', {'class': 'info-count'}).find('span', {'class': 'info-count-item info-count-item-play'}).find('em').text
    people = info.find('div', {'class': 'info-count'}).find('span', {'class': 'info-count-item info-count-item-fans'}).find('em').text
    barrage = info.find('div', {'class': 'info-count'}).find('span', {'class': 'info-count-item info-count-item-review'}).find('em').text
    info_row = info.find('div', {'class': 'info-row info-update'}).findAll('span')
    start = info_row[0].text.replace(' ', '').replace('\n', '')
    total = info_row[1].text.replace(',', u'，')
    cv = info.find('div', {'class': 'info-row info-cv'}).findAll('span', {'class': 'info-cv-item'})
    cvs = []
    for each in cv:
        cvs.append(each.text)
    cv = ''.join(cvs)
    cv = cv[1:]
    content = info.find('div', {'class': 'info-desc'}).text.replace('\n', '')
    print title
    return [title.encode('utf-8'), span.encode('utf-8'), plays.encode('utf-8'), people.encode('utf-8'), barrage.encode('utf-8'), start.encode('utf-8'), total.encode('utf-8'), cv.encode('utf-8'), content.encode('utf-8')]


if __name__ == '__main__':
    # content = get_bangumi()
    # with open('1.json', 'rb+') as f:
    #     x = f.read()
    # cj = eval(x)
    # print len(cj['result']['list'])
    # x = get_info('https://bangumi.bilibili.com/anime/3461')
    # for each in x:
    #     print each
    # head = ['番名', '标签', '总播放', '追番人数', '弹幕总数', '开播时间', '话数', '声优', '简介']
    with open('1.json', 'rb+') as f:
        x = f.read()
    cj = eval(x)
    l = cj['result']['list']
    infomation = []
    # 2963
    j = 7
    # for i in range(400*j, 400*(j+1)):
    for i in range(400*j, 2963):
        print i
        url = l[i]['url']
        infomation.append(get_info(url))
        time.sleep(0.5)
    with open('info.csv', 'ab+') as f:
        w = csv.writer(f)
        for each in infomation:
            w.writerow(each)
