# coding:utf-8

# 此处为原始数据处理，第3种处理方式，将抓到的微博热搜数据，除去热搜标签，转存到data目录下的data.csv中
import datetime

# 开始日期
start_date = datetime.datetime.strptime('2021-01-14', '%Y-%m-%d')
days = 17   # 有多少天

title_path = './HotData/HotTitle/{day}HotTitle.txt'
txt_path = './HotData/HotContent/{day}HotContent.txt'
csv_path = './data/data.csv'

with open(csv_path, 'w+', -1) as c_f:  # a+为追加写入，w+为覆盖写入
    c_f.write('content\n')

for i in range(0, days):  # 有多少天
    title_list = []
    the_day = start_date + datetime.timedelta(days=i)
    the_day_str = the_day.strftime('%Y%m%d')

    the_title_path = title_path.format(day=the_day_str)
    the_txt_path = txt_path.format(day=the_day_str)
    print(the_title_path)

    with open(the_title_path, 'r', -1) as f:
        for line in f:
            if line != '\n':
                line = line.replace('\n', '').replace(' ', '')
                title_list.append(line)

    with open(csv_path, 'a+', -1) as c_f:   # a+为追加写入，w+为覆盖写入
        with open(the_txt_path, 'r', -1) as t_f:
            for line in t_f:
                if line != '\n':
                    feed = line
                    for val in title_list:
                        title = '#{0}#'.format(val)
                        feed = feed.replace(title, '')
                    feed = feed.replace('收起全文d', '').replace('【】', '').replace(',', '，')
                    c_f.write(feed)
