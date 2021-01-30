# -*- coding=UTF-8 -*-
# 需要requests、bs4、pandas库
import os
import time
import requests
import bs4


# 爬虫请求模块
def crawl(url):
    '''
    爬虫模块
    返回r，即网页源码
    '''

    headers = {
        'Host': 's.weibo.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://weibo.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r
    except:
        return 0
    # 爬虫结束


# 热搜列表数据处理
def data_processing(r):
    html_xpath = bs4.BeautifulSoup(r.text, 'html.parser')
    title = []
    https = html_xpath.find_all('td', attrs={'class': 'td-02'})
    for i in range(len(https)):
        tag = https[i].text.split('\n')
        if i == 0:
            tag[2] = '0'
        title.append(tag[1])
    return title


# 热搜列表存储路径
def build_data_path():
    time_name = time.strftime('%Y%m%dHotTitle', time.localtime())
    all_path = "./HotData/HotTitle"
    if not os.path.exists(all_path):
        # 创建多层路径
        os.makedirs(all_path)
    # 最终文件存储位置
    root = all_path + "/"
    path = root + time_name + '.txt'
    return path


# 热搜详情数据处理
def detail_processing(r=None):
    html_xpath = bs4.BeautifulSoup(r.text, 'html.parser')
    feeds_1 = html_xpath.find_all('p', attrs={'node-type': 'feed_list_content_full'})
    feeds_2 = html_xpath.find_all('p', attrs={'node-type': 'feed_list_content'})
    feeds = feeds_1 + feeds_2
    content = []
    for feed in feeds:
        feed = str(feed)
        if '展开全文' in feed:
            continue
        x = []
        i = 0
        for val in feed:
            if val in ['<', '>']:
                x.append(i)
            i += 1
        x = x[1: -1]
        feed_x = ''
        for i in range(len(x)):
            if i % 2 == 0:
                feed_x += feed[x[i] + 1: x[i + 1]]
        feed_x = feed_x.replace('\n', '').replace(' ', '')
        if feed_x not in content:
            content.append(feed_x)
    return content


# 热搜详情存储路径
def build_detail_path():
    time_name = time.strftime('%Y%m%dHotContent', time.localtime())
    all_path = "./HotData/HotContent"
    if not os.path.exists(all_path):
        # 创建多层路径
        os.makedirs(all_path)
    # 最终文件存储位置
    root = all_path + "/"
    path = root + time_name + '.txt'
    return path


# 写入文件模块1
def write_txt(data, path):
    with open(path, 'a+', -1) as fw:
        for val in data:
            fw.write(val + '\n\n')


# 写入文件模块2
def write_txt_2(data, path):
    data_list = []
    try:
        with open(path, 'r', -1) as f:
            for line in f:
                data_list.append(line.split('\n')[0])
    except:
        pass

    new_data_list = []
    with open(path, 'a+', -1) as fw:
        for val in data:
            if val not in data_list:
                new_data_list.append(val)
                fw.write(val + '\n')
    return new_data_list


def main():
    main_url = "https://s.weibo.com/top/summary?cate=realtimehot"
    r = crawl(main_url)  # 爬取实时热搜列表
    d = data_processing(r)  # 热搜列表数据处理
    hot_search_list = d[1:]  # 生成数组格式的热搜列表
    if r:
        new_data_list = write_txt_2(hot_search_list, build_data_path())  # 热搜列表存入txt文件，并返回新增的热搜
        print('新增热搜：')
        for i, event in enumerate(new_data_list):
            print('{i},{e}'.format(i=i + 1, e=event))
            event_url = 'https://s.weibo.com/weibo?q={0}&Refer=top'.format(event)
            detail = crawl(event_url)  # 爬取每条热搜详情
            detail_data = detail_processing(detail)  # 热搜详情数据处理
            write_txt(detail_data, build_detail_path())  # 热搜详情暂时存入html文件
        print('获取完毕，2秒后关闭...')
    else:
        print('爬虫失败，检查网络...')
    time.sleep(2)


if __name__ == '__main__':
    main()
