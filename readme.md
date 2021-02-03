
# 运行顺序

    0.把热搜数据分别拷贝到HotData/HotTitle和Hotdata/HotContent文件夹中，默认放入了20210114-20210130号的数据
    
    1.运行[1]org_data_process.py，运行前需要根据第0步拷贝的数据更改参数"开始日期 和 结束日期"，将选取的数据存入[1]org_data.csv
    
    2.运行[2]k-means.py，将[1]org_data.csv数据聚类，存入[2]cluster_data.txt。
    
    3.运行[3]random_select.py，从不同聚类中按比例随机选取数据，挑选出来的数据存入[3]selected_data.txt中
    完成后，备份一份[3]selected_data.txt，存为[3]selected_data_back.txt，以防后续需要使用
    
    4.运行[4]ltp_application.py，使用ltp对[3]selected_data.txt中的数据进行词性标注，标注后的数据存入[4]ltp_data.txt
    ltp处理完成后，需要手动修改[4]ltp_data.txt中标注不准确的数据再进行下一步
    
    5.运行[5]tag_data.py，将[4]ltp_data.txt的数据转成序列标注的数据，存入[5]tag_data.txt，得到标注数据集