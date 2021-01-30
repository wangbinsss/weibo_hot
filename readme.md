
# 运行顺序

    1.把热搜数据分别拷贝到HotData/HotTitle和Hotdata/HotContent文件夹中
    
    2.运行[1]org_data_process_1.py，运行前需要根据第1步拷贝的数据更改参数"开始日期 和 结束日期"
    
    3.运行[2]k-means.py，将数据聚类，
    
    4.运行[3]random_select.py，在聚类后的数据中随机选取数据，最终挑选出来的数据在selected_data.txt中