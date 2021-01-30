# coding:utf-8

# 此处为原始数据处理，第二种处理方式，将抓到的所有微博热搜数据直接转存到data目录下的data.csv中
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

    the_txt_path = txt_path.format(day=the_day_str)
    with open(csv_path, 'a+', -1) as c_f:   # a+为追加写入，w+为覆盖写入
        with open(the_txt_path, 'r', -1) as t_f:
            for line in t_f:
                if line != '\n':
                    feed = line
                    feed = feed.replace('收起全文d', '').replace(',', '，')
                    c_f.write(feed)
