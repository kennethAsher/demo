#读取已存在的一个事先有内容的测试文件test1.docx代码
import docx
# file = docx.Document('hello.docx')
# print('段落数：'+str(len(file.paragraphs)))
# for para in file.paragraphs:
#     print(para.text)
# for i in range(len(file.paragraphs)):
#     print(f'第{str(i)}段的内容是：{file.paragraphs[i].text}')

#文档中内容批量替换
import os
# xmldir = '/test /text'
# xmllist = os.listdir(xmldir)
# for txt in xmllist:
#     if '.txt' in txt:
#         fo = open(xmldir+'/'+'new_{}'.format(txt), 'w')
#         print('{}'.format(txt))
#         fi = open(xmldir+'/'+'{}'.format(txt), 'r')
#         content = fi.readlines()
#         for line in content:
#             line = line.replace('替换前的内容','替换后的内容')
#             fo.write(line)
#         fo.close()
#         print('替换完成')

#利用docxtpl将指定数据
# from docxtpl import DocxTemplate
# tpl = DocxTemplate('hello.docx')
# context = {
#     'name':name,
#     'department':department,
#     'position':position,
#     'time':time,
#     'id':id_card,
#     'addr':addr}
# tpl.render(context)
# tpl.save('{}的合同.docx'.format(name))


# 05 将所有受邀者的公司名和代表姓名填入路径为test/test_name_list.xlsx的表格
# 在需要填字的地方打上“***”，然后Python来填字，最后保存为test/邀请函.docx，下面代码段为读入信息，然后写入word文件中。
from openpyxl import load_workbook
wb = load_workbook('test/test_name_list.xlsx')
ws = wb['name']
names = []
for row in range(2, ws.max_row+1):
    company = ws['A'+str(row)].values
    name = we['B'+str(now)].values
    names.append(f'{company} {name}')
doc = docx.Document('test/邀请函.docx')
for name in names:
    doc.paragraphs[1].runs[2].text = name
    doc.save('test/邀请函_{}'.format(name))

