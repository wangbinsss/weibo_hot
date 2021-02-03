# coding:utf-8
# 这里是ltp的运行示例，直接运行即可
from ltp import LTP

ltp = LTP()

seg, hidden = ltp.seg(["他叫汤姆去拿外衣。"])
pos = ltp.pos(hidden)
print(seg[0])
print(pos[0])
result = []
for idx, val in enumerate(seg[0]):
    pag = [val, pos[0][idx]]
    result.append(pag)
print(result)
