import pandas as pd
import os
import glob
from pathlib import Path

dir_path = glob.iglob('/User/kenneth/Desetop/data/')
for file in dir_path:
    file = os.listdir(file)
    print(file)

#由于是多层文件夹，os.path只能一层一层的读，所以我们使用Pathlib
p = Path(dir_path)
file_list = list(p.glob('**/*.md'))
filelist = list(filter(lambda x: str(x).find('23点')>=0, file_list))
with open(file) as f:
    lines = f.readlines()
    lines = [i.strip() for i in lines]
    data = list(filter(None, lines))
    del data[0]
    data = data[0:100]
    date=re.findall('年(.+)2', str(file))[0]
    content = data[::2]
    rank = data[1::2]
    for i in range(len(content)):
        content[i]=re.findall('、(.+)', content[i])[0]
    for i in range(len(rank)):
        rank[i]=re.findall(' (.+)', rank[i])[0]
'''
https://mp.weixin.qq.com/s/IODiVirevSPIPALR64zDoA
'''