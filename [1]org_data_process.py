# coding:utf-8
# 此处为原始数据处理，第一种处理方式，将抓到的微博热搜数据txt_path中每天每条热搜选取一条微博，存到csv_path中
# 默认使用了这种方式，其他两种方式参见org_data_process_2、org_data_process_3

import datetime

# 开始日期 和 结束日期
start_day = '2021-01-14'
end_day = '2021-01-30'


title_path = './HotData/HotTitle/{day}HotTitle.txt'
txt_path = './HotData/HotContent/{day}HotContent.txt'
csv_path = './data/[1]org_data.csv'
with open(csv_path, 'w+', -1) as c_f:  # a+为追加写入，w+为覆盖写入
    c_f.write('content\n')
start_date = datetime.datetime.strptime(start_day, '%Y-%m-%d')
end_date = datetime.datetime.strptime(end_day, '%Y-%m-%d')
days = (end_date - start_date).days + 1
print(days)
for i in range(0, days):
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

    tmp = []
    with open(csv_path, 'a+', -1) as c_f:   # a+为追加写入，w+为覆盖写入
        for val in title_list:
            title = '#{0}#'.format(val)
            print(title)
            with open(the_txt_path, 'r', -1) as t_f:

                for line in t_f:
                    if line != '\n':
                        feed = line
                        if title in feed and feed not in tmp:
                            print(title)
                            tmp.append(feed)
                            feed = feed.replace('收起全文d', '').replace('【】', '').replace(',', '，')
                            c_f.write(feed)
                            break
