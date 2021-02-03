# coding: utf-8
# 此处将ltp标注的文字转为序列标注文本，将ltp_path处理后的数据存入tag_path

ltp_path = './data/[4]ltp_data.txt'  # ltp词性标注后的文本
tag_path = './data/[5]tag_data.txt'  # 根据ltp标注生成的序列标注文本
tag_map = {'nh': ['B-PER', 'I-PER'], 'ns': ['B-LOC', 'I-LOC'], 'ni': ['B-ORG', 'I-ORG']}

with open(ltp_path, 'r', -1) as ltp_f:
    with open(tag_path, 'w+', -1) as tag_f:
        for line in ltp_f:
            if not line or line == '\n':
                continue
            ltp_line = line[:-1]
            ltp_line = ltp_line.split(' ')
            tag_line = ''
            for val in ltp_line:
                val = val.split('/')
                if val[1] in tag_map:
                    for idx, word in enumerate(list(val[0])):
                        if idx == 0:
                            word_tag = tag_map[val[1]][0]
                        else:
                            word_tag = tag_map[val[1]][1]
                        tag_word = '{0}/{1}'.format(word, word_tag)
                        tag_line += tag_word + ' '
                else:
                    for word in list(val[0]):
                        tag_word = '{0}/{1}'.format(word, 'O')
                        tag_line += tag_word + ' '
            tag_line += '\n\n'
            tag_f.write(tag_line)
