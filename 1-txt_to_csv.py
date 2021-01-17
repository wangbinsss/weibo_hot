# coding:utf-8
# 此处将抓到的txt数据处理后，转存到data目录下的csv数据中
txt_path = './HotData/20210117HotContent.txt'
csv_path = './data/data.csv'
data_list = []
# with open(csv_path, 'a+', -1) as c_f:     # a+为追加写入，w+为覆盖写入
with open(csv_path, 'w+', -1) as c_f:
    c_f.write('content\n')
    with open(txt_path, 'r', -1) as t_f:
        for line in t_f:
            if line != '\n':
                feed = line
                feed = feed.replace('收起全文d', '').replace(',', '，')
                x = []
                i = 0
                for val in feed:
                    if val == '#':
                        x.append(i)
                    i += 1
                if len(x) > 1:
                    feed = feed[0: x[0]] + feed[x[1] + 1:]
                c_f.write(feed)
