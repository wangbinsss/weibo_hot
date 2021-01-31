# -*- coding: UTF-8 -*-
# 此处从聚类完成的数据cluster_data.txt中按比例随机选取数据，存到selected_data.txt中
import random

cluster_data_path = './data/cluster_data.txt'
final_data_path = './data/selected_data.txt'

eq_list = []
with open(cluster_data_path, 'r', -1) as f:
    i = 1
    for line in f:
        if '=' * 40 + '\n' == line:
            # print(i)
            eq_list.append(i)
        i += 1

ran_num_list = []
for j in range(len(eq_list)):
    if j % 2 == 0:
        length = eq_list[j + 1] - eq_list[j] - 1
        # print(length)
        num = length//5
        # print('--', num)
        for n in range(num):
            random_nums = random.randint(eq_list[j] + 1, eq_list[j + 1] - 1)
            while random_nums in ran_num_list:
                random_nums = random.randint(eq_list[j] + 1, eq_list[j + 1] - 1)
            ran_num_list.append(random_nums)

with open(cluster_data_path, 'r', -1) as c_f:
    with open(final_data_path, 'w+', -1) as final_f:
        i = 1
        for line in c_f:
            if i in ran_num_list:
                final_f.write(line)
            i += 1
