# coding:utf-8
# 此处使用ltp进行词性编注，将selected_data_path的文本标注后存入ltp_path

from ltp import LTP


def ltp_func(text_list):
    ltp = LTP()
    seg, hidden = ltp.seg(text_list)
    pos = ltp.pos(hidden)
    result = []
    for idx, val in enumerate(seg[0]):
        pag = [val, pos[0][idx]]
        result.append('/'.join(pag))
    return result


if __name__ == '__main__':
    selected_data_path = './data/[3]selected_data.txt'    # 需要词性标注的原文本
    ltp_path = './data/[4]ltp_data.txt'      # ltp词性标注后的文本
    with open(selected_data_path, 'r', -1) as text_f:
        with open(ltp_path, 'w+', -1) as ltp_f:
            for line in text_f:
                if line and line != '\n':
                    ltp_line = ltp_func([line])
                    ltp_f.write(' '.join(ltp_line) + '\n')
                    ltp_f.write('\n')
