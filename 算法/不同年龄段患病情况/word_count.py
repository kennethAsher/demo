# encoding=utf-8
#这个脚本主要实现的功能是把纯文本语料库xuewei.txt（将所有的病症统计）转化成jieba分词和词频统计的字典，分别是dic_for_use和dic_for_idf

ifn = r"xuewei.txt"
ofn = r"dic_for_idf.txt"
ofn2 = r"dic_for_use.txt"
infile = open(ifn,'r')
outfile = open(ofn,'w')
outfile2 = open(ofn2,'w')
'''
read直接从整个文件都读出来，所有的行堆在一个返回值里面
readline读取一行内容，并且讲读取的一行剔除
readlines讲所有的行返回成一个list
'''
for eachline in infile.readlines():
    line = eachline.strip()
    line1 = line+' 100\n'
    line2 = line+' 100 n\n'
    outfile.write(line1)
    outfile2.write(line2)

infile.close
outfile.close
outfile2.close