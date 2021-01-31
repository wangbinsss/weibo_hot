# -*- coding: UTF-8 -*-
# 此处对data/data.csv执行k-means聚合算法，生成的数据存入data/cluster_data.txt

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from dict.normalization import normalize_corpus


K = 10  # 分组，聚出几个类别
F = 8  # 几个特征词


def k_means_main(num_clusters, features):
    # num_clusters: 聚类组数，features：特征词数
    data_path = './data/data.csv'
    cluster_data_path = './data/cluster_data.txt'

    def build_feature_matrix(documents, feature_type='frequency',
                             ngram_range=(1, 1), min_df=0.0, max_df=1.0):
        feature_type = feature_type.lower().strip()  # feature_type为tfidf

        if feature_type == 'binary':
            vectorizer = CountVectorizer(binary=True,
                                         max_df=max_df, ngram_range=ngram_range)
        elif feature_type == 'frequency':
            vectorizer = CountVectorizer(binary=False, min_df=min_df,
                                         max_df=max_df, ngram_range=ngram_range)
        elif feature_type == 'tfidf':
            vectorizer = TfidfVectorizer()
        else:
            raise Exception("Wrong feature type entered. Possible values: 'binary', 'frequency', 'tfidf'")

        feature_matrix = vectorizer.fit_transform(documents).astype(float)

        return vectorizer, feature_matrix

    # 第一步：读取数据
    book_data = pd.read_csv(data_path)  # 读取文件
    # ,sep=",",error_bad_lines=False,engine='python',encoding='utf-8'
    # print(book_data.head())  # 2822 rows x 5 columns

    book_content = book_data['content'].tolist()
    # print('内容:', book_content[0][:10])  # 内容前10个字

    # 第二步：数据载入、分词
    # normalize corpus
    norm_book_content = normalize_corpus(book_content)  # 返回的是分词后的集合['现代人 内心 流失 的 东西……','在 第一次世界大战 的……'，……]

    # 第三步：提取 tf-idf 特征
    vectorizer, feature_matrix = build_feature_matrix(norm_book_content,
                                                      feature_type='tfidf',
                                                      min_df=0.2, max_df=0.90,
                                                      ngram_range=(1, 2))
    # 查看特征数量
    print(feature_matrix.shape)  # 得到tf-idf矩阵，稀疏矩阵表示法  (2822, 16281) 2822行，16281个词汇（根据16281个词汇建立词的索引）
    """
      (0, 11185)	0.17921956529547814   表示为：第0个列表元素，**词典中索引为11185的元素**， 权值0.17921956529547814
      (0, 3199)	0.1644425715576606
      (0, 10416)	0.21232583039538178
      (0, 1451)	0.15573088636535332
    """
    # 获取特征名字
    feature_names = vectorizer.get_feature_names()  # 显示所有文本的词汇，列表类型
    # print(vectorizer.vocabulary_)    #词汇表，字典类型
    # print(feature_matrix.toarray())   #.toarray() 是将结果转化为稀疏矩阵
    # 打印某些特征
    print(feature_names[:10])  # 显示前10个文本的词汇，列表类型

    # 第四步：提取完特征后，进行聚类
    from sklearn.cluster import KMeans

    # KMeans++
    def k_means(feature_matrix, num_clusters=10):
        km = KMeans(n_clusters=num_clusters,
                    max_iter=10000)  # km打印结果是KMeans的参数
        km.fit(feature_matrix)
        clusters = km.labels_  # 编号 [4 6 6 ... 2 2 2]
        return km, clusters

    km_obj, clusters = k_means(feature_matrix=feature_matrix,
                               num_clusters=num_clusters)
    book_data['Cluster'] = clusters  # 在原先的csv文本中加入一列Cluster后的数字
    # print(book_data)

    # 第五步：查看每个cluster的数量
    from collections import Counter

    # 获取每个cluster的数量
    c = Counter(clusters)
    print(c.items())

    def get_cluster_data(clustering_obj, book_data,
                         feature_names, num_clusters,
                         topn_features=10):
        cluster_details = {}
        # 获取cluster的center
        ordered_centroids = clustering_obj.cluster_centers_.argsort()[:, ::-1]
        # 获取每个cluster的关键特征
        # 获取每个cluster的书
        for cluster_num in range(num_clusters):
            cluster_details[cluster_num] = {}
            cluster_details[cluster_num]['cluster_num'] = cluster_num
            key_features = [feature_names[index]
                            for index
                            in ordered_centroids[cluster_num, :topn_features]]
            cluster_details[cluster_num]['key_features'] = key_features

            # books = book_data[book_data['Cluster'] == cluster_num]['title'].values.tolist()
            books = book_data[book_data['Cluster'] == cluster_num]['content'].values.tolist()
            cluster_details[cluster_num]['books'] = books

        return cluster_details

    def print_cluster_data(cluster_data):
        # print cluster details
        cluster_num_list = []
        with open(cluster_data_path, 'w+', -1) as f:
            for cluster_num, cluster_details in cluster_data.items():
                print('Cluster {} details:'.format(cluster_num))
                print(len(cluster_details['books']))
                print('-' * 20)
                print('Key features:', cluster_details['key_features'])
                print('content in this cluster:')
                print(cluster_details['books'][0])
                print('=' * 40)
                f.write('Cluster {} details:'.format(cluster_num) + '\n')
                f.write(str(len(cluster_details['books'])) + '\n')
                f.write('-' * 20 + '\n')
                f.write('Key features:{0}'.format(cluster_details['key_features']) + '\n')
                f.write('content in this cluster:' + '\n')
                f.write('=' * 40 + '\n')
                for val in cluster_details['books']:
                    f.write(val + '\n')
                f.write('=' * 40 + '\n\n')
                cluster_num_list.append(len(cluster_details['books']))
        return cluster_num_list

    import matplotlib.pyplot as plt
    from sklearn.manifold import MDS
    from sklearn.metrics.pairwise import cosine_similarity
    import random
    from matplotlib.font_manager import FontProperties

    def plot_clusters(num_clusters, feature_matrix,
                      cluster_data, book_data,
                      plot_size=(16, 8)):
        # generate random color for clusters
        def generate_random_color():
            color = '#%06x' % random.randint(0, 0xFFFFFF)
            return color

        # define markers for clusters
        markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']
        # build cosine distance matrix
        cosine_distance = 1 - cosine_similarity(feature_matrix)
        # dimensionality reduction using MDS
        mds = MDS(n_components=2, dissimilarity="precomputed",
                  random_state=1)
        # get coordinates of clusters in new low-dimensional space
        plot_positions = mds.fit_transform(cosine_distance)
        x_pos, y_pos = plot_positions[:, 0], plot_positions[:, 1]
        # build cluster plotting data
        cluster_color_map = {}
        cluster_name_map = {}
        for cluster_num, cluster_details in cluster_data[0:500].items():
            # assign cluster features to unique label
            cluster_color_map[cluster_num] = generate_random_color()
            cluster_name_map[cluster_num] = ', '.join(cluster_details['key_features'][:5]).strip()
        # map each unique cluster label with its coordinates and books
        cluster_plot_frame = pd.DataFrame({'x': x_pos,
                                           'y': y_pos,
                                           'label': book_data['Cluster'].values.tolist(),
                                           'book': book_data['book'].values.tolist()
                                           })
        grouped_plot_frame = cluster_plot_frame.groupby('label')
        # set plot figure size and axes
        fig, ax = plt.subplots(figsize=plot_size)
        ax.margins(0.05)
        # plot each cluster using co-ordinates and book titles
        for cluster_num, cluster_frame in grouped_plot_frame:
            marker = markers[cluster_num] if cluster_num < len(markers) \
                else np.random.choice(markers, size=1)[0]
            ax.plot(cluster_frame['x'], cluster_frame['y'],
                    marker=marker, linestyle='', ms=12,
                    label=cluster_name_map[cluster_num],
                    color=cluster_color_map[cluster_num], mec='none')
            ax.set_aspect('auto')
            ax.tick_params(axis='x', which='both', bottom='off', top='off',
                           labelbottom='off')
            ax.tick_params(axis='y', which='both', left='off', top='off',
                           labelleft='off')
        fontP = FontProperties()
        fontP.set_size('small')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True,
                  shadow=True, ncol=5, numpoints=1, prop=fontP)
        # add labels as the film titles
        for index in range(len(cluster_plot_frame)):
            ax.text(cluster_plot_frame.ix[index]['x'],
                    cluster_plot_frame.ix[index]['y'],
                    cluster_plot_frame.ix[index]['book'], size=8)
            # show the plot
        plt.show()

    # 第六步：查看结果
    cluster_data = get_cluster_data(clustering_obj=km_obj,
                                    book_data=book_data,
                                    feature_names=feature_names,
                                    num_clusters=num_clusters,
                                    topn_features=features)

    cluster_list = print_cluster_data(cluster_data)

    # 求方差
    arr_var = np.var(cluster_list)
    print('=' * 40)
    print('分组：{0}，特征词：{1}，方差：{2}'.format(num_clusters, features, arr_var))
    print('=' * 40)
    return [features, num_clusters, arr_var]
    # 画出簇类
    # plot_clusters(num_clusters=num_clusters,
    #               feature_matrix=feature_matrix,
    #               cluster_data=cluster_data,
    #               book_data=book_data,
    #               plot_size=(16, 8))
    # 计算不同参数的方差，请复制以下代码到主函数中运行
    # var_list = []
    # for i in range(2, 11):
    #     for j in range(2, 11):
    #         var = k_means_main(i, j)  # 方差
    #         var_list.append(var)
    # f = 0
    # n = 0
    # var = 10000000
    # for v in var_list:
    #     if v[2] < var:
    #         var = v[2]
    #         f = v[0]
    #         n = v[1]
    # print('*' * 40)
    # print('最小方差{0}，分组：{1}，特征词：{2}'.format(var, n, f))
    # print('*' * 40)


if __name__ == '__main__':
    k_means_main(K, F)
